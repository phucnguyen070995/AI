from numpy import random
import numpy as np
from functools import reduce
import time

#Code co su dung numpy. De chay duoc code can phai cai numpy

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

#Thoi gian chay thuc te tren may Dell CORE i5
# So luong con hau      10          100        1.000    10.000  50.000   100.000 
#Thoi gian lan 1 (giay) 0.82        1.21       1.87     9.01    53.72    132.45
#Thoi gian lan 2(giay)  4.02        1.11       1.76     10.27   99.77    165.20                                                      165.19

def initDiagonal(numberOfQueens):
    return [0 for number in range (2 * numberOfQueens -1)]

def countQueensOnDiagonal(positionsOfQueens):
    positiveDiagonal = initDiagonal(len(positionsOfQueens));
    negativeDiagonal = initDiagonal(len(positionsOfQueens));

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
                        positionsOfQueens[i] = value_j;
                        positionsOfQueens[j] = value_i
                        #recalculate collisions
                        collisions = collisions - collReduce
                        #check solution
                        if collisions == 0:
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

    
if __name__ == "__main__":

    start_time = time.time()

    numberOfQueens = int(input('Please input number rows on a chessboard: '));

    while numberOfQueens < 4:
        numberOfQueens = int(input('Please input number rows on a chessboard greater than 3: '));

    queensInChessboard = queen_search(numberOfQueens)
    
    #to check collision of solution of collison = 0 then output is perfect 
    [positiveDiagonal, negativeDiagonal] = countQueensOnDiagonal(queensInChessboard)
    collisions = countCollisions(positiveDiagonal, negativeDiagonal)

    print(collisions)
    print("--- %s seconds ---" % (time.time() - start_time))

    
