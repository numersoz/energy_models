from typing import Callable, Dict
from scipy.optimize import root_scalar


class CurveSpeedControlledFan:
    def __init__(
        self,
        rho: float,
        area_outlet: float,
        eta_fan: float,
        eta_motor: float,
        f_motor_to_air: float,
        fan_curve: Callable[[float, float], float],
        system_pressure_func: Callable[[float], float],
        belt_loss_func: Callable[[float], float] = lambda x: 0.0,
        vfd_loss_func: Callable[[float], float] = lambda x: 0.0,
    ):
        """
        High-fidelity variable-speed fan model with system pressure feedback.

        Args:
            rho (float): Air density (kg/m³).
            area_outlet (float): Fan outlet area (m²).
            eta_fan (float): Fan efficiency (0-1).
            eta_motor (float): Motor efficiency (0-1).
            f_motor_to_air (float): Fraction of motor losses added to air stream.
            fan_curve (Callable[[float, float], float]): Function mapping (Q, RPM) to fan pressure rise (Pa).
            system_pressure_func (Callable[[float], float]): Function mapping Q to downstream system pressure loss (Pa).
            belt_loss_func (Callable[[float], float], optional): Returns belt loss (W) from shaft power.
            vfd_loss_func (Callable[[float], float], optional): Returns VFD loss (W) from motor input power.
        """
        self.rho = rho
        self.area_outlet = area_outlet
        self.eta_fan = eta_fan
        self.eta_motor = eta_motor
        self.f_motor_to_air = f_motor_to_air
        self.fan_curve = fan_curve
        self.system_pressure_func = system_pressure_func
        self.belt_loss_func = belt_loss_func
        self.vfd_loss_func = vfd_loss_func

    def compute(self, rpm: float, h_in: float) -> Dict[str, float]:
        """
        Compute fan performance at given fan speed and outlet static pressure.

        Args:
            rpm (float): Fan rotational speed in RPM.
            h_in (float): Inlet air enthalpy (J/kg).

        Returns:
            Dict[str, float]: Dictionary of computed fan performance values.
        """

        def residual(Q: float) -> float:
            return self.fan_curve(Q, rpm) - self.system_pressure_func(Q)

        sol = root_scalar(residual, bracket=[0.01, 20.0], method='brentq')
        if not sol.converged:
            raise RuntimeError("Fan flow solver did not converge.")
        Q = sol.root

        # Compute pressures
        delta_p_fan = self.fan_curve(Q, rpm)
        v_out = Q / self.area_outlet
        p_velocity = 0.5 * self.rho * v_out**2
        delta_p_static = delta_p_fan - p_velocity

        # Power calculations
        W_shaft = Q * delta_p_fan / self.eta_fan
        W_belt = self.belt_loss_func(W_shaft)
        W_motor_in = (W_shaft + W_belt) / self.eta_motor
        W_vfd = self.vfd_loss_func(W_motor_in)
        W_electric = W_motor_in + W_vfd

        # Thermal output
        m_dot = self.rho * Q
        Q_to_air = self.f_motor_to_air * (W_electric - W_shaft - W_belt)
        h_out = h_in + (Q_to_air / m_dot) if m_dot > 0 else h_in

        return {
            "Q": Q,
            "RPM": rpm,
            "DeltaP_fan": delta_p_fan,
            "DeltaP_static": delta_p_static,
            "W_shaft": W_shaft,
            "W_belt": W_belt,
            "W_motor_in": W_motor_in,
            "W_vfd": W_vfd,
            "W_electric": W_electric,
            "Q_to_air": Q_to_air,
            "h_out": h_out,
            "m_dot": m_dot,
        }
