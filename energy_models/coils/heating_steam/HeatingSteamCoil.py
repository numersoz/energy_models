from typing import Callable, Dict

class SteamHeatingCoil:
    def __init__(
        self,
        h_fg: float,  # Latent heat of vaporization (J/kg)
        cp_cond: float,  # Specific heat of condensate (J/kg·K)
        deltaT_subcool_total: float,  # Total subcooling (°C)
        m_dot_max: float,  # Max steam mass flow rate (kg/s)
        availability_schedule: Callable[[float], bool] = lambda t: True,
        control_schedule: Callable[[float], float] = lambda t: 1.0,  # Load fraction [0-1]
    ):
        """
        Steam heating coil with subcooling and latent heat modeling.

        Args:
            h_fg (float): Latent heat of vaporization of steam (J/kg)
            cp_cond (float): Specific heat of condensate (J/kg·K)
            deltaT_subcool_total (float): Total subcooling temperature (°C)
            m_dot_max (float): Max steam flow rate (kg/s)
            availability_schedule (Callable): True if coil is available at time t
            control_schedule (Callable): Returns load fraction [0-1] at time t
        """
        self.h_fg = h_fg
        self.cp_cond = cp_cond
        self.deltaT_subcool_total = deltaT_subcool_total
        self.m_dot_max = m_dot_max
        self.availability_schedule = availability_schedule
        self.control_schedule = control_schedule

    def compute(self, t: float) -> Dict[str, float]:
        """
        Compute the steam heating coil output at time t.

        Args:
            t (float): Simulation time in hours

        Returns:
            dict: Output parameters including heat added and steam flow rate
        """
        if not self.availability_schedule(t):
            return {"Q_total": 0.0, "m_dot_steam": 0.0}

        load_fraction = max(0.0, min(1.0, self.control_schedule(t)))
        m_dot_steam = self.m_dot_max * load_fraction

        Q_latent = m_dot_steam * self.h_fg
        Q_sensible = m_dot_steam * self.cp_cond * self.deltaT_subcool_total
        Q_total = Q_latent + Q_sensible

        return {
            "Q_total": Q_total,
            "Q_latent": Q_latent,
            "Q_sensible": Q_sensible,
            "m_dot_steam": m_dot_steam,
        }
