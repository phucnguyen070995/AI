import time

def printBanCo(arr):
    for i in range(len(arr)):
        for j in range(arr[i][0]):
            print(' * ', end='')
        print(' Q ', end='')
        for j in range(arr[i][0] + 1, len(arr)):
            print(' * ', end="")
        print()

def searchDFS(n):
    start_time = time.time()
    print('Dang su dung giai thuat DFS:')
    #Tao search tree voi tang i la tim kiem vi tri dat con hau cho hang thu i - 1
    res = []
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
            if isNextState(Stack, nextState):
                Stack.append(nextState)
            if len(Stack) == n + 1:
                res.append(Stack[1:])
        # print(Stack)

    print("--- %s seconds ---" % (time.time() - start_time))
    return res


def searchBrFS(n):
    start_time = time.time()
    res = []
    Stack = []
    print("--- %s seconds ---" % (time.time() - start_time))
    return 0

def searchHeuristic(n):
    start_time = time.time()
    print("--- %s seconds ---" % (time.time() - start_time))

def isNextState(Stack, state):
    for i in range(1, len(Stack)):
        if (i - 1 + Stack[i][0]) == (len(Stack) - 1 + state[0]) or (i - 1 - Stack[i][0]) == (len(Stack) - 1 - state[0]) or Stack[i][0] == state[0]:
            return False
    return True

if __name__ =="__main__":
    n = int(input('Moi nhap so chieu ban co nxn: '))
    res = searchDFS(n)
    print(len(res))
    for banco in res:
        print('*********************************')
        printBanCo(banco)

