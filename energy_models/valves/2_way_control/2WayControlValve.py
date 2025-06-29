from typing import Dict, Literal


class TwoWayControlValve:
    def __init__(
        self,
        kvs: float,
        x0: float,
        characteristic: Literal["equal_percentage", "linear", "quick_opening"],
        exponent: float,
        rho: float,
    ):
        """
        2-Way control valve with selectable flow characteristic.

        Args:
            kvs (float): Nominal flow coefficient at full open (m³/h·√kPa)
            x0 (float): Minimum effective stroke (0-1)
            characteristic (str): Flow type: "equal_percentage", "linear", "quick_opening"
            exponent (float): Exponent for equal-percentage curve
            rho (float): Water density (kg/m³)
        """
        self.kvs = kvs
        self.x0 = x0
        self.characteristic = characteristic
        self.exponent = exponent
        self.rho = rho

    def kv(self, x: float) -> float:
        """
        Compute Kv at valve position x, based on selected characteristic.

        Args:
            x (float): Valve position (0-1)

        Returns:
            float: Partial Kv
        """
        if x <= self.x0:
            return 0.0

        scaled_x = (x - self.x0) / (1 - self.x0)

        if self.characteristic == "equal_percentage":
            return self.kvs * (scaled_x ** self.exponent)
        elif self.characteristic == "linear":
            return self.kvs * scaled_x
        elif self.characteristic == "quick_opening":
            return self.kvs * (scaled_x ** 0.5)
        else:
            raise ValueError(f"Unknown valve characteristic: {self.characteristic}")

    def compute(self, x: float, delta_p: float) -> Dict[str, float]:
        """
        Compute flow through valve.

        Args:
            x (float): Valve position (0-1)
            delta_p (float): Pressure drop across valve (kPa)

        Returns:
            dict: Kv, volumetric flow (m³/h), and mass flow (kg/s)
        """
        kv_val = self.kv(x)
        V_dot = kv_val * (delta_p ** 0.5)  # m³/h
        m_dot = self.rho * V_dot / 3600    # kg/s

        return {
            "kv": kv_val,
            "V_dot": V_dot,
            "m_dot": m_dot,
        }