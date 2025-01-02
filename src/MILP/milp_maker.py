import logging
from typing import Dict

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

    def solve_for_day(self, day: int) -> Dict[str, str]:
        problem = LpProblem(f"ShiftAssignment_Day_{day}", LpMinimize)
        logger.debug(f"make problem: {problem.name}")

        x = {
            (e, r): LpVariable(f"x_{e}_{day}_{r}", cat="Binary")
            for e in self.employees
            for r in self.roles
        }

        # 制約条件1: 各役職は1人の担当者のみ
        for r in self.roles:
            problem += (
                lpSum(x[(e, r)] for e in self.employees) == 1,
                f"RoleAssignment_Day_{day}_{r}",
            )

        # 制約条件2: 従業員のシフト可能性に基づく制約
        for e in self.employees:
            for r in self.roles:
                problem += (
                    x[(e, r)] <= self.availability[e][day],
                    f"Availability_Day_{day}_{e}_{r}",
                )

        # 制約条件3: 各従業員の役職適性を考慮
        for e in self.employees:
            for r in self.roles:
                problem += (
                    x[(e, r)] <= self.role_compatibility[e][r],
                    f"Compatibility_Day_{day}_{e}_{r}",
                )

        # 制約条件4: 各従業員は1日に1つの役職のみ
        # ただし、メディカル, 外来は複数の役職を担当可能
        for e in self.employees:
            if e == "メディカル" or e == "外来":
                continue
            problem += (
                lpSum(x[(e, r)] for r in self.roles) <= 1,
                f"SingleRoleAssignment_Day_{day}_{e}",
            )

        logger.debug(f"fulltime: {self.fulltime}")

        # 制約条件5: 血圧と受付のいずれかは社員が担当
        # problem += (
        #     lpSum(x[(e, "血圧")] for e in self.employees if self.fulltime[e])
        #     + lpSum(x[(e, "受付")] for e in self.employees if self.fulltime[e])
        #     >= 1,
        #     f"FulltimeRoleAssignment_Day_{day}",
        # )

        logger.debug(f"num of variables: {len(problem.variables())}")

        # 目的関数: 外来 * 100 + メディカルの割り当てを最小化
        problem += lpSum(x[("外来", r)] for r in self.roles) * 100 + lpSum(
            x[("メディカル", r)] for r in self.roles
        )

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
                r: e
                for e in self.employees
                for r in self.roles
                if x[(e, r)].value() == 1
            }
            return schedule
        else:
            raise Exception(f"Day {day} のスケジュールが見つかりませんでした。")
