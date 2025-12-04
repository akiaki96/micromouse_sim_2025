from functools import total_ordering
try:
    import pyperclip
except:
    print("No module named 'pyperclip'")

from WallData import *
import heapq

walldata = WallData()

# walldata.set_wall([
#     "c888888888888889",
#     "4000000000000001",
#     "4000000000000001",
#     "4000000000000001",
#     "4000000000000001",
#     "4000000000000001",
#     "4000000000000001",
#     "4000000000000001",
#     "4000000000000001",
#     "4000000000000001",
#     "4000000000000001",
#     "4000000000000001",
#     "4000000000000001",
#     "4000000000000001",
#     "4000000000000001",
#     "6222222222222223",
# ])

# maze_list = [
# "6aaaaa2aaa2aaaa3",
# "c362aa8aa296a221",
# "615c2aa2a8a16155",
# "555616a8aaa15541",
# "49c1c162a23c1415",
# "563c355c21435555",
# "55c3554a14154955",
# "5c3c895615555695",
# "4356aa1c95415569",
# "555caa96a8954143",
# "5542aa3caa215555",
# "4954368a2a955555",
# "5695482a8aa94155",
# "5c348a8aa36a9d49",
# "43c96aaa3c96aa83",
# "dcaa8aaa8aa8aaa9",
# ]

maze_list = [input()[1:-1] for _ in range(16)]

# walldata.set_wall(
# list(reversed(maze_list))
# )
clip_str = ""
print()
for x in range(16):
    num = 0
    for y in range(16-1):
        # num += walldata.get_wall_abs(x,y,Nth) << y
        num += ((int(maze_list[15 - y][x], 16)>>1) & 1) << y
    walldata.wall_hor[x] = num

    print("0b{:015b}".format(num), end=" ")
    clip_str += "0b{:015b}".format(num) + " "
# print()

for y in range(16):
    num = 0
    for x in range(16-1):
        # num += walldata.get_wall_abs(x,y,Est) << x
        num += (int(maze_list[15 - y][x], 16) & 1) << x
    walldata.wall_ver[y] = num
    print("0b{:015b}".format(num), end=" ")
    clip_str += "0b{:015b}".format(num) + " "
clip_str += "\n"
print()
walldata.print_wall()
try:
    pyperclip.copy(clip_str)
except:
    ...