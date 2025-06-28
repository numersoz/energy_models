# 📘 Fan: ConstantVolume — Mathematical Model

Reference: https://bigladdersoftware.com/epx/docs/9-2/input-output-reference/group-fans.html#fanconstantvolume

## 📌 Summary

| Property               | Value                                  |
|------------------------|----------------------------------------|
| **Fan Type**           | ConstantVolume                         |
| **Control Type**       | Constant                               |
| **Flow Behavior**      | Fixed at design value                  |
| **Pressure Rise**      | User-specified                         |
| **Power Model**        | Simple (constant)                      |
| **Heat to Air**        | Modeled via motor and fan efficiency   |
| **Scheduling**         | Availability schedule only             |
| **Best For**           | Constant-volume AHUs, packaged units   |
| **Notes**              | Power does not vary with flow          |


---

#### 1. Fan Pressure Rise:

$$
\Delta P = P_{\text{outlet}} - P_{\text{inlet}}
$$

- $\Delta P$: Pressure rise across the fan (Pa)  
- $P_{\text{outlet}}$: Pressure at fan outlet (Pa)  
- $P_{\text{inlet}}$: Pressure at fan inlet (Pa)

---

#### 2. Shaft Power:

$$
\dot{W}_{\text{shaft}} = \frac{\dot{m} \cdot \Delta P}{\rho \cdot \eta_{\text{fan}}}
$$

- $\dot{W}_{\text{shaft}}$: Power delivered to the fan shaft (W)  
- $\dot{m}$: Mass flow rate of air (kg/s)  
- $\rho$: Air density (kg/m³)  
- $\eta_{\text{fan}}$: Fan total efficiency (unitless, 0–1)  
- $\Delta P$: Fan pressure rise (Pa)

---

#### 3. Electric Power Input:

$$
\dot{W}_{\text{electric}} = \frac{\dot{W}_{\text{shaft}}}{\eta_{\text{motor}}}
$$

- $\dot{W}_{\text{electric}}$: Electrical power input to the motor (W)  
- $\eta_{\text{motor}}$: Motor efficiency (unitless, 0–1)

---

#### 4. Heat Added to Air Stream:

$$
\dot{Q}_{\text{to air}} = f_{\text{motor to air}} \cdot (\dot{W}_{\text{electric}} - \dot{W}_{\text{shaft}})
$$

- $\dot{Q}_{\text{to air}}$: Heat added to the air stream by the motor (W)  
- $f_{\text{motor to air}}$: Fraction of motor losses transferred to air (unitless, 0–1)

---

#### 5. Outlet Air Enthalpy:

$$
h_{\text{out}} = h_{\text{in}} + \frac{\dot{Q}_{\text{to air}}}{\dot{m}}
$$

- $h_{\text{out}}$: Outlet air specific enthalpy (J/kg)  
- $h_{\text{in}}$: Inlet air specific enthalpy (J/kg)  
- $\dot{Q}_{\text{to air}}$: Heat added to air stream (W)  
- $\dot{m}$: Mass flow rate of air (kg/s)
