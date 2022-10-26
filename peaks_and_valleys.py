import numpy as np
import scipy.signal as sg
import os

desktop_path = os.path.join(os.path.expanduser("~"), 'Desktop')

intput_file = desktop_path + r'\1-STRESS max（z方向）.csv'
output_file = desktop_path + r'\res-1-STRESS max（z方向）.csv'

list = []
with open(file=intput_file, mode='r', encoding='utf-8') as file_in:
    for line in file_in.readlines():
        list.append(float(line.strip('\n')))


def get_maxima(values: np.ndarray):
    """极大值点"""
    max_index = sg.argrelmax(values)[0]
    # return max_index, values[max_index]
    return values[max_index]


def get_minima(values: np.ndarray):
    """极小值点"""
    min_index = sg.argrelmin(values)[0]  # 极小值的下标
    # return min_index, values[min_index]  # 返回极小值
    return values[min_index]


data_np = np.array(list)
data_peaks = get_maxima(data_np)
data_valleys = get_minima(data_np)
print(len(data_peaks))
print(len(data_valleys))

with open(file=output_file, mode='w', encoding='utf-8') as file_out:
    for i in range(min(len(data_peaks), len(data_valleys))):
        # file_out.write(f'{data_peaks[i]},{data_valleys[i]}\n')
        file_out.write(f'{data_peaks[i]}\n{data_valleys[i]}\n')
