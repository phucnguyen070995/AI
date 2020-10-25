import time
import random as rd
from numpy import random
import numpy as np
from functools import reduce

#Code co su dung numpy. De chay duoc code can phai cai numpy cho bai search 100.000 queens su dung herictic

# -----------------------------------------------------------searchDFS--------------------------------------------------------------
#Mo phong giai thuat:
#Dung Stack de luu tru cac trang thai cua cac buoc duyet tim kiem

# Data luu vao stack nhu sau:
# - Luu tung cap gia tri [a,b]
# - Thu tu cua cap gia tri trong danh sach cho ta biet vi tri theo hang cua con hau
# - Gia tri b trong cap gia tri [a, b] cho ta biet vi tri theo hang cua con hau hien tai
# - Gia tri a trong cap gia tri [a, b] luu giu trang thai truoc do de thuc hien quay lui
# - Gia tri bat dau tu 0, nen 4 con hau duoc goi tuong ung la hau[0], hau[1], hau[2] va hau[3]. 
# - Luu y: Gia tri hang 0 cot 0 se la goc tren ben trai cua ban co
# - Vi du neu Stack co gia tri nhu sau: Stack:  [[-1, 1], [1, 2]] ==> Ban co da dat 2 con hau, con hau [0] o cot [1] va con hau [1] o cot [2]

# Trang thai khoi dau: Stack:  [[-1, -1]] ==> Chua co con hau nao tren ban co
# Buoc di:
#     - Neu so quan hau < n: 
#         Lan luot chon gia tri va dat cac con hau vao stack theo quy tac:
#             Neu khong vi pham (dung ham check isNextStateDFS) thi chap nhan vi tri con hau hien tai va cho vao Stack
#             Nguoc lai: loai phan tu khoi Stack (quay lui)
#     - Lap lai cho den khi so quan hau = n
#         Neu toan bo ban co khong vi pham: Xuat ket qua va dung chuong trinh
#         Nguoc lai: loai phan tu khoi Stack (quay lui)
#     - Thuc hien cho den khi tim duoc 1 ban co phu hop yeu cau
# Trang thai ket thuc: Stack co cac con hau thoa man yeu cau

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
    state = [rd.randrange(n) for _ in range(n)]
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
            state[rd.randrange(n)] = rd.randrange(n)
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
# Y tuong: neu ta xep con hau so le theo kieu bac thang thi cac con hau se khong the tan cong lan nhau. 
# Vi du:  (n=8)
# * * * Q * * * *
# * * * * * * Q *
# * * Q * * * * *
# * * * * * * * Q
# * Q * * * * * *
# * * * * Q * * *
# Q * * * * * * *
# * * * * * Q * *
# ==> Nhu vay ta hoan toan co the tim duoc mot cach giai voi N bat ky bang cach dat so le nhu the nay

# Giai thuat Cho n con hau:
# - Chia n cho 12 lay so du r. (r= 8 voi bai toan tam quan hau).
# - Viet lan luot cac so chan tu 2 den n.
# - Neu so du r la 3 hoac 9, chuyen 2 xuong cuoi danh sach.
# - Bo sung lan luot cac so le tu 1 den n vao cuoi danh sach, nhung neu r la 8, doi cho tung cap nghia la duoc 3, 1, 7, 5, 11, 9, ….
# - Neu r = 2, doi cho 1 va 3, sau do chuyen 5 xuong cuoi danh sach.
# - Neu r = 3 hoac 9, chuyen 1 va 3 xuong cuoi danh sach.
# - Lay danh sach tren lam danh sach chi so cot, ghep vao danh sach chi so dong theo thu tu tu nhien ta duoc mot loi giai cua bai toan.
# Ghi chu: ban co co the xoay nen co the viet code theo nhieu cach, nhung van tren nguyen tac dat con hau so le voi nhau!

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
    return [col - 1 for col in res]

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


# -----------------------------------------------------------herictic resolve >= 100.000 queens --------------------------------------------------------------

#Giai thuat tim kiem dua tren a gradient-base heuristic

#Muc tieu: Dat cac con hau tren ban co sao cho khong cung dong, cot, duong cheo de khong tan cong lan nhau
#Thong tin can luu: vi tri tung con hau (cot, dong tuong ung tren ban co)

#Ta se chon list de luu cac thong tin voi cu the nhu sau:
# Dong: la index cua list
# Cot: gia tri cua tung phan tu trong list, tuong ung voi tung index
# Khoi tao gia tri cho list cac con hau (cot): Ta khoi tao random cac gia tri hoan vi tu 0 den numberOfQueen - 1 (nuberOfQueen: so luong con hau tren ban co)
# Voi cac khoi tao tren: tai bat ky vi tri nao deu dam bao cac con hau khong bi tan cong theo cot (vi cac gia tri random hoan vi deu khau nhau => cac cot deu khac nhau)
#va khong bi tan cong theo dong (vi dong luu theo index ma index trong list khong the trung nhau)
#=> Vi vay Van de con lai ta phai giai quyet xung dot o cac duong cheo.


#Ta co 2 loai duong cheo tren ban co:
# Duong cheo duong (positiveDiagonal): Tong dong (index) + cot (value tai index) bang nhau neu cung nam tren 1 duong cheo duong 
#dong (index) + cot (value tai index) chay tu 0 den 2n-2

# Duong cheo am (negativeDiagonal): dong (index) - cot (value tai index) bang nhau neu cung nam tren 1 duong cheo am
#dong (index) - cot (value tai index) chay tu -(n-1) den (n-1)

#Voi n-queens ta co 2n-1 duong cheo duong va 2n - 1 duong cheo am
#Vi vay ta tao ra 2 list de luu so luong cac con hau tren cac dong cheo voi index la hang so (tong hoac hieu cua dong (index), cot (value tai index)) tuong ung tung duong cheo

#So luong con hau tan cong (collisions) tren tung duong cheo co k con hau se la k-1 collisions

#Ta su dung a local search de tim kiem cac con hau bi tan cong va dung ham heuristic de tinh toan co nen swap hay khong

#A gradient-based heuristic: Muc dich chinh o day la de swap 2 con hau sao cho so luong con hau bi tan cong (collisions) giam sau khi swap
#Neu sau khi swap collisions giao thi swap con khong thi bo qua, tiep tuc tim kiem cap tot hon de swap

#Thuc hien thao tac tren den khi collisions = 0 thi return vi tri cac con hau
#Neu thuc hien het vong lap for nhung van khong ket qua thi quay lai buoc init random moi vi tri con hau va lap lai qua tinh tim kiem, swap nhu tren.

#Vi 1 con hau anh huong den 2 duong cheo, o day minh swap 2 con hau nen anh huong den 4 duong cheo tai vi tri cu va 4 duong cheo tai vi tri moi
# => anh huong den 8 duong cheo => ta phai check so luong collisions truoc va sau khi swap cua 8 duong cheo
#Neu swap thi tinh lai so colisions sau khi swap

#Do phuc tap cua giai thuat:
#Random permutation: O(n)
#Do phuc tap cua bai toan phu thuoc nhieu vao buoc tim kiem va swap:
#Trong truong hop xau nhat: viec tim kiem va swap O(n^2) cho 2 vong for. Va moi lan lap phai thuc hien giam collisions toi da la n-1 lan
#=> thoi gian thuc thi cua giai thuat a gradient-base heuristic la O(n^3)

#Ve viec khong tim thay ket qua phai random lai thi it xay ra. Trong truong hop n nho thi da so se chay 1 lan

#Thoi gian chay thuc te tren may Dell CORE i5 (chua ke thoi gian check)
# So luong con hau      10          100        1.000    10.000  50.000   100.000 
#Thoi gian lan 1 (giay) 0.82        1.21       1.87     9.01    53.72    132.45
#Thoi gian lan 2(giay)  4.02        1.11       1.76     10.27   99.77    165.20                                                      165.19

def initDiagonal(numberOfQueens):
    return [0 for number in range (2 * numberOfQueens -1)]

def countQueensOnDiagonal(positionsOfQueens):
    positiveDiagonal = initDiagonal(len(positionsOfQueens))
    negativeDiagonal = initDiagonal(len(positionsOfQueens))

    for number in positionsOfQueens:
        positiveDiagonal[number + positionsOfQueens[number]] += 1
        negativeDiagonal[number - positionsOfQueens[number]] += 1

    return (positiveDiagonal, negativeDiagonal)

def countCollisions(positiveDiagonal, negativeDiagonal):
    def reduceFunc(acc, i):
        return (acc[0] + max(0, i[0] - 1), acc[1] + max(0, i[1] - 1))

    zipDiagonal = zip(positiveDiagonal, negativeDiagonal)

    (positiveCollisions, negativeCollisions) = reduce(reduceFunc, zipDiagonal, (0, 0))

    return positiveCollisions + negativeCollisions

def isAttacked(index, value, positiveDiagonal, negativeDiagonal):
    return (positiveDiagonal[index+ value] + negativeDiagonal[index - value]) > 2

def queen_search(queens):
    start_time = time.time()
    collisions = 1 # start first loop
    while collisions > 0:
        #init positions of queens using random.pernmutations
        positionsOfQueens = np.random.permutation(queens)

        #count number of queens in each diagonal line positive and negative
        [positiveDiagonal, negativeDiagonal] = countQueensOnDiagonal(positionsOfQueens)
        #count collisions
        collisions = countCollisions(positiveDiagonal, negativeDiagonal)
        #check it is solution
        if collisions == 0:
            print("--- %s seconds ---" % (time.time() - start_time))
            return positionsOfQueens

        #local search and swap
        for i in range(queens):
            for j in range(i+1, queens):

                value_i = positionsOfQueens[i]
                value_j = positionsOfQueens[j]
                #Check if queen is attacked then using herictic
                if (isAttacked(i, value_i, positiveDiagonal, negativeDiagonal)
                    or isAttacked(j, value_j, positiveDiagonal, negativeDiagonal)):
                    
                    #using herictic function to check collisions reduce
                    collReduce = swapsPerformed(i, j, value_i, value_j, positiveDiagonal, negativeDiagonal)
                    #if collisions reduce then swap
                    if (collReduce > 0):
                        #swap
                        positionsOfQueens[i] = value_j
                        positionsOfQueens[j] = value_i
                        #recalculate collisions
                        collisions = collisions - collReduce
                        #check solution
                        if collisions == 0:
                            print("--- %s seconds ---" % (time.time() - start_time))
                            return positionsOfQueens

def swapsPerformed(index_x, index_y, value_x, value_y, positiveDiagonal, negativeDiagonal):
    #save old number of queen in 8 diagonal line relate to swap
    doubleCollisions = 0
    oldPosDiagonal_x = positiveDiagonal[index_x + value_x]
    oldPosDiagonal_y = positiveDiagonal[index_y + value_y]
    oldNegDiagonal_x = negativeDiagonal[index_x - value_x]
    oldNegDiagonal_y = negativeDiagonal[index_y - value_y]
    
    oldPosDiagonal_xy = positiveDiagonal[index_x + value_y]
    oldPosDiagonal_yx = positiveDiagonal[index_y + value_x]
    oldNegDiagonal_xy = negativeDiagonal[index_x - value_y]
    oldNegDiagonal_yx = negativeDiagonal[index_y - value_x]

    if (index_x + value_x == index_y + value_y):
        doubleCollisions = max(0, oldPosDiagonal_x - 1) + max(0, oldNegDiagonal_xy - 1)


    if (index_x - value_x == index_y - value_y):
        doubleCollisions = max(0, oldNegDiagonal_x - 1) + max(0, oldPosDiagonal_xy - 1)
    
    #count old collition in 8 diagonal line
    oldCollision = max(0, oldPosDiagonal_x - 1) + max(0, oldPosDiagonal_y - 1) + \
                    max(0, oldNegDiagonal_x - 1) + max(0, oldNegDiagonal_y - 1) + \
                    max(0, oldPosDiagonal_xy - 1) + max(0, oldPosDiagonal_yx - 1) + \
                    max(0, oldNegDiagonal_xy - 1) + max(0, oldNegDiagonal_yx - 1) - doubleCollisions

    #count queen after swap
    positiveDiagonal[index_x + value_x] -= 1
    positiveDiagonal[index_y + value_y] -= 1
    negativeDiagonal[index_x - value_x] -= 1
    negativeDiagonal[index_y - value_y] -= 1

    positiveDiagonal[index_x + value_y] += 1
    positiveDiagonal[index_y + value_x] += 1
    negativeDiagonal[index_x - value_y] += 1
    negativeDiagonal[index_y - value_x] += 1

    #save new number of queen in 8 diagonal line relate to swap
    newPosDiagonal_x = positiveDiagonal[index_x + value_x]
    newPosDiagonal_y = positiveDiagonal[index_y + value_y]
    newNegDiagonal_x = negativeDiagonal[index_x - value_x]
    newNegDiagonal_y = negativeDiagonal[index_y - value_y]
    
    newPosDiagonal_xy = positiveDiagonal[index_x + value_y]
    newPosDiagonal_yx = positiveDiagonal[index_y + value_x]
    newNegDiagonal_xy = negativeDiagonal[index_x - value_y]
    newNegDiagonal_yx = negativeDiagonal[index_y - value_x]

    if (index_x + value_x == index_y + value_y):
        doubleCollisions = max(0, newPosDiagonal_x - 1) + max(0, newNegDiagonal_xy - 1)


    if (index_x - value_x == index_y - value_y):
        doubleCollisions = max(0, newNegDiagonal_x - 1) + max(0, newPosDiagonal_xy - 1)

    #count new collition in 8 diagonal line
    newCollision = max(0, newPosDiagonal_x - 1) + max(0, newPosDiagonal_y - 1) + \
                    max(0, newNegDiagonal_x - 1) + max(0, newNegDiagonal_y - 1) + \
                    max(0, newPosDiagonal_xy - 1) + max(0, newPosDiagonal_yx - 1) + \
                    max(0, newNegDiagonal_xy - 1) + max(0, newNegDiagonal_yx - 1) - doubleCollisions
    
    #check collisions reduce => return number of Collisions reduce
    if (newCollision < oldCollision):
        return  oldCollision - newCollision
    #collisions don't reduce, save value old for 8 diagonal line
    positiveDiagonal[index_x + value_x] = oldPosDiagonal_x
    positiveDiagonal[index_y + value_y] = oldPosDiagonal_y
    negativeDiagonal[index_x - value_x] = oldNegDiagonal_x
    negativeDiagonal[index_y - value_y] = oldNegDiagonal_y

    positiveDiagonal[index_x + value_y] = oldPosDiagonal_xy
    positiveDiagonal[index_y + value_x] = oldPosDiagonal_yx
    negativeDiagonal[index_x - value_y] = oldNegDiagonal_xy
    negativeDiagonal[index_y - value_x] = oldNegDiagonal_yx

    return 0


# -----------------------------------------------------------__main__--------------------------------------------------------------
if __name__ =="__main__":
    while True:
        print('Chon giai thuat:')
        print('1: Giai thuat DFS (n < 41, neu n > 40 thoi gian chay > 1 phut)')
        print('2: Giai thuat BrFS (n < 12, neu n > 11 thoi gian chay > 1 phut))')
        print('3: Giai thuat Heuristic (Hill Climbing) (n < 150 de chay time <4 phut)')
        print('4: Giai thuat co the giai quyet ban co kich thuoc lon (n tuy y, thoi gian nho)')
        print('5: Giai thuat a gradient-base heuristic quyet ban co kich thuoc lon (n tuy y, thoi gian lon)')
        print('6: THOAT!')
        choice = int(input('Lua chon giai thuat: '))
        if choice == 6:
            break
        while choice < 1 or choice > 6:
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
            if n < 1001:
                printBanCo(res)
                check(res)
        elif choice == 5:
            res = queen_search(n)
            if n < 1001:
                printBanCo(res)
                check(res)
        else:
            print('Khong co tuy chon nay!')
