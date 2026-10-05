#!/usr/bin/env python3
"""darts501 - 飞镖 501 结镖计算器。

给定剩余分数，算出以 double（或牛眼）收尾的结镖路线。
纯标准库。
"""

import argparse
import sys

# (分数, 名称, 是否算作 double 收尾)
_SEGMENTS = []
for i in range(1, 21):
    _SEGMENTS.append((i, f"S{i}", False))
for i in range(1, 21):
    _SEGMENTS.append((2 * i, f"D{i}", True))
for i in range(1, 21):
    _SEGMENTS.append((3 * i, f"T{i}", False))
_SEGMENTS.append((25, "25", False))     # 外圈牛眼, 单倍
_SEGMENTS.append((50, "Bull", True))    # 牛眼算 double 收尾

# 同分数去重: 同分保留分值表达最高的记法 (T > D > S), 保证路线简洁
_BEST_LABEL = {}
for score, label, is_double in _SEGMENTS:
    key = (score, is_double)
    rank = 2 if label.startswith("T") else (1 if label.startswith("D") or label == "Bull" else 0)
    if key not in _BEST_LABEL or rank > _BEST_LABEL[key][1]:
        _BEST_LABEL[key] = (label, rank)

SEGMENTS = sorted(
    ((score, label, is_double) for (score, is_double), (label, _r) in _BEST_LABEL.items()),
    key=lambda t: -t[0],
)
DOUBLES = {score: label for score, label, is_double in SEGMENTS if is_double}


def checkout(score, max_darts=3):
    """返回结镖路线 (list of str), 找不到返回 None。

    优先更少镖数; 同镖数下优先分值大的镖先行 (标准打法习惯)。
    """
    if score in DOUBLES:
        return [DOUBLES[score]]
    if max_darts >= 2:
        for s1, l1, _d1 in SEGMENTS:
            rest = score - s1
            if rest in DOUBLES:
                return [l1, DOUBLES[rest]]
    if max_darts >= 3:
        for s1, l1, _d1 in SEGMENTS:
            for s2, l2, _d2 in SEGMENTS:
                rest = score - s1 - s2
                if rest in DOUBLES:
                    return [l1, l2, DOUBLES[rest]]
    return None


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="飞镖 501 结镖计算器: 给出以 double 收尾的结镖路线。"
    )
    ap.add_argument("score", type=int, help="剩余分数 (2-170)")
    ap.add_argument("--darts", type=int, default=3, choices=(1, 2, 3),
                    help="最多用几镖结镖 (默认 3)")
    args = ap.parse_args(argv)

    if not 2 <= args.score <= 170:
        print(f"error: 分数必须在 2-170 之间, 得到 {args.score}", file=sys.stderr)
        return 2

    route = checkout(args.score, args.darts)
    if route is None:
        print(f"{args.score}: 无法结镖")
        return 1
    print(f"{args.score}: {' '.join(route)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
