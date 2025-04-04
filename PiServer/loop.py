from tree import RGBXmasTree
from time import sleep

tree = RGBXmasTree()

colors = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]

for color in colors:
    tree.color = color
    sleep(1)