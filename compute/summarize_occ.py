"""Summarise compare_occ_{default,inter}.json, checking offset volumes against exact formulas.

Exact volumes for the convex parts (K ⊕ rB for outward offsets; inner parallel body for inward):
  - Box a×b×c: inward (a-2r)(b-2r)(c-2r), empty when r ≥ min/2.
    Outward (Steiner): V + S r + M r² + 4/3 π r³, with M = (π/4)·(total edge length).
  - Cylinder R, H: inward π(R-r)²(H-2r). Outward Steiner with M = πH + π²R.
  - Filleted box (edge 10, fillet 2) = cube6 ⊕ B(2):
      inward r ≤ 2: cube6 ⊕ B(2-r); 2 < r < 5: (10-2r)³.
      outward: cube6 ⊕ B(2+r).
"""
import json, math

def steiner(V, S, M, r): return V + S * r + M * r * r + 4 / 3 * math.pi * r ** 3
def box_out(a, b, c, r): return steiner(a * b * c, 2 * (a * b + b * c + c * a), math.pi / 4 * 4 * (a + b + c), r)
def box_in(a, b, c, r):
    m = min(a, b, c)
    return None if 2 * r >= m else (a - 2 * r) * (b - 2 * r) * (c - 2 * r)
def cyl_out(R, H, r): return steiner(math.pi * R * R * H, 2 * math.pi * R * R + 2 * math.pi * R * H, math.pi * H + math.pi ** 2 * R, r)
def cyl_in(R, H, r): return None if r >= min(R, H / 2) else math.pi * (R - r) ** 2 * (H - 2 * r)
def fil(r):   # signed r: >0 outward
    if r >= 0: return box_out(6, 6, 6, 2 + r)
    r = -r
    if r <= 2: return box_out(6, 6, 6, 2 - r)
    return None if r >= 5 else (10 - 2 * r) ** 3

EXACT = {
    "plate": lambda r: box_out(4, 4, 1, r) if r >= 0 else box_in(4, 4, 1, -r),
    "plate_t0.3": lambda r: box_out(4, 4, 0.3, r) if r >= 0 else box_in(4, 4, 0.3, -r),
    "plate_t0.1": lambda r: box_out(4, 4, 0.1, r) if r >= 0 else box_in(4, 4, 0.1, -r),
    "box": lambda r: box_out(10, 10, 10, r) if r >= 0 else box_in(10, 10, 10, -r),
    "cylinder": lambda r: cyl_out(3, 10, r) if r >= 0 else cyl_in(3, 10, -r),
    "filleted": fil,
}


def verdict(name, s, rec, res):
    r = s * rec["exact"]
    ex = EXACT.get(name)
    expect = ex(r) if ex else "?"
    st = res["status"]
    if st != "done":
        got = "无结果" if st in ("empty result", "not done") else st
        if expect is None:
            return "对（应为空）", got
        return ("失败" if expect != "?" else "失败"), got
    got = f"{res['volume']:.4g}"
    if expect is None:
        return "错（应为空却有结果）", got
    if expect == "?":
        ok = res["valid"] and res["shells"] == 1 and res["euler"] == rec["euler0"]
        return ("拓扑对" if ok else "拓扑错") + ("" if res["valid"] else "，体检不合格"), got
    rel = abs(res["volume"] - expect) / expect
    tag = "对" if rel < 1e-3 and res["shells"] == 1 else "错"
    if tag == "错" and res["valid"]:
        tag += "（体检合格）"
    return tag + f"（误差 {rel:.1%}）" if rel >= 1e-3 else tag, got


if __name__ == "__main__":
    for mode in ("default", "inter"):
        try:
            data = json.load(open(f"compare_occ_{mode}.json"))
        except FileNotFoundError:
            continue
        print(f"\n===== mode: {mode} =====")
        for rec in data:
            row = []
            for k, res in rec["offsets"].items():
                v, got = verdict(rec["name"], float(k), rec, res)
                row.append(f"{k}:{v}")
            print(rec["name"], " | ".join(row))
