from typing import Callable, Dict


class ElectricHeatingCoil:
    def __init__(
        self,
        q_nominal: float,
        eta: float,
        rho_air: float,
        availability_schedule: Callable[[float], bool] = lambda t: True,
        load_fraction_func: Callable[[float], float] = lambda t: 1.0,
    ):
        """
        Electric Heating Coil Model (Coil:Heating:Electric)

        Args:
            q_nominal (float): Nominal heating capacity (W)
            eta (float): Efficiency (0-1), usually 1.0
            rho_air (float): Air density (kg/m³)
            availability_schedule (Callable): Returns True if coil is available at time t
            load_fraction_func (Callable): Returns load fraction [0-1] at time t
        """
        self.q_nominal = q_nominal
        self.eta = eta
        self.rho_air = rho_air
        self.availability_schedule = availability_schedule
        self.load_fraction_func = load_fraction_func

    def compute(
        self, t: float, m_dot_air: float, h_in: float
    ) -> Dict[str, float]:
        """
        Compute coil performance at time t.

        Args:
            t (float): Current time (e.g., in hours)
            m_dot_air (float): Air mass flow rate (kg/s)
            h_in (float): Inlet air enthalpy (J/kg)

        Returns:
            dict: Contains total heating, power draw, outlet enthalpy
        """
        if not self.availability_schedule(t):
            return {
                "Q_total": 0.0,
                "W_electric": 0.0,
                "h_out": h_in,
            }

        load_frac = max(min(self.load_fraction_func(t), 1.0), 0.0)
        q_total = self.q_nominal * load_frac
        w_electric = q_total / self.eta if self.eta > 0 else 0.0
        h_out = h_in + q_total / m_dot_air if m_dot_air > 0 else h_in

        return {
            "Q_total": q_total,
            "W_electric": w_electric,
            "h_out": h_out,
        }
