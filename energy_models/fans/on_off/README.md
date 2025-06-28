# 📘 Fan: On/Off — Mathematical Model

Reference: https://bigladdersoftware.com/epx/docs/8-2/input-output-reference/group-fans.html#fanonoff

## 📌 Summary

| Property               | Value                                  |
|------------------------|----------------------------------------|
| **Fan Type**           | OnOff                                  |
| **Control Type**       | Binary (On/Off)                        |
| **Flow Behavior**      | 0 or design value                      |
| **Pressure Rise**      | User-specified                         |
| **Power Model**        | Simple                                 |
| **Heat to Air**        | Included                               |
| **Scheduling**         | Controlled via thermostat or logic     |
| **Best For**           | Small unitary systems, PTACs, RTUs     |
| **Notes**              | Often tied to zone demand              |


---

#### 🔹 1. Operating Concept

- The fan cycles **fully ON or fully OFF** based on the load.
- When ON, it runs at **design flow** and **design pressure rise**.
- Average power and airflow over a timestep are adjusted via **runtime fraction** \(R\).

---

#### 🔹 2. Shaft Power at Design Flow

$$
\dot{W}_{\text{shaft,design}} = \frac{\dot{m}_{\text{design}} \cdot \Delta P}{\rho \cdot \eta_{\text{fan}}}
$$

- $\dot{W}_{\text{shaft,design}}$: Shaft power (W)  
- $\dot{m}_{\text{design}}$: Design mass flow rate (kg/s)  
- $\Delta P$: Fan pressure rise (Pa)  
- $\rho$: Air density (kg/m³)  
- $\eta_{\text{fan}}$: Fan total efficiency (unitless, 0–1)

---

#### 🔹 3. Electric Power at Design Flow

$$
\dot{W}_{\text{electric,design}} = \frac{\dot{W}_{\text{shaft,design}}}{\eta_{\text{motor}}}
$$

- $\dot{W}_{\text{electric,design}}$: Electric input power (W)  
- $\eta_{\text{motor}}$: Motor efficiency (unitless, 0–1)

---

#### 🔹 4. Runtime Fraction (for part-load behavior)

If the required flow is less than design, the fan **cycles** to meet the load:

$$
R = \frac{\dot{m}_{\text{requested}}}{\dot{m}_{\text{design}}}
$$

- $R$: Fan runtime fraction (0–1)  
- $\dot{m}_{\text{requested}}$: Requested/actual mass flow (kg/s)

---

#### 🔹 5. Average Electric Power During Timestep

$$
\dot{W}_{\text{electric,avg}} = R \cdot \dot{W}_{\text{electric,design}}
$$

- $\dot{W}_{\text{electric,avg}}$: Average electric power over timestep (W)

---

#### 🔹 6. Heat Added to Airstream

$$
\dot{Q}_{\text{to air}} = f_{\text{motor to air}} \cdot (\dot{W}_{\text{electric}} - \dot{W}_{\text{shaft}})
$$

- $\dot{Q}_{\text{to air}}$: Waste heat transferred to air stream (W)  
- $f_{\text{motor to air}}$: Fraction of motor heat entering air (unitless, 0–1)  
- $\dot{W}_{\text{electric}}$: Electric power input (W)  
- $\dot{W}_{\text{shaft}}$: Shaft power output (W)

---

#### 🔹 7. Outlet Enthalpy

$$
h_{\text{out}} = h_{\text{in}} + \frac{\dot{Q}_{\text{to air}}}{\dot{m}}
$$

- $h_{\text{out}}$: Outlet air specific enthalpy (J/kg)  
- $h_{\text{in}}$: Inlet air specific enthalpy (J/kg)  
- $\dot{m}$: Air mass flow rate (kg/s)

---

### 📝 Notes

- For **multi-speed fans**, the parent system determines the runtime and speed selection.
- Power scaling may use an optional **power ratio curve** at each speed.
- All calculations apply **only during "ON" periods**, and are averaged using runtime fraction \(R\).

