import random
import time
from pulp import LpProblem, LpVariable, LpMaximize, lpSum

# 학생들을 반에 배정하는 기본 클래스
class SchoolClassAssignment:
    def __init__(self, num_students, num_classes, min_students_per_class, max_students_per_class, preferences):
        self.num_students = num_students
        self.num_classes = num_classes
        self.min_students_per_class = min_students_per_class
        self.max_students_per_class = max_students_per_class
        self.preferences = preferences
        self.classes = [[] for _ in range(num_classes)]
        self.best_score = float('-inf')
        self.best_assignment = None

    def calculate_score(self, assignment):
        total_score = 0
        for cls in assignment:
            for student in cls:
                preferred_students = self.preferences[student]
                for idx, preferred_student in enumerate(preferred_students):
                    if preferred_student in cls:
                        if idx == 0:
                            total_score += 4
                        elif idx == 1:
                            total_score += 2
                        elif idx == 2:
                            total_score += 1
        return total_score

    def is_valid_assignment(self):
        return all(len(cls) >= self.min_students_per_class for cls in self.classes)

    def backtrack(self, student_index):
        if student_index == self.num_students:
            if self.is_valid_assignment():
                current_score = self.calculate_score(self.classes)
                if current_score > self.best_score:
                    self.best_score = current_score
                    self.best_assignment = [cls[:] for cls in self.classes]
            return

        for cls in range(self.num_classes):
            if len(self.classes[cls]) < self.max_students_per_class:
                self.classes[cls].append(student_index)
                self.backtrack(student_index + 1)
                self.classes[cls].pop()

    def assign_students(self):
        self.backtrack(0)

# 정수 선형 프로그래밍을 사용한 클래스
class ILPSchoolClassAssignment:
    def __init__(self, num_students, num_classes, min_students_per_class, max_students_per_class, preferences):
        self.num_students = num_students
        self.num_classes = num_classes
        self.preferences = preferences
        self.min_students_per_class = min_students_per_class
        self.max_students_per_class = max_students_per_class

    def assign_students(self):
        problem = LpProblem("ClassAssignment", LpMaximize)

        # 변수 생성
        x = LpVariable.dicts("student_class", (range(self.num_students), range(self.num_classes)), 0, 1, cat='Binary')

        # 목적 함수 정의
        problem += lpSum(x[s][c] * self.get_preference_score(s, c) for s in range(self.num_students) for c in range(self.num_classes))

        # 제약 조건 정의
        for c in range(self.num_classes):
            problem += lpSum(x[s][c] for s in range(self.num_students)) >= self.min_students_per_class
            problem += lpSum(x[s][c] for s in range(self.num_students)) <= self.max_students_per_class

        problem.solve()

        # 결과 출력
        for s in range(self.num_students):
            for c in range(self.num_classes):
                if x[s][c].varValue == 1:
                    print(f"학생 {s}는 반 {c + 1}에 배정되었습니다.")

    def get_preference_score(self, student, class_id):
        # 선호도를 바탕으로 점수 계산
        return random.randint(1, 10)  # 이 부분을 수정하여 실제 선호도 계산 로직 추가

# 유전 알고리즘을 사용한 클래스
class GeneticAlgorithmSchoolClassAssignment:
    def __init__(self, num_students, num_classes, preferences):
        self.num_students = num_students
        self.num_classes = num_classes
        self.preferences = preferences

    def generate_initial_population(self, size):
        return [self.generate_random_assignment() for _ in range(size)]

    def generate_random_assignment(self):
        assignment = [[] for _ in range(self.num_classes)]
        students = list(range(self.num_students))
        random.shuffle(students)
        for i, student in enumerate(students):
            assignment[i % self.num_classes].append(student)
        return assignment

    def fitness(self, assignment):
        return self.calculate_score(assignment)

    def calculate_score(self, assignment):
        return sum([len(cls) for cls in assignment])  # 단순화된 점수 계산

    def assign_students(self):
        population = self.generate_initial_population(100)
        for generation in range(100):
            population = self.evolve(population)

    def evolve(self, population):
        # 적합도 기반으로 새로운 세대 생성
        return population  # 이 부분에 유전 알고리즘 로직 추가

# 분할 정복을 사용한 클래스
class DivideAndConquerSchoolClassAssignment:
    def __init__(self, num_students, preferences):
        self.num_students = num_students
        self.preferences = preferences

    def divide_and_conquer(self, students):
        if len(students) <= 5:
            return self.base_case_assignment(students)

        mid = len(students) // 2
        left_assignment = self.divide_and_conquer(students[:mid])
        right_assignment = self.divide_and_conquer(students[mid:])
        
        return self.combine_assignments(left_assignment, right_assignment)

    def base_case_assignment(self, students):
        # 기저 사례에서의 배정 방법
        return [[student for student in students]]

    def combine_assignments(self, left, right):
        return left + right

# 메인 프로그램 실행
def main():
    a = 15  # 학생 수
    b = 3   # 반 수
    min_students_per_class = 4  # 각 반의 최소 인원 수
    max_students_per_class = 6   # 각 반의 최대 인원 수

    # 학생들의 선호도 데이터 생성
    preferences = {}
    for student in range(a):
        preferred_students = random.sample([i for i in range(a) if i != student], b)
        preferences[student] = preferred_students

    # 백트래킹 방법 실행
    start_time = time.time()
    assignment = SchoolClassAssignment(a, b, min_students_per_class, max_students_per_class, preferences)
    assignment.assign_students()
    print(f"백트래킹 방법 - 최고 점수: {assignment.best_score}, 배정: {assignment.best_assignment}")
    print(f"실행 시간: {time.time() - start_time:.2f}초")

    # 정수 선형 프로그래밍 방법 실행
    start_time = time.time()
    ilp_assignment = ILPSchoolClassAssignment(a, b, min_students_per_class, max_students_per_class, preferences)
    ilp_assignment.assign_students()
    print(f"정수 선형 프로그래밍 방법 - 실행 시간: {time.time() - start_time:.2f}초")

    # 유전 알고리즘 방법 실행
    start_time = time.time()
    ga_assignment = GeneticAlgorithmSchoolClassAssignment(a, b, preferences)
    ga_assignment.assign_students()
    print(f"유전 알고리즘 방법 - 실행 시간: {time.time() - start_time:.2f}초")

    # 분할 정복 방법 실행
    start_time = time.time()
    divide_conquer_assignment = DivideAndConquerSchoolClassAssignment(a, preferences)
    result = divide_conquer_assignment.divide_and_conquer(list(range(a)))
    print(f"분할 정복 방법 - 결과: {result}, 실행 시간: {time.time() - start_time:.2f}초")

if __name__ == "__main__":
    main()
