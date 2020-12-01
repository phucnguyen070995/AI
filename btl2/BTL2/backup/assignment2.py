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
    return Tr - Tc

def assign(file_input, file_output):
    # read input
    arr = DocFile(file_input)
    x0, y0 = arr[0]
    num_shippers = arr[1][1]
    num_orders = arr[1][0]
    idx = np.array(range(num_orders))[np.newaxis].T
    list_orders = np.hstack((idx, np.array(arr[2:])))

    #tao array chua id va loi nhuan hien tai
    dtype = [('id', int), ('profit', float), ('x', int), ('y', int)]
    values = [(i, 0, x0, y0) for i in range(num_shippers)]
    current_profit = np.array(values, dtype=dtype)
    #tao list chua order hien tai
    append_order = [[] for i in range(num_shippers)]


    # run algorithm
    while len(list_orders) != 0:
        #chon idx shiper co abs profit nho nhat
        abs_current_profit = current_profit.copy()
        for i in range(num_shippers):
            abs_current_profit[i] = (abs_current_profit[i][0], abs(abs_current_profit[i][1]), abs_current_profit[i][2], abs_current_profit[i][3])
        idx = np.sort(abs_current_profit, kind='heapsort', order='profit')[0][0]
        print('-1-----------------------')
        print(abs_current_profit)
        print(idx)
        dtype = [('id', int), ('abs_profit', float)]
        values = [(list_orders[i,0], abs(current_profit[idx][1] + profit(list(current_profit[idx])[2:], list_orders[i]))) for i in range(len(list_orders))]
        print('0-----------------------')
        print(values)
        all_order_profit = np.array(values, dtype=dtype)
        print('1-----------------------')
        print(all_order_profit)
        #chon id don hang co chi phi den do dat gan bang 0
        all_order_profit = np.sort(all_order_profit, kind='heapsort', order='abs_profit')
        print('2-----------------------')
        print(all_order_profit)
        print('3-----------------------')
        print(all_order_profit[0][0])
        id_arr = list(list_orders[:,0])
        print('4-----------------------')
        print(id_arr)
        id_order = [i for i in range(len(id_arr)) if id_arr[i] == all_order_profit[0][0]][0]
        print('5-----------------------')
        print(id_order)
        # print(current_profit[0][0])
        # print(current_profit[0][1])
        # print(list(current_profit[0])[2:])
        # print()
        current_profit[idx] = (current_profit[idx][0], current_profit[idx][1] + profit(list(current_profit[idx])[2:], list_orders[id_order]), list_orders[id_order,1], list_orders[id_order,2])

        #append new order append_order
        append_order[current_profit[idx][0]].append(all_order_profit[0][0])
        print('6------------------')
        print(append_order)

        #update list_orders
        list_orders = np.delete(list_orders, [id_order * 5 + i for i in range(5)])
        list_orders = list_orders.reshape(len(list_orders) // 5, 5)
        print('7------------------')
        print(list_orders)
        # current_profit = np.sort(current_profit, kind='heapsort', order='profit')
        print('**********************************')
        print(current_profit)
        print(append_order)
        print('**********************************')


    # write output
    # print(append_order)


assign('input.txt', 'output.txt')
