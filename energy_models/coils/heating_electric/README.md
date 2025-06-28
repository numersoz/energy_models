# 📘 Coil:Heating:Electric — Mathematical Model

Reference: https://bigladdersoftware.com/epx/docs/8-0/input-output-reference/page-042.html#coilheatingelectric

## 📌 Summary

| Property                | Value                                 |
|------------------------|----------------------------------------|
| **Coil Type**          | Electric Resistance Heating Coil      |
| **Energy Source**      | On‑electricity                        |
| **Heating Capacity**   | User-specified nominal capacity (W)   |
| **Efficiency**         | User-defined (typically 1.0)          |
| **Control Logic**      | Temperature or capacity controlled    |
| **Scheduling**         | Availability schedule                 |
| **Best For**           | Reheat coils, space heating, cabins   |
| **Notes**              | Simple model, no latent or UA curves  |

---

#### 1. Electric Heating Rate:

Electric heating provided when coil is enabled and load exists:

$$
\dot{Q}_{\text{total}} = \dot{Q}_{\text{nominal}} \cdot f_{\text{load}}
$$

- $\dot{Q}_{\text{total}}$: delivered heat [W]  
- $\dot{Q}_{\text{nominal}}$: user-specified nominal capacity [W]  
- $f_{\text{load}}$: load fraction (0–1)

---

#### 2. Electric Power Consumption:

Assumes efficiency $\eta$ (default = 1.0):

$$
\dot{W}_{\text{electric}} = \frac{\dot{Q}_{\text{total}}}{\eta}
$$

- $\dot{W}_{\text{electric}}$: coil’s electric power draw [W]  
- $\eta$: coil efficiency (0–1)

Total energy consumption over time:

$$
E = \int \dot{W}_{\text{electric}} \, dt
$$

---

#### 3. Outlet Air Enthalpy:

Air enthalpy increases by:

$$
h_{\text{out}} = h_{\text{in}} + \frac{\dot{Q}_{\text{total}}}{\dot{m}_{\text{air}}}
$$

- $h_{\text{in}}, h_{\text{out}}$: inlet/outlet enthalpies [J/kg]  
- $\dot{m}_{\text{air}}$: air mass flow rate [kg/s]

---

#### 4. Control Strategies:

- **Temperature-controlled**: heats air to meet a setpoint temperature  
- **Load-controlled**: proportional heating to match zone demand  
- Coil only operates if **availability schedule** is ON

---

#### 5. Multi‑Stage Option (if enabled):

- Staged control logic (e.g., two-stage electric heating)
- Each stage has:
  - $\dot{Q}_{\text{stageN}}$
  - $\eta_{\text{stageN}}$
- Stages fire based on load thresholds

---

#### ✅ Typical Outputs:

- `Heating Coil Air Heating Rate [W]`  
- `Heating Coil Electric Power [W]`  
- `Heating Coil Electric Energy [J]`

---
