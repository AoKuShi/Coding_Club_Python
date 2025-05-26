import random
import time
from heapq import nlargest

class SchoolClassAssignment:
    def __init__(self, num_students, num_classes, min_students_per_class, max_students_per_class, preferences):
        self.num_students = num_students
        self.num_classes = num_classes
        self.min_students_per_class = min_students_per_class
        self.max_students_per_class = max_students_per_class
        self.preferences = preferences  # 각 학생의 선호 및 비선호 학생 목록
        self.best_assignments = []

    def calculate_score(self, assignment):
        total_score = 0
        # 각 반에 배정된 학생들을 기준으로 점수 계산
        for cls in assignment:
            for student in cls:
                preferred_students = self.preferences[student]['preferred']
                non_preferred_students = self.preferences[student]['non_preferred']
                
                # 선호 학생 점수 추가 (같은 반에 있을 때)
                for idx, preferred_student in enumerate(preferred_students):
                    if preferred_student in cls:  # 선호 학생이 같은 반에 있으면
                        total_score += 4 - idx * 2  # 1순위 4점, 2순위 2점, 3순위 1점
                
                # 비선호 학생 점수 추가 (다른 반에 있을 때)
                for idx, non_preferred_student in enumerate(non_preferred_students):
                    # 비선호 학생이 다른 반에 있을 때 점수 추가
                    if all(non_preferred_student not in other_cls for other_cls in assignment if other_cls != cls):
                        total_score += 8 - idx * 4  # 1순위 8점, 2순위 4점, 3순위 2점

        return total_score

    def is_valid_assignment(self, assignment):
        """각 반의 인원 수가 최소 인원 수와 최대 인원 수 조건을 만족하는지 확인"""
        return all(self.min_students_per_class <= len(cls) <= self.max_students_per_class for cls in assignment)

    def assign_students(self, assignment, student_index=1):
        if student_index > self.num_students:
            if self.is_valid_assignment(assignment):  # 모든 반의 인원 조건 확인
                score = self.calculate_score(assignment)
                sorted_assignment = sorted([sorted(cls) for cls in assignment])  # 중복 체크를 위해 정렬
                if sorted_assignment not in [sorted([sorted(c) for c in a[1]]) for a in self.best_assignments]:
                    self.best_assignments.append((score, sorted_assignment))
            return

        # 학생을 각 반에 배정하며 점수를 계산
        for cls in assignment:
            if len(cls) < self.max_students_per_class:
                cls.append(student_index)
                self.assign_students(assignment, student_index + 1)
                cls.pop()

    def find_optimal_assignments(self, n=10):
        # 초기 빈 반들로 시작
        assignment = [[] for _ in range(self.num_classes)]
        self.assign_students(assignment)
        
        # 상위 n개의 배정 결과를 점수 기준으로 가져오기
        return nlargest(n, self.best_assignments, key=lambda x: x[0])

    def print_assignments(self, top_n_assignments):
        max_score = top_n_assignments[0][0]
        print(f"최고 점수 {max_score}를 기록한 그룹들:")

        for idx, (score, assignment) in enumerate(top_n_assignments):
            print(f"\n그룹 {idx + 1}: 점수 = {score}")
            for i, students in enumerate(assignment):
                print(f"반 {i + 1}: {students}")

# 테스트 데이터 설정
a = 5  # 학생 수 (1부터 5까지)
b = 3  # 반 수
min_students_per_class = 1  # 각 반의 최소 인원 수
max_students_per_class = 3  # 각 반의 최대 인원 수
n = 10  # 상위 n개의 배정을 출력할 갯수

# 학생 선호도 데이터 (학생 번호를 1~5로 수정)
preferences = {
    1: {'preferred': [2], 'non_preferred': [4, 3]},
    2: {'preferred': [1], 'non_preferred': [4, 3]},
    3: {'preferred': [2, 5], 'non_preferred': [4]},
    4: {'preferred': [1], 'non_preferred': [5, 3]},
    5: {'preferred': [4, 2], 'non_preferred': [1]}
}

# 생성된 선호도 데이터 출력
print("학생별 선호도 데이터:")
for student, pref in preferences.items():
    formatted_preferences = []
    for s in pref['preferred']:
        formatted_preferences.append(f"+{s}")
    for s in pref['non_preferred']:
        formatted_preferences.append(f"-{s}")
    print(f"학생 {student}: {formatted_preferences}")

# 프로그램 실행
start_time = time.time()

assignment = SchoolClassAssignment(a, b, min_students_per_class, max_students_per_class, preferences)
top_n_assignments = assignment.find_optimal_assignments(n)

end_time = time.time()
execution_time = end_time - start_time

assignment.print_assignments(top_n_assignments)
print(f"\n프로그램 실행 시간: {execution_time:.2f}초")
