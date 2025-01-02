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
        # ただし、派遣は複数の役職を担当可能
        for e in self.employees:
            if e == "派遣":
                continue
            problem += (
                lpSum(x[(e, r)] for r in self.roles) <= 1,
                f"SingleRoleAssignment_Day_{day}_{e}",
            )

        logger.debug(f"fulltime: {self.fulltime}")

        # 制約条件5: 血圧と受付のいずれかは社員が担当
        problem += (
            lpSum(x[(e, "血圧")] for e in self.employees if self.fulltime[e])
            + lpSum(x[(e, "受付")] for e in self.employees if self.fulltime[e])
            >= 1,
            f"FulltimeRoleAssignment_Day_{day}",
        )

        logger.debug(f"num of variables: {len(problem.variables())}")

        # 目的関数: 派遣の割り当てを最小化
        problem += lpSum(x[("派遣", r)] for r in self.roles)

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


if __name__ == "__main__":
    import sys
    from pathlib import Path

    sys.path.append(str(Path(__file__).parent.parent))
    import argparse

    from utils.logger import setup_logger

    parser = argparse.ArgumentParser(description="シフトを作成します。")
    parser.add_argument("-l", "--loglevel", help="ログレベル", default="INFO")
    logger = setup_logger("shift_scheduler", parser.parse_args().loglevel)
    # データの定義
    # シフト可能性（サンプルデータ）
    availability = {
        "齋藤": {
            1: True,
            2: False,
            3: True,
            4: True,
            5: True,
            6: True,
            7: False,
            8: True,
            9: True,
            10: True,
        },
        "山田": {
            1: False,
            2: True,
            3: True,
            4: False,
            5: False,
            6: False,
            7: True,
            8: True,
            9: True,
            10: True,
        },
        "和田": {
            1: True,
            2: True,
            3: True,
            4: False,
            5: True,
            6: True,
            7: False,
            8: True,
            9: False,
            10: True,
        },
        "田中": {
            1: False,
            2: False,
            3: False,
            4: True,
            5: False,
            6: True,
            7: False,
            8: True,
            9: True,
            10: False,
        },
        "佐藤": {
            1: True,
            2: True,
            3: True,
            4: False,
            5: True,
            6: True,
            7: False,
            8: False,
            9: True,
            10: False,
        },
        "中村": {
            1: True,
            2: False,
            3: True,
            4: True,
            5: False,
            6: True,
            7: True,
            8: True,
            9: True,
            10: True,
        },
        "小林": {
            1: False,
            2: True,
            3: False,
            4: True,
            5: True,
            6: False,
            7: True,
            8: True,
            9: True,
            10: True,
        },
        "加藤": {
            1: True,
            2: True,
            3: True,
            4: True,
            5: True,
            6: True,
            7: True,
            8: False,
            9: True,
            10: True,
        },
        "吉田": {
            1: True,
            2: False,
            3: True,
            4: False,
            5: False,
            6: True,
            7: True,
            8: True,
            9: False,
            10: True,
        },
        "山本": {
            1: True,
            2: True,
            3: True,
            4: True,
            5: True,
            6: True,
            7: True,
            8: False,
            9: True,
            10: True,
        },
        "派遣": {
            1: True,
            2: True,
            3: False,
            4: True,
            5: False,
            6: True,
            7: True,
            8: False,
            9: True,
            10: True,
        },
    }

    # 各役職への適性（サンプルデータ）
    role_compatibility = {
        "齋藤": {"血圧": True, "採血": True, "受付": True},
        "山田": {"血圧": True, "採血": False, "受付": True},
        "和田": {"血圧": False, "採血": True, "受付": True},
        "田中": {"血圧": True, "採血": False, "受付": True},
        "佐藤": {"血圧": True, "採血": True, "受付": True},
        "中村": {"血圧": False, "採血": True, "受付": True},
        "小林": {"血圧": True, "採血": True, "受付": True},
        "加藤": {"血圧": True, "採血": True, "受付": False},
        "吉田": {"血圧": False, "採血": True, "受付": True},
        "山本": {"血圧": True, "採血": True, "受付": True},
        "派遣": {"血圧": False, "採血": True, "受付": False},
    }

    maker = MILPMaker(availability, role_compatibility)

    # 日毎のスケジュール解決
    for day in list(availability.values())[0].keys():
        try:
            schedule = maker.solve_for_day(day)
            print(f"Day {day}:")
            for role, employee in schedule.items():
                print(f"  {role}: {employee}")
        except Exception as e:
            print(f"  {e}")
        print()
