from typing import Dict, Literal
import math


class ThreeWayControlValve:
    """
    3-Way Characterized Control Valve Model

    Supports independent flow characteristics for A-AB and B-AB ports.

    Flow characteristics:
        - "equal_percentage" (nonlinear)
        - "linear" (direct proportional)
        - "quick_opening" (concave down)

    B-AB port flow is scaled by a bypass ratio (typically 0.7 per Belimo).

    Attributes:
        kvs_a (float): Nominal Kv for A-AB (m³/h·√kPa)
        kvs_b (float): Nominal Kv for B-AB (m³/h·√kPa)
        rho (float): Fluid density (kg/m³)
        x0 (float): Minimum effective opening (default: 0.15)
        exponent_a (float): Exponent for equal-percentage curve A-AB
        exponent_b (float): Exponent for equal-percentage curve B-AB
        characteristic_a (str): Flow characteristic of A-AB
        characteristic_b (str): Flow characteristic of B-AB
        bypass_ratio (float): Maximum Kv(B-AB) as % of Kv(A-AB)
    """

    def __init__(
        self,
        kvs_a: float,
        kvs_b: float,
        rho: float,
        x0: float = 0.15,
        exponent_a: float = 3.5,
        exponent_b: float = 3.5,
        characteristic_a: Literal["equal_percentage", "linear", "quick_opening"] = "equal_percentage",
        characteristic_b: Literal["equal_percentage", "linear", "quick_opening"] = "linear",
        bypass_ratio: float = 0.7,
    ):
        """
        Initialize the 3-way valve model.

        Args:
            kvs_a (float): Nominal Kv for A-AB (m³/h·√kPa)
            kvs_b (float): Nominal Kv for B-AB (m³/h·√kPa)
            rho (float): Fluid density (kg/m³)
            x0 (float): Minimum stroke threshold (0-1)
            exponent_a (float): Exponent for A-AB (if equal-percentage)
            exponent_b (float): Exponent for B-AB (if equal-percentage)
            characteristic_a (str): A-AB port flow type ("equal_percentage", "linear", "quick_opening")
            characteristic_b (str): B-AB port flow type
            bypass_ratio (float): Bypass scaling factor (default 0.7)
        """
        self.kvs_a = kvs_a
        self.kvs_b = kvs_b
        self.rho = rho
        self.x0 = x0
        self.exponent_a = exponent_a
        self.exponent_b = exponent_b
        self.characteristic_a = characteristic_a
        self.characteristic_b = characteristic_b
        self.bypass_ratio = bypass_ratio

    def _kv(self, x: float, kvs: float, characteristic: str, exponent: float = 3.5) -> float:
        """Compute Kv based on characteristic curve.

        Args:
            x (float): Valve position (0-1)
            kvs (float): Full-stroke Kv
            characteristic (str): Flow type
            exponent (float): Only used for equal-percentage

        Returns:
            float: Effective flow coefficient
        """
        if x <= self.x0:
            return 0.0
        normalized = (x - self.x0) / (1 - self.x0)
        if characteristic == "equal_percentage":
            return kvs * normalized ** exponent
        elif characteristic == "linear":
            return kvs * normalized
        elif characteristic == "quick_opening":
            return kvs * math.sqrt(normalized)
        raise ValueError(f"Unsupported characteristic: {characteristic}")

    def kv_a(self, x: float) -> float:
        """Return Kv of A-AB port at signal x."""
        return self._kv(x, self.kvs_a, self.characteristic_a, self.exponent_a)

    def kv_b(self, x: float) -> float:
        """Return Kv of B-AB port at signal x (inverted and scaled)."""
        raw_kv = self._kv(1 - x, self.kvs_b, self.characteristic_b, self.exponent_b)
        return raw_kv * self.bypass_ratio

    def compute(self, x: float, delta_p_a: float, delta_p_b: float) -> Dict[str, float]:
        """
        Compute volumetric and mass flow rates for both A-AB and B-AB.

        Args:
            x (float): Valve signal (0-1)
            delta_p_a (float): Pressure drop across A-AB (kPa)
            delta_p_b (float): Pressure drop across B-AB (kPa)

        Returns:
            dict: Includes Kv, V_dot, and m_dot for both ports
        """
        kv_a_val = self.kv_a(x)
        kv_b_val = self.kv_b(x)

        V_dot_a = kv_a_val * math.sqrt(delta_p_a)  # m³/h
        V_dot_b = kv_b_val * math.sqrt(delta_p_b)  # m³/h

        m_dot_a = self.rho * V_dot_a / 3600  # kg/s
        m_dot_b = self.rho * V_dot_b / 3600  # kg/s

        return {
            "kv_a": kv_a_val,
            "V_dot_a": V_dot_a,
            "m_dot_a": m_dot_a,
            "kv_b": kv_b_val,
            "V_dot_b": V_dot_b,
            "m_dot_b": m_dot_b,
        }
