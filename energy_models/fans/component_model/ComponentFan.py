from typing import Callable, Dict


class ComponentFan:
    def __init__(
        self,
        rho: float,
        area_outlet: float,
        eta_fan: float,
        eta_motor: float,
        f_motor_to_air: float,
        pressure_coeffs: tuple,
        belt_loss_func: Callable[[float], float] = lambda x: 0.0,
        vfd_loss_func: Callable[[float], float] = lambda x: 0.0,
        static_reset_func: Callable[[float], float] = lambda Q: 0.0,
    ):
        """
        Initialize the Fan:ComponentModel.

        Args:
            rho (float): Air density (kg/m³)
            area_outlet (float): Fan outlet area (m²)
            eta_fan (float): Fan efficiency (0-1)
            eta_motor (float): Motor efficiency (0-1)
            f_motor_to_air (float): Fraction of motor heat added to air stream
            pressure_coeffs (tuple): Coefficients (C1-C6) for fan pressure rise model
            belt_loss_func (Callable): Function returning belt losses (W) from shaft power
            vfd_loss_func (Callable): Function returning VFD losses (W) from motor input
            static_reset_func (Callable): Function returning duct static pressure setpoint (Pa)
        """
        self.rho = rho
        self.area_outlet = area_outlet
        self.eta_fan = eta_fan
        self.eta_motor = eta_motor
        self.f_motor_to_air = f_motor_to_air
        self.C1, self.C2, self.C3, self.C4, self.C5, self.C6 = pressure_coeffs
        self.belt_loss_func = belt_loss_func
        self.vfd_loss_func = vfd_loss_func
        self.static_reset_func = static_reset_func

    def compute(self, Q: float, P_o: float, h_in: float) -> Dict[str, float]:
        """
        Compute the fan performance for given conditions.

        Args:
            Q (float): Volumetric flow rate (m³/s)
            P_o (float): Ambient/zone static pressure (Pa)
            h_in (float): Inlet air enthalpy (J/kg)

        Returns:
            Dict[str, float]: Computed fan results
        """
        P_sm = self.static_reset_func(Q)
        delta_P_total = (
            self.C1
            + self.C2 * Q
            + self.C3 * Q**2
            + self.C4 * (P_sm - P_o)
            + self.C5 * (P_sm - P_o) ** 2
            + self.C6 * Q * (P_sm - P_o)
        )

        velocity_out = Q / self.area_outlet
        delta_P_static = delta_P_total - 0.5 * self.rho * velocity_out**2

        W_shaft = Q * delta_P_total / self.eta_fan
        W_belt = self.belt_loss_func(W_shaft)
        W_motor_in = (W_shaft + W_belt) / self.eta_motor
        W_vfd = self.vfd_loss_func(W_motor_in)
        W_electric = W_motor_in + W_vfd

        Q_to_air = self.f_motor_to_air * (W_electric - W_shaft - W_belt)
        m_dot = self.rho * Q
        h_out = h_in + (Q_to_air / m_dot) if m_dot > 0 else h_in

        return {
            "P_static_setpoint": P_sm,
            "DeltaP_total": delta_P_total,
            "DeltaP_static": delta_P_static,
            "W_shaft": W_shaft,
            "W_belt": W_belt,
            "W_motor_in": W_motor_in,
            "W_vfd": W_vfd,
            "W_electric": W_electric,
            "Q_to_air": Q_to_air,
            "h_out": h_out,
            "m_dot": m_dot,
        }
