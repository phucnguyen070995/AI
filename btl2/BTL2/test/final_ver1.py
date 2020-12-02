# Them cac thu vien neu can
import numpy as np
import math
from itertools import combinations
from itertools import permutations
import time

#my functions
def LuuFile(path, data):
    file = open(path, 'a')
    for line in data:
        line = ' '.join([str(x) for x in line])
        file.writelines(line)
        file.writelines('\n')
    file.close()

def Clear(path):
    file = open(path, 'w')
    file.writelines('')
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

# ham tinh loi nhuan tu vi tri order1 sang order2
def profit(order1, order2):
    #doanh thu
    Tr = 5 + order2[3] + order2[4] * 2
    #chi phi
    Tc = math.sqrt((order1[1] - order2[1])**2 + (order1[2] - order2[2])**2) * 0.5
    return Tr - Tc

def assign(file_input, file_output):
    start_time = time.time()
    # read input
    arr = DocFile(file_input)
    x0, y0 = arr[0]
    num_shippers = arr[1][1]
    num_orders = arr[1][0]
    # print(num_shippers, num_orders)
    idx_orders = np.array(range(num_orders))[np.newaxis].T
    list_orders = np.hstack((idx_orders, np.array(arr[2:])))

    #danh sach profit tu order1 den order2 (co phan biet thu tu order
    tmp = permutations(list_orders, 2)
    dict_pairs = {}
    #tu kho den tat ca don hang id -1 la kho
    for order in list_orders:
        dict_pairs[str((-1,order[0]))] = profit([-1,x0,y0,0,0],order)
    for pairs in tmp:
        dict_pairs[str((pairs[0][0], pairs[1][0]))] = profit(pairs[0],pairs[1])
    # print(dict_pairs)



    #dict chua 10 dinh nui
    dict_num_orders_mountain = {}


    while True:
        # dict chua danh sach don hang cua tat ca shipper
        append_order = {}
        for id in range(num_shippers):
            append_order[id] = []

        # chuan bi bo vo while
        # sinh bo so ngau nhien
        while True:
            array_random = np.random.randint(num_shippers, size=num_orders)
            if len(set(array_random)) == num_shippers:
                # print(len(set(array_random)))
                break
        # print(array_random)

        # xep cac don vao vao shiper tuong ung tu bo so ngau nhien
        idx_order = 0
        for id in array_random:
            append_order[id].append(idx_order)
            idx_order += 1
        # print(append_order)

        # danh sach arr_profit
        arr_profit = []
        for id in range(num_shippers):
            all_profit = dict_pairs[str((-1, append_order[id][0]))]
            for i in range(len(append_order[id]) - 1):
                all_profit += dict_pairs[str((append_order[id][i], append_order[id][i + 1]))]
            arr_profit.append(all_profit)
        # print(arr_profit)

        # tinh he so toi uu
        opt_value = sum([abs(x[0] - x[1]) for x in list(combinations(arr_profit, 2))])

        if len(dict_num_orders_mountain) == 0:
            dict_num_orders_mountain[opt_value] = append_order
            # print(dict_num_orders_mountain)

        while True:
            # tinh he so toi uu
            opt_value = sum([abs(x[0] - x[1]) for x in list(combinations(arr_profit, 2))])

            # tim mean cua tat ca profit
            mean = sum(arr_profit) / num_shippers
            diff_mean = [abs(mean - arr_profit[i]) if len(append_order[i]) > 1 else 0 for i in range(num_shippers)]

            # tim shipper co chenh lech profit voi mean profit lon nhat
            shipper_need_change1 = diff_mean.index((max(diff_mean)))

            # list_orders = [x for x in range(num_orders)]
            # danh sach don hang cua shipper gay anh huong lon
            shipper_need_change_array1 = append_order[shipper_need_change1]

            # kiem tra don hang nao lam gia tri chenh lech voi mean nhieu nhat thi bo ra
            temp_profit_array1 = []
            for i in range(len(append_order[shipper_need_change1])):
                if i == 0:
                    temp_profit_array1.append(
                        arr_profit[shipper_need_change1] - dict_pairs[str((- 1, shipper_need_change_array1[i]))] -
                        dict_pairs[str((shipper_need_change_array1[i], shipper_need_change_array1[i + 1]))] +
                        dict_pairs[str((- 1, shipper_need_change_array1[i + 1]))])
                elif i == len(append_order[shipper_need_change1]) - 1:
                    temp_profit_array1.append(arr_profit[shipper_need_change1] - dict_pairs[
                        str((shipper_need_change_array1[i - 1], shipper_need_change_array1[i]))])
                else:
                    temp_profit_array1.append(arr_profit[shipper_need_change1] - dict_pairs[
                        str((shipper_need_change_array1[i - 1], shipper_need_change_array1[i]))] - dict_pairs[str(
                        (shipper_need_change_array1[i], shipper_need_change_array1[i + 1]))] + dict_pairs[str(
                        (shipper_need_change_array1[i - 1], shipper_need_change_array1[i + 1]))])
            diff_mean_temp_profit_array1 = [abs(x - mean) for x in temp_profit_array1]

            # tim ra don hang gay anh huong
            idx_order1 = diff_mean_temp_profit_array1.index(min(diff_mean_temp_profit_array1))
            order_need_change = shipper_need_change_array1[idx_order1]

            # tim shipper co chenh lech profit voi mean profit nho nhat
            shipper_need_change2 = diff_mean.index((min(diff_mean)))

            # danh sach don hang cua shipper gay anh huong lon
            shipper_need_change_array2 = append_order[shipper_need_change2]

            # kiem tra don hang nao lam gia tri chenh lech voi mean it nhat thi them vao
            temp_profit_array2 = []
            for i in range(len(append_order[shipper_need_change2]) + 1):
                if i == 0:
                    temp_profit_array2.append(
                        arr_profit[shipper_need_change2] - dict_pairs[str((- 1, shipper_need_change_array2[i]))] +
                        dict_pairs[str((- 1, order_need_change))] + dict_pairs[
                            str((order_need_change, shipper_need_change_array2[i]))])
                elif i == len(append_order[shipper_need_change2]):
                    temp_profit_array2.append(arr_profit[shipper_need_change2] + dict_pairs[
                        str((shipper_need_change_array2[i - 1], order_need_change))])
                else:
                    temp_profit_array2.append(arr_profit[shipper_need_change2] - dict_pairs[
                        str((shipper_need_change_array2[i - 1], shipper_need_change_array2[i]))] + dict_pairs[
                                                  str((order_need_change, shipper_need_change_array2[i]))] +
                                              dict_pairs[
                                                  str((shipper_need_change_array2[i - 1], order_need_change))])
            diff_mean_temp_profit_array2 = [abs(x - mean) for x in temp_profit_array2]

            # tim ra don hang gay anh huong
            idx_order2 = diff_mean_temp_profit_array2.index(min(diff_mean_temp_profit_array2))

            # kiem tra xem co toi uu hon khong
            temp_arr_profit = arr_profit.copy()
            temp_arr_profit[shipper_need_change1] = temp_profit_array1[idx_order1]
            temp_arr_profit[shipper_need_change2] = temp_profit_array2[idx_order2]

            # tinh he so toi uu tam thoi
            temp_opt_value = sum([abs(x[0] - x[1]) for x in list(combinations(temp_arr_profit, 2))])

            # print('**********************************')
            # print('He so toi uu buoc trc    He so toi uu buoc nay')
            # print(opt_value, temp_opt_value)
            # print('Neu He so toi uu buoc trc < He so toi uu buoc nay thi End Loop')

            if temp_opt_value > opt_value:
                # print('Ket thuc')
                # print('**********************************')
                break

            # cap nhat gia tri opt_value moi
            opt_value = temp_opt_value

            # cap nhat dan sach don hang moi
            append_order[shipper_need_change1] = append_order[shipper_need_change1][:idx_order1] + append_order[
                                                                                                       shipper_need_change1][
                                                                                                   idx_order1 + 1:]
            append_order[shipper_need_change2] = append_order[shipper_need_change2][:idx_order2] + [order_need_change] + \
                                                 append_order[shipper_need_change2][idx_order2:]

            # cap nhat arr_profit
            arr_profit = temp_arr_profit

            # print('Danh sach don hang buoc hien tai')
            # print(append_order)
            # print('**********************************')


        #kiem tra voi tap cac dinh nui
        # print(opt_value)
        if len(dict_num_orders_mountain) == num_orders and all([opt_value >= x for x in (dict_num_orders_mountain.keys())]):
            # print(opt_value, dict_num_orders_mountain.keys())
            # print([opt_value >= x for x in (dict_num_orders_mountain.keys())])
            break
        elif len(dict_num_orders_mountain) == num_orders:
            del dict_num_orders_mountain[max(dict_num_orders_mountain.keys())]
            dict_num_orders_mountain[opt_value] = append_order
        else:
            dict_num_orders_mountain[opt_value] = append_order


        # print(dict_num_orders_mountain)

    print('He so toi uu tim duoc:')
    print(min(dict_num_orders_mountain.keys()))
    print('Danh sach don hang cuoi cung')
    print(dict_num_orders_mountain[min(dict_num_orders_mountain.keys())])
    print('**********************************')
    print('Thoi gian chay: {0}'.format(str(time.time() - start_time)))
    print('**********************************')
    # Clear(file_output)
    # LuuFile(file_output, ['Thoi gian chay: {0}'.format(str(time.time() - start_time))])
    # LuuFile(file_output, ['He so toi uu: {0}'.format(str(dict_num_orders_mountain.keys())))])
    # LuuFile(file_output, append_order.values())
    # print(min(dict_num_orders_mountain.keys()))
for i in range(11):
    input = 'input' + str(i) + '.txt'
    output = 'output_Phuc' + str(i) + '.txt'
    assign(input, output)
    print('Done testcase ' + str(i) + '!')
# assign('input10.txt', 'output_Phuc10.txt')