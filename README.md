# 🏡 Land Plot Fitting System

## 📘 Project Description
This project is a **semi-automated system** that calculates and visualizes how new rectangular objects can fit on a rectangular land plot.  
It considers:
- the overall plot dimensions,  
- a restricted border around the edges, and  
- existing objects already placed on the plot.  

It then determines the **available free space** and identifies which **new objects** can fit within it.  
Finally, it creates a **visualization** using `matplotlib` that shows:
- the plot boundary,  
- the restricted border,  
- existing objects (blue),  
- and new fitting objects (green).  

---

## ⚙️ Features
✅ Calculates total, usable, and free area on a rectangular plot  
✅ Validates all input data with clear error messages  
✅ Selects which new objects can fit based on available space  
✅ Visualizes the full layout with `matplotlib`  
✅ Saves output as an image `plot_visualization.png`  

---

## 🧩 Function Overview

```python
def find_fitting_objects(
    plot_width: float,
    plot_length: float,
    restricted_border: float,
    existing_objects: list[dict],
    new_objects: list[dict]
) -> dict:
    """
    Returns:
        {
            "free_space": float,
            "fitting_objects": list[str]
        }
    """
