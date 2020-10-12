import time
import random

def searchDFS(n):
    print('Dang su dung giai thuat DFS:')
    start_time = time.time()
    #Tao search tree voi tang i la tim kiem vi tri dat con hau cho hang thu i - 1
    Stack = [[-1, -1]]
    while True:
        if len(Stack) == 1 and Stack[0][-1] == n - 1:
            break
        if Stack[-1][-1] < n - 1:
            Stack[-1] = [Stack[-1][0], Stack[-1][1] + 1]
        else:
            Stack = Stack[:-1]
            continue
        if len(Stack) < n + 1:
            nextState = [Stack[-1][-1], -1]
            if isNextStateDFS(Stack, nextState):
                Stack.append(nextState)
            if len(Stack) == n + 1:
                break
        print(Stack)
    print("--- %s seconds ---" % (time.time() - start_time))
    return Stack[1:]

def isNextStateDFS(Stack, state):
    for i in range(1, len(Stack)):
        if (i - 1 + Stack[i][0]) == (len(Stack) - 1 + state[0]) or (i - 1 - Stack[i][0]) == (len(Stack) - 1 - state[0]) or Stack[i][0] == state[0]:
            return False
    return True

def searchBrFS(n):
    print('Dang su dung giai thuat BrFS:')
    start_time = time.time()
    Queue = [[x] for x in range(n)]
    while len(Queue) != 0:
        state = Queue[0]
        Queue = Queue[1:]
        for i in range(n):
            if isNextStateBrFS(state, i):
                state.append(i)
                if len(state) == n:
                    print("--- %s seconds ---" % (time.time() - start_time))
                    return res
                else: Queue.append(state)
                state = state[:-1]

def isNextStateBrFS(state, n):
    for i in range(len(state)):
        if (i + state[i]) == (len(state) + n) or (i - state[i]) == (len(state) - n) or state[i] == n:
            return False
    return True

def searchHeuristic(n):
    start_time = time.time()
    print('Dang su dung giai thuat Heuristic (Hill Climbing):')
    # Khoi tao trang thai ban dau
    state = [0]*n
    for i in range(n):
        state[i] = random.randrange(n)
    arr_h = [cal_h(state, i, state[i]) for i in range(n)]
    check_idx = [0, 0]
    while max(arr_h) != 1:
        max_h = max(arr_h)
        selectRow = arr_h.index(max_h)
        # tim vi tri tot nhat de thay the
        arr_min_h = [cal_h(state, selectRow, col) for col in range(n)]
        min_h = min(arr_min_h)
        selectCol = arr_min_h.index(min_h)
        #trong truong hop vi tri moi la vi tri cu ta se lay random de tao ra trang thai moi

        if state[selectRow] == selectCol or selectCol == check_idx[0]:
            state[random.randrange(n)] = random.randrange(n)
        else:
            check_idx = check_idx[1:] + [selectCol]
            state[selectRow] = selectCol
        arr_h = [cal_h(state, i, state[i]) for i in range(n)]
    print("--- %s seconds ---" % (time.time() - start_time))
    return state

# ham tinh chi phi 1 vi tri trong state (chi phi cang cao, cang de bi tan cong)
def cal_h(state, row, col):
    h = 0
    for i in range(len(state)):
        if (i + state[i]) == (row + col) or (i - state[i]) == (row - col) or state[i] == col:
            h += 1
    return h

def printBanCo(arr):
    for i in range(len(arr)):
        for j in range(arr[i][0]):
            print(' * ', end='')
        print(' Q ', end='')
        for j in range(arr[i][0] + 1, len(arr)):
            print(' * ', end="")
        print()

if __name__ =="__main__":
    n = int(input('Moi nhap so chieu ban co nxn: '))
    while n < 4:
        n = int(input('Moi nhap lai so chieu ban co nxn: '))
    res = searchDFS(n)
    # printBanCo(res)
    # res = searchBrFS(n)
    # printBanCo(res)
    # res = searchHeuristic(n)
    # printBanCo([[idx] for idx in res])
