from typing import Callable, Dict


class CoolingWaterCoil:
    def __init__(
        self,
        Q_rated: float,
        SHR: float,
        rho_air: float,
        availability_schedule: Callable[[float], bool],
        cap_temp_curve: Callable[[float, float], float],
        cap_flow_curve: Callable[[float, float], float],
    ):
        """
        Chilled-water cooling coil model.

        Args:
            Q_rated (float): Rated total cooling capacity (W)
            SHR (float): Sensible heat ratio (0–1)
            rho_air (float): Air density (kg/m³)
            availability_schedule (Callable): Function returning True if coil is available at time t
            cap_temp_curve (Callable): Capacity modifier function of (T_air_in, T_water_in)
            cap_flow_curve (Callable): Capacity modifier function of (V_dot_air, V_dot_water)
        """
        self.Q_rated = Q_rated
        self.SHR = SHR
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
            t (float): Current time (e.g., in hours)
            T_air_in (float): Inlet air temperature (°C)
            T_water_in (float): Inlet water temperature (°C)
            V_dot_air (float): Air volumetric flow rate (m³/s)
            V_dot_water (float): Water volumetric flow rate (m³/s)
            h_in (float): Inlet air enthalpy (J/kg)

        Returns:
            dict: Includes total, sensible, latent cooling, outlet enthalpy
        """
        if not self.availability_schedule(t):
            return {
                "Q_total": 0.0,
                "Q_sensible": 0.0,
                "Q_latent": 0.0,
                "h_out": h_in,
            }

        f_temp = self.cap_temp_curve(T_air_in, T_water_in)
        f_flow = self.cap_flow_curve(V_dot_air, V_dot_water)

        Q_total = self.Q_rated * f_temp * f_flow
        Q_sensible = self.SHR * Q_total
        Q_latent = Q_total - Q_sensible

        m_dot_air = self.rho_air * V_dot_air
        h_out = h_in - Q_total / m_dot_air if m_dot_air > 0 else h_in

        return {
            "Q_total": Q_total,
            "Q_sensible": Q_sensible,
            "Q_latent": Q_latent,
            "h_out": h_out,
        }
