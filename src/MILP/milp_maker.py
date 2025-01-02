import logging
import random
from collections import defaultdict
from typing import Dict, List

import pulp
from pulp import PULP_CBC_CMD, LpMaximize, LpProblem, LpVariable, lpSum

logger = logging.getLogger("shift_scheduler")


class MILPMaker:
    def __init__(self, availability, role_compatibility, fulltime, weights):
        # 従業員と役職の初期化
        self.employees = list(availability.keys())
        self.roles = list(role_compatibility[self.employees[0]].keys())
        self.availability = availability
        self.role_compatibility = role_compatibility
        self.fulltime = fulltime
        self.weights = weights

        logger.debug(f"Initialized MILPMaker with employees: {self.employees}")
        logger.debug(f"Roles: {self.roles}")
        logger.debug(f"Availability: {self.availability}")
        logger.debug(f"Role compatibility: {self.role_compatibility}")
        logger.debug(f"Fulltime employees: {self.fulltime}")
        logger.debug(f"Weights: {self.weights}")

    def solve_for_day(
        self, day: int, num_trials: int = 1
    ) -> List[Dict[str, List[str]]]:
        # 問題を作成
        problem = self._create_base_problem(day)

        # LP の出力
        logger.debug(problem)

        schedules = []

        for i in range(num_trials):

            logger.info(f"Solving Day {day}[{i}] ...")
            seed = random.randint(0, 100000)
            logger.debug(f"Seed: {seed}")
            result = problem.solve(
                PULP_CBC_CMD(msg=False, options=[f"randomSeed={seed}"])
            )

            if result == 1:
                # 解を抽出
                schedule = self._extract_solution(problem, day)
            else:
                logger.error(f"Day {day} {i}: No solution found.")
                schedule = {role: ["未割当"] for role in self.roles}

            schedules.append(schedule)

        return schedules

    def _is_binary(self, var: LpVariable) -> bool:
        # 下限と上限が 0 と 1 である場合は、Binary となると判定する
        return var.lowBound == 0 and var.upBound == 1

    def _create_base_problem(self, day: int) -> LpProblem:
        # 線形計画問題を作成
        # 最大化問題
        problem = LpProblem(f"ShiftAssignment_Day_{day}", LpMaximize)
        logger.debug(f"Creating problem: {problem.name}")

        # 変数を定義
        x = {}
        for e in self.employees:
            for r in self.roles:
                if (e == "メディカル") or ("不足" in e) or ("不要" in e):
                    # integer
                    x[(e, r)] = LpVariable(f"{e}_{r}", lowBound=0, cat=pulp.LpInteger)
                else:
                    # binary
                    x[(e, r)] = LpVariable(f"{e}_{r}", cat=pulp.LpBinary)

        # 各種制約と目的関数を追加
        self._add_role_constraints(problem, x, day)
        self._add_availability_constraints(problem, x, day)
        self._add_role_compatibility_constraints(problem, x)
        self._add_single_role_constraints(problem, x)
        self._add_fulltime_constraints(problem, x)
        self._add_objective_function(problem, x)

        return problem

    def _add_role_constraints(self, problem: LpProblem, x: Dict, day: int):
        # 各役職の必要人数の制約を追加
        for r in self.roles:
            required_count = {
                "採血": 4,
                "血圧": 2,
                "計測": 3,
                "胃カメラ": 6,
                "5F採血": 2,
            }.get(r, 1)

            problem += (
                lpSum(x[(e, r)] for e in self.employees) == required_count,
                f"RoleAssignment_Day_{day}_{r}",
            )

    def _add_availability_constraints(self, problem: LpProblem, x: Dict, day: int):
        # 従業員の出勤可能性に基づく制約を追加
        for e in self.employees:
            for r in self.roles:
                if not self.availability[e][day]:
                    problem += (
                        x[(e, r)] == 0,
                        f"Availability_Day_{day}_{e}_{r}",
                    )

    def _add_role_compatibility_constraints(self, problem: LpProblem, x: Dict):
        # 各従業員の役職適性に基づく制約を追加
        for e in self.employees:
            for r in self.roles:
                if not self.role_compatibility[e][r]:
                    problem += (
                        x[(e, r)] == 0,
                        f"RoleCompatibility_{e}_{r}",
                    )

    def _add_single_role_constraints(self, problem: LpProblem, x: Dict):
        # 各従業員が1日に1つの役職のみ担当する制約を追加
        for e in self.employees:
            if "不足" in e or "不要" in e:
                continue
            elif e == "メディカル":
                problem += (
                    lpSum(x[(e, r)] for r in self.roles) <= 4,
                    f"SingleRoleAssignment_{e}",
                )
            else:
                problem += (
                    lpSum(x[(e, r)] for r in self.roles) <= 1,
                    f"SingleRoleAssignment_{e}",
                )

    def _add_fulltime_constraints(self, problem: LpProblem, x: Dict):
        # フルタイム従業員が特定の役職を担当する制約を追加
        problem += (
            lpSum(x[(e, "受付")] for e in self.employees if self.fulltime[e]) >= 1,
            "FulltimeRoleAssignment_Reception",
        )
        problem += (
            lpSum(x[(e, "胃カメラ")] for e in self.employees if self.fulltime[e]) >= 1,
            "FulltimeRoleAssignment_Gastroscopy",
        )

    def _add_objective_function(self, problem: LpProblem, x: Dict):
        # 重みに基づいて, 目的関数を設定
        # weights に基づいて, 目的関数を設定
        problem += (
            lpSum(
                self.weights[e] * x[(e, r)] for e in self.employees for r in self.roles
            ),
            "Objective",
        )

    def _extract_solution(self, problem: LpProblem, day: int) -> Dict[str, List[str]]:
        """
        現在の解を抽出し、再び同じ解が得られないようにする制約を追加。
        簡単のため,binaryのものだけを考慮する
        """
        # 解を抽出し、スケジュールとして返す
        schedule = defaultdict(list)

        for var in problem.variables():
            employee, role = var.name.split("_")
            for i in range(int(var.varValue)):
                schedule[role].append(employee)

        return schedule
