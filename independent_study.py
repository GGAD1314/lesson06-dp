#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
独立研究任务（20分）
① 回溯法：n-后问题是什么、与动规穷举有何不同
② 完全背包（物品可重复）改哪一行
③ 分支限界一句话 + 比回溯好在哪
"""


# ============================================================
# ① n-皇后问题（回溯法实现 + 与动规对比）
# ============================================================

def n_queens_backtracking(n):
    """
    n-皇后问题：在n×n棋盘上放n个皇后，互不攻击
    （同一行/列/对角线不能有两个皇后）
    使用回溯法求解
    """
    solutions = []
    # queens[i] = 第i行皇后在第几列
    queens = [0] * n

    def is_safe(row, col):
        """检查在(row, col)放皇后是否安全"""
        for prev_row in range(row):
            # 同列？
            if queens[prev_row] == col:
                return False
            # 同对角线？
            if abs(queens[prev_row] - col) == abs(prev_row - row):
                return False
        return True

    def backtrack(row):
        if row == n:
            # 找到一个解
            solutions.append(queens[:])
            return
        for col in range(n):
            if is_safe(row, col):
                queens[row] = col
                backtrack(row + 1)

    backtrack(0)
    return solutions


# ============================================================
# ② 完全背包（物品可重复使用）
# ============================================================

def unbounded_knapsack(names, weights, values, capacity):
    """
    完全背包：物品可以无限次使用
    与0-1背包的区别：
      0-1背包的递推是：
        for i in range(1, n+1):
            for c in range(capacity, w[i]-1, -1):  # 倒序
                dp[c] = max(dp[c], dp[c-w[i]] + v[i])

      完全背包改一行：把倒序改成正序
        for i in range(1, n+1):
            for c in range(w[i], capacity+1):      # 正序
                dp[c] = max(dp[c], dp[c-w[i]] + v[i])
    """
    n = len(names)
    dp = [0] * (capacity + 1)

    for i in range(n):
        w_i = weights[i]
        v_i = values[i]
        # 关键改动：正序遍历（不是0-1的倒序）
        for c in range(w_i, capacity + 1):
            if dp[c - w_i] + v_i > dp[c]:
                dp[c] = dp[c - w_i] + v_i

    return dp[capacity], dp


# ============================================================
# ③ 分支限界（0-1背包的分支限界 + 上界函数）
# ============================================================

def knapsack_branch_and_bound(names, weights, values, capacity):
    """
    分支限界法解0-1背包
    与回溯法的区别：回溯是深度优先+可行性剪枝；
                 分支限界是广度/优先队列+上界剪枝
    """
    from collections import deque

    n = len(names)
    best_val = 0
    best_set = []

    # 计算剩余物品的上界（贪心估计）
    def upper_bound(i, current_w, current_v):
        """从第i件开始，用贪心估计能达到的最大价值上界"""
        remaining_w = capacity - current_w
        bound = current_v
        j = i
        while j < n and weights[j] <= remaining_w:
            bound += values[j]
            remaining_w -= weights[j]
            j += 1
        if j < n and remaining_w > 0:
            bound += values[j] * remaining_w / weights[j]
        return bound

    # 队列元素: (下一个物品索引, 当前重量, 当前价值, 当前选中集)
    queue = deque([(0, 0, 0, [])])

    while queue:
        i, w, v, selected = queue.popleft()

        if i == n:
            if v > best_val:
                best_val = v
                best_set = selected
            continue

        # 上界剪枝
        if upper_bound(i, w, v) <= best_val:
            continue

        # 分支1：不选第i件
        queue.append((i + 1, w, v, selected))

        # 分支2：选第i件（如果装得下）
        if w + weights[i] <= capacity:
            queue.append((i + 1, w + weights[i], v + values[i], selected + [i]))

    return best_val, best_set


# ============================================================
# 演示
# ============================================================

if __name__ == '__main__':
    NAMES = ['帐篷', '炉具', '睡袋', '食物', '水具']
    WEIGHTS = [300, 200, 350, 400, 250]
    VALUES = [60, 50, 100, 120, 95]
    CAPACITY = 1000

    print("=" * 60)
    print("独立研究任务")
    print("=" * 60)

    # ---------- ① n-皇后 ----------
    print("\n" + "=" * 60)
    print("① n-皇后问题")
    print("=" * 60)

    print("\n  n-后问题是什么：")
    print("    在n×n的棋盘上放置n个皇后，使得任意两个皇后")
    print("    不在同一行、同一列、也不在同一条对角线上。")
    print("    目标是找到所有满足条件的放置方案。")

    print("\n  示例：4-皇后")
    sols = n_queens_backtracking(4)
    print(f"    共找到 {len(sols)} 个解:")
    for si, sol in enumerate(sols):
        board = []
        for row in range(4):
            line = [' . '] * 4
            line[sol[row]] = ' Q '
            board.append(''.join(line))
        print(f"\n    解{si+1}: {sol} (皇后列位置)")
        for line in board:
            print(f"      {line}")

    print("\n  与动规穷举的不同：")
    print("    动规穷举：穷举所有 2^n 种放法再过滤，n=8时256种还行，")
    print("              但动规本身不直接处理n-后（没有重叠子问题结构）")
    print("    回溯法：边构造边剪枝。放第r行时，只需要检查与前面r-1行")
    print("            皇后是否冲突，不冲突才继续。大量不可能的分支")
    print("            早早被剪掉，实际搜索量远小于2^n。")
    print("    关键区别：回溯是'构造+剪枝'，动规是'拆重叠子问题+存表'。")
    print("    n-后没有重叠子问题结构（每个解必须完整构造），")
    print("    所以回溯更适合；而背包/硬币有重叠子问题，动规更高效。")

    # ---------- ② 完全背包 ----------
    print("\n" + "=" * 60)
    print("② 完全背包（物品可重复）")
    print("=" * 60)

    print("\n  改动哪一行：")
    print("    0-1背包内层循环： for c in range(capacity, w-1, -1)  # 倒序")
    print("    完全背包内层循环： for c in range(w, capacity+1)       # 正序")
    print("\n  为什么？")
    print("    倒序遍历保证每个物品只用一次（dp[c-w]还没被本轮更新）")
    print("    正序遍历允许同一物品被多次选（dp[c-w]在本轮已更新）")

    val_c, dp_c = unbounded_knapsack(NAMES, WEIGHTS, VALUES, CAPACITY)
    print(f"\n  完全背包（容量{CAPACITY}g）:")
    print(f"    最大重要度: {val_c}")
    print(f"    （物品可无限次，理论上价值可以无限增长，")
    print(f"     这里所有重量≥1，所以还是有限的）")

    # ---------- ③ 分支限界 ----------
    print("\n" + "=" * 60)
    print("③ 分支限界法（Branch and Bound）")
    print("=" * 60)

    print("\n  一句话：")
    print("    回溯法（深搜+可行性剪枝）遇上上界函数，")
    print("    变成优先/广度优先+上界剪枝，剪得更狠。")

    print("\n  比回溯好在哪：")
    print("    回溯法只知道'这个分支可能不行'（可行性），")
    print("    分支限界还要估计'这个分支最好能到多少'（上界）。")
    print("    如果上界 ≤ 当前最优，整枝剪掉，不浪费时间。")
    print("\n    关键区别：")
    print("      回溯：搜索顺序不重要，找到一个解就行，深度优先")
    print("      限界：优先找上界高的分支（广搜/优先队列），")
    print("            更早发现好解，从而剪更多枝")

    val_bb, sel_bb = knapsack_branch_and_bound(NAMES, WEIGHTS, VALUES, CAPACITY)
    print(f"\n  分支限界结果（容量{CAPACITY}g）:")
    print(f"    最大重要度: {val_bb}")
    print(f"    选中: {sel_bb} → {[NAMES[i] for i in sel_bb]}")
    print(f"    与动规结果一致 ✓" if val_bb == 315 else "    ✗ 不一致")
