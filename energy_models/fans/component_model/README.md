# 📘 Fan: ComponentModel — Detailed Physics-Based Fan

Reference: https://bigladdersoftware.com/epx/docs/9-6/input-output-reference/group-fans.html#fancomponentmodel

## 📌 Summary

| Property               | Value                                               |
|------------------------|-----------------------------------------------------|
| **Fan Type**           | ComponentModel                                      |
| **Control Type**       | Fully flexible (modulating + cycling)              |
| **Flow Behavior**      | Variable based on pressure and control input       |
| **Pressure Rise**      | Curve-based via duct static and flow               |
| **Power Model**        | Physics-based (fan, motor, belt, VFD)              |
| **Heat to Air**        | Explicitly modeled                                 |
| **Scheduling**         | Via schedules and optional control functions       |
| **Best For**           | High-fidelity modeling, calibration, digital twins |
| **Notes**              | Complex setup but most realistic fan model         |


---

#### 1. Total Pressure Rise

Fan total pressure rise is modeled as a quadratic function of flow and static pressure:

$$
\Delta P_{\text{fan,tot}} = C_1 + C_2 Q + C_3 Q^2 + C_4 (P_{\text{sm}} - P_o) + C_5 (P_{\text{sm}} - P_o)^2 + C_6 Q \cdot (P_{\text{sm}} - P_o)
$$

- $\Delta P_{\text{fan,tot}}$: Total fan pressure rise (Pa)  
- $Q$: Fan volumetric flow rate (m³/s)  
- $P_{\text{sm}}$: Static pressure set point (Pa)  
- $P_o$: Ambient/zone static pressure (Pa)  
- $C_1$–$C_6$: Pressure rise curve coefficients

---

#### 2. Static Pressure Rise

Subtracting outlet velocity pressure yields the static rise:

$$
\Delta P_{\text{fan,static}} = \Delta P_{\text{fan,tot}} - \tfrac12 \rho V^2
$$

- $V = \frac{Q}{A_{\text{out}}}$: Outlet velocity (m/s)  
- $\rho$: Air density (kg/m³)

---

#### 3. Shaft Power

$$
\dot{W}_{\text{shaft}} = \frac{Q \cdot \Delta P_{\text{fan,tot}}}{\eta_{\text{fan}}}
$$

- $\eta_{\text{fan}}$: Fan total efficiency (0–1)

---

#### 4. Belt and Motor Efficiency

- Belt loss included via belt efficiency curves.
- Motor power is:

$$
\dot{W}_{\text{motor\_in}} = \frac{\dot{W}_{\text{shaft}}}{\eta_{\text{motor}}}
$$

---

#### 5. VFD Losses (if present)

- Includes variable-frequency drive (VFD) efficiency in series.

---

#### 6. Heat Added to Air

$$
\dot{Q}_{\text{to air}} = f_{\text{motor to air}} \cdot (\dot{W}_{\text{motor\_in}} - \dot{W}_{\text{shaft}} - \dot{W}_{\text{belt}})
$$

- $f_{\text{motor to air}}$: Fraction of motor heat entering airflow (0–1)

---

#### 7. Outlet Air Enthalpy

$$
h_{\text{out}} = h_{\text{in}} + \frac{\dot{Q}_{\text{to air}}}{\dot{m}}
$$

- $h_{\text{in/out}}$: Inlet and outlet enthalpy (J/kg)  
- $\dot{m} = \rho Q$: Mass flow (kg/s)

---

#### 8. Duct Static Pressure Reset Control (optional)

Static pressure setpoint varies with flow:

$$
P_{\text{sm}} = C_a + C_b Q
$$

- $C_a, C_b$: Linear curve coefficients
