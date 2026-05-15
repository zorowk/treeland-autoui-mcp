#coding: utf-8

from __future__ import annotations

from copy import deepcopy
from typing import Any


Rect = dict[str, float]


def normalize_box(bbox: list[float], screen_width: float, screen_height: float) -> Rect:
    """Convert OmniParser [x1, y1, x2, y2] ratios to pixel coordinates."""
    xmin, ymin, xmax, ymax = bbox
    return {
        "x1": float(xmin) * screen_width,
        "y1": float(ymin) * screen_height,
        "x2": float(xmax) * screen_width,
        "y2": float(ymax) * screen_height,
    }


def is_element_in_window(elem_box: Rect, win_geometry: dict[str, Any]) -> bool:
    cx = (elem_box["x1"] + elem_box["x2"]) / 2
    cy = (elem_box["y1"] + elem_box["y2"]) / 2
    wx1 = _number(win_geometry.get("x"))
    wy1 = _number(win_geometry.get("y"))
    wx2 = wx1 + _number(win_geometry.get("width"))
    wy2 = wy1 + _number(win_geometry.get("height"))
    return wx1 <= cx <= wx2 and wy1 <= cy <= wy2


def fuse_omniparser_with_treeland(
    omniparser_elements: list[dict[str, Any]],
    treeland_tree: dict[str, Any],
) -> dict[str, Any]:
    fused_tree = deepcopy(treeland_tree)
    screen_width, screen_height = screen_size_from_treeland(fused_tree)
    windows = flatten_treeland_windows(fused_tree, initialize_elements=True)
    desktop_unparented_elements = []
    assigned_count = 0

    for index, element in enumerate(omniparser_elements):
        bbox = element.get("bbox")
        if not _valid_bbox(bbox):
            desktop_unparented_elements.append(_build_element_record(index, element, None, None))
            continue

        absolute_box = normalize_box(bbox, screen_width, screen_height)
        captured = False
        for window in windows:
            geometry = window.get("geometry") or {}
            if not is_element_in_window(absolute_box, geometry):
                continue

            window["elements"].append(
                _build_element_record(index, element, absolute_box, _relative_box(absolute_box, geometry))
            )
            assigned_count += 1
            captured = True
            break

        if not captured:
            desktop_unparented_elements.append(_build_element_record(index, element, absolute_box, None))

    fused_tree["desktop_unparented_elements"] = desktop_unparented_elements
    fused_tree["fusion_stats"] = {
        "screen_width": screen_width,
        "screen_height": screen_height,
        "total_elements": len(omniparser_elements),
        "assigned_elements": assigned_count,
        "unassigned_elements": len(desktop_unparented_elements),
        "window_count": len(windows),
    }
    return fused_tree


def screen_size_from_treeland(tree: dict[str, Any]) -> tuple[float, float]:
    background_rects = []
    for layer in tree.get("layers", []):
        if layer.get("name") != "background":
            continue
        for window in layer.get("windows", []):
            for key in ("boundingRect", "geometry"):
                rect = window.get(key) or {}
                if _has_area(rect):
                    background_rects.append(rect)
                    break
    if background_rects:
        min_x = min(_number(rect.get("x")) for rect in background_rects)
        min_y = min(_number(rect.get("y")) for rect in background_rects)
        max_x = max(_number(rect.get("x")) + _number(rect.get("width")) for rect in background_rects)
        max_y = max(_number(rect.get("y")) + _number(rect.get("height")) for rect in background_rects)
        return max_x - min_x, max_y - min_y
    raise ValueError("Unable to determine screen size from Treeland background layer")


def flatten_treeland_windows(
    tree: dict[str, Any],
    initialize_elements: bool = False,
) -> list[dict[str, Any]]:
    window_entries: list[tuple[float, float, dict[str, Any]]] = []
    for layer in tree.get("layers", []):
        layer_name = layer.get("name", "")
        for window in layer.get("windows", []):
            _append_window(window_entries, window, layer_name, layer.get("layer"), initialize_elements)

        for workspace in layer.get("workspaces", []):
            if workspace.get("isActive") is not True:
                continue
            for window in workspace.get("windows", []):
                _append_window(window_entries, window, layer_name, layer.get("layer"), initialize_elements)

    window_entries.sort(key=lambda entry: (entry[0], entry[1]), reverse=True)
    return [window for _, _, window in window_entries]


def _append_window(
    window_entries: list[tuple[float, float, dict[str, Any]]],
    window: dict[str, Any],
    layer_name: str,
    layer_value: Any,
    initialize_elements: bool,
) -> None:
    geometry = window.get("geometry") or {}
    if not _has_area(geometry):
        return
    if layer_name == "workspace" and window.get("visible") is not True:
        return

    window.setdefault("layer", layer_value)
    if initialize_elements:
        window["elements"] = []
    else:
        window.setdefault("elements", [])
    window_entries.append((_number(window.get("layer", layer_value)), _number(window.get("z")), window))


def _build_element_record(
    index: int,
    element: dict[str, Any],
    absolute_box: Rect | None,
    relative_box: Rect | None,
) -> dict[str, Any]:
    record = {
        "id": index,
        "type": element.get("type"),
        "content": element.get("content"),
        "bbox": element.get("bbox"),
        "interactivity": element.get("interactivity"),
        "source": element.get("source"),
    }
    if absolute_box is not None:
        record["absolute_box"] = absolute_box
    if relative_box is not None:
        record["relative_box"] = relative_box
    return record


def _relative_box(absolute_box: Rect, geometry: dict[str, Any]) -> Rect:
    win_x = _number(geometry.get("x"))
    win_y = _number(geometry.get("y"))
    return {
        "x1": absolute_box["x1"] - win_x,
        "y1": absolute_box["y1"] - win_y,
        "x2": absolute_box["x2"] - win_x,
        "y2": absolute_box["y2"] - win_y,
    }


def _valid_bbox(bbox: Any) -> bool:
    if not isinstance(bbox, list) or len(bbox) != 4:
        return False
    try:
        [_number(value) for value in bbox]
    except (TypeError, ValueError):
        return False
    return True


def _has_area(rect: dict[str, Any]) -> bool:
    return _number(rect.get("width")) > 0 and _number(rect.get("height")) > 0


def _number(value: Any) -> float:
    if value is None:
        return 0.0
    return float(value)
