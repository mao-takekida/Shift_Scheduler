import logging
from typing import Dict, List

from pulp import PULP_CBC_CMD, LpMinimize, LpProblem, LpVariable, lpSum

logger = logging.getLogger("shift_scheduler")


class MILPMaker:
    def __init__(self, availability, role_compatibility, fulltime):
        logger.debug(f"employees: {list(availability.keys())}")
        logger.debug(
            f"roles: {list(role_compatibility[list(availability.keys())[0]].keys())}"
        )
        logger.debug(f"availability: {availability}")
        logger.debug(f"role_compatibility: {role_compatibility}")
        logger.debug(f"fulltime: {fulltime}")

        self.employees = list(availability.keys())
        self.roles = list(role_compatibility[self.employees[0]].keys())
        self.availability = availability
        self.role_compatibility = role_compatibility
        self.fulltime = fulltime

    def solve_for_day(self, day: int) -> Dict[str, List[str]]:
        problem = LpProblem(f"ShiftAssignment_Day_{day}", LpMinimize)
        logger.debug(f"make problem: {problem.name}")

        x = {
            (e, r): LpVariable(f"x_{e}_{day}_{r}", cat="Binary")
            for e in self.employees
            for r in self.roles
        }

        # 採血4
        # 血圧2
        # 計測3
        # 胃カメラ6
        # 採血(五階)2
        # その他1
        # 制約条件: 各役職の人数を満たす
        for r in self.roles:
            if r == "採血":
                problem += (
                    lpSum(x[(e, r)] for e in self.employees) == 4,
                    f"RoleAssignment_Day_{day}_{r}",
                )
            elif r == "血圧":
                problem += (
                    lpSum(x[(e, r)] for e in self.employees) == 2,
                    f"RoleAssignment_Day_{day}_{r}",
                )
            # elif r == "計測":
            #     problem += (
            #         lpSum(x[(e, r)] for e in self.employees) == 3,
            #         f"RoleAssignment_Day_{day}_{r}",
            #     )
            # elif r == "胃カメラ":
            #     problem += (
            #         lpSum(x[(e, r)] for e in self.employees) == 6,
            #         f"RoleAssignment_Day_{day}_{r}",
            #     )
            # elif r == "採血(五階)":
            #     problem += (
            #         lpSum(x[(e, r)] for e in self.employees) == 2,
            #         f"RoleAssignment_Day_{day}_{r}",
            #     )
            else:
                problem += (
                    lpSum(x[(e, r)] for e in self.employees) == 1,
                    f"RoleAssignment_Day_{day}_{r}",
                )

        # 制約条件: 従業員のシフト可能性に基づく制約
        for e in self.employees:
            for r in self.roles:
                problem += (
                    x[(e, r)] <= self.availability[e][day],
                    f"Availability_Day_{day}_{e}_{r}",
                )

        # 制約条件: 各従業員の役職適性を考慮
        for e in self.employees:
            for r in self.roles:
                problem += (
                    x[(e, r)] <= self.role_compatibility[e][r],
                    f"Compatibility_Day_{day}_{e}_{r}",
                )

        # 制約条件: 各従業員は1日に1つの役職のみ
        # ただし、メディカル, 外来不足は複数の役職を担当可能
        for e in self.employees:
            if e == "メディカル" or e == "外来不足":
                continue
            problem += (
                lpSum(x[(e, r)] for r in self.roles) <= 1,
                f"SingleRoleAssignment_Day_{day}_{e}",
            )

        logger.debug(f"fulltime: {self.fulltime}")

        # 制約条件: 受付のいずれかは社員が担当
        problem += (
            lpSum(x[(e, "受付")] for e in self.employees if self.fulltime[e]) >= 1,
            f"FulltimeRoleAssignment_Day_Reception_{day}",
        )
        # 制約条件: 胃カメラのいずれかは社員が担当
        problem += (
            lpSum(x[(e, "胃カメラ")] for e in self.employees if self.fulltime[e]) >= 1,
            f"FulltimeRoleAssignment_Day_Gastroscopy_{day}",
        )

        logger.debug(f"num of variables: {len(problem.variables())}")

        # 目的関数: 外来不足 * 100 + メディカルの割り当てを最小化
        problem += lpSum(x[("外来不足", r)] for r in self.roles) * 100 + lpSum(
            x[("メディカル", r)] for r in self.roles
        )

        logger.debug(f"objective function: {problem.objective}")

        logger.debug(f"num of variables: {len(problem.variables())}")
        for var in problem.variables():
            logger.debug(f"{var.name}: {var.varValue}")
        logger.debug(f"num of constraints: {len(problem.constraints)}")
        for name, constraint in problem.constraints.items():
            # 制約の内容を記述
            logger.debug(f"{name}: ({constraint})")

        logger.info(f"Solving Day {day}...")
        result = problem.solve(PULP_CBC_CMD(msg=False))
        logger.debug(f"Solved: {result}")

        if result == 1:
            schedule = {
                r: [e for e in self.employees if x[(e, r)].value() == 1]
                for r in self.roles
            }
            return schedule
        else:
            raise Exception(f"Day {day} のスケジュールが見つかりませんでした。")
