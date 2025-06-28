# 📘 Coil:Heating:Water — Mathematical Model

Reference: https://bigladdersoftware.com/epx/docs/23-2/input-output-reference/group-heating-and-cooling-coils.html#coilheatingwater

## 📌 Summary

| Property                   | Value                                         |
|----------------------------|-----------------------------------------------|
| **Coil Type**              | Hot Water Heating Coil                        |
| **Energy Source**          | Hot Water (hydronic)                          |
| **Heating Capacity**       | Curve-modified rated capacity                 |
| **Water Side Control**     | Modulating (3-way or 2-way valve)             |
| **Air Side Flow**          | Constant or variable (depends on system)      |
| **Power Consumption**      | Indirect (via water pumps)                    |
| **Scheduling**             | Availability schedule                         |
| **Best For**               | AHUs, FCUs, cabin reheat coils                |
| **Notes**                  | Similar to chilled water coil model           |

---

#### 1. Total Heating Output:

$$
\dot{Q}_{\text{total}} = \dot{Q}_{\text{rated}} \cdot f_{\text{cap,temp}}(T_{\text{air,in}}, T_{\text{water,in}}) \cdot f_{\text{cap,flow}}(\dot{V}_{\text{air}}, \dot{V}_{\text{water}})
$$

- $\dot{Q}_{\text{total}}$: Heating rate (W)  
- $\dot{Q}_{\text{rated}}$: Rated heating capacity (W)  
- $f_{\text{cap,temp}}$: Temperature modifier (bivariate)  
- $f_{\text{cap,flow}}$: Flow modifier (bivariate)  
- $T_{\text{air,in}}$: Inlet air temperature (°C)  
- $T_{\text{water,in}}$: Inlet water temperature (°C)  
- $\dot{V}_{\text{air}}$, $\dot{V}_{\text{water}}$: Volumetric air/water flow rates (m³/s)

---

#### 2. Coil Outlet Enthalpy:

$$
h_{\text{out}} = h_{\text{in}} + \frac{\dot{Q}_{\text{total}}}{\dot{m}_{\text{air}}}
$$

- $h_{\text{in}}$, $h_{\text{out}}$: Inlet/outlet air enthalpy (J/kg)  
- $\dot{m}_{\text{air}}$: Air mass flow rate (kg/s)

---

#### 3. Control Logic:

- Coil output modulated by water valve  
- Fully bypassed if availability = False or load = 0  
- Heating output reduces unmet heating load in air loop

---
