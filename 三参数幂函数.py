'''三参数幂函数求解'''
import math
import numpy as np


# 将s0的值代入方程，求得等式值
def fun_s(s0, delta, N):
    n = len(N)
    L_y0 = (np.log(delta - s0) / (delta - s0)).sum() - (1 / n) * np.log(delta - s0).sum() * (1 / (delta - s0)).sum()
    L_yy = (np.log(delta - s0) ** 2).sum() - (1 / n) * ((np.log(delta - s0).sum()) ** 2)
    L_x0 = (np.log(N) / (delta - s0)).sum() - (1 / n) * np.log(N).sum() * (1 / (delta - s0)).sum()
    L_xy = (np.log(N) * np.log(delta - s0)).sum() - (1 / n) * np.log(N).sum() * np.log(delta - s0).sum()

    return L_y0 / L_yy - L_x0 / L_xy


# 若s0的结果大于0则调用该方程，使用二分法求解s0的值
def fun_iter(delta, N):
    low = 0
    high = np.min(delta)
    while (high > low):
        mid = (low + high) / 2
        tmp = fun_s(mid, delta, N)
        # print(f"tmp的值为:{tmp},low的值为:{low},high的值为:{high},mid的值为:{mid}")
        if (abs(high - low) < 10e-5):
            return mid
        if (tmp < 0):
            high = mid
        elif (tmp > 0):
            low = mid


# 求解m的值
def fun_m(s0, delta, N):
    n = len(N)
    L_yy = (np.log(delta - s0) ** 2).sum() - (1 / n) * ((np.log(delta - s0).sum()) ** 2)
    L_xy = (np.log(N) * np.log(delta - s0)).sum() - (1 / n) * np.log(N).sum() * np.log(delta - s0).sum()

    return -L_xy / L_yy


# 求解c的值
def fun_c(s0, delta, N):
    n = len(N)
    x_mean = (1 / n) * np.log(N).sum()
    y_mean = (1 / n) * np.log(delta - s0).sum()
    L_yy = (np.log(delta - s0) ** 2).sum() - (1 / n) * ((np.log(delta - s0).sum()) ** 2)
    L_xy = (np.log(N) * np.log(delta - s0)).sum() - (1 / n) * np.log(N).sum() * np.log(delta - s0).sum()

    return np.exp(x_mean - y_mean * L_xy / L_yy)


# 得到对数寿命
def get_param(stress_list, Nlist, max_stress):
    # 求解s0，先假设s0=0，若求解结果为负数，则s0的值为0
    s0 = 0
    s0_0 = fun_s(0, stress_list, Nlist)
    if (s0_0 > 0): s0 = fun_iter(stress_list, Nlist)

    m = fun_m(s0, stress_list, Nlist)
    c = fun_c(s0, stress_list, Nlist)
    # print(f'm={m},c={c},s0={s0}')
    lgN = math.log10(c) - m * math.log10(max_stress - s0)
    # cycles = c / (pow(max_stress - s0, m))
    return s0, m, c, lgN


if __name__ == '__main__':
    N = np.array([1e4, 5e4, 1e5, 5e5, 1e6, 5e6])
    stress_list = np.array([310.275, 227.535, 172.375, 137.9, 124.11, 117.215])
    # stress_list = np.array([144.4132047, 106.2096465, 82.27375619, 64.43917128, 55.00561452, 49.13897475])
    # stress_list = np.array([132.1858107, 85.36948417, 72.06989821, 51.20818833, 45.25774283, 35.89415743])
    # stress_list = np.array([152.1718475, 111.9296155, 86.78609757, 67.91270502, 57.83639293, 51.53475936])
    max_stress = 132.063
    s0, m, c, lgN = get_param(stress_list, N, max_stress)
    print(f's0的值为{s0},m的值为{m:.4f},c的值为{c}')
    print(f'最大应力为{max_stress}时，寿命循环数为{pow(10, lgN)}')
