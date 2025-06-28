# 📘 FanPerformance: NightVentilation — Night Cooling Exhaust Fan

Reference: https://bigladdersoftware.com/epx/docs/9-6/input-output-reference/group-fans.html#fanperformancenightventilation

## 📌 Summary

| Property               | Value                                          |
|------------------------|------------------------------------------------|
| **Fan Type**           | Performance:NightVentilation (modifier)       |
| **Control Type**       | Switched via availability manager             |
| **Flow Behavior**      | Applies alternate flow fraction at night      |
| **Pressure Rise**      | Alternate value used in night mode            |
| **Power Model**        | Same formula, different input parameters      |
| **Heat to Air**        | Modeled as usual                              |
| **Scheduling**         | Controlled via AvailabilityManager logic      |
| **Best For**           | Passive cooling, night purge systems          |
| **Notes**              | Used in conjunction with base fan definition  |


---

#### 🔹 1. Alternate Design Flow & Pressure

Defines alternate “night” fan behavior:
- **Night flow fraction** $f_{\text{night}}$ (0–1)
- **Night pressure rise** $\Delta P_{\text{night}}$ (Pa)

---

#### 🔹 2. Mass Flow at Night

If nighttime cooling is active:

$$
\dot V_{\text{night}} = f_{\text{night}} \cdot \dot V_{\text{design}}
$$
$$
\dot m_{\text{night}} = \rho \cdot \dot V_{\text{night}}
$$

- $\dot V_{\text{design}}$: Design airflow (m³/s)  
- $\rho$: Air density (kg/m³)

---

#### 🔹 3. Electric Power (Night Conditions)

Given night mass flow and pressure:

$$
\dot W_{\text{electric, night}} = \frac{\dot m_{\text{night}} \cdot \Delta P_{\text{night}}}
{\rho \cdot \eta_{\text{total}}}
$$

- $\eta_{\text{total}}$: Combined fan + motor efficiency

---

#### 🔹 4. Shaft Power & Heat Rejection

$$
\dot W_{\text{shaft, night}} = \frac{\dot m_{\text{night}} \cdot \Delta P_{\text{night}}}
{\rho \cdot \eta_{\text{fan}}}
$$
$$
\dot Q_{\text{to air}} = \dot W_{\text{electric, night}} - \dot W_{\text{shaft, night}}
$$

---

#### 🔹 5. Outlet Enthalpy Rise

$$
h_{\text{out}} = h_{\text{in}} + \frac{\dot Q_{\text{to air}}}{\dot m_{\text{night}}}
$$

- Represents the **warmth added** by the motor/fan to the air stream

---

### ✅ Summary

- Enables defining a **night mode** for exhaust/supply fans with different design parameters
- Works with **AvailabilityManager:NightVentilation**
- Applies only when that manager calls nighttime operation
- Ensures correct power and heat modeling during night cooling strategies
