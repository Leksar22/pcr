"""
Утилиты для расчета показателя перемешивания
"""
import os
from contextlib import chdir
from typing import List, Tuple
import numpy as np

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

__author__ = 'Исламов А.И.'
__all__ = ('calc_stirring_speed_by_time', 'calc_stirring_speed_by_latest_10_time', 'get_stirring_speed_by_times',
           'get_avg_stirring_speed_by_all_times', 'plot_stirring_speed_by_all_time_foreach_alpha',
           'plot_stirring_speed_by_alpha')

MAGNITUDE_FILE = 'mag(U)'
VOLUME_FILE = 'V'
LATEST_TIME = '1.1'
MIN_TIME = 0.01
MAX_TIME = 1.1
DELTA_TIME = 0.1
LATEST_10_TIME = ['1.01', '1.02', '1.03', '1.04', '1.05', '1.06', '1.07', '1.08', '1.09', '1.1']

path_to_tube_result = os.path.abspath(__file__ + "/../../../sources/tube/")


def calc_stirring_speed_by_time(time: str, path: str = None, ) -> float:
    """
    Расчет коэффициента перемешивания по времени
    :param path: путь
    :param time:
    :return:
    """
    path = path or path_to_tube_result
    volume_path = os.path.join(path, time, VOLUME_FILE)
    magnitude_path = os.path.join(path, time, MAGNITUDE_FILE)
    result = 0
    with open(volume_path) as volume_f, open(magnitude_path) as magnitude_f:
        start_str = False
        for volume_i, magnitude_i in zip(volume_f, magnitude_f):
            volume_i, magnitude_i = volume_i.strip(), magnitude_i.strip()
            if not start_str:
                start_str = '(' in (volume_i, magnitude_i)
                continue
            elif ')' in (volume_i, magnitude_i):
                break
            result += float(volume_i) * abs(float(magnitude_i))

        return result


def calc_stirring_speed_by_latest_10_time() -> float:
    """
    Расчет коэффициента перемешивания, усредненного по финальному срезу
    :return:
    """
    return sum([calc_stirring_speed_by_time(t) for t in LATEST_10_TIME]) / len(LATEST_10_TIME)


def get_stirring_speed_by_times(path: str = None, by_latest=None) -> Tuple[List, List]:
    """
    Расчет коэффициента перемешивания, усредненного по всем временным промежуткам
    :param path: путь
    :param by_latest: рассмотреть только N последних временных интервалов
    :return: x, y
    """
    path = path or path_to_tube_result
    res_list = []
    x = []

    by_latest = None if by_latest is None else -by_latest

    for time_dir in sorted(os.listdir(path) or [], key=float)[by_latest:]:
        if time_dir in ['0']:
            continue
        res = calc_stirring_speed_by_time(time_dir, path)
        print(f'{time_dir}_avg: {res}')
        res_list.append(res)
        x.append(float(time_dir))

    return x, res_list


def get_avg_stirring_speed_by_all_times(path: str) -> float:
    """
    Расчет коэффициента перемешивания, усредненного по всем временным промежуткам
    :param path: путь
    :return:
    """
    _, res_list = get_stirring_speed_by_times(path)

    return sum(res_list) / len(res_list)


def plot_stirring_speed_by_all_time_foreach_alpha(path: str) -> None:
    """
    Построение графика ksi(time) для всех alpha
    :param path: путь до каталога с результатами расчетов
    ..
        . (<- path)
            /alpha=0
            /alpha=10
            ...
            /alpha=n
    :return:
    """
    if not path:
        return

    dirs = list(filter(lambda x: x.startswith('alpha='), os.listdir(path)))
    if not dirs:
        return

    for dir_i in sorted(dirs, key=lambda al: float(al[al.find('=') + 1:])):
        path_i = os.path.join(path, dir_i)
        x, y = get_stirring_speed_by_times(path_i)
        if not all([x, y]):
            continue

        plt.plot(x, y, '-', linewidth=2, label=dir_i)  # markersize=2

    ax = plt.gca()
    ax.set_xticks(np.arange(0, MAX_TIME + DELTA_TIME, DELTA_TIME), minor=False)
    ax.set_xlim([0, MAX_TIME])

    plt.xlabel('time')
    plt.ylabel('ksi')
    plt.ticklabel_format(axis='both', style='sci', useMathText=True, scilimits=(0, 0))
    plt.title('Коэффициент перемешивания (ksi) при time∈[0.01;1.1] с шагом 0.01 для разных углов наклона пробирки (alpha)')
    plt.legend()
    plt.show()


def plot_stirring_speed_by_alpha(path: str = None) -> None:
    """
    :param path: путь до каталога с результатами расчетов
    ..
        . (<- path)
            /alpha=0
            /alpha=10
            ...
            /alpha=n
    :return:
    """
    if not path:
        return

    dirs = list(filter(lambda x: x.startswith('alpha='), os.listdir(path)))
    if not dirs:
        return

    x, y = [], []
    for dir_i in sorted(dirs, key=lambda al: float(al[al.find('=') + 1:])):
        path_i = os.path.join(path, dir_i)
        _, y_i = get_stirring_speed_by_times(path_i, by_latest=40)
        if not y_i:
            continue

        avg_y = sum(y_i) / len(y_i)
        x.append(float(dir_i[dir_i.find('=') + 1:]))
        y.append(avg_y)

    plt.plot(x, y, '-', linewidth=2)
    ax = plt.gca()
    ax.set_xticks(np.arange(0, 100, 10), minor=False)  # alpha
    ax.set_xlim([0, 90])

    plt.xlabel('alpha')
    plt.ylabel('ksi')
    plt.ticklabel_format(axis='y', style='sci', useMathText=True, scilimits=(0, 0))
    plt.title('Зависимость коэффициента перемешивания (ksi) от угла наклона пробирки (alpha)')
    plt.show()
