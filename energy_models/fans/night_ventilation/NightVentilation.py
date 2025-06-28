from typing import Callable, Dict


class NightVentilationFan:
    def __init__(
        self,
        V_dot_design: float,
        delta_p_day: float,
        delta_p_night: float,
        rho: float,
        eta_fan: float,
        eta_total: float,
        flow_fraction_day: Callable[[float], float] = lambda t: 1.0,
        flow_fraction_night: Callable[[float], float] = lambda t: 1.0,
        availability_schedule: Callable[[float], bool] = lambda t: True,
        is_night_ventilation: Callable[[float], bool] = lambda t: False,
    ):
        """
        Night ventilation fan with dual operation modes.

        Args:
            V_dot_design (float): Design volumetric flow rate (m³/s)
            delta_p_day (float): Pressure rise during daytime (Pa)
            delta_p_night (float): Pressure rise at night (Pa)
            rho (float): Air density (kg/m³)
            eta_fan (float): Fan-only efficiency (0–1)
            eta_total (float): Fan + motor combined efficiency (0–1)
            flow_fraction_day (Callable): Daytime flow fraction function
            flow_fraction_night (Callable): Nighttime flow fraction function
            availability_schedule (Callable): Availability function (True = ON)
            is_night_ventilation (Callable): True if night ventilation is active
        """
        self.V_dot_design = V_dot_design
        self.delta_p_day = delta_p_day
        self.delta_p_night = delta_p_night
        self.rho = rho
        self.eta_fan = eta_fan
        self.eta_total = eta_total
        self.flow_fraction_day = flow_fraction_day
        self.flow_fraction_night = flow_fraction_night
        self.availability_schedule = availability_schedule
        self.is_night_ventilation = is_night_ventilation

    def compute(self, t: float, h_in: float) -> Dict[str, float]:
        """
        Compute fan operation at time t.

        Args:
            t (float): Simulation time (in hours)
            h_in (float): Inlet air enthalpy (J/kg)

        Returns:
            dict: Results include flow rate, power, heat, outlet enthalpy
        """
        if not self.availability_schedule(t):
            return {
                "V_dot": 0.0,
                "m_dot": 0.0,
                "W_shaft": 0.0,
                "W_electric": 0.0,
                "Q_to_air": 0.0,
                "h_out": h_in,
            }

        if self.is_night_ventilation(t):
            flow_frac = max(min(self.flow_fraction_night(t), 1.0), 0.0)
            delta_p = self.delta_p_night
        else:
            flow_frac = max(min(self.flow_fraction_day(t), 1.0), 0.0)
            delta_p = self.delta_p_day

        V_dot = flow_frac * self.V_dot_design
        m_dot = self.rho * V_dot

        W_shaft = (m_dot * delta_p) / (self.rho * self.eta_fan)
        W_electric = (m_dot * delta_p) / (self.rho * self.eta_total)
        Q_to_air = W_electric - W_shaft
        h_out = h_in + Q_to_air / m_dot if m_dot > 0 else h_in

        return {
            "V_dot": V_dot,
            "m_dot": m_dot,
            "W_shaft": W_shaft,
            "W_electric": W_electric,
            "Q_to_air": Q_to_air,
            "h_out": h_out,
        }
