'''
picross solver


[ ] : checked white
[#] : checked black
 .  : unknown

<< sample problem >>
 .  .  .  .  .  .  .  .  .  .   2 1 3
 .  .  .  .  .  .  .  .  .  .   1 1 2
 .  .  .  .  .  .  .  .  .  .   1 1 2
 .  .  .  .  .  .  .  .  .  .   1 2
 .  .  .  .  .  .  .  .  .  .   2 3
 .  .  .  .  .  .  .  .  .  .   3 4
 .  .  .  .  .  .  .  .  .  .   4 3 1
 .  .  .  .  .  .  .  .  .  .   1 5 1
 .  .  .  .  .  .  .  .  .  .   1 2 2 1
 .  .  .  .  .  .  .  .  .  .   1 2 1 3

 8  1  3  4  1  2  2  1  6  7
 1  3  1     2  1  4  3  1  2  
    1                 2  1   

<< answer of sample problem >>
[#][#][ ][ ][#][ ][ ][#][#][#]  2 1 3
[#][ ][ ][ ][ ][ ][#][ ][#][#]  1 1 2
[#][ ][ ][ ][ ][ ][#][ ][#][#]  1 1 2
[#][ ][ ][ ][ ][ ][ ][ ][#][#]  1 2
[#][#][ ][ ][ ][ ][ ][#][#][#]  2 3
[#][#][#][ ][ ][ ][#][#][#][#]  3 4
[#][#][#][#][ ][#][#][#][ ][#]  4 3 1
[#][ ][#][#][#][#][#][ ][#][ ]  1 5 1
[ ][#][ ][#][#][ ][#][#][ ][#]  1 2 2 1
[#][ ][#][#][ ][#][ ][#][#][#]  1 2 1 3

 8  1  3  4  1  2  2  1  6  7
 1  3  1     2  1  4  3  1  2  
    1                 2  1   
'''

from itertools import combinations
import time
import sys

class Board:

    UNKNOWN = 0
    BLACK   = 1
    WHITE   = 2

    def __init__(self):
        self.problem_rows = []
        self.problem_cols = []
        self.board_rows = []
        self.board_cols = []
        self.num_rows = 0
        self.num_cols = 0

        self.show_each_step = True
        self.print_info_on_load = False
        self.print_step_time = False

    def _read_next_effective_line_from( self, file ):
        while True:
            line = file.readline()
            if not line: return None
            line = line.strip()
            if len(line)==0:    continue
            if line[0]=='\n':   continue
            if line[0]!='#':    return line
        return ''

    def load( self, file_name ):
        try:
            f = open(file_name, 'r', encoding="utf-8")
        except:
            print('Cannot open file %s' % file_name)
            return False

        try:
            line = self._read_next_effective_line_from(f)
            self.num_cols = int(line)
            line = self._read_next_effective_line_from(f)
            self.num_rows = int(line)
            for _ in range(self.num_rows):
                line = self._read_next_effective_line_from(f)
                problem = [int(a) for a in line.split()]
                self.problem_rows.append(problem)
            for _ in range(self.num_cols):
                line = self._read_next_effective_line_from(f)
                problem = [int(a) for a in line.split()]
                self.problem_cols.append(problem)
        except:
            print("Unexpected error:", sys.exc_info()[0])
            print('Format error !')
            return False

        for _ in range(self.num_rows):
            self.board_rows.append( [Board.UNKNOWN]*self.num_cols )

        for _ in range(self.num_cols):
            self.board_cols.append( [Board.UNKNOWN]*self.num_rows )
            
        f.close()

        if self.print_info_on_load:
            print(self.num_cols)
            print(self.num_rows)
            print(self.problem_rows)
            print(self.problem_cols)
            print(self.board_rows)
            print(self.board_cols)
            print('')

        return True

    def _print_row( self, row ):
        ss = ""
        for s in self.board_rows[row]:
            if s==Board.UNKNOWN:  ss += " . " 
            if s==Board.BLACK:    ss += "[#]" 
            if s==Board.WHITE:    ss += "[ ]"
        ss += " " 
        for s in self.problem_rows[row]:
            ss += str(s) + " "
        print(ss)

    def _print_problem_cols( self ):
        count = max( [len(a) for a in self.problem_cols] )
        for r in range(count):
            ss = ''
            for c in range(self.num_cols):
                if r<len(self.problem_cols[c]):
                    ss += '{:2} '.format((self.problem_cols[c])[r])
                else:
                    ss += '   '
            print(ss)

    def print( self ):
        for i in range(self.num_rows):
            self._print_row(i)
        self._print_problem_cols()

    def set( self, x, y, val ):
         self.board_rows[y][x] = val
         self.board_cols[x][y] = val
    
    def get( self, x, y ):
         # return self.board_rows[y][x]
         return self.board_cols[x][y]

    def _get_slice( self, total, slice ):
        '''
        total 을 slice 갯수만큼의 덩어리들로 나누는 방법을 나열한다 (0개는 안됨)
        '''
        ensemble = []
        for a in combinations( range(1,total), slice-1):
            b = list(a)
            c = []
            sum = 0
            for i in b:
                c.append(i-sum)
                sum = i
            c.append(total-sum)
            ensemble.append(c)
        return ensemble

    def _get_slices( self, total_white, num_slice ):
        '''
        공백을 배분하는 가지수를 리턴한다.
        총갯수와 조각 갯수가 주어졌을때 쪼갤 수 있는 경우를 모두 나열
        첫번째와 마지막은 0이 가능하고, 나머지는 1이상이어야 한다.
        ex) 4,3 -> 4개를 3조각으로 나눈다
        ==> 0,1,3  0,2,2  0,3,1  0,4,0  1,1,2  1,2,1  1,3,0  2,1,1  2,2,0  3,1,0  
        '''
        ensemble = []
        if num_slice>2:
            l1 = Board._get_slice( self, total_white, num_slice-2 )
            ensemble.extend([[0]+a+[0] for a in l1]) # 좌우에 0 추가
        l2 = Board._get_slice( self, total_white, num_slice-1 )
        ensemble.extend([[0]+a for a in l2]) # 왼쪽에 0 추가
        ensemble.extend([a+[0] for a in l2]) # 오른쪽에 0 추가
        l3 = Board._get_slice( self, total_white, num_slice-0 )
        ensemble.extend(l3) # 그대로
        return ensemble

    def _get_pattern( self, problem, white_slices ):
        '''
        문제에 공백을 배분하는 가짓수를 배합하여 가능한 패턴을 생성한다
        '''
        #TODO 에러검사 추가!!
        ensemble = []
        for white_slice in white_slices:
            branch = []
            branch += [Board.WHITE]*white_slice[0]
            for b,w in zip(problem,white_slice[1:]):
                branch += [Board.BLACK]*b
                branch += [Board.WHITE]*w
            ensemble.append(branch)
        return ensemble

    DicX = {}
    DicY = {}

    def GetPatternsX( self, x, h, problem ):
        if x in self.DicX:
            return self.DicX.get(x)

        total_black = sum(problem)
        total_white = h-total_black
        num_slice = len(problem)+1

        white_slices = Board._get_slices( self, total_white, num_slice )
        patterns = Board._get_pattern( self, problem, white_slices )

        self.DicX[x] = patterns
        return patterns

    def GetPatternsY( self, y, w, problem ):
        if y in self.DicY:
            return self.DicY.get(y)

        total_black = sum(problem)
        total_white = w-total_black
        num_slice = len(problem)+1

        white_slices = Board._get_slices( self, total_white, num_slice )
        patterns = Board._get_pattern( self, problem, white_slices )

        self.DicY[y] = patterns
        return patterns

    def _filter_patterns_h( self, y, patterns ):
        '''
        y번째줄의 패턴에서 현재 보드와 맞지않는것들을 제거한다.
        '''
        filtered_patterns = []
        for p in patterns:
            add = True
            for x,v in enumerate(p):
                m = Board.get( self, x, y )
                if m != Board.UNKNOWN and v != m:
                    add = False
                    break
            if add:
                filtered_patterns.append(p)
        return filtered_patterns

    def _filter_patterns_v( self, x, patterns ):
        '''
        x번째컬럼의 패턴에서 현재 보드와 맞지않는것들을 제거한다.
        '''
        filtered_patterns = []
        for p in patterns:
            add = True
            for y,v in enumerate(p):
                m = Board.get( self, x, y )
                if m != Board.UNKNOWN and v != m:
                    add = False
                    break
            if add:
                filtered_patterns.append(p)
        return filtered_patterns

    def solve_static( self, x_indices=None, y_indices=None ):
        '''
        가로, 세로 모든 줄과 열을 한번 훑으면서
        보드의 configuration으로부터 바로 유추할 수 있는 칸들을 푼다
        '''

        if self.print_step_time:
            start = time.process_time()

        w = self.num_cols
        h = self.num_rows

        if x_indices==None:
            x_indices=range(w)
        if y_indices==None:
            y_indices=range(h)

        changed_x = set()
        changed_y = set()

        # 가로방향 풀이
        for y in y_indices:
            problem = self.problem_rows[y]
            patterns = Board.GetPatternsY( self, y, w, problem )
            filtered_patterns = Board._filter_patterns_h( self, y, patterns )
            if self.show_each_step:
                print('row',y)
                print(white_slices)
                print(patterns)
                print(filtered_patterns)

            if len(filtered_patterns)<=0: continue
            for x in range(w):
                m = Board.get( self, x, y )
                if m!=Board.UNKNOWN: continue
                b = True
                m = filtered_patterns[0][x]
                for p in filtered_patterns:
                    if p[x]!=m:
                        b = False
                        break
                if b:
                    Board.set( self, x, y, m )
                    changed_x.add(x)
                    changed_y.add(y)

        # 세로방향 풀이
        for x in x_indices:
            problem = self.problem_cols[x]
            patterns = Board.GetPatternsX( self, x, h, problem )
            filtered_patterns = Board._filter_patterns_v( self, x, patterns )
            if self.show_each_step:
                print('row',y)
                print(white_slices)
                print(patterns)
                print(filtered_patterns)

            if len(filtered_patterns)<=0: continue
            for y in range(h):
                m = Board.get( self, x, y )
                if m!=Board.UNKNOWN: continue
                b = True
                m = filtered_patterns[0][y]
                for p in filtered_patterns:
                    if p[y]!=m:
                        b = False
                        break
                if b:
                    Board.set( self, x, y, m )
                    changed_x.add(x)
                    changed_y.add(y)

        if self.print_step_time:
            print( 'time = %5.2f' % (time.process_time()-start) )

        return list(changed_x), list(changed_y)
