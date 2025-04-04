from tree import RGBXmasTree
from time import sleep

tree = RGBXmasTree()

for pixel in tree:
    pixel.color = (1, 0, 0)
    sleep(1)