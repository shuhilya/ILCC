import os
import yaml
import numpy as np
import sys
from PIL import Image, ImageDraw

params = yaml.safe_load(open("config.yaml"))

numbers = []
if len(sys.argv) < 2:
    exit("Please, write numbers of images, in which you should erase chessboard!!")
for i in range(1,len(sys.argv)):
    arg = str(sys.argv[i])
    if not arg.isdigit():
        exit("Argument {:d} is not an unsigned number!!".format(i))
    numbers.append(int(arg))
dir_name = params['base_dir'] + "/output/img_corners"
raw_img_dir = params['base_dir'] + "/img"
for number in numbers:
    img_corn_name = str(number).zfill(params["file_name_digits"]) + "_img_corners.txt"
    img_corn_dir = os.path.join(dir_name, img_corn_name)
    if not os.path.exists(img_corn_dir):
        exit("The file {:s} does not exist!!".format(img_corn_dir))
    corners_in_img_arr = np.genfromtxt(img_corn_dir, delimiter=",").astype(np.int32)
    if len(corners_in_img_arr) == 0:
        exit("Empty input file: {:s}!!".format(img_corn_dir))
    raw_img_name = str(number).zfill(params["file_name_digits"]) + ".jpg"
    raw_img_path = os.path.join(raw_img_dir, raw_img_name)
    if not os.path.exists(raw_img_path):
        exit("The file {:s} does not exist!!".format(raw_img_path))
    my_img = Image.open(raw_img_path)
    my_img.load()
    shape = my_img.size
    i = 0
    x_min = shape[0]
    x_max = 0
    y_min = shape[1]
    y_max = 0
    while (i < corners_in_img_arr.shape[0]):
        if x_min > corners_in_img_arr[i][0]:
            x_min = corners_in_img_arr[i][0]
        if x_max < corners_in_img_arr[i][0]:
            x_max = corners_in_img_arr[i][0]
        if y_min > corners_in_img_arr[i][1]:
            y_min = corners_in_img_arr[i][1]
        if y_max < corners_in_img_arr[i][1]:
            y_max = corners_in_img_arr[i][1]
        i += 1
    first = (x_min, y_min)
    second = (x_max, y_min)
    third = (x_max, y_max)
    fourth = (x_min, y_max)
    img_draw = ImageDraw.Draw(my_img, "RGB")
    img_draw.polygon([first, second, third, fourth], fill=(255,255,0))
    my_img.save(raw_img_path)