# Them cac thu vien neu can
import numpy as np
import math

#my functions
def LuuFile(path, data):
    file = open(path, 'a', encoding = 'utf-8')
    file.writelines(data)
    file.writelines('\n')
    file.close()

def DocFile(path):
    arrSo = []
    file = open(path, 'r', encoding= 'utf-8')
    for line in file:
        data = line.strip()
        arr = [int(x) for x in data.split(' ')]
        arrSo.append(arr)
    file.close()
    return arrSo

#ham tinh loi nhuan
def profit(position, order):
    #doanh thu
    Tr = 5 + order[3] + order[4] * 2
    Tc = math.sqrt((position[0] - order[1])**2 + (position[1] - order[2])**2) * 0.5 + 10
    print(Tr, Tc)
    return Tr - Tc

def assign(file_input, file_output):
    # read input
    arr = DocFile(file_input)
    x0, y0 = arr[0]
    num_shippers = arr[1][1]
    num_orders = arr[1][0]
    idx = np.array(range(num_orders))[np.newaxis].T
    list_orders = np.hstack((idx, np.array(arr[2:])))

    # run algorithm
    print(x0, y0)
    print(num_shippers)
    print(num_orders)
    print(list_orders)

    # write output
    print([profit([x0, y0], x) for x in list_orders])


assign('input.txt', 'output.txt')
