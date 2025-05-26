preferences = {
    1: [2, -4, 3],
    2: [3, 4, -1],
    3: [2, -5, -1],
    4: [-1, 3, 5],
    5: [2, -4, 3]
}

# 점수 초기화
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
