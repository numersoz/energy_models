# 🕒 Scheduler Class — Markdown Documentation

This class mimics EnergyPlus's schedule system and allows Python-based control of system behavior like fans, coils, or lighting over time. It supports:

- Weekday, weekend, and holiday behaviors
- Hourly or sub-hourly resolution
- Optional linear interpolation
- Plug-and-play usage with simulation classes (e.g., `ZoneExhaustFan`)

---

## 🧠 Concept

A `Scheduler` is a generalized controller that returns a value (e.g., flow fraction) based on:

- **Hour of the day**
- **Day type** (weekday, weekend, holiday)
- **Custom override days**

It is used to replicate EnergyPlus objects like `Schedule:Compact`, `Schedule:Day:Hourly`, and `Schedule:File`.

---

## 📦 Features

| Feature                  | Supported |
|--------------------------|-----------|
| Hourly resolution        | ✅        |
| Weekend override         | ✅        |
| Holiday override         | ✅        |
| Value interpolation      | ✅        |
| Plug-in function creation| ✅        |

---

## 🧰 Constructor

```python
Scheduler(
    default: List[float],                # 24 hourly values (0–23)
    weekend: Optional[List[float]] = None,
    holiday: Optional[List[float]] = None,
    interpolate: bool = False,
    holiday_dates: Optional[List[date]] = None
)
