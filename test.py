from tkinter import W
from matplotlib import pyplot as plt
import functools as fct
import itertools as itr
import copy
import math


#1
def print_polygon(polygons, xlimit=[0, 10], ylimit=[0, 10]):
    #Функция принимает в себя последовательность полигонов и строит график
    for polygon in polygons:
        for i in range(len(polygon) - 1):
            plt.plot((polygon[i][0], polygon[i + 1][0]),
                     (polygon[i][1], polygon[i + 1][1]),
                     color="green")
        plt.plot((polygon[len(polygon) - 1][0], polygon[0][0]),
                 (polygon[len(polygon) - 1][1], polygon[0][1]),
                 color="green")
    plt.xlim(xlimit)
    plt.ylim(ylimit)
    plt.show()


#Пример:
print_polygon((((0, 1.5), (1, 2.5), (2, 1.5)), ((3, 1.5), (4, 2.5), (5, 1.5))), xlimit=[-2, 5])


#2.1
def gen_rectangle(step=2, start_x=0, start_y=0, l=1, w=1):
    """
    Функция-генератор генерирует за каждую итерацию набор точек для создания одного полигона(прямоугольника)
    Аргумент step отвечает за расстояние между соседними полигонами относительно нижней левой вершины
    """
    cnt = 0
    while True:
        yield tuple(
            map(lambda x: (l + x[0] + start_x, w + x[1] + start_y),
                ((0 + cnt * step, 0), (0 + cnt * step, 1), (1 + cnt * step, 1),
                 (1 + cnt * step, 0))))
        cnt += 1


print_polygon(
    tuple(itr.islice(gen_rectangle(start_x=-3, start_y=-2, l=2, w=4), 5)))


#2.2
def gen_triangle(step=3, start_x=0, start_y=0, l=1, w=1):
    """
    Функция-генератор генерирует за каждую итерацию набор точек для создания одного полигона(треугольника)
    Аргумент step отвечает за расстояние между соседними полигонами относительно нижней левой вершины
    """
    cnt = 0
    while True:
        yield tuple(
            map(lambda x: (l + x[0] + start_x, w + x[1] + start_y),
                ((0 + cnt * step, 0), (1 + cnt * step, 1),
                 (2 + cnt * step, 0))))
        cnt += 1


print_polygon(
    tuple(itr.islice(gen_triangle(start_x=5, start_y=3, l=1, w=1), 5)))


#2.3
def gen_hexagon(step=1, start_x=0, start_y=0, l=1, w=1):
    """
    Функция-генератор генерирует за каждую итерацию набор точек для создания одного полигона(шестиугольника)
    Аргумент step отвечает за расстояние между соседними полигонами относительно нижней левой вершины
    """
    cnt = 0
    while True:
        n = 2
        yield tuple(
            map(lambda x: (l + x[0] + start_x, w + x[1] + start_y),
                ((0 + cnt * step, 0.5), (0.25 + cnt * step, 0.067),
                 (0.75 + cnt * step, 0.067), (1 + cnt * step, 0.5),
                 (0.75 + cnt * step, 1 - 0.067),
                 (0.25 + cnt * step, 1 - 0.067))))
        cnt += 1


print_polygon(tuple(itr.islice(gen_hexagon(start_x=2, start_y=3, l=5, w=5),
                               3)))

#2.4 - создаем мутанта
mutant = tuple(itr.islice(gen_hexagon(9), 2)) + tuple(
    itr.islice(gen_triangle(5), 3))[1:] + tuple(itr.islice(
        gen_rectangle(3), 3))
print_polygon(mutant)


#3.1
#Параллельный перенос позволяет передвинуть график по оси x и/или y
def tr_translate(polygon, x, y):
    return tuple(map(lambda coord: (coord[0] + x, coord[1] + y), polygon))


#Пример: передвинем на 2 вправо, на 3 вверх
print_polygon(
    tuple(map(tr_translate, itr.islice(gen_rectangle(), 3), [2] * 3, [3] * 3)))

#Еще один пример -> передвинем только одну фигуру из ряда вверх на 2 и вправо на 2
polygons = list(itr.islice(gen_triangle(), 3))
polygons[1] = tr_translate(polygons[1], 2, 2)
print_polygon(polygons)


#3.2
#поворот позволяет совершить вращение фигуры на определнное количество градусов
#относительно указанной точки
def tr_rotate(polygon, dot_x, dot_y, degree):
    sin_value = math.sin(degree)
    cos_value = math.cos(degree)
    return tuple(
        map(
            lambda coord: ((coord[0] - dot_x) * cos_value -
                           (coord[1] - dot_y) * sin_value + dot_x,
                           (coord[0] - dot_x) * sin_value +
                           (coord[1] - dot_y) * cos_value + dot_y), polygon))


#Пример: ряд из двух треугольников, один обычный, второй развернем на 180 градусов.
triangles = list(itr.islice(gen_triangle(), 2))
triangles[0] = tr_rotate(triangles[0], 0, 0, math.pi)
print_polygon(triangles)


#3.3
def tr_symmetry(figure, p1x, p1y, p2x, p2y):
    dx = p2x - p1x
    dy = p2y - p1y
    result_figure = []
    for i in figure:
        p0x = i[0]
        p0y = i[1]
        ax = (((dx * p0x + dy * p0y) * -1 * dx) -
              (dy * (dy * p1x - dx * p1y))) / (-1 * dx * dx - dy * dy)
        ay = ((dx * (dy * p1y - dx * p1y)) -
              (dy * (dx * p0x + dy * p0y))) / (-1 * dx * dx - dy * dy)
        x = ax + (ax - p0x)
        y = ay + (ay - p0y)
        result_figure.append((x, y))
    return tuple(result_figure)


triangles = list(itr.islice(gen_triangle(), 2))

n = 2
# Пример:
new_triangles = list(
    map(tr_symmetry, triangles, [0] * n, [1.05] * n, [1] * n, [1.05] * n)), triangles
print_polygon(triangles)
print_polygon(new_triangles)


#3.4
def tr_homothety(figure, Ox, Oy, k):
    return tuple(
        map(
            lambda coord: (coord[0] * k - Ox * (k + 1), coord[1] * k - Oy *
                           (k + 1)), figure))


#Пример:
n = 5
polygons = list(itr.islice(gen_rectangle(), 5))
new_polygons = list(
    map(tr_homothety, polygons, [-1] * n, [-1] * n, range(1, n + 1)))
print_polygon(new_polygons)

#4.1
n = 7
first = list(
    map(tr_rotate, tuple(itr.islice(gen_rectangle(), n)), [0] * n, [0] * n,
        [math.pi / 4] * n))
second = tuple(map(tr_translate, first, [-1.2] * n, [1.2] * n))
third = tuple(map(tr_translate, first, [-2.4] * n, [2.4] * n))
print_polygon(first)
print_polygon(second)
print_polygon(third)

#4.2
n = 7
first = list(
    map(tr_rotate, tuple(itr.islice(gen_rectangle(), n)), [10] * n, [0] * n,
        [math.pi / 4] * n))
second = tuple(itr.islice(gen_rectangle(), n))
print_polygon(first)
print_polygon(second)

#4.3
n = 6
triangles = list(itr.islice(gen_triangle(), n))
new_triangles = list(
    map(tr_symmetry, triangles, [0] * n, [1.2] * n, [1] * n, [1.2] * n))
print_polygon(triangles)
print_polygon(new_triangles)

#4.4
n = 6
polygons = list(itr.islice(gen_rectangle(), n))
first_part = list(
    map(tr_homothety, polygons, [-0.5] * n, [-0.5] * n, range(1, n + 1)))

second_part = []
for polygon in first_part:
    second_part.append(
        tuple(map(lambda coords: (-coords[0], -coords[1]), polygon)))

second_part = tuple(map(tr_translate, second_part, [5] * n, [5] * n))[1:]
first_part = tuple(
    map(tr_rotate, first_part, [5] * n, [0] * n, [math.pi / 6] * n))
second_part = tuple(
    map(tr_rotate, second_part, [5] * n, [0] * n, [math.pi / 6] * n))

print_polygon(first_part[1:])
# print_polygon(second_part)