# 📘 Coil:Heating:Steam — Mathematical Model

Reference: https://bigladdersoftware.com/epx/docs/8-7/input-output-reference/group-heating-and-cooling-coils.html#coilheatingsteam

## 📌 Summary

| Property                    | Value                                                |
|----------------------------|------------------------------------------------------|
| **Coil Type**              | Steam-to-Air Heating Coil                            |
| **Energy Source**          | Process steam (condenses in coil)                   |
| **Max Steam Flow**         | User-specified (autosizable)                        |
| **Subcooling**             | User-defined (°C) for steam & condensate loop       |
| **Control Type**           | ZoneLoadControl or TemperatureSetpointControl        |
| **Heating Output**         | Sensible only (no humidity change modeled)          |
| **Scheduling**             | Availability schedule required                      |
| **Best For**               | Reheat coils, AHUs, FCUs requiring steam heat       |

---

#### 1. Steam Flow & Heat Release:

Steam condenses and gives sensible heat to air:

$$
Q_{\text{total}} = \dot{m}_{\text{steam}} \cdot h_{fg} + \dot{m}_{\text{steam}} \cdot c_{p,\text{cond}} \cdot \Delta T_{\text{subcool}}
$$

- $\dot{m}_{\text{steam}}$: Steam mass flow rate (kg/s)  
- $h_{fg}$: Latent heat of vaporization at system pressure (J/kg)  
- $c_{p,\text{cond}}$: Specific heat of condensate (J/kg·K)  
- $\Delta T_{\text{subcool}}$: Total subcooling (°C), includes steam and loop losses

---

#### 2. Condensate Subcooling:

- Steam outlet is subcooled by $\Delta T_{\text{subcool,steam}}$  
- Condensate loop subcools further by $\Delta T_{\text{subcool,loop}}$  
- Both contribute to total sensible heat

---

#### 3. Control Logic:

- **TemperatureSetpointControl**: Matches outlet air temperature to node setpoint  
- **ZoneLoadControl**: Meets zone sensible load  
- Coil only operates if **availability schedule** is active

---

#### 4. Output Variables:

- `Heating Coil Heating Energy [J]`  
- `Total Steam Coil Heating Rate [W]`  
- `Steam Trap Loss Rate [W]`  
- `Steam Mass Flow Rate [kg/s]`  
- `Steam Inlet and Outlet Temperature [°C]`

---

#### 5. Applications:

- Steam reheating coils in AHUs or VAV terminals  
- Cruise ship or cargo vessel FCUs with steam supply  
- Industrial buildings with existing steam systems  
