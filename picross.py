import os
import board




def MoveToScriptPath():
    full_path = os.path.realpath(__file__)
    dir_name = os.path.dirname(full_path)
    os.chdir(dir_name)

def WaitKey():
    data = ''
    try:
        data = input("Press enter to continue")
    except SyntaxError:
        pass
    return data





MoveToScriptPath()
bd = board.Board()
if not bd.load('board1.txt'):
    print('Failed to load board !!!')
    exit(-1)
bd.show_each_step = False
bd.print_info_on_load = False
bd.print_step_time = True

print('board size =', bd.num_cols,'x',bd.num_rows)
bd.print()


dx,dy = range(bd.num_cols),range(bd.num_rows)
while(True):
    print('solve for ',dx,dy)
    if len(dx)+len(dy) <= 0:
        break
    # key = WaitKey()
    # if key == 'q':
    #     break
    dx,dy = bd.solve_static(dx,dy)
    print('------')
    bd.print()

print('Done....................')






# TODO 불필요한 계산 하지 않도록
# - 이미 채워진 칸은 패스 (UNKNOWN에 대해서만 처리하도록)
# - 테두리에 블랙이 있으면, 연장해서 X까지 채워넣기. (중복안되도록 미리 검사))
#    ==> 이건 반드시 필요한가?? 안필요할지도

# TODO s잘못된 경우 판별 로직 추가

# TODO 찍어야 되는 경우 해결 위해 해공간 탐색 추가
# ==> 잘못된 경우 판별 가능해야 한다.

# TODO 안풀리는 문제, 다중해 문제 판별 추가 (꼭 해야함??)
# 그런데, 안풀리는 문제가 존재하나? (가로/세로 문제합이 같은 경우 중에)

