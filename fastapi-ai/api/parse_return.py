"""Utility to parse JSON-like return data into readable "标题: 值" lines.

Function: parse_return_to_text(data) -> str

If `data` is a JSON string it will be parsed. The output flattens nested
structures into dotted keys and array indices, for example:

待办事项: 购买小包尿不湿

If an integer looks like a millisecond timestamp (>= 1e12) it's converted to
an ISO datetime string for readability.
"""
from __future__ import annotations

import json
import os
from datetime import datetime
from typing import Any, List


def parse_return_to_text(data: Any, order: List[str] | None = None) -> str:
    """Convert JSON/dict/list into readable lines 'title: value'.

    Args:
        data: dict/list or JSON string containing the data.

    Returns:
        A string with one "key: value" per line. Keys use dot notation for
        dicts and [i] for list indices.
    """
    """
    Behavior changed to only read the first-level `fields` of each item.

    For each item in `data['items']`, iterate its `fields` mapping and
    produce lines like "标题: 值" where:
      - bool -> '是' / '否'
      - list -> join items with '、' (if list items are dicts and contain
        a 'text' key, use that; otherwise stringify)
      - dict -> if it contains 'text' use that, otherwise JSON-stringify
      - large int (>=1e12) is treated as ms epoch and formatted as ISO
    """

    if isinstance(data, str):
        data = json.loads(data)

    lines: List[str] = []

    def _format_scalar(val: Any) -> str:
        if val is None:
            return ""
        if isinstance(val, bool):
            return "是" if val else "否"
        if isinstance(val, int) and val >= 1_000_000_000_000:
            try:
                return datetime.fromtimestamp(val / 1000.0).isoformat(sep=" ")
            except Exception:
                return str(val)
        if isinstance(val, (str, int, float)):
            return str(val)
        if isinstance(val, dict):
            # Prefer a 'text' field if present
            if "text" in val and isinstance(val["text"], (str, int, float)):
                return str(val["text"])
            # Fallback to compact JSON
            try:
                return json.dumps(val, ensure_ascii=False)
            except Exception:
                return str(val)
        return str(val)

    # Walk only the items -> fields one level
    items = []
    if isinstance(data, dict) and "items" in data and isinstance(data["items"], list):
        items = data["items"]
    elif isinstance(data, list):
        items = data
    else:
        # If the structure is a plain fields dict
        if isinstance(data, dict) and "fields" in data and isinstance(data["fields"], dict):
            items = [data]

    for item in items:
        fields = item.get("fields", {}) if isinstance(item, dict) else {}
        if not isinstance(fields, dict):
            continue

        # Determine key order: use provided `order` list first, then remaining keys
        keys = []
        if order:
            for key in order:
                if key in fields and key not in keys:
                    keys.append(key)
        for key in fields:
            if key not in keys:
                keys.append(key)

        for k in keys:
            v = fields.get(k)

            # Special handling: 距离截止日 field which may be like
            # {"type":1, "value":[{"text":"🕑还有18.5天到期","type":"text"}]}
            if isinstance(v, dict) and "value" in v and isinstance(v["value"], list):
                # take first element's text if available
                first = v["value"][0] if v["value"] else None
                if isinstance(first, dict) and "text" in first:
                    val_str = _format_scalar(first.get("text"))
                    lines.append(f"{k}: {val_str}")
                    continue

            # Handle lists
            if isinstance(v, list):
                parts: List[str] = []
                for el in v:
                    if isinstance(el, dict):
                        # if dict has 'text' use it
                        if "text" in el:
                            parts.append(_format_scalar(el.get("text")))
                        else:
                            parts.append(_format_scalar(el))
                    else:
                        parts.append(_format_scalar(el))
                val_str = "、".join([p for p in parts if p is not None and p != ""])
            else:
                val_str = _format_scalar(v)

            lines.append(f"{k}: {val_str}")

        # blank line after each item
        lines.append("")

    # Remove trailing blank line if present
    if lines and lines[-1] == "":
        lines = lines[:-1]

    return "\n".join(lines)


if __name__ == "__main__":
    # Demo: load sibling return_data.json and print parsed output
    base = os.path.dirname(__file__)
    path = os.path.join(base, "return_data.json")
    if not os.path.exists(path):
        print(f"No file found at: {path}")
    else:
        with open(path, "r", encoding="utf-8") as f:
            raw = f.read()
        text = parse_return_to_text(raw)
        print(text)
