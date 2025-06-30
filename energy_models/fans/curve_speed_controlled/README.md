# 📘 Fan: Curve-Based with System Feedback — Variable-Speed Model

Reference: https://bigladdersoftware.com/epx/docs/9-6/input-output-reference/group-fans.html#fancomponentmodel

## 📌 Summary

| Property               | Value                                                  |
|------------------------|--------------------------------------------------------|
| **Fan Type**           | Variable-speed with RPM input                         |
| **Control Type**       | Speed-controlled (RPM setpoint)                       |
| **Flow Behavior**      | Solved from fan curve and system resistance           |
| **Pressure Rise**      | Interpolated from manufacturer fan curve              |
| **Power Model**        | Full physics: fan, motor, belt, VFD                   |
| **Heat to Air**        | Explicitly modeled                                    |
| **System Loss**        | Based on downstream pressure curve                    |
| **Best For**           | High-fidelity simulation, digital twins, calibration  |
| **Notes**              | Requires full fan curve and system resistance model   |

---

#### 1. Flow Rate (Implicit Root-Solved)

Fan curve defines pressure rise as a function of flow and RPM:

$$
\Delta P_{\text{fan}}(Q, \text{RPM}) = \text{fan\_curve}(Q, \text{RPM})
$$

System resistance defines required pressure:

$$
\Delta P_{\text{system}}(Q) = \text{downstream\_pressure\_func}(Q)
$$

We solve for flow $ Q $ such that:

$$
\Delta P_{\text{fan}}(Q, \text{RPM}) = \Delta P_{\text{system}}(Q)
$$

- `fan_curve(Q, RPM)`: Interpolated fan data (m³/s vs Pa for given RPM)  
- `downstream_pressure_func(Q)`: Returns downstream pressure loss at Q (Pa)  
- `RPM`: Fan rotational speed input (rev/min)  
- **Solving this equation yields**: volumetric flow rate $ Q $ (m³/s)

---

#### 2. Air Velocity and Static Pressure Rise

Outlet air velocity is:

$$
v_{\text{out}} = \frac{Q}{A_{\text{out}}}
$$

Outlet velocity pressure is:

$$
P_{\text{velocity}} = \tfrac12 \rho v_{\text{out}}^2
$$

Then:

$$
\Delta P_{\text{fan,static}} = \Delta P_{\text{fan}} - P_{\text{velocity}}
$$

- $ v_{\text{out}} $: Outlet velocity (m/s)  
- $ A_{\text{out}} $: Outlet cross-sectional area (m²)  
- $ \rho $: Air density (kg/m³)

---

#### 3. Shaft Power

$$
\dot{W}_{\text{shaft}} = \frac{Q \cdot \Delta P_{\text{fan}}}{\eta_{\text{fan}}}
$$

- $ \eta_{\text{fan}} $: Fan total efficiency (0–1)

---

#### 4. Belt and Motor Losses

**Belt Loss:**

$$
\dot{W}_{\text{belt}} = \text{belt\_loss\_func}(\dot{W}_{\text{shaft}})
$$

**Motor Input Power:**

$$
\dot{W}_{\text{motor\_in}} = \frac{\dot{W}_{\text{shaft}} + \dot{W}_{\text{belt}}}{\eta_{\text{motor}}}
$$

- $ \eta_{\text{motor}} $: Motor efficiency (0–1)

---

#### 5. VFD Losses (Optional)

$$
\dot{W}_{\text{vfd}} = \text{vfd\_loss\_func}(\dot{W}_{\text{motor\_in}})
$$

Total electric power:

$$
\dot{W}_{\text{electric}} = \dot{W}_{\text{motor\_in}} + \dot{W}_{\text{vfd}}
$$

---

#### 6. Heat Added to Air

$$
\dot{Q}_{\text{to air}} = f_{\text{motor to air}} \cdot (\dot{W}_{\text{electric}} - \dot{W}_{\text{shaft}} - \dot{W}_{\text{belt}})
$$

- $ f_{\text{motor to air}} $: Fraction of motor losses entering air stream (0–1)

---

#### 7. Outlet Air Enthalpy

$$
h_{\text{out}} = h_{\text{in}} + \frac{\dot{Q}_{\text{to air}}}{\dot{m}}, \quad \dot{m} = \rho Q
$$

- $ h_{\text{in/out}} $: Inlet/outlet enthalpy (J/kg)  
- $ \dot{m} $: Air mass flow rate (kg/s)

---
