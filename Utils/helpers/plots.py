"""
Хелперы для построения графиков
"""
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

__author__ = 'Исламов А.И.'
__all__ = ('plot_block_coordinates',)

path_to_block_topology = os.path.abspath(__file__ + "/../../../sources/tube/blockTopology.obj")


def plot_block_coordinates():
    """
    Вывести точки из blockTopology.obj
    :return:
    """
    if not os.path.isfile(path_to_block_topology):
        print('blockTopology.obj is not found!')
        print(__file__)
        print(path_to_block_topology)
        return

    with open(path_to_block_topology) as f:
        data = {i: list(map(float, val.split(' ')[1:])) for i, val in enumerate(f.readlines()) if val[0] == 'v'}

    if not data:
        print('blockTopology.obj is empty!')
        return

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    for key, value in data.items():
        if 20 < key < 80:
            continue
        ax.scatter(value[0], value[1], value[2], color='b')
        ax.text(value[0], value[1], value[2], str(key))
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    plt.show(block=False)

#
# def gnuplot():
#     import subprocess
#
#     # Читаем данные из файла
#     with open(path_to_block_topology) as file:
#         data = file.readlines()
#
#     # Запускаем Gnuplot
#     gnuplot = subprocess.Popen(['gnuplot'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
#                                universal_newlines=True)
#
#     # Отправляем команды в Gnuplot для рисования вершин
#     gnuplot.stdin.write('set term x11\n')
#     gnuplot.stdin.write('set datafile separator " "\n')
#     gnuplot.stdin.write('splot "-" with points pointtype 7\n')
#
#     for line_num, line in enumerate(data):
#         if line.startswith('v'):
#             vertex = line.split()
#             x, y, z = vertex[1], vertex[2], vertex[3]
#             gnuplot.stdin.write(f'{x} {y} {z}\n')
#
#     gnuplot.stdin.write('e\n')
#     gnuplot.stdin.flush()
#
#     # Отобразить ребра между вершинами
#     gnuplot.stdin.write('set datafile separator " "\n')
#     gnuplot.stdin.write('plot "-" with lines\n')
#
#     for line in data:
#         if line.startswith('l'):
#             edge = line.split()
#             start_vertex = int(edge[1])
#             end_vertex = int(edge[2])
#             x1, y1, z1 = data[start_vertex - 1].split()[1], data[start_vertex - 1].split()[2], \
#             data[start_vertex - 1].split()[3]
#             x2, y2, z2 = data[end_vertex - 1].split()[1], data[end_vertex - 1].split()[2], data[end_vertex - 1].split()[
#                 3]
#             gnuplot.stdin.write(f'{x1} {y1} {z1}\n')
#             gnuplot.stdin.write(f'{x2} {y2} {z2}\n')
#             gnuplot.stdin.write('\n')
#
#     gnuplot.stdin.write('e\n')
#     gnuplot.stdin.flush()
#
#     # Подождать, пока пользователь не закроет окно Gnuplot (введет exit)
#     input("Press Enter to exit")
#
#     # Завершить Gnuplot
#     gnuplot.stdin.write('exit\n')
#     gnuplot.stdin.close()
#     gnuplot.wait()
