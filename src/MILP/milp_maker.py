from pulp import LpProblem, LpVariable, lpSum, LpStatus
from pulp import PULP_CBC_CMD

class ShiftScheduler:
    def __init__(self, employees, roles, availability, role_compatibility):
        self.employees = employees
        self.roles = roles
        self.availability = availability
        self.role_compatibility = role_compatibility

    def solve_for_day(self, day):
        problem = LpProblem(f"ShiftAssignment_Day_{day}", sense=1)
        x = {
            (e, r): LpVariable(f"x_{e}_{day}_{r}", cat="Binary")
            for e in self.employees
            for r in self.roles
        }

        # 制約条件1: 各役職は1人の担当者のみ
        for r in self.roles:
            problem += lpSum(x[(e, r)] for e in self.employees) == 1, f"RoleAssignment_Day_{day}_{r}"

        # 制約条件2: 従業員のシフト可能性に基づく制約
        for e in self.employees:
            for r in self.roles:
                problem += x[(e, r)] <= self.availability[e][day - 1], f"Availability_{e}_{day}_{r}"

        # 制約条件3: 各従業員の役職適性を考慮
        for e in self.employees:
            for r in self.roles:
                problem += x[(e, r)] <= self.role_compatibility[e][r], f"Compatibility_{e}_{day}_{r}"

        # 制約条件4: 各従業員は1日に1つの役職のみ
        for e in self.employees:
            problem += lpSum(x[(e, r)] for r in self.roles) <= 1, f"SingleRoleAssignment_{e}_{day}"

        # 目的関数: 割り当てを最大化
        problem += lpSum(x[(e, r)] for e in self.employees for r in self.roles), f"MaximizeAssignments_Day_{day}"
        
        result = problem.solve(PULP_CBC_CMD(msg=False))

        if result == 1:
            schedule = {r: e for e in self.employees for r in self.roles if x[(e, r)].value() == 1}
            return schedule
        else:
            raise Exception(f"解が見つかりませんでした: Day {day}")

if __name__ == '__main__':
    # データの定義
    employees = ["齋藤", "山田", "和田", "田中", "佐藤", "中村", "小林", "加藤", "吉田", "山本"]
    days = list(range(1, 11))  # 日数 (1〜10)
    roles = ["血圧", "採血", "受付"]

    # シフト可能性（サンプルデータ）
    availability = {
        "齋藤": [1, 0, 1, 1, 1, 1, 0, 1, 1, 1],
        "山田": [0, 1, 1, 1, 1, 0, 1, 1, 1, 1],
        "和田": [1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
        "田中": [1, 1, 0, 1, 0, 1, 1, 1, 1, 0],
        "佐藤": [1, 1, 1, 0, 1, 1, 1, 0, 1, 1],
        "中村": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        "小林": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        "加藤": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        "吉田": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        "山本": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    }

    # 各役職への適性（サンプルデータ）
    role_compatibility = {
        "齋藤": {"血圧": 1, "採血": 1, "受付": 1},
        "山田": {"血圧": 1, "採血": 1, "受付": 1},
        "和田": {"血圧": 1, "採血": 1, "受付": 1},
        "田中": {"血圧": 1, "採血": 1, "受付": 1},
        "佐藤": {"血圧": 1, "採血": 1, "受付": 1},
        "中村": {"血圧": 1, "採血": 1, "受付": 1},
        "小林": {"血圧": 1, "採血": 1, "受付": 1},
        "加藤": {"血圧": 1, "採血": 1, "受付": 1},
        "吉田": {"血圧": 1, "採血": 1, "受付": 1},
        "山本": {"血圧": 1, "採血": 1, "受付": 1}
    }

    scheduler = ShiftScheduler(employees, roles, availability, role_compatibility)

    # 日毎のスケジュール解決
    for day in days:
        print(f"Day {day}:")
        try:
            schedule = scheduler.solve_for_day(day)
            for role, employee in schedule.items():
                print(f"  {role}: {employee}")
        except Exception as e:
            print(f"  {e}")
            
        
