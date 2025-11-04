"""
plot_layout_all_in_one.py
--------------------------------
Proof-of-concept system that:
1) Computes free space on a rectangular land plot with a restricted border.
2) Selects which new rectangular objects can fit (by area check vs. free space).
3) Visualizes the plot, restricted border, existing objects (blue),
   and fitting new objects (green) using matplotlib.

NOTE:
- "Fitting" is checked PER OBJECT by area (not cumulative packing).
- Visualization is approximate (simple shelf layout for PoC).
"""

from typing import List, Dict, Tuple
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


# ----------------------------- Validation helpers -----------------------------

def _validate_positive_number(value, name: str):
    """Ensure a value is a positive number; raise informative errors otherwise."""
    if not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a number.")
    if value <= 0:
        raise ValueError(f"{name} must be a positive number.")


def _validate_object_dict(obj: Dict, required_keys: List[str], name: str):
    """
    Validate a single object dictionary has required keys and positive dimensions.
    For new objects, 'name' must be a non-empty string.
    """
    if not isinstance(obj, dict):
        raise TypeError(f"Each item in {name} must be a dict.")
    for k in required_keys:
        if k not in obj:
            raise ValueError(f"Missing key '{k}' in {name} item: {obj}")
    if "name" in required_keys:
        if not isinstance(obj["name"], str) or not obj["name"].strip():
            raise ValueError(f"'name' in {name} must be a non-empty string.")
    for dim_key in ["width", "length"]:
        _validate_positive_number(obj[dim_key], f"{name}['{dim_key}']")


def _validate_inputs(
    plot_width: float,
    plot_length: float,
    restricted_border: float,
    existing_objects: List[Dict],
    new_objects: List[Dict],
):
    """Validate top-level parameters and the object lists."""
    _validate_positive_number(plot_width, "plot_width")
    _validate_positive_number(plot_length, "plot_length")
    _validate_positive_number(restricted_border, "restricted_border")

    # The border must not eat up all the usable area
    if restricted_border * 2 >= plot_width or restricted_border * 2 >= plot_length:
        raise ValueError("restricted_border is too large: it leaves no usable area.")

    if not isinstance(existing_objects, list):
        raise TypeError("existing_objects must be a list of dicts.")
    if not isinstance(new_objects, list):
        raise TypeError("new_objects must be a list of dicts.")

    for item in existing_objects:
        _validate_object_dict(item, ["width", "length"], "existing_objects")
    for item in new_objects:
        _validate_object_dict(item, ["name", "width", "length"], "new_objects")


# ----------------------------- Area computations ------------------------------

def _areas(
    plot_width: float,
    plot_length: float,
    restricted_border: float,
    existing_objects: List[Dict],
) -> Tuple[float, float, float]:
    """
    Return (total_area, usable_area, free_space_rounded).
    - total_area = plot_width * plot_length
    - usable_area = (plot_width - 2*border) * (plot_length - 2*border)
    - free_space = max(0, usable_area - sum(existing areas)), rounded to 2 decimals
    """
    total_area = plot_width * plot_length
    usable_w = plot_width - 2 * restricted_border
    usable_l = plot_length - 2 * restricted_border
    usable_area = usable_w * usable_l

    existing_area = sum(obj["width"] * obj["length"] for obj in existing_objects)
    free_space = usable_area - existing_area
    free_space = max(0.0, free_space)
    free_space = round(free_space, 2)
    return total_area, usable_area, free_space


# ------------------------- Very simple layout for PoC --------------------------

def _simple_shelf_layout(
    items: List[Dict],
    start_x: float,
    start_y: float,
    max_width: float,
    max_length: float,
    gap: float = 0.5,
):
    """
    Minimal row-wise layout for visualization only.
    - No rotations, no collision checks with existing layout.
    - If an item cannot fit within the given area at all, it is skipped.
    Returns a list of (x, y, item_dict).
    """
    placed = []
    x = start_x + gap
    y = start_y + gap
    row_h = 0.0

    for it in items:
        w, h = it["width"], it["length"]

        # Skip if larger than the whole available area (for visualization)
        if w > max_width or h > max_length:
            continue

        # New row if we exceed width
        if x + w + gap > start_x + max_width:
            x = start_x + gap
            y += row_h + gap
            row_h = 0.0

        # Stop placing if we exceed available height
        if y + h + gap > start_y + max_length:
            continue

        placed.append((x, y, it))
        x += w + gap
        row_h = max(row_h, h)

    return placed


# -------------------------------- Visualization --------------------------------

def visualize_plot(
    plot_width: float,
    plot_length: float,
    restricted_border: float,
    existing_objects: List[Dict],
    fitting_objects: List[Dict],
    filename: str = "plot_visualization.png",
) -> str:
    """
    Draws:
    - Plot boundary (black outline)
    - Restricted border area (light red)
    - Usable area (white with red outline)
    - Existing objects (blue rectangles)
    - New fitting objects (green rectangles)
    Saves to `filename` and returns the path.
    """
    usable_w = plot_width - 2 * restricted_border
    usable_l = plot_length - 2 * restricted_border

    fig = plt.figure(figsize=(8, 12))  # one figure, no style/colors specified
    ax = plt.gca()
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(0, plot_width)
    ax.set_ylim(0, plot_length)
    ax.set_xlabel("Width (m)")
    ax.set_ylabel("Length (m)")
    ax.set_title("Plot Layout: Border, Usable Area, Existing & Fitting Objects")

    # Outer plot
    outer = Rectangle((0, 0), plot_width, plot_length, fill=False, linewidth=2)
    ax.add_patch(outer)

    # Restricted border as a translucent red overlay
    full_red = Rectangle((0, 0), plot_width, plot_length, linewidth=0, facecolor="red", alpha=0.15)
    ax.add_patch(full_red)

    # Usable area: white fill with red edge
    usable = Rectangle(
        (restricted_border, restricted_border),
        usable_w,
        usable_l,
        linewidth=2,
        edgecolor="red",
        facecolor="white",
        alpha=1.0,
    )
    ax.add_patch(usable)

    # Existing objects (blue), placed from bottom-left of usable area
    existing_pos = _simple_shelf_layout(
        existing_objects,
        start_x=restricted_border,
        start_y=restricted_border,
        max_width=usable_w,
        max_length=usable_l,
        gap=0.5,
    )
    for (x, y, it) in existing_pos:
        rect = Rectangle((x, y), it["width"], it["length"], linewidth=1.5, edgecolor="blue", facecolor="none")
        ax.add_patch(rect)
        ax.text(x + it["width"] / 2, y + it["length"] / 2, "Existing", ha="center", va="center", fontsize=8, color="blue")

    # Fitting new objects (green), placed in the top-right half of the usable area
    half_w, half_l = usable_w / 2, usable_l / 2
    fitting_pos = _simple_shelf_layout(
        fitting_objects,
        start_x=restricted_border + half_w,
        start_y=restricted_border + half_l,
        max_width=half_w,
        max_length=half_l,
        gap=0.5,
    )
    for (x, y, it) in fitting_pos:
        rect = Rectangle((x, y), it["width"], it["length"], linewidth=1.5, edgecolor="green", facecolor="none")
        ax.add_patch(rect)
        label = it.get("name", "New")
        ax.text(x + it["width"] / 2, y + it["length"] / 2, label, ha="center", va="center", fontsize=8, color="green")

    # Legend
    leg_plot = Rectangle((0, 0), 1, 1, fill=False, edgecolor="black", linewidth=2)
    leg_border = Rectangle((0, 0), 1, 1, fill=True, facecolor="red", alpha=0.15, edgecolor="red")
    leg_existing = Rectangle((0, 0), 1, 1, fill=False, edgecolor="blue", linewidth=1.5)
    leg_new = Rectangle((0, 0), 1, 1, fill=False, edgecolor="green", linewidth=1.5)
    ax.legend(
        [leg_plot, leg_border, usable, leg_existing, leg_new],
        ["Plot boundary", "Restricted border", "Usable area", "Existing objects", "Fitting new objects"],
        loc="upper right",
    )

    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return filename


# -------------------------------- Main function --------------------------------

def find_fitting_objects(
    plot_width: float,
    plot_length: float,
    restricted_border: float,
    existing_objects: List[Dict],
    new_objects: List[Dict],
) -> Dict:
    """
    Core API as required by the spec.

    Returns:
      {
        "free_space": float,          # in m^2, rounded to 2 decimals, never negative
        "fitting_objects": List[str]  # names of new objects with area <= free_space
      }

    IMPORTANT: The "fits" check is per-object vs. free_space (NOT cumulative packing).
    """
    _validate_inputs(plot_width, plot_length, restricted_border, existing_objects, new_objects)
    _, _, free_space = _areas(plot_width, plot_length, restricted_border, existing_objects)

    if free_space <= 0.0:
        return {"free_space": 0.0, "fitting_objects": []}

    fitting_names = []
    for obj in new_objects:
        area = obj["width"] * obj["length"]
        if area <= free_space:
            fitting_names.append(obj["name"])

    return {"free_space": free_space, "fitting_objects": fitting_names}


# --------------------------------- Demo / Example -------------------------------

if __name__ == "__main__":
    # Demo inputs (same idea as the task example)
    plot_width = 50
    plot_length = 100
    restricted_border = 4
    existing_objects = [{"width": 10, "length": 20}, {"width": 5, "length": 5}]
    new_objects = [
        {"name": "Shed", "width": 10, "length": 10},
        {"name": "Garage", "width": 20, "length": 30},
        {"name": "Cabin", "width": 15, "length": 15},
    ]

    # 1) Compute result (free space + which new objects fit by area)
    result = find_fitting_objects(
        plot_width=plot_width,
        plot_length=plot_length,
        restricted_border=restricted_border,
        existing_objects=existing_objects,
        new_objects=new_objects,
    )
    print(result)
    # According to the formal formula:
    # usable_area = (50 - 2*4) * (100 - 2*4) = 42 * 92 = 3864
    # existing_area = 10*20 + 5*5 = 225
    # free_space = 3864 - 225 = 3639.0

    # 2) Visualize only the new objects that fit (by name)
    names_set = set(result["fitting_objects"])
    fitting_objs = [o for o in new_objects if o["name"] in names_set]

    out_img = visualize_plot(
        plot_width=plot_width,
        plot_length=plot_length,
        restricted_border=restricted_border,
        existing_objects=existing_objects,
        fitting_objects=fitting_objs,
        filename="plot_visualization.png",
    )
    print("Saved plot to:", out_img)
