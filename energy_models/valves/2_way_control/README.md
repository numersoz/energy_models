# 📘 Valve: 2-Way Control Valve — Configurable Characteristic Model

Reference: https://www.belimo.com/mam/europe/technical-documentation/project_planning_notes/belimo_notes-for-project-planning_2-way-3-way-characterised-control-valves_en-gb.pdf

## 📌 Summary

| Property                   | Value                                                        |
|----------------------------|--------------------------------------------------------------|
| **Valve Type**             | Characterized 2-Way Control Valve                           |
| **Control Method**         | Modulating (continuous 0–1 signal)                          |
| **Flow Characteristic**    | Equal-Percentage, Linear, or Quick Opening (user-selectable)|
| **Input Signal**           | Valve position (0–1)                                        |
| **Output**                 | Water flow rate (m³/h or kg/s)                              |
| **Dependencies**           | Pressure drop, actuator position                            |
| **Best For**               | Cooling/heating coil flow control                           |
| **Notes**                  | Selectable Kv shaping enables flexible control performance  |

---

#### 1. Flow Through Valve:

$$
\dot{V} = k_v(x) \cdot \sqrt{\Delta p}
$$

- $\dot{V}$: Volumetric flow rate (m³/h)  
- $k_v(x)$: Flow coefficient based on characteristic type  
- $\Delta p$: Pressure drop across valve (kPa)

---

#### 2. Flow Coefficient Curves by Type:

**(a) Equal-Percentage:**

$$
k_v(x) = 
\begin{cases}
0 & x \leq x_0 \\\\
k_{vs} \cdot \left( \frac{x - x_0}{1 - x_0} \right)^n & x > x_0
\end{cases}
$$

**(b) Linear:**

$$
k_v(x) = 
\begin{cases}
0 & x \leq x_0 \\\\
k_{vs} \cdot \left( \frac{x - x_0}{1 - x_0} \right) & x > x_0
\end{cases}
$$

**(c) Quick Opening:**

$$
k_v(x) = 
\begin{cases}
0 & x \leq x_0 \\\\
k_{vs} \cdot \sqrt{ \frac{x - x_0}{1 - x_0} } & x > x_0
\end{cases}
$$

- $k_{vs}$: Nominal flow coefficient (m³/h·√kPa)  
- $x$: Valve position (0–1)  
- $x_0$: Minimum effective stroke (e.g. 0.15)  
- $n$: Equal-percentage exponent (e.g. 3.5)

---

#### 3. Mass Flow Rate:

$$
\dot{m} = \rho \cdot \frac{\dot{V}}{3600}
$$

- $\dot{m}$: Mass flow rate (kg/s)  
- $\rho$: Water density (kg/m³)

---

#### 4. Valve Authority (Optional Design Metric):

$$
\text{Authority} = \frac{\Delta p_{\text{valve}}}{\Delta p_{\text{valve}} + \Delta p_{\text{coil}}}
$$

- Design target: Authority ≥ 0.5 for good modulating behavior

---

#### 5. Control Logic:

- Control signal $x \in [0, 1]$ determines valve position
- User selects flow characteristic: Equal-Percentage / Linear / Quick Opening
- Flow rate shaped via $k_v(x)$, then scaled by pressure
- Output mass flow is fed to coil or terminal unit

---

#### 6. Choosing a Characteristic:

| Type             | Behavior                                  | Best For                             |
|------------------|--------------------------------------------|---------------------------------------|
| **Equal-Percentage** | Slow at low signal, steep at high signal | Compensating for nonlinear coils      |
| **Linear**        | Constant change in flow per % open        | Constant ΔP circuits or test loops    |
| **Quick Opening** | High flow early, flattens near top        | On/off-like applications or dump valves |

---
