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
# -----------------------------------------------------------searchBrFS--------------------------------------------------------------
#Mo phong giai thuat:
#Dung Queue de luu tru cac trang thai cua cac buoc duyet tim kiem

#Trang thai luu trong list state voi: 
#chi so cua list tuong ung voi vi tri cot cua con hau
#gia tri theo tung chi muc trong list tuong ung voi vi tri dong cua con hau
#=> vi tri cua con hau: [cot, dong] tuong ung [index, state[index]]

#Trang thai muc tieu: list day du n cac vi tri dong cua con hau sao cho cac con hau khong
# cung hang, cot, duong cheo

#Genarate ra cac trang thai:
#Buoc Khoi tao trang thai: cac trang thai la cac dong cua ban co, se luu trong Queue
#Tiep theo: Lay tung trang thai trong Queue ra de tim kiem them trang thai tiep theo. 
#Dung ham isNextStateBrFS de kiem tra trang thai tiep theo co hop le khong
#Neu hop le thi them trang thai vao Queue, neu khong hop le thi bo qua
#Va tiep tuc tim kiem cac trang thai 
#Lap lai qua trinh tren den khi tim duoc trang thai co du so luong con hau thi dung

def searchBrFS(n):
    print('Dang su dung giai thuat BrFS:')
    start_time = time.time()
    #Khoi tao Queue: luu tru cac trang thai o buoc tim kiem dau tien
    Queue = [[x] for x in range(n)]
    #G
    while True:
        state = Queue[0]
        Queue = Queue[1:]
        for i in range(n):
            if isNextStateBrFS(state, i):
                state.append(i)
                if len(state) == n:
                    print("--- %s seconds ---" % (time.time() - start_time))
                    print(state)
                    return state
                else: Queue.append(state)
                state = state[:-1]
        print(Queue)

#Kiem tra trang thai tiep theo co hop le hay khong: 
#khong nam tren cung duong cheo hoac cung cot voi cac trang thai da co
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
    res = searchBrFS(n)
    # printBanCo(res)
    # res = searchHeuristic(n)
    # print(res)
    # printBanCo([[idx] for idx in res])
    # res = handle_over100000(n)
    # print(res)
    # printBanCo(res)
    # arr = [0,2,1,3]
    # printBanCo([[idx] for idx in res])
    # check(res)
    # res[10], res[15] = res[15], res[10]
    # printBanCo([[idx] for idx in res])
    # check(res)
