# 📘 Valve: 3-Way Control Valve — Configurable Characteristic Model

Reference: https://www.belimo.com/mam/europe/technical-documentation/project_planning_notes/belimo_notes-for-project-planning_2-way-3-way-characterised-control-valves_en-gb.pdf

## 📌 Summary

| Property                   | Value                                                                |
|----------------------------|----------------------------------------------------------------------|
| **Valve Type**             | Characterized 3-Way Mixing or Diverting Valve                        |
| **Control Method**         | Modulating (continuous 0–1 signal)                                   |
| **Flow Characteristic**    | User-defined for both A–AB and B–AB ports                            |
| **Input Signal**           | Valve position (0–1)                                                 |
| **Outputs**                | Two flow paths: A–AB and B–AB                                        |
| **Dependencies**           | Pressure drop at each port, actuator position                        |
| **Best For**               | Constant flow systems, configurable hydraulic design                 |
| **Notes**                  | Each port can be set to Equal %, Linear, or Quick Opening; Bypass flow cap adjustable |

---

#### 1. Flow Through A–AB (Control Port):

$$
\dot{V}_A = k_{v,A}(x) \cdot \sqrt{\Delta p_A}
$$

- $\dot{V}_A$: Flow through control port A–AB (m³/h)  
- $k_{v,A}(x)$: Flow coefficient based on chosen A-port characteristic  
- $\Delta p_A$: Pressure drop across A–AB (kPa)

---

#### 2. Flow Through B–AB (Bypass Port):

$$
\dot{V}_B = k_{v,B}(x) \cdot \sqrt{\Delta p_B}
$$

- $\dot{V}_B$: Flow through B–AB (m³/h)  
- $k_{v,B}(x)$: Flow coefficient based on B-port characteristic, scaled by cap ratio  
- $\Delta p_B$: Pressure drop across B–AB (kPa)

---

#### 3. Flow Coefficient Curves (Both Ports):

Let $x_0$ be minimum effective stroke, $n$ be exponent, and $r$ be bypass cap ratio (e.g., 0.7).

**Equal-Percentage:**

$$
k_v(x) = 
\begin{cases}
0 & x \leq x_0 \\
k_{vs} \cdot \left(\frac{x - x_0}{1 - x_0}\right)^n & x > x_0
\end{cases}
$$

**Linear:**

$$
k_v(x) = 
\begin{cases}
0 & x \leq x_0 \\
k_{vs} \cdot \left(\frac{x - x_0}{1 - x_0}\right) & x > x_0
\end{cases}
$$

**Quick Opening:**

$$
k_v(x) = 
\begin{cases}
0 & x \leq x_0 \\
k_{vs} \cdot \sqrt{\frac{x - x_0}{1 - x_0}} & x > x_0
\end{cases}
$$

Note: For B–AB, multiply result by cap ratio $r$.

---

#### 4. Mass Flow Rate:

$$
\dot{m}_A = \rho \cdot \frac{\dot{V}_A}{3600}, \quad \dot{m}_B = \rho \cdot \frac{\dot{V}_B}{3600}
$$

- $\dot{m}_A$, $\dot{m}_B$: Mass flow through each port (kg/s)  
- $\rho$: Fluid density (kg/m³)

---

#### 5. Total System Flow:

$$
\dot{V}_{\text{total}} = \dot{V}_A + \dot{V}_B
$$

- Sum of control and bypass flow

---

#### 6. Valve Authority (A–AB Port Only):

$$
\text{Authority} = \frac{\Delta p_A}{\Delta p_A + \Delta p_{\text{coil}}}
$$

- Helps determine control stability

---

#### 7. Control Logic:

- Each port characteristic independently selectable: `equal_percentage`, `linear`, or `quick_opening`
- Bypass port can be scaled using `bypass_ratio` (default 0.7)
- Flow and mass calculations follow same logic for both ports

---

#### 8. Supported Configurations

| A–AB (Control Port)   | B–AB (Bypass Port)   | Feasible? | Notes |
|------------------------|------------------------|-----------|--------|
| Equal-Percentage       | Linear                 | ✅ Common | Matches Belimo standard |
| Equal-Percentage       | Equal-Percentage       | ✅ Rare   | Nonlinear balance |
| Equal-Percentage       | Quick Opening          | ⚠️ Risk | Less predictable bypass |
| Linear                 | Linear                 | ✅ Simple | Uniform change on both sides |
| Linear                 | Equal-Percentage       | ⚠️ Risk | May create instability |
| Quick Opening          | Linear                 | ⚠️ Risk | Overshoot potential |
| Quick Opening          | Quick Opening          | ❌ Avoid | Poor control behavior |

---

#### 9. Why Adjustable Bypass Ratio?

> “The flow rate in the bypass B–AB is designed to be 70% of the kvs value of the control path (A–AB). The characteristic curve in the bypass is linear.”  
> — Belimo Notes for Project Planning

- **Default**: 70% of A–AB Kv  
- **Adjustable**: Use `bypass_ratio` to override this value if needed  
- Ensures better match for coils or terminals in non-standard systems

---