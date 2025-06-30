from typing import Callable, Tuple

# -------------------------------
# 🔹 Single-variable Curves
# -------------------------------


def curve_linear(c1: float, c2: float) -> Callable[[float], float]:
    """y = C1 + C2 * x"""
    return lambda x: c1 + c2 * x


def curve_quadratic(c1: float, c2: float, c3: float) -> Callable[[float], float]:
    """y = C1 + C2 * x + C3 * x^2"""
    return lambda x: c1 + c2 * x + c3 * x**2


def curve_cubic(c1: float, c2: float, c3: float, c4: float) -> Callable[[float], float]:
    """y = C1 + C2 * x + C3 * x^2 + C4 * x^3"""
    return lambda x: c1 + c2 * x + c3 * x**2 + c4 * x**3


def curve_quartic(
    c1: float, c2: float, c3: float, c4: float, c5: float
) -> Callable[[float], float]:
    """y = C1 + C2 * x + C3 * x^2 + C4 * x^3 + C5 * x^4"""
    return lambda x: c1 + c2 * x + c3 * x**2 + c4 * x**3 + c5 * x**4


def curve_exponent(c1: float, c2: float, c3: float) -> Callable[[float], float]:
    """y = C1 + C2 * x^C3"""
    return lambda x: c1 + c2 * (x**c3)


# -------------------------------
# 🔹 Two-variable Curves
# -------------------------------


def curve_quadratic_linear(
    c: Tuple[float, float, float, float, float, float],
) -> Callable[[float, float], float]:
    """
    y = C1 + C2*x + C3*x^2 + C4*z + C5*x*z + C6*x^2*z
    """
    return (
        lambda x, z: c[0]
        + c[1] * x
        + c[2] * x**2
        + c[3] * z
        + c[4] * x * z
        + c[5] * x**2 * z
    )


def curve_cubic_linear(
    c: Tuple[float, float, float, float, float, float, float, float],
) -> Callable[[float, float], float]:
    """
    y = C1 + C2*x + C3*x^2 + C4*x^3 + C5*z + C6*x*z + C7*x^2*z + C8*x^3*z
    """
    return (
        lambda x, z: c[0]
        + c[1] * x
        + c[2] * x**2
        + c[3] * x**3
        + c[4] * z
        + c[5] * x * z
        + c[6] * x**2 * z
        + c[7] * x**3 * z
    )


def curve_biquadratic(
    c: Tuple[float, float, float, float, float, float],
) -> Callable[[float, float], float]:
    """
    y = C1 + C2*x + C3*x^2 + C4*z + C5*z^2 + C6*x*z
    """
    return (
        lambda x, z: c[0]
        + c[1] * x
        + c[2] * x**2
        + c[3] * z
        + c[4] * z**2
        + c[5] * x * z
    )


def curve_bicubic(c: Tuple[float, ...]) -> Callable[[float, float], float]:
    """
    Full 13-coefficient bi-cubic curve
    """
    return lambda x, z: (
        c[0]
        + c[1] * x
        + c[2] * x**2
        + c[3] * x**3
        + c[4] * z
        + c[5] * z**2
        + c[6] * z**3
        + c[7] * x * z
        + c[8] * x**2 * z
        + c[9] * x * z**2
        + c[10] * x**2 * z**2
        + c[11] * x * z**3
        + c[12] * x**3 * z
    )


# -------------------------------
# 🔹 Three-variable Curve
# -------------------------------


def curve_triquadratic(c: Tuple[float, ...]) -> Callable[[float, float, float], float]:
    """
    w = C1 + C2*x + C3*x^2 + C4*y + C5*y^2 + C6*z + C7*z^2 +
        C8*x*y + C9*x*z + C10*y*z + C11*x*y*z
    """
    return lambda x, y, z: (
        c[0]
        + c[1] * x
        + c[2] * x**2
        + c[3] * y
        + c[4] * y**2
        + c[5] * z
        + c[6] * z**2
        + c[7] * x * y
        + c[8] * x * z
        + c[9] * y * z
        + c[10] * x * y * z
    )


# -------------------------------
# 🔹 Specialized Curves
# -------------------------------


def curve_functional_pressure_drop(c1: float, c2: float) -> Callable[[float], float]:
    """
    ΔP = C1 + C2 * V^2
    """
    return lambda v: c1 + c2 * v**2


def curve_fan_pressure_rise(
    c: Tuple[float, float, float, float, float, float],
) -> Callable[[float, float], float]:
    """
    ΔP = C1 + C2*Q + C3*Q^2 + C4*Pduct + C5*Pduct^2 + C6*Q*Pduct
    """
    return lambda q, p_duct: (
        c[0]
        + c[1] * q
        + c[2] * q**2
        + c[3] * p_duct
        + c[4] * p_duct**2
        + c[5] * q * p_duct
    )


def curve_rectangular_hyperbola_2(
    c1: float, c2: float, c3: float
) -> Callable[[float], float]:
    """
    y = (C1 * x) / (C2 + x) + C3 * x
    """
    return lambda x: (c1 * x) / (c2 + x) + c3 * x

def make_speed_scaled_fan_curve(
    base_curve: Callable[[float, float], float],
    N_ref: float,
) -> Callable[[float, float, float], float]:
    """
    Wraps a fan pressure curve to support speed scaling via affinity laws.

    Args:
        base_curve (Callable): A function f(Q, P_duct) -> ΔP at reference speed.
        N_ref (float): Reference fan speed (RPM) used to derive base_curve.

    Returns:
        Callable[[float, float, float], float]: ΔP = f(Q, P_duct, RPM)
    """
    return lambda Q, P_duct, N: (N / N_ref) ** 2 * base_curve(Q / (N / N_ref), P_duct)

