from typing import Callable, Dict, Optional


class CoolingWaterCoil:
    def __init__(
        self,
        Q_rated: float,
        SHR: float,
        rho_air: float,
        availability_schedule: Callable[[float], bool],
        cap_temp_curve: Callable[[float, float], float],
        cap_flow_curve: Callable[[float, float], float],
        pressure_drop_curve_air: Optional[Callable[[float], float]] = None,
        pressure_drop_curve_water: Optional[Callable[[float], float]] = None,
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
            pressure_drop_curve_air (Callable, optional): Function of air flow rate (m³/s) returning pressure drop (Pa)
            pressure_drop_curve_water (Callable, optional): Function of water flow rate (m³/s) returning pressure drop (Pa)
        """
        self.Q_rated = Q_rated
        self.SHR = SHR
        self.rho_air = rho_air
        self.availability_schedule = availability_schedule
        self.cap_temp_curve = cap_temp_curve
        self.cap_flow_curve = cap_flow_curve
        self.pressure_drop_curve_air = pressure_drop_curve_air
        self.pressure_drop_curve_water = pressure_drop_curve_water

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
            dict: Includes:
                - "Q_total": Total cooling load (W)
                - "Q_sensible": Sensible portion (W)
                - "Q_latent": Latent portion (W)
                - "h_out": Outlet air enthalpy (J/kg)
                - "DeltaP_air": Airside pressure drop across coil (Pa), if modeled
                - "DeltaP_water": Waterside pressure drop across coil (Pa), if modeled
        """
        if not self.availability_schedule(t):
            return {
                "Q_total": 0.0,
                "Q_sensible": 0.0,
                "Q_latent": 0.0,
                "h_out": h_in,
                "DeltaP_air": 0.0,
                "DeltaP_water": 0.0,
            }

        f_temp = self.cap_temp_curve(T_air_in, T_water_in)
        f_flow = self.cap_flow_curve(V_dot_air, V_dot_water)

        Q_total = self.Q_rated * f_temp * f_flow
        Q_sensible = self.SHR * Q_total
        Q_latent = Q_total - Q_sensible

        m_dot_air = self.rho_air * V_dot_air
        h_out = h_in - Q_total / m_dot_air if m_dot_air > 0 else h_in

        delta_p_air = self.pressure_drop_curve_air(V_dot_air) if self.pressure_drop_curve_air else 0.0
        delta_p_water = self.pressure_drop_curve_water(V_dot_water) if self.pressure_drop_curve_water else 0.0

        return {
            "Q_total": Q_total,
            "Q_sensible": Q_sensible,
            "Q_latent": Q_latent,
            "h_out": h_out,
            "DeltaP_air": delta_p_air,
            "DeltaP_water": delta_p_water,
        }
