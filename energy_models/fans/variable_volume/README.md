# 📘 Fan: Variable Volume — Mathematical Model

Reference: https://bigladdersoftware.com/epx/docs/9-2/input-output-reference/group-fans.html#fanvariablevolume

## 📌 Summary

| Property               | Value                                  |
|------------------------|----------------------------------------|
| **Fan Type**           | VariableVolume                         |
| **Control Type**       | Modulating (0–1)                       |
| **Flow Behavior**      | Varies with load                       |
| **Pressure Rise**      | Fixed                                  |
| **Power Model**        | Curve-based (e.g., polynomial)         |
| **Heat to Air**        | Modeled via motor efficiency           |
| **Scheduling**         | Availability + flow fraction schedule  |
| **Best For**           | VAV systems, demand-controlled AHUs    |
| **Notes**              | Supports variable-speed fans (VFD)     |


---

#### 1. Shaft Power:

$$
\dot{W}_{\text{shaft}} = \frac{\dot{m} \cdot \Delta P}{\rho \cdot \eta_{\text{fan}}}
$$

- $\dot{W}_{\text{shaft}}$: Shaft power (W)  
- $\dot{m}$: Mass flow rate (kg/s)  
- $\Delta P$: Fan pressure rise (Pa)  
- $\rho$: Air density (kg/m³)  
- $\eta_{\text{fan}}$: Fan total efficiency (0–1)

---

#### 2. Flow Fraction (Part-Load Ratio):

$$
f = \frac{\dot{m}}{\dot{m}_{\text{design}}}
$$

- $f$ (or PLR): Flow fraction (–)  
- $\dot{m}_{\text{design}}$: Design mass flow rate (kg/s)

---

#### 3. Part-Load Power Fraction:

EnergyPlus uses a 4th-order polynomial:

$$
P_{\text{frac}}(f) = C_1 + C_2 f + C_3 f^2 + C_4 f^3 + C_5 f^4
$$

- $P_{\text{frac}}$: Part-load power fraction (–)  
- $C_1$–$C_5$: User-input coefficients defining the curve :contentReference[oaicite:1]{index=1}

---

#### 4. Electric Power at Part Load:

$$
\dot{W}_{\text{electric}} = P_{\text{frac}}(f)\cdot \dot{W}_{\text{electric,design}}
$$

- $\dot{W}_{\text{electric,design}}$: Electric power at design flow (W)

---

#### 5. Heat Added to Air:

$$
\dot{Q}_{\text{to air}} = f_{\text{motor to air}} \cdot (\dot{W}_{\text{electric}} - \dot{W}_{\text{shaft}})
$$

- $\dot{Q}_{\text{to air}}$: Heat to airstream (W)  
- $f_{\text{motor to air}}$: Fraction of motor heat entering air (–)

---

#### 6. Outlet Air Enthalpy:

$$
h_{\text{out}} = h_{\text{in}} + \frac{\dot{Q}_{\text{to air}}}{\dot{m}}
$$

- $h_{\text{in}}$, $h_{\text{out}}$: Inlet/outlet specific enthalpy (J/kg)

---
