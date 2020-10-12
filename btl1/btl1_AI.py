import time
import random

# def searchDFS(n):
#     print('Dang su dung giai thuat DFS:')
#     start_time = time.time()
#     #Tao search tree voi tang i la tim kiem vi tri dat con hau cho hang thu i - 1
#     Stack = [[-1, -1]]
#     while True:
#         if Stack[-1][-1] < n - 1:
#             Stack[-1] = [Stack[-1][0], Stack[-1][1] + 1]
#         else:
#             Stack = Stack[:-1]
#             continue
#         if len(Stack) < n + 1:
#             nextState = [Stack[-1][-1], -1]
#             if isNextStateDFS(Stack, nextState):
#                 Stack.append(nextState)
#             if len(Stack) == n + 1:
#                 break
#         print(Stack)
#         printBanCo(Stack[1:])
#     print("--- %s seconds ---" % (time.time() - start_time))
#     return Stack[1:]

def searchDFS(n):
    print('Dang su dung giai thuat DFS:')
    start_time = time.time()
    #Tao search tree voi tang i la tim kiem vi tri dat con hau cho hang thu i - 1
    Stack = [[-1, -1]]
    new_flag = 0
    while True:
        if Stack[-1][-1] < n - 1 and Stack[-1][-1] != Stack[-1][0] - 1:
            Stack[-1] = [Stack[-1][0], Stack[-1][1] + 1]
        elif new_flag == 1:
            Stack[-1][-1] = 0
            new_flag = 0
        else:
            Stack = Stack[:-1]
            continue
        if len(Stack) < n + 1:
            nextState = [Stack[-1][-1], Stack[-1][-1] + 1 if Stack[-1][-1] + 1 <= n - 1 else -1]
            if isNextStateDFS(Stack, nextState):
                Stack.append(nextState)
                new_flag = 1
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
    while True:
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

def handle_over100000(n):
    start_time = time.time()
    print('Dang su dung giai thuat Heuristic (Handle duoc N > 100000):')
    r = n % 12
    res = list(range(2, n + 1, 2))
    if r == 3 or r == 9:
        res = res[1:] + [2]
        res = res + list(range(5, n + 1, 2)) + [1, 3]
        print("--- %s seconds ---" % (time.time() - start_time))
        return res
    if r == 8:
        for i in range(3, n + 1, 4):
            res = res + [i, i - 2]
    elif r == 2:
        res = res + [3, 1] + list(range(7, n + 1, 2)) + [5]
    else:
        res = res + list(range(1, n + 1, 2))
    print("--- %s seconds ---" % (time.time() - start_time))
    return [[idx - 1] for idx in res]

def check(res):
    for i in range(len(res)):
        for j in range(len(res)):
            if i != j and ((i + res[i]) == (j + res[j]) or (i - res[i]) == (j - res[j]) or res[i] == res[j]):
                print('Hai vi tri tan cong lan nhau la: Hang thu: ' + str(i) + ', cot thu: ' + str(res[i]) + ' va hang thu: ' + str(j) + ', cot thu: ' + str(res[j]))
                return
    print('OK!')

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
    # for n in range(4, 41):
    #     print('n = ' + str(n))
    #     res = searchDFS(n)
    #     printBanCo(res)
    # res = searchDFS(n)
    # printBanCo(res)
    # res = searchBrFS(n)
    # printBanCo(res)
    res = searchHeuristic(n)
    # print(res)
    # printBanCo([[idx] for idx in res])
    # res = handle_over100000(n)
    # print(res)
    # printBanCo(res)
    # arr = [0,2,1,3]
    printBanCo([[idx] for idx in res])
    check(res)
    res[10], res[15] = res[15], res[10]
    printBanCo([[idx] for idx in res])
    check(res)
