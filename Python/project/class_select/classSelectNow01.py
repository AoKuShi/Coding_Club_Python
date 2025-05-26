import time

class SchoolClassAssignment:
    def __init__(self, num_students, num_classes, min_students_per_class, max_students_per_class, preferences):
        self.num_students = num_students
        self.num_classes = num_classes
        self.min_students_per_class = min_students_per_class
        self.max_students_per_class = max_students_per_class
        self.preferences = preferences
        self.classes = [[] for _ in range(num_classes)]
        self.all_assignments = []

    def calculate_score(self, assignment):
        total_score = 0
        for cls in assignment:
            for student in cls:
                preferred_students = self.preferences[student]  # student는 1부터 시작
                for idx, preferred_student in enumerate(preferred_students):
                    if preferred_student > 0:  # 긍정적 선호도
                        if preferred_student in cls:
                            if idx == 0:
                                total_score += 4
                            elif idx == 1:
                                total_score += 2
                            elif idx == 2:
                                total_score += 1
                    elif preferred_student < 0:  # 부정적 선호도
                        disliked_student = abs(preferred_student)
                        if disliked_student not in cls:
                            if idx == 0:
                                total_score += 8
                            elif idx == 1:
                                total_score += 4
                            elif idx == 2:
                                total_score += 2
        return total_score

    def is_valid_assignment(self):
        return all(len(cls) >= self.min_students_per_class for cls in self.classes)

    def backtrack(self, student_index):
        if student_index == self.num_students:
            if self.is_valid_assignment():
                current_assignment = [cls[:] for cls in self.classes]
                score = self.calculate_score(current_assignment)
                self.all_assignments.append((score, current_assignment))
            return

        for cls in range(self.num_classes):
            if len(self.classes[cls]) < self.max_students_per_class:
                self.classes[cls].append(student_index + 1)  # 1부터 시작
                self.backtrack(student_index + 1)
                self.classes[cls].pop()

    def assign_students(self):
        self.backtrack(0)  # student_index는 0부터 시작하지만, 실제 학생 인덱스는 1부터 시작

    def get_top_n_assignments(self, n=10):
        self.all_assignments.sort(reverse=True, key=lambda x: x[0])
        max_score = self.all_assignments[0][0]
        top_assignments = [assignment for assignment in self.all_assignments if assignment[0] == max_score]
        remaining_assignments = [assignment for assignment in self.all_assignments if assignment[0] < max_score]
        top_n_additional = remaining_assignments[:n]
        return top_assignments + top_n_additional

    def print_assignments(self, top_n_assignments):
        max_score = top_n_assignments[0][0]
        print(f"최고 점수 {max_score}를 기록한 그룹들:")

        for idx, (score, assignment) in enumerate(top_n_assignments):
            print(f"\n그룹 {idx + 1}: 점수 = {score}")
            for i, students in enumerate(assignment):
                print(f"반 {i + 1}: {students}")


# 테스트
a = 5
b = 3
min_students_per_class = 1
max_students_per_class = 2
n = 5

# 학생들의 선호도 데이터 생성 (1번부터 5번까지)
preferences = {
    1: [2, -4, 3],
    2: [3, 4, -1],
    3: [2, -5, -1],
    4: [-1, 3, 5],
    5: [2, -4, 3]
}

scores = {i: {'positive': 0, 'negative': 0} for i in preferences.keys()}

# 점수 계산
for student, prefs in preferences.items():
    for idx, pref in enumerate(prefs):
        if pref > 0:  # 같이 있고 싶은 학생
            if idx == 0:
                scores[pref]['positive'] += 4  # 1순위
            elif idx == 1:
                scores[pref]['positive'] += 2  # 2순위
            elif idx == 2:
                scores[pref]['positive'] += 1  # 3순위
        elif pref < 0:  # 같이 있고 싶지 않은 학생
            if idx == 0:
                scores[-pref]['negative'] += 8  # 1순위
            elif idx == 1:
                scores[-pref]['negative'] += 4  # 2순위
            elif idx == 2:
                scores[-pref]['negative'] += 2  # 3순위

# 결과 출력
for student, score in scores.items():
    print(f"학생 {student}: +점수 = {score['positive']}, -점수 = {score['negative']}")

print()

start_time = time.time()

assignment = SchoolClassAssignment(a, b, min_students_per_class, max_students_per_class, preferences)
assignment.assign_students()
top_n_assignments = assignment.get_top_n_assignments(n)

end_time = time.time()
execution_time = end_time - start_time

assignment.print_assignments(top_n_assignments)
print(f"\n프로그램 실행 시간: {execution_time:.2f}초")
