from typing import Callable, Dict


class HeatingWaterCoil:
    def __init__(
        self,
        Q_rated: float,
        rho_air: float,
        availability_schedule: Callable[[float], bool],
        cap_temp_curve: Callable[[float, float], float],
        cap_flow_curve: Callable[[float, float], float],
    ):
        """
        Hot-water heating coil model.

        Args:
            Q_rated (float): Rated heating capacity (W)
            rho_air (float): Air density (kg/m³)
            availability_schedule (Callable): Returns True if coil is available at time t
            cap_temp_curve (Callable): Capacity modifier based on (T_air_in, T_water_in)
            cap_flow_curve (Callable): Capacity modifier based on (V_dot_air, V_dot_water)
        """
        self.Q_rated = Q_rated
        self.rho_air = rho_air
        self.availability_schedule = availability_schedule
        self.cap_temp_curve = cap_temp_curve
        self.cap_flow_curve = cap_flow_curve

    def compute(
        self,
        t: float,
        T_air_in: float,
        T_water_in: float,
        V_dot_air: float,
        V_dot_water: float,
        h_in: float,
    ) -> Dict[str, float]:
        """
        Compute coil output at time t.

        Args:
            t (float): Time (e.g., in hours)
            T_air_in (float): Inlet air temperature (°C)
            T_water_in (float): Inlet water temperature (°C)
            V_dot_air (float): Air volumetric flow rate (m³/s)
            V_dot_water (float): Water volumetric flow rate (m³/s)
            h_in (float): Inlet air enthalpy (J/kg)

        Returns:
            dict: Includes heating power and outlet enthalpy
        """
        if not self.availability_schedule(t):
            return {
                "Q_total": 0.0,
                "h_out": h_in,
            }

        f_temp = self.cap_temp_curve(T_air_in, T_water_in)
        f_flow = self.cap_flow_curve(V_dot_air, V_dot_water)

        Q_total = self.Q_rated * f_temp * f_flow
        m_dot_air = self.rho_air * V_dot_air
        h_out = h_in + Q_total / m_dot_air if m_dot_air > 0 else h_in

        return {
            "Q_total": Q_total,
            "h_out": h_out,
        }
