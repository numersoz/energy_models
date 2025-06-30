# 📈 EnergyPlus Performance Curves — All Types and Formulas

These curves are used throughout EnergyPlus to model performance of HVAC and plant components such as fans, coils, pumps, and pressure drops. So custom curves not covered by EnergyPlus also exist.

Reference: https://bigladdersoftware.com/epx/docs/9-0/input-output-reference/group-performance-curves.html#group---performance-curves

---

## 🔹 1. Curve:Linear

$$
y = C_1 + C_2 \cdot x
$$

---

## 🔹 2. Curve:Quadratic

$$
y = C_1 + C_2 \cdot x + C_3 \cdot x^2
$$

---

## 🔹 3. Curve:Cubic

$$
y = C_1 + C_2 \cdot x + C_3 \cdot x^2 + C_4 \cdot x^3
$$

---

## 🔹 4. Curve:Quartic

$$
y = C_1 + C_2 \cdot x + C_3 \cdot x^2 + C_4 \cdot x^3 + C_5 \cdot x^4
$$

---

## 🔹 5. Curve:Exponent

$$
y = C_1 + C_2 \cdot x^{C_3}
$$

---

## 🔹 6. Curve:QuadraticLinear

$$
y = C_1 + C_2 \cdot x + C_3 \cdot x^2 + C_4 \cdot z + C_5 \cdot x \cdot z + C_6 \cdot x^2 \cdot z
$$

Where:
- $x$ = independent variable 1  
- $z$ = independent variable 2

---

## 🔹 7. Curve:CubicLinear

$$
y = C_1 + C_2 \cdot x + C_3 \cdot x^2 + C_4 \cdot x^3 + C_5 \cdot z + C_6 \cdot x \cdot z + C_7 \cdot x^2 \cdot z + C_8 \cdot x^3 \cdot z
$$

Where:
- $x$ = independent variable 1  
- $z$ = independent variable 2

---

## 🔹 8. Curve:BiQuadratic

$$
y = C_1 + C_2 \cdot x + C_3 \cdot x^2 + C_4 \cdot z + C_5 \cdot z^2 + C_6 \cdot x \cdot z
$$

Where:
- $x$ = independent variable 1  
- $z$ = independent variable 2

---

## 🔹 9. Curve:BiCubic

$$
\begin{aligned}
y =&\ C_1 + C_2 x + C_3 x^2 + C_4 x^3 + C_5 z + C_6 z^2 + C_7 z^3 \\
   &+ C_8 x z + C_9 x^2 z + C_{10} x z^2 + C_{11} x^2 z^2 + C_{12} x z^3 + C_{13} x^3 z
\end{aligned}
$$

Where:
- $x$, $z$ = independent variables

---

## 🔹 10. Curve:TriQuadratic

$$
\begin{aligned}
w =&\ C_1 + C_2 x + C_3 x^2 + C_4 y + C_5 y^2 + C_6 z + C_7 z^2 \\
   &+ C_8 x y + C_9 x z + C_{10} y z + C_{11} x y z
\end{aligned}
$$

Where:
- $x$, $y$, $z$ = independent variables  
- $w$ = output value

---

## 🔹 11. Curve:Functional:PressureDrop

Used for modeling pressure loss in piping or ductwork:

$$
\Delta P = C_1 + C_2 \cdot V^2
$$

Where:
- $\Delta P$ = pressure drop (Pa)  
- $V$ = fluid velocity (m/s)

---

## 🔹 12. Curve:FanPressureRise

Used in `Fan:ComponentModel` to model dynamic pressure characteristics:

$$
\Delta P = C_1 + C_2 \cdot Q + C_3 \cdot Q^2 + C_4 \cdot P_{\text{duct}} + C_5 \cdot P_{\text{duct}}^2 + C_6 \cdot Q \cdot P_{\text{duct}}
$$

Where:
- $Q$ = air volume flow rate (m³/s)  
- $P_{\text{duct}}$ = duct static pressure (Pa)  
- $\Delta P$ = fan total pressure rise (Pa)

---

## 🔹 13. Curve:RectangularHyperbola2

Used to represent hyperbolic relationships, such as coil UA:

$$
y = \frac{C_1 \cdot x}{C_2 + x} + C_3 \cdot x
$$

Where:
- $x$ = independent variable  
- $y$ = dependent variable

---

---

## 🔹 14. Curve:FanPressureRise:SpeedScaled

Extends `Curve:FanPressureRise` to support variable-speed fans using fan affinity laws.

### ⚙️ Speed-Aware Pressure Rise

$$
\Delta P(N) = \left( \frac{N}{N_{\text{ref}}} \right)^2 \cdot \Delta P\left( \frac{Q}{N / N_{\text{ref}}},\ P_{\text{duct}} \right)
$$

Where:
- $N$ = current fan speed (RPM)  
- $N_{\text{ref}}$ = reference fan speed (RPM at which the coefficients were derived)  
- $Q$ = actual flow rate (m³/s)  
- $P_{\text{duct}}$ = duct static pressure (Pa)  
- $\Delta P$ = fan total pressure rise (Pa)

### 🧠 Notes
- This preserves the shape of the original fan curve.
- Enables reuse of fan manufacturer data from a single speed across a full operating range.
- Required for accurate modeling of VFD-controlled fans.
