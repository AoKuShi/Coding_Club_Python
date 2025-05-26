def infinite_sequence(formula):
  n = 1
  while True:
    yield eval(formula)
    n += 1

# 사용자 입력 받기
sequence_generator = infinite_sequence(input("틀수열 : "))
#seqB = input("나열식 : ")
count = int(input("틀수열의 길이 : "))
seqA = [next(sequence_generator) for _ in range(count)]

# 수열에서 제거된 요소를 'e'로 만들기
for i in range(count):
  if(seqA[i] != None):
    j = seqA[i]
    k = i + j
    while (k < count):
      seqA[k] = None
      k += j

# 'e'를 제외한 수열을 추출
filtered_seq = [x for x in seqA if x is not None]
print(filtered_seq)

#2**n 일 때, 2**n**2의 규칙성을 갖는다
