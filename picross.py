import board


def WaitKey():
    try:
        input("Press enter to continue")
        print('--------')
    except SyntaxError:
        pass



bd = board.Board()
bd.load('board1.txt')
bd.print()
print('------')

w = bd.num_cols
h = bd.num_rows
print('board size =',w,'x',h)

while(True):
    bd.solve_static()
    bd.print()
    WaitKey()

print('Done....................')



# TODO 테스트문제2 안풀리는것 분석
# ==> 이건 탐색 필요하다
#     탐색에서는 해결불가 판단이 필요하다

# TODO 클래스로 함수들 옮기고 정리

# TODO 종료검사 방법 추가

# TODO 불필요한 계산 하지 않도록
# 1. 이미 채워진 칸은 패스
# 2. 
# 3. 테두리에 블랙이 있으면, 연장해서 X까지 채워넣기. (중복안되도록 미리 검사))
#    ==> 이건 반드시 필요한가?? 안필요할지도

# TODO 계속될 테스트 용이하게 하기 위해 비전 인식 추가 (또는 문제 자동 생성)

# TODO 찍어야 되는 경우 해결 위해 해공간 탐색 추가

# TODO 안풀리는 경우, 다중해 경우 판별 추가 (꼭 해야함??)
# 그런데, 안풀리는 경우가 존재하나? (가로/세로 문제합이 같은 경우 중에)

