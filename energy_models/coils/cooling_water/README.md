# 📘 Coil: Cooling:Water — Mathematical Model

Reference: https://bigladdersoftware.com/epx/docs/23-2/input-output-reference/group-heating-and-cooling-coils.html#coilcoolingwater

## 📌 Summary

| Property                   | Value                                         |
|----------------------------|-----------------------------------------------|
| **Coil Type**              | Chilled-Water Cooling Coil                   |
| **Energy Source**          | Chilled Water (hydronic system)              |
| **Cooling Capacity**       | Curve-modified rated total capacity           |
| **Sensible Heat Ratio**    | Specified or calculated                      |
| **Water Side Control**     | Flow varies with load (valve modulation)     |
| **Air Side Flow**          | Fixed or variable (system dependent)         |
| **Power Consumption**      | Indirect (pumping), not part of this coil    |
| **Scheduling**             | Availability schedule                         |
| **Best For**               | Central chilled water systems (AHUs, FCUs)   |
| **Notes**                  | Uses modifier curves for off-design behavior |

---

#### 1. Total Cooling Capacity:

$$
\dot{Q}_{\text{total}} = \dot{Q}_{\text{rated}} \cdot f_{\text{cap,temp}}(T_{\text{air,in}}, T_{\text{water,in}}) \cdot f_{\text{cap,flow}}(\dot{V}_{\text{air}}, \dot{V}_{\text{water}})
$$

- $\dot{Q}_{\text{total}}$: Actual total cooling rate (W)  
- $\dot{Q}_{\text{rated}}$: Rated total cooling capacity (W)  
- $f_{\text{cap,temp}}$: Temperature modifier curve  
- $f_{\text{cap,flow}}$: Flow modifier curve  
- $T_{\text{air,in}}$: Inlet air temperature (°C)  
- $T_{\text{water,in}}$: Inlet water temperature (°C)  
- $\dot{V}_{\text{air}}, \dot{V}_{\text{water}}$: Actual air/water volumetric flow rates (m³/s)

---

#### 2. Sensible Cooling:

$$
\dot{Q}_{\text{sensible}} = \text{SHR} \cdot \dot{Q}_{\text{total}}
$$

- $\dot{Q}_{\text{sensible}}$: Sensible cooling (W)  
- $\text{SHR}$: Sensible Heat Ratio (0–1)

---

#### 3. Latent Cooling:

$$
\dot{Q}_{\text{latent}} = \dot{Q}_{\text{total}} - \dot{Q}_{\text{sensible}}
$$

- $\dot{Q}_{\text{latent}}$: Latent cooling (W)

---

#### 4. Coil Outlet Air Conditions:

EnergyPlus calculates outlet air state from energy balance and moisture balance:

- **Dry-bulb temp**: Reduced from sensible load  
- **Humidity ratio**: Adjusted by latent removal  
- **Enthalpy**:

$$
h_{\text{out}} = h_{\text{in}} - \frac{\dot{Q}_{\text{total}}}{\dot{m}_{\text{air}}}
$$

- $h_{\text{in}}$, $h_{\text{out}}$: Inlet and outlet enthalpy (J/kg)  
- $\dot{m}_{\text{air}}$: Air mass flow rate (kg/s)

---

#### 5. Curve Types Used:

- `CapFT`: Bi-quadratic function of air & water inlet temps  
- `CapFFlow`: Quadratic or cubic function of air/water flow  
- `EIRFT`: (If used for coil power, not common)  
- `EIRFFlow`: (Optional, for power estimates)

---

#### 6. Control Logic:

- Water flow modulated by control valve to meet cooling load  
- On/off controlled by **availability schedule**  
- Coil bypassed if load is zero or unavailable

---

#### 7. Airside Pressure Drop

The coil introduces a pressure drop to the air stream, which varies with air velocity or volumetric flow rate. This pressure loss must be overcome by the fan and is important for accurate fan power modeling.

A simplified quadratic model is typically used:

$$
\Delta P_{\text{coil}}(Q) = K \cdot Q^2
$$

- $Q$: Air volumetric flow rate (m³/s)  
- $K$: Empirical resistance coefficient (Pa·s²/m⁶), specific to coil geometry, wet/dry state, and number of rows  
- $\Delta P_{\text{coil}}$: Air pressure drop across the coil (Pa)

Alternatively, this can be implemented via a callable function, fitted to manufacturer airside pressure drop curves.

---

#### 8. Waterside Pressure Drop

Manufacturers typically provide water-side pressure drop as a function of water volumetric flow rate in charts or tables.

- Flow rate is given in **L/s** or **m³/h**
- Pressure drop is provided in **kPa** or **Pa**

A typical approach to modeling this relationship is:

$$
\Delta P_{\text{water}} = K_w \cdot \dot{V}_{\text{water}}^n
$$

Where:

- $\Delta P_{\text{water}}$: Pressure drop across the coil water side (Pa or kPa)  
- $\dot{V}_{\text{water}}$: Water volumetric flow rate (m³/s)  
- $K_w$: Empirical water-side resistance coefficient  
- $n$: Exponent typically between 1.8 and 2.0 for turbulent flow

Alternatively, a Kv-type formulation may be used:

$$
\dot{V}_{\text{water}} = K_v \cdot \sqrt{\Delta P}
$$

These relationships can be implemented as callable functions or curve fits based on manufacturer data and are essential for pump head estimation and system control logic.

---
