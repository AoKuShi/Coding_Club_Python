def calculate_scores(preferences, groups):
    # 각 학생의 선호 및 비선호 학생 목록을 저장
    scores = [0] * len(preferences)
    
    # 학생이 속한 반을 찾기 위한 딕셔너리
    student_to_group = {}
    for group_id, group in enumerate(groups):
        for student_id in group:
            student_to_group[student_id] = group_id
    
    # 점수 계산
    for student_id, student_pref in enumerate(preferences, start=1):  # 학생 번호 1부터 시작
        print(f"\n학생 {student_id} 점수 계산:")

        # 선호 학생 처리
        preferred_students = []
        disliked_students = []
        
        # 선호도에서 선호 학생과 비선호 학생 구분
        for rank, pref in enumerate(student_pref[:3]):
            target_student = abs(int(pref))  # 선호 학생의 ID는 숫자
            if int(pref) > 0:  # 선호 학생
                preferred_students.append((target_student, rank + 1))
            else:  # 비선호 학생
                disliked_students.append((target_student, rank + 1))
        
        # 선호 학생 처리
        for target_student, rank in preferred_students:
            if target_student == student_id:  # 자기 자신은 제외
                continue
            target_group = student_to_group.get(target_student)  # 선호 학생이 속한 반을 찾기
            if target_group == student_to_group[student_id]:  # 같은 반이면
                if rank == 1:
                    scores[student_id - 1] += 4  # 1순위: 4점 (인덱스는 0부터 시작)
                    print(f"  선호 학생 {target_student} (1순위): 같은 반 -> +4점")
                elif rank == 2:
                    scores[student_id - 1] += 2  # 2순위: 2점
                    print(f"  선호 학생 {target_student} (2순위): 같은 반 -> +2점")
                elif rank == 3:
                    scores[student_id - 1] += 1  # 3순위: 1점
                    print(f"  선호 학생 {target_student} (3순위): 같은 반 -> +1점")

        # 비선호 학생 처리
        for target_student, rank in disliked_students:
            if target_student == student_id:  # 자기 자신은 제외
                continue
            target_group = student_to_group.get(target_student)  # 비선호 학생이 속한 반을 찾기
            if target_group != student_to_group[student_id]:  # 다른 반이면
                if rank == 1:
                    scores[student_id - 1] += 8  # 1순위: 8점
                    print(f"  비선호 학생 {target_student} (1순위): 다른 반 -> +8점")
                elif rank == 2:
                    scores[student_id - 1] += 4  # 2순위: 4점
                    print(f"  비선호 학생 {target_student} (2순위): 다른 반 -> +4점")
                elif rank == 3:
                    scores[student_id - 1] += 2  # 3순위: 2점
                    print(f"  비선호 학생 {target_student} (3순위): 다른 반 -> +2점")

    return scores


# 테스트 데이터
preferences = [
    ['+2', '-4', '-3'],
    ['+1', '-4', '-3'],
    ['+2', '+5', '-4'],
    ['+1', '-5', '-3'],
    ['+4', '+2', '-1']
]

groups = [
    [1, 4, 5],  # 반 1
    [2],         # 반 2
    [3]          # 반 3
]

# 점수 계산
scores = calculate_scores(preferences, groups)
print(f"\n최종 점수: {scores}")
