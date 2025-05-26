import random
import time

class SchoolClassAssignment:
    def __init__(self, num_students, num_classes, min_students_per_class, max_students_per_class, preferences):
        self.num_students = num_students
        self.num_classes = num_classes
        self.min_students_per_class = min_students_per_class  # 각 반의 최소 인원 수
        self.max_students_per_class = max_students_per_class  # 각 반의 최대 인원 수
        self.preferences = preferences
        self.top_assignments = []  # 최종 상위 배정 리스트

    def calculate_class_score(self, cls):
        """특정 반의 점수 계산"""
        class_score = 0
        for student in cls:
            preferred_students = self.preferences[student]
            for idx, preferred_student in enumerate(preferred_students):
                if preferred_student in cls:
                    if idx == 0:
                        class_score += 4
                    elif idx == 1:
                        class_score += 2
                    elif idx == 2:
                        class_score += 1
        return class_score

    def calculate_total_score(self, assignment):
        """배정 전체의 점수 계산"""
        return sum(self.calculate_class_score(cls) for cls in assignment)

    def generate_initial_assignments(self):
        """학생을 각 반에 무작위로 배정하여 초기 배정 집합 생성"""
        initial_assignments = []
        for _ in range(10000):  # 초기 10000개의 랜덤 배정 생성
            assignment = [[] for _ in range(self.num_classes)]
            students = list(range(self.num_students))
            random.shuffle(students)

            # 각 반에 최소 인원 수를 먼저 배정
            for cls in range(self.num_classes):
                for _ in range(self.min_students_per_class):
                    if students:
                        student = students.pop()
                        assignment[cls].append(student)

            # 나머지 학생들을 각 반의 최대 인원을 초과하지 않도록 배정
            for student in students:
                # 최대 인원을 넘지 않는 반만 선택
                available_classes = [cls for cls in range(self.num_classes) if len(assignment[cls]) < self.max_students_per_class]
                if available_classes:
                    assigned_class = random.choice(available_classes)
                    assignment[assigned_class].append(student)

            # 모든 반이 최소 인원 이상인 경우에만 추가
            if all(len(cls) >= self.min_students_per_class for cls in assignment):
                initial_assignments.append(assignment)
        return initial_assignments

    def filter_top_assignments(self, assignments, score_type, top_n):
        """특정 점수 타입에서 상위 n개의 배정을 남김"""
        scored_assignments = [(self.calculate_total_score(assignment), assignment) for assignment in assignments]
        scored_assignments.sort(reverse=True, key=lambda x: x[0])
        return [assignment for _, assignment in scored_assignments[:top_n]]

    def assign_students(self):
        # 초기 랜덤 배정 생성
        initial_assignments = self.generate_initial_assignments()
        
        # 단계별 필터링
        # 4점 기준 상위 1000개 필터링
        filtered_assignments = self.filter_top_assignments(initial_assignments, score_type=4, top_n=1000)
        # 2점 기준 상위 500개 필터링
        filtered_assignments = self.filter_top_assignments(filtered_assignments, score_type=2, top_n=500)
        # 1점 기준 상위 100개 필터링
        self.top_assignments = self.filter_top_assignments(filtered_assignments, score_type=1, top_n=100)

    def print_top_assignments(self):
        print(f"상위 100개 배정 결과 (1점 기준 최고점 포함):")
        for idx, assignment in enumerate(self.top_assignments):
            print(f"\n배정 {idx + 1}: 전체 점수 = {self.calculate_total_score(assignment)}")
            for i, cls in enumerate(assignment):
                class_score = self.calculate_class_score(cls)
                print(f"반 {i + 1} (점수: {class_score}): {cls}")

# 학생 수 (a명), 반 수 (b개), 각 반의 최소 및 최대 인원 수
a = 15
b = 5
min_students_per_class = 4  # 각 반의 최소 인원 수
max_students_per_class = 6   # 각 반의 최대 인원 수

# 학생들의 선호도 데이터 생성
preferences = {}
for student in range(a):
    preferred_students = random.sample([i for i in range(a) if i != student], 3)
    preferences[student] = preferred_students

# 프로그램 실행
start_time = time.time()

assignment = SchoolClassAssignment(a, b, min_students_per_class, max_students_per_class, preferences)
assignment.assign_students()
assignment.print_top_assignments()

end_time = time.time()
execution_time = end_time - start_time
print(f"\n프로그램 실행 시간: {execution_time:.2f}초")
