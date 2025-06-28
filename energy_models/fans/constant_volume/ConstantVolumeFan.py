"""
Variable speed constant volume fan model.
"""


class ConstantVolumeFan:
    def __init__(
        self,
        delta_p: float,
        rho: float,
        eta_fan: float,
        eta_motor: float,
        f_motor_to_air: float,
    ):
        """Initialize the fan with design parameters.

        Args:
            delta_p: Pressure rise across fan (Pa).
            rho: Air density (kg/m³).
            eta_fan: Fan total efficiency (0-1).
            eta_motor: Motor efficiency (0-1).
            f_motor_to_air: Fraction of motor heat added to air (0-1).
        """
        self.delta_p = delta_p
        self.rho = rho
        self.eta_fan = eta_fan
        self.eta_motor = eta_motor
        self.f_motor_to_air = f_motor_to_air

    def compute(self, m_dot: float, h_in: float) -> dict:
        """Compute fan outputs for given mass flow and inlet enthalpy.

        Args:
            m_dot: Mass flow rate (kg/s).
            h_in: Inlet air enthalpy (J/kg).

        Returns:
            dict: A dictionary containing:
                - W_shaft (float): Shaft power input to the fan (W).
                - W_electric (float): Electric power consumed by the motor (W).
                - Q_to_air (float): Heat added to air due to motor losses (W).
                - h_out (float): Outlet air enthalpy (J/kg).
        """
        W_shaft = (m_dot * self.delta_p) / (self.rho * self.eta_fan)
        W_electric = W_shaft / self.eta_motor
        Q_to_air = self.f_motor_to_air * (W_electric - W_shaft)
        h_out = h_in + Q_to_air / m_dot

        return {
            "W_shaft": W_shaft,
            "W_electric": W_electric,
            "Q_to_air": Q_to_air,
            "h_out": h_out,
        }
