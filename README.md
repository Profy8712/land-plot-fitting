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
```

---

## 🧠 Logic Explanation

1. **Total area:**  
   `total_area = plot_width * plot_length`  

2. **Usable area:**  
   Subtracts the restricted border from both sides:  
   `usable_area = (plot_width - 2 * restricted_border) * (plot_length - 2 * restricted_border)`  

3. **Free space:**  
   Removes the area occupied by existing objects:  
   `free_space = usable_area - sum(width * length for each existing object)`  

4. **Fitting objects:**  
   Chooses new objects whose individual area does not exceed the free space.

---

## 🧮 Example Usage

```python
result = find_fitting_objects(
    plot_width=50,
    plot_length=100,
    restricted_border=4,
    existing_objects=[
        {"width": 10, "length": 20},
        {"width": 5, "length": 5}
    ],
    new_objects=[
        {"name": "Shed", "width": 10, "length": 10},
        {"name": "Garage", "width": 20, "length": 30},
        {"name": "Cabin", "width": 15, "length": 15}
    ]
)

print(result)
# {'free_space': 3639.0, 'fitting_objects': ['Shed', 'Garage', 'Cabin']}
```

---

## 🎨 Visualization

The visualization displays:
- Plot boundary (black)
- Restricted border area (light red)
- Usable inner area (white with red frame)
- Existing objects (blue)
- Fitting new objects (green)

The figure is saved as:
```
plot_visualization.png
```

---

## 🧠 Input Validation
The function checks:
- All numeric inputs are positive  
- Border does not consume entire plot area  
- Lists contain proper dictionaries with required keys  
- Invalid inputs raise clear exceptions (`TypeError`, `ValueError`)

---

## 🖥 Installation & Run

### 1️⃣ Clone the repository
```bash
git clone https://github.com/Profy8712/land-plot-fitting.git
cd land-plot-fitting
```

### 2️⃣ (Optional) Create and activate virtual environment
```bash
python -m venv venv
source venv/Scripts/activate  # Windows
# or
source venv/bin/activate      # macOS/Linux
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Run the program
```bash
python plot_layout_all_in_one.py
```

You will see output like:
```
{'free_space': 3639.0, 'fitting_objects': ['Shed', 'Garage', 'Cabin']}
Saved plot to: plot_visualization.png
```

---

## 🧱 Project Structure
```
land_plot_fitting/
│
├── plot_layout_all_in_one.py   # main script with validation and visualization
├── requirements.txt            # dependencies (matplotlib)
├── README.md                   # project documentation
├── .gitignore                  # ignored files and folders
└── plot_visualization.png      # generated output image
```

---

## 📹 Video Walkthrough
When recording your demo:
1. Explain the project goal  
2. Show the code structure and logic  
3. Run the example and explain results  
4. Open the generated visualization  
5. Show one or two validation errors  
6. Conclude with possible future improvements

Tools you can use:
- [Canva Desktop](https://www.canva.com/)
- [Loom](https://www.loom.com/)

---

## 🚀 Future Improvements
- Add cumulative selection (total area of new objects ≤ free space)  
- Allow rotation of objects (width ↔ length)  
- Implement non-overlapping placement (packing algorithm)  
- Export result as SVG/PDF  
- Add simple GUI or web interface  

---

**Author:** [@Profy8712](https://github.com/Profy8712)  
📅 *Created for the Land Plot Fitting proof-of-concept task*
