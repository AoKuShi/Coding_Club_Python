import random
import time

class SchoolClassAssignment:
    def __init__(self, num_students, num_classes, min_students_per_class, max_students_per_class, preferences):
        self.num_students = num_students
        self.num_classes = num_classes
        self.min_students_per_class = min_students_per_class  # 각 반의 최소 인원 수
        self.max_students_per_class = max_students_per_class  # 각 반의 최대 인원 수
        self.preferences = preferences
        self.classes = [[] for _ in range(num_classes)]  # 각 반을 초기화
        self.all_assignments = []  # 모든 배정 결과를 저장할 리스트

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
        """ 각 반의 인원 수가 최소 인원 수를 충족하는지 확인 """
        return all(len(cls) >= self.min_students_per_class for cls in self.classes)

    def backtrack(self, student_index):
        if student_index == self.num_students:
            if self.is_valid_assignment():  # 최소 인원 수 조건 체크
                current_assignment = [cls[:] for cls in self.classes]
                score = self.calculate_score(current_assignment)
                self.all_assignments.append((score, current_assignment))
            return

        for cls in range(self.num_classes):
            if len(self.classes[cls]) < self.max_students_per_class:  # 인원 수 제한 체크
                self.classes[cls].append(student_index)  # 학생을 현재 반에 배정
                self.backtrack(student_index + 1)  # 다음 학생으로 진행
                self.classes[cls].pop()  # 학생을 현재 반에서 제거

    def assign_students(self):
        self.backtrack(0)  # 학생 인덱스를 0으로 시작하여 배정 시작

    def get_top_n_assignments(self, n=10):
        # 점수 순으로 정렬 후 상위 n+1개의 배정 결과 반환
        self.all_assignments.sort(reverse=True, key=lambda x: x[0])
        
        # 최고 점수를 가진 그룹들을 먼저 필터링
        max_score = self.all_assignments[0][0]
        top_assignments = [assignment for assignment in self.all_assignments if assignment[0] == max_score]

        # n개의 추가 그룹을 추출
        remaining_assignments = [assignment for assignment in self.all_assignments if assignment[0] < max_score]
        top_n_additional = remaining_assignments[:n]

        # 상위 그룹에 추가 그룹을 합쳐서 반환
        return top_assignments + top_n_additional

    def print_assignments(self, top_n_assignments):
        max_score = top_n_assignments[0][0]
        print(f"최고 점수 {max_score}를 기록한 그룹들:")

        for idx, (score, assignment) in enumerate(top_n_assignments):
            print(f"\n그룹 {idx + 1}: 점수 = {score}")
            for i, students in enumerate(assignment):
                print(f"반 {i + 1}: {students}")

# 학생 수 (a명), 반 수 (b개), 각 반의 최소 및 최대 인원 수
a = 5
b = 3
min_students_per_class = 1  # 각 반의 최소 인원 수
max_students_per_class = 3   # 각 반의 최대 인원 수
n = 5  # 추가로 상위 n개의 배정을 출력

# 학생들의 선호도 데이터 생성
preferences = {}
for student in range(a):
    preferred_students = random.sample([i for i in range(a) if i != student], b)
    preferences[student] = preferred_students

# 프로그램 실행
start_time = time.time()

assignment = SchoolClassAssignment(a, b, min_students_per_class, max_students_per_class, preferences)
assignment.assign_students()
top_n_assignments = assignment.get_top_n_assignments(n)

end_time = time.time()
execution_time = end_time - start_time

assignment.print_assignments(top_n_assignments)
print(f"\n프로그램 실행 시간: {execution_time:.2f}초")
