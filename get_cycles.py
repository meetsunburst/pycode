'''
读取随机谱中的最大最小应力并拟合三参数幂函数后根据最大应力求解寿命
'''
import numpy as np
from 三参数幂函数 import get_param
import os

desktop_path = os.path.join(os.path.expanduser("~"), 'Desktop')


# 求取kt2点多不同寿命对应的应力
def get_stress_Kt2_list(Kt2, factor1, factor3, Kt1list, Kt3list):
    res = []
    # 求解Kt=2点多的方程组的系数
    A = np.array([[factor1, 1], [factor3, 1]])
    for i in range(len(Kt1list)):
        b = np.array([Kt1list[i], Kt3list[i]])
        a, b = np.linalg.solve(A, b)
        life = a * Kt2 + b
        res.append(life)
    return np.array(res)


# goodman修正获取Kt时的对应应力
def goodman(Kt_list, delta_m, delta_b):
    return np.array([Kt2_tmp * (1 - (delta_m / delta_b)) for Kt2_tmp in Kt_list])
    # res_delta = []
    # for i in range(len(Kt_list)):
    #     tmp = Kt_list[i] * (1 - (delta_m / delta_b))
    #     res_delta.append(tmp)
    # return np.array(res_delta)


# 读取随机谱求取寿命
def get_cycles(delta_b, Kt2_stress_list, Nlist):
    input_file_path = desktop_path + r'\data.csv'
    output_file_path = desktop_path + r'\res.csv'

    with open(file=input_file_path, mode='r', encoding='utf-8') as file_in:
        with open(file=output_file_path, mode='w', encoding='utf-8') as file_out:
            file_out.write(f'lgN\n')
            # line = file_read.readline()
            line = file_in.readline()
            while line:
                max_stress, min_streess = map(float, line.strip().split(","))
                mid_stress = (max_stress + min_streess) / 2
                # print(f'最大应力是：{max_stress}，均值应力是：{mid_stress}')
                goodman_stress_list = goodman(Kt2_stress_list, mid_stress, delta_b)
                # print(goodman_stress_list)
                try:
                    s0, m, c, lgN = get_param(goodman_stress_list, Nlist, max_stress)
                except Exception as e:
                    print(e.args)
                    file_out.write(f'{100}\n')
                else:
                    file_out.write(f'{str(lgN)}\n')
                line = file_in.readline()


# 等幅谱求寿命
def get_cycles_equal(Kt2_stress_list, Nlist):
    delta_m = 39.111
    max_stress = 71.111

    goodman_stress_list = goodman(Kt2_stress_list, delta_m, delta_b)
    s0, m, c, lgN = get_param(goodman_stress_list, Nlist, max_stress)

    print(f'goodman_stress={list(goodman_stress_list)}')
    print(f's0的值为{s0:.4f},m的值为{m:.4f},c的值为{c:.4f},寿命循环数为{pow(10, lgN)}')


if __name__ == '__main__':
    # 应力集中系数
    factor1 = 1
    factor3 = 3
    # 要求的应力集中系数
    Kt2 = 2.941
    delta_b = 487

    Nlist = [1e4, 5e4, 1e5, 5e5, 1e6, 5e6]
    # 根据马的数据
    Kt1_list = [310.275, 227.535, 172.375, 137.9, 124.11, 117.215]
    Kt3_list = [131.005, 96.53, 75.845, 58.6075, 48.265, 41.37]
    # 根据PDF算的
    # Kt1_list = [316.2341, 200.6278, 172.1047, 132.687, 122.9616, 109.5215]
    # Kt3_list = [135.3152, 87.5863, 73.793, 51.8678, 45.5316, 35.4598]

    Kt2_stress_list = get_stress_Kt2_list(Kt2, factor1, factor3, Kt1_list, Kt3_list)
    # print(f'Kt2_stress_list={list(Kt2_stress_list)}')

    # 求解等幅谱
    get_cycles_equal(Kt2_stress_list, Nlist)
    # 求解随机谱
    # get_cycles(delta_b, Kt2_stress_list, Nlist)
