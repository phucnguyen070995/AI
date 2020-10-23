import time
import random

# -----------------------------------------------------------searchDFS--------------------------------------------------------------
def searchDFS(n):
    print('Dang su dung giai thuat DFS:')
    start_time = time.time()
    #Tao search tree voi tang i la tim kiem vi tri dat con hau cho hang thu i - 1
    Stack = [[-1, -1]]
    new_flag = 0
    while True:
        if Stack[-1][-1] < n - 1 and Stack[-1][-1] != Stack[-1][0] - 3:
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
    print("--- %s seconds ---" % (time.time() - start_time))
    return [row[0] for row in Stack[1:]]

def isNextStateDFS(Stack, state):
    for i in range(1, len(Stack)):
        if Stack[i][0] == state[0] or (i - 1 + Stack[i][0]) == (len(Stack) - 1 + state[0]) or (i - 1 - Stack[i][0]) == (len(Stack) - 1 - state[0]):
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
    Queue = [[x] for x in range(n)]
    while True:
        state = Queue[0]
        Queue = Queue[1:]
        for i in range(n):
            if isNextStateBrFS(state, i):
                state.append(i)
                if len(state) == n:
                    print("--- %s seconds ---" % (time.time() - start_time))
                    return state
                else: Queue.append(state)
                state = state[:-1]

def isNextStateBrFS(state, n):
    for i in range(len(state)):
        if (i + state[i]) == (len(state) + n) or (i - state[i]) == (len(state) - n) or state[i] == n:
            return False
    return True

# -----------------------------------------------------------searchHeuristic--------------------------------------------------------------
def searchHeuristic(n):
    start_time = time.time()
    print('Dang su dung giai thuat Heuristic (Hill Climbing):')
    # Khoi tao trang thai ban dau
    state = [random.randrange(n) for _ in range(n)]
    # arr_h mang gia tri dinh gia cho moi con hau
    arr_h = [cal_h(state, i, state[i]) for i in range(n)]
    #check_idx dung de phat hien dang o truong hop toi uu o dinh cuc bo, 2 vi tri cot co gia tri luong gia bang nhau se chuyen qua lai, tao vong lap vo tan
    check_idx = [0, 0]
    # max(arr_h) == 1 luc nay khong co con hau nao tan cong duoc lan nhau, ket thuc giai thuat
    while max(arr_h) != 1:
        max_h = max(arr_h)
        # chon con hau bi tan cong nhieu nhat, co ham dinh gia cao nhat
        selectRow = arr_h.index(max_h)
        # arr_min_h mang gia tri dinh gia cho cac o trong cung hang de tim vi tri moi cho con hau
        arr_min_h = [cal_h(state, selectRow, col) for col in range(n)]
        # tim vi tri tot nhat de thay the, vi tri tren cung hang co ham dinh gia thap nhat (it bi tan cong nhat de chuyen con hau toi vi tri moi nay)
        min_h = min(arr_min_h)
        # cot co ham dinh gia thap nhat
        selectCol = arr_min_h.index(min_h)
        #trong truong hop vi tri moi la vi tri cu ta se lay random de tao ra trang thai moi
        if state[selectRow] == selectCol or selectCol == check_idx[0]:
            state[random.randrange(n)] = random.randrange(n)
        # cap nhat lai mang check_idx, dong thoi cap nhat gia tri moi cho quan hau
        else:
            check_idx = check_idx[1:] + [selectCol]
            state[selectRow] = selectCol
        # chuan bi mang dinh gia arr_h cho vong lap tiep theo
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

# -----------------------------------------------------------handle_over100000--------------------------------------------------------------
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
    return res

# -----------------------------------------------------------check_banco_isvalid--------------------------------------------------------------
def check(res):
    for i in range(len(res)):
        for j in range(len(res)):
            if i != j and ((i + res[i]) == (j + res[j]) or (i - res[i]) == (j - res[j]) or res[i] == res[j]):
                print('Hai vi tri tan cong lan nhau la: Hang thu: ' + str(i) + ', cot thu: ' + str(res[i]) + ' va hang thu: ' + str(j) + ', cot thu: ' + str(res[j]))
                return
    print('OK!')

# -----------------------------------------------------------printBanCo--------------------------------------------------------------
def printBanCo(arr):
    for i in range(len(arr)):
        for j in range(arr[i]):
            print(' * ', end='')
        print(' Q ', end='')
        for j in range(arr[i] + 1, len(arr)):
            print(' * ', end="")
        print()

# -----------------------------------------------------------__main__--------------------------------------------------------------
if __name__ =="__main__":
    while True:
        print('Chon giai thuat:')
        print('1: Giai thuat DFS (n < 41, neu n > 40 thoi gian chay > 1 phut)')
        print('2: Giai thuat BrFS (n < 12, neu n > 11 thoi gian chay > 1 phut))')
        print('3: Giai thuat Heuristic (Hill Climbing) (n < 150 de chay time <4 phut)')
        print('4: Giai thuat co the giai quyet ban co kich thuoc lon (n tuy y)')
        print('5: THOAT!')
        choice = int(input('Lua chon giai thuat: '))
        if choice == 5:
            break
        while choice < 1 or choice > 5:
            choice = int(input('Khong co tuy chon nay, lua chon giai thuat: '))
        n = int(input('Moi nhap so chieu ban co nxn: '))
        while n < 4:
            n = int(input('Moi nhap lai so chieu ban co nxn: '))
        if choice == 1:
            res = searchDFS(n)
            printBanCo(res)
            check(res)
        elif choice == 2:
            res = searchBrFS(n)
            printBanCo(res)
            check(res)
        elif choice == 3:
            res = searchHeuristic(n)
            printBanCo(res)
            check(res)
        elif choice == 4:
            res = handle_over100000(n)
            printBanCo(res)
            check(res)
        else:
            print('Khong co tuy chon nay!')
