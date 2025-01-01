from pulp import LpProblem, LpVariable, lpSum, LpStatus

class ShiftScheduler:
    def __init__(self, employees, days, roles, availability, role_compatibility):
        self.employees = employees
        self.days = days
        self.roles = roles
        self.availability = availability
        self.role_compatibility = role_compatibility
        self.problem = LpProblem("ShiftAssignment", sense=1)
        self.x = {
            (e, d, r): LpVariable(f"x_{e}_{d}_{r}", cat="Binary")
            for e in employees
            for d in days
            for r in roles
        }

    def add_constraints(self):
        # 制約条件1: 各役職は1人の担当者のみ
        for d in self.days:
            for r in self.roles:
                self.problem += lpSum(self.x[(e, d, r)] for e in self.employees) == 1, f"RoleAssignment_{d}_{r}"

        # 制約条件2: 従業員はその日の1つの役職のみを担当
        for e in self.employees:
            for d in self.days:
                self.problem += lpSum(self.x[(e, d, r)] for r in self.roles) <= 1, f"OneRolePerDay_{e}_{d}"

        # 制約条件3: 従業員のシフト可能性に基づく制約
        for e in self.employees:
            for d in self.days:
                for r in self.roles:
                    self.problem += self.x[(e, d, r)] <= self.availability[e][d - 1], f"Availability_{e}_{d}_{r}"

        # 制約条件4: 各従業員の役職適性を考慮
        for e in self.employees:
            for d in self.days:
                for r in self.roles:
                    self.problem += self.x[(e, d, r)] <= self.role_compatibility[e][r], f"Compatibility_{e}_{d}_{r}"

    def set_objective(self):
        # 目的関数: 全体の割り当てを最大化
        self.problem += lpSum(self.x[(e, d, r)] for e in self.employees for d in self.days for r in self.roles), "MaximizeAssignments"

    def solve(self):
        # self.problem.solve()
        result = self.problem.solve()
        if result == 1:
            print("Optimal solution found")
        else:
            raise Exception("解が見つかりませんでした。")
        

    def get_schedule(self):
        schedule = {}
        for d in self.days:
            schedule[d] = {}
            for r in self.roles:
                for e in self.employees:
                    if self.x[(e, d, r)].value() == 1:
                        schedule[d][r] = e
        return schedule

if __name__ == '__main__':
    # データの定義
    employees = ["齋藤", "山田", "和田", "田中", "佐藤"]
    days = list(range(1, 11))  # 日数 (1〜10)
    roles = ["血圧", "採血", "受付"]

    # シフト可能性（サンプルデータ）
    availability = {
        "齋藤": [1, 0, 1, 1, 1, 1, 0, 1, 1, 1],
        "山田": [0, 1, 1, 1, 1, 0, 1, 1, 1, 1],
        "和田": [1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
        "田中": [1, 1, 0, 1, 0, 1, 1, 1, 1, 0],
        "佐藤": [1, 1, 1, 0, 1, 1, 1, 0, 1, 1]
    }

    # 各役職への適性（サンプルデータ）
    role_compatibility = {
        "齋藤": {"血圧": 1, "採血": 1, "受付": 1},
        "山田": {"血圧": 1, "採血": 1, "受付": 1},
        "和田": {"血圧": 1, "採血": 0, "受付": 1},
        "田中": {"血圧": 0, "採血": 1, "受付": 1},
        "佐藤": {"血圧": 1, "採血": 1, "受付": 1}
    }

    # スケジューラの作成と解決
    scheduler = ShiftScheduler(employees, days, roles, availability, role_compatibility)
    scheduler.add_constraints()
    scheduler.set_objective()
    scheduler.solve()

    # 結果の表示
    schedule = scheduler.get_schedule()
    for day, assignments in schedule.items():
        print(f"Day {day}:")
        for role, employee in assignments.items():
            print(f"  {role}: {employee}")
