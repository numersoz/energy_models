from typing import Callable, Dict


class VariableVolumeFan:
    def __init__(
        self,
        m_dot_design: float,
        delta_p: float,
        rho: float,
        eta_fan: float,
        eta_motor: float,
        f_motor_to_air: float,
        power_curve: Callable[[float], float],
    ):
        """Initialize the fan with design parameters.

        Args:
            m_dot_design (float): Design mass flow rate (kg/s)
            delta_p (float): Fan pressure rise (Pa)
            rho (float): Air density (kg/m^3)
            eta_fan (float): Fan total efficiency (0-1)
            eta_motor (float): Motor efficiency (0-1)
            f_motor_to_air (float): Fraction of motor losses to air stream (0-1)
            power_curve (Callable[[float], float]): Function that maps PLR → P_frac
        """
        self.m_dot_design = m_dot_design
        self.delta_p = delta_p
        self.rho = rho
        self.eta_fan = eta_fan
        self.eta_motor = eta_motor
        self.f_motor_to_air = f_motor_to_air
        self.power_curve = power_curve

        # Calculate design electric power
        self.w_shaft_design = (m_dot_design * delta_p) / (rho * eta_fan)
        self.w_electric_design = self.w_shaft_design / eta_motor

    def compute(self, m_dot: float, h_in: float) -> Dict[str, float]:
        """
        Compute fan performance at given mass flow and inlet enthalpy.

        Args:
            m_dot (float): Actual mass flow rate (kg/s)
            h_in (float): Inlet specific enthalpy (J/kg)

        Returns:
            Dict[str, float]: Includes PLR, P_frac, W_shaft, W_electric, Q_to_air, h_out
        """
        plr = m_dot / self.m_dot_design if self.m_dot_design > 0 else 0.0
        plr = max(0.0, min(plr, 1.0))  # Clamp between 0 and 1
        p_frac = self.power_curve(plr)

        w_shaft = (m_dot * self.delta_p) / (self.rho * self.eta_fan)
        w_electric = p_frac * self.w_electric_design
        q_to_air = self.f_motor_to_air * (w_electric - w_shaft)
        h_out = h_in + (q_to_air / m_dot) if m_dot > 0 else h_in

        return {
            "PLR": plr,
            "P_frac": p_frac,
            "W_shaft": w_shaft,
            "W_electric": w_electric,
            "Q_to_air": q_to_air,
            "h_out": h_out,
        }
