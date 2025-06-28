from typing import Callable, Dict


class ZoneExhaustFan:
    def __init__(
        self,
        V_dot_max: float,
        delta_p: float,
        rho: float,
        eta_fan: float,
        eta_total: float,
        flow_fraction_schedule: Callable[[float], float] = lambda t: 1.0,
        availability_schedule: Callable[[float], bool] = lambda t: True,
    ):
        """
        Initialize a zone exhaust fan.

        Args:
            V_dot_max (float): Maximum volumetric flow rate (m³/s)
            delta_p (float): Pressure rise across the fan (Pa)
            rho (float): Air density (kg/m³)
            eta_fan (float): Fan-only efficiency (0-1)
            eta_total (float): Total efficiency (fan + motor, 0-1)
            flow_fraction_schedule (Callable): Returns flow fraction [0-1] at time t
            availability_schedule (Callable): Returns True if fan is available at time t
        """
        self.V_dot_max = V_dot_max
        self.delta_p = delta_p
        self.rho = rho
        self.eta_fan = eta_fan
        self.eta_total = eta_total
        self.flow_fraction_schedule = flow_fraction_schedule
        self.availability_schedule = availability_schedule

    def compute(self, t: float, h_in: float) -> Dict[str, float]:
        """
        Compute fan performance at time t.

        Args:
            t (float): Current time (e.g., in hours)
            h_in (float): Inlet enthalpy (J/kg)

        Returns:
            dict: Includes flow rate, power, heat addition, and outlet enthalpy
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

        f_frac = max(min(self.flow_fraction_schedule(t), 1.0), 0.0)
        V_dot = f_frac * self.V_dot_max
        m_dot = self.rho * V_dot

        W_shaft = (m_dot * self.delta_p) / (self.rho * self.eta_fan)
        W_electric = (m_dot * self.delta_p) / (self.rho * self.eta_total)
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
