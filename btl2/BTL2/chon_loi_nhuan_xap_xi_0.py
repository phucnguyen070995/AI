# Them cac thu vien neu can
import numpy as np
import math
from itertools import combinations

#my functions
def LuuFile(path, data):
    file = open(path, 'a')
    file.writelines(data)
    file.writelines('\n')
    file.close()

def DocFile(path):
    arrSo = []
    file = open(path, 'r')
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
    idx_orders = np.array(range(num_orders))[np.newaxis].T
    list_orders = np.hstack((idx_orders, np.array(arr[2:])))

    #tao array chua id va loi nhuan hien tai
    dtype = [('id', int), ('profit', float), ('x', int), ('y', int)]
    values = [(i, 0, x0, y0) for i in range(num_shippers)]
    current_profit = np.array(values, dtype=dtype)
    #tao list chua order hien tai
    append_order = [[] for i in range(num_shippers)]

    # Khoi tao danh sach goi hang theo cach chon con duong co loi nhuan gan bang 0 de gan cho cac shipper giup buoc sau de tien toi muc tieu
    # run algorithm
    while len(list_orders) != 0:
        #chon idx shiper co abs profit nho nhat
        abs_current_profit = current_profit.copy()
        for i in range(num_shippers):
            abs_current_profit[i] = (abs_current_profit[i][0], abs(abs_current_profit[i][1]), abs_current_profit[i][2], abs_current_profit[i][3])
        idx = np.sort(abs_current_profit, kind='heapsort', order='profit')[0][0]

        dtype = [('id', int), ('abs_profit', float)]
        values = [(list_orders[i,0], abs(current_profit[idx][1] + profit(list(current_profit[idx])[2:], list_orders[i]))) for i in range(len(list_orders))]

        all_order_profit = np.array(values, dtype=dtype)

        #chon id don hang co chi phi den do dat gan bang 0
        all_order_profit = np.sort(all_order_profit, kind='heapsort', order='abs_profit')
        id_arr = list(list_orders[:,0])
        id_order = [i for i in range(len(id_arr)) if id_arr[i] == all_order_profit[0][0]][0]
        current_profit[idx] = (current_profit[idx][0], current_profit[idx][1] + profit(list(current_profit[idx])[2:], list_orders[id_order]), list_orders[id_order,1], list_orders[id_order,2])

        #append new order append_order
        append_order[current_profit[idx][0]].append(all_order_profit[0][0])
        print('6------------------')
        print(append_order)

        #update list_orders
        list_orders = np.delete(list_orders, [id_order * 5 + i for i in range(5)])
        list_orders = list_orders.reshape(len(list_orders) // 5, 5)
        print('**********************************')
        print(current_profit)
        print(append_order)
        print('**********************************')

    # Moi buoc lap se xem shipper nao dang co abs(this_profit - mean) lon nhat (so don hang > 1) moi duoc thuc hien buoc tiep theo,
    # và kiem tra tung don hang de neu bo don hang do ra thi gia tri this_profit se gan mean nhat sau do nhet vao shipper co abs(this_profit - mean) nho nhat.
    arr_profit = [x[1] for x in current_profit]
    print(arr_profit)
    mean = sum(arr_profit) / num_shippers
    diff_mean = [abs(mean - x) for x in arr_profit]
    print(mean, diff_mean)
    idx_need_change = diff_mean.index((max(diff_mean)))
    print(idx_need_change)
    print(list(combinations(arr_profit, 2)))
    opt_value = sum([abs(x[0] - x[1]) for x in list(combinations(arr_profit, 2))])
    print(opt_value)
    #cap nhat lai list_orders
    list_orders = np.hstack((idx_orders, np.array(arr[2:])))
    print(list_orders)
    # while True:






    # for path in append_order:
    #     data = " ".join([str(x) for x in path])
    #     LuuFile(file_output, data)

assign('input.txt', 'output1.txt')
