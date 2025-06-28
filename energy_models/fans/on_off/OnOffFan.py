from typing import Dict


class OnOffFan:
    def __init__(
        self,
        m_dot_design: float,
        delta_p: float,
        rho: float,
        eta_fan: float,
        eta_motor: float,
        f_motor_to_air: float,
    ):
        """
        Initialize an On/Off fan model.

        Args:
            m_dot_design (float): Design mass flow rate (kg/s)
            delta_p (float): Fan pressure rise (Pa)
            rho (float): Air density (kg/m³)
            eta_fan (float): Fan total efficiency (0-1)
            eta_motor (float): Motor efficiency (0-1)
            f_motor_to_air (float): Fraction of motor losses to air (0-1)
        """
        self.m_dot_design = m_dot_design
        self.delta_p = delta_p
        self.rho = rho
        self.eta_fan = eta_fan
        self.eta_motor = eta_motor
        self.f_motor_to_air = f_motor_to_air

        # Precompute design shaft and electric power
        self.w_shaft_design = (m_dot_design * delta_p) / (rho * eta_fan)
        self.w_electric_design = self.w_shaft_design / eta_motor

    def compute(self, m_dot_requested: float, h_in: float) -> Dict[str, float]:
        """
        Compute fan performance for a timestep.

        Args:
            m_dot_requested (float): Requested air mass flow rate (kg/s)
            h_in (float): Inlet specific enthalpy (J/kg)

        Returns:
            dict: {
                "RuntimeFraction": (0-1),
                "W_electric_avg": (W),
                "W_shaft_avg": (W),
                "Q_to_air": (W),
                "h_out": (J/kg),
                "m_dot": (kg/s)
            }
        """
        R = min(max(m_dot_requested / self.m_dot_design, 0.0), 1.0)
        m_dot = R * self.m_dot_design

        w_electric_avg = R * self.w_electric_design
        w_shaft_avg = R * self.w_shaft_design
        q_to_air = self.f_motor_to_air * (w_electric_avg - w_shaft_avg)

        h_out = h_in + (q_to_air / m_dot) if m_dot > 0 else h_in

        return {
            "RuntimeFraction": R,
            "W_electric_avg": w_electric_avg,
            "W_shaft_avg": w_shaft_avg,
            "Q_to_air": q_to_air,
            "h_out": h_out,
            "m_dot": m_dot,
        }
