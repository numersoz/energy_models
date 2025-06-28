# 📘 Fan: ZoneExhaust — Exhaust Fan for Zones

Reference: https://bigladdersoftware.com/epx/docs/8-0/input-output-reference/page-043.html#fanzoneexhaust

## 📌 Summary

| Property               | Value                                     |
|------------------------|-------------------------------------------|
| **Fan Type**           | ZoneExhaust                               |
| **Control Type**       | Modulating (via schedule)                 |
| **Flow Behavior**      | Flow fraction of design flow              |
| **Pressure Rise**      | User-defined                              |
| **Power Model**        | Simple                                    |
| **Heat to Air**        | Included                                  |
| **Scheduling**         | Flow fraction + availability schedules    |
| **Best For**           | Bathrooms, kitchens, local exhaust fans  |
| **Notes**              | Not part of central air system loop       |

---

#### 🔹 1. Flow Rate Control

- Uses **fixed design flow** $\dot V_{\text{max}}$ (m³/s)
- Optional **flow fraction schedule** $f_{\text{fract}}$ may vary flow:

$$
\dot V = f_{\text{fract}} \cdot \dot V_{\text{max}}
$$

Convert to mass flow:

$$
\dot m = \rho \cdot \dot V
$$

- $\dot V$: instantaneous zone exhaust flow (m³/s)  
- $f_{\text{fract}}$: scheduled flow fraction (0–1)  
- $\rho$: standard air density (kg/m³)

---

#### 🔹 2. Pressure Rise

- Uses a constant user-defined $\Delta P$ (Pa), same at all loads

---

#### 🔹 3. Electric Power Input

$$
\dot W_{\text{electric}} = \frac{\dot m \cdot \Delta P}{\rho \cdot \eta_{\text{total}}}
$$

- $\dot W_{\text{electric}}$: Fan electric power (W)  
- $\Delta P$: Fan pressure rise (Pa)  
- $\eta_{\text{total}}$: Combined fan + motor efficiency (0–1)

---

#### 🔹 4. Heat Added to Airstream

All motor/fan heat is added to the air stream:

$$
\dot Q_{\text{to air}} = \dot W_{\text{electric}} - \dot W_{\text{shaft}}
$$

Where:

$$
\dot W_{\text{shaft}} = \frac{\dot m \cdot \Delta P}{\rho \cdot \eta_{\text{fan}}}
$$

- $\eta_{\text{fan}}$: fan-only efficiency (0–1)

---

#### 🔹 5. Outlet Enthalpy

$$
h_{\text{out}} = h_{\text{in}} + \frac{\dot Q_{\text{to air}}}{\dot m}
$$

- $h_{\text{in}}$, $h_{\text{out}}$: Specific enthalpy (J/kg)

---

#### 🔹 6. Availability Logic

Fan operation is dependent on:

- Local **availability schedule**
- (If zone-coupled) **system availability manager**
- **Minimum temperature** or **flow fraction schedule** logic

---

#### 🔹 7. System Coupling Effects

- Optionally tracks **balanced vs unbalanced** exhaust
- Interfaces with zone return and outdoor air systems to maintain airway balance

---

### ✅ Summary
Fan:ZoneExhaust is a **simplified exhaust fan model** that:
- Provides scheduled or fixed flow exhaust,
- Calculates electric power based on pressure rise and efficiency,
- Adds all generated heat to exhaust air,
- Contributes to zone and system airflow balancing.
