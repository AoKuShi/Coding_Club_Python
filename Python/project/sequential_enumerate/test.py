def infinite_sequence(formula):
    n = 0
    while True:
        yield eval(formula)
        n += 1

# 사용자 입력 받기
user_formula = input("수열을 정의하는 식을 입력하세요 (예: 2*n - 1): ")

# 무한한 수열 생성기
sequence_generator = infinite_sequence(user_formula)

print("무한한 수열을 생성합니다. 'q'를 입력하면 종료됩니다.")
while True:
    user_input = input("다음 요소를 원하시면 엔터를 누르세요 (종료하려면 'q' 입력): ")
    if user_input.lower() == 'q':
        break
    else:
        print("생성된 요소:", next(sequence_generator))