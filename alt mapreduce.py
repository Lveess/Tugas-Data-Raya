from functools import reduce
import json
from pathlib import Path
from typing import Any, List


# Load dataraw from `dataraw.json` if present; otherwise use a small default list.
def load_dataraw() -> List[Any]:
    # Try several candidate paths in order:
    candidates = [
        Path("BMI CALCULATOR/dataraw.json"),
        Path("dataraw.json"),
        Path("big data BMI.json"),
    ]
    for p in candidates:
        if not p.exists():
            continue
        try:
            with p.open("r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    return data
                except Exception:
                    # try a tolerant fallback: extract JSON objects by scanning braces
                    f.seek(0)
                    text = f.read()
                    objs = []
                    i = 0
                    n = len(text)
                    while i < n:
                        if text[i] == '{':
                            depth = 0
                            j = i
                            while j < n:
                                if text[j] == '{':
                                    depth += 1
                                elif text[j] == '}':
                                    depth -= 1
                                    if depth == 0:
                                        try:
                                            obj_text = text[i:j+1]
                                            objs.append(json.loads(obj_text))
                                        except Exception:
                                            pass
                                        i = j
                                        break
                                j += 1
                        i += 1
                    if objs:
                        return objs
        except Exception:
            continue
    # final fallback: small numeric list
    return [1, 2, 3, 4, 5]


dataraw = load_dataraw()

def split_data(data, parts=2):
    """Split `data` into `parts` roughly equal partitions."""
    if parts <= 0:
        return []
    k, m = divmod(len(data), parts)
    return [data[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(parts)]

def DNmap(data):
    """Map operation on a datanode: return the sum of its items."""
    return sum(data) if data else 0

def DNReduce(mapped_values):
    """Reduce operation across mapped values: sum the partial results."""
    return sum(mapped_values)

def MapReduce(datanamenode):
    """Apply DNmap to each datanode and then DNReduce on the results."""
    map_data = [DNmap(d) for d in datanamenode]
    return DNReduce(map_data)


if __name__ == "__main__":
    # keep raw data intact
    print("dataraw: ")
    try:
        # if it's a list of dicts, try to extract a numeric field (prefer 'BMI')
        sample = dataraw[:]
    except Exception:
        sample = dataraw
    print(sample)

    # If dataraw is a list of objects, attempt to extract numeric values for MapReduce.
    def extract_numeric_list(data):
        if not isinstance(data, list):
            return []
        # list of numbers
        if all(isinstance(x, (int, float)) for x in data):
            return data
        # list of dicts -> try 'BMI' then other numeric-looking fields
        if all(isinstance(x, dict) for x in data):
            # try common BMI keys (case-insensitive)
            for key_candidate in ("BMI", "bmi"):
                vals = []
                ok = True
                for obj in data:
                    v = obj.get(key_candidate)
                    try:
                        vals.append(float(v))
                    except Exception:
                        ok = False
                        break
                if ok and vals:
                    return vals

            # try some alternative keys used in dataset
            keys_to_try = ["Berat (kg)", "Berat_kg", "Berat", "weight"]
            for k in keys_to_try:
                vals = []
                ok = True
                for obj in data:
                    v = obj.get(k)
                    try:
                        vals.append(float(v))
                    except Exception:
                        ok = False
                        break
                if ok and vals:
                    return vals

            # fallback: choose the numeric field present in most records
            counts = {}
            for obj in data:
                for kk, vv in obj.items():
                    try:
                        float(vv)
                        counts.setdefault(kk, 0)
                        counts[kk] += 1
                    except Exception:
                        continue
            if counts:
                best = max(counts.items(), key=lambda t: t[1])[0]
                vals = []
                for obj in data:
                    try:
                        vals.append(float(obj.get(best, 0)))
                    except Exception:
                        vals.append(0.0)
                return vals
        return []

    numeric_data = extract_numeric_list(dataraw)
    if not numeric_data:
        # fallback to splitting the original dataraw if it's already numeric list
        namenode = split_data(dataraw, parts=2)
    else:
        namenode = split_data(numeric_data, parts=2)
    print("datanode partitions:", namenode)

    # run MapReduce over the datanodes
    total = MapReduce(datanamenode=namenode)
    print("MapReduce total:", total)

