import os
import yaml
import sys
import re

params = yaml.safe_load(open("config.yaml"))

numbers = []
pcd_pattern = re.compile('^\d{1,4}\.csv$')
s = '^\d{1,4}\.' + params['image_format'] + '$'
img_pattern = re.compile(s)
if len(sys.argv) < 2:
    exit("Please, write numbers of pcd, which you should delete!!")
for i in range(1,len(sys.argv)):
    arg = str(sys.argv[i])
    if not arg.isdigit():
        exit("Argument {:d} is not an unsigned number!!".format(i))
    numbers.append(int(arg))
pcd_dir_name = params['base_dir'] + "/pcd"
raw_img_dir = params['base_dir'] + "/img"
if not os.path.exists(pcd_dir_name):
    exit("Directory {:s} is not exits!!".format(pcd_dir_name))
if not os.path.exists(raw_img_dir):
    exit("Directory {:s} is not exits!!".format(raw_img_dir))
pcd_list = [f for f in os.listdir(pcd_dir_name) if os.path.isfile(os.path.join(pcd_dir_name, f)) and pcd_pattern.match(f)]
pcd_list.sort()
img_list = [f for f in os.listdir(raw_img_dir) if os.path.isfile(os.path.join(raw_img_dir, f)) and img_pattern.match(f)]
img_list.sort()
if len(pcd_list) != len(img_list):
    exit("Pcd list  and ing list is not equal!!")
for i in range(0, len(pcd_list)):
    pcd_data = pcd_list[i].split('.')
    pcd_number = int(pcd_data[0])
    img_data = img_list[i].split('.')
    img_number = int(img_data[0])
    if (pcd_number != i + 1):
        exit("Pcd file {:s} has uncorrect number!!".format(pcd_list[i]))
    if (img_number != i + 1):
        exit("Img file has uncorrect number!!".format(img_list[i]))
flags = [1]*len(pcd_list)
for i in numbers:
    if i < len(pcd_list) + 1:
        flags[i - 1] = 0
    else:
        exit("The files {:s}.csv and {:s}.{:s} do not exist!!".format(str(i).zfill(params["file_name_digits"]), str(i).zfill(params["file_name_digits"]), params['image_format']))
print flags

i = 0
end_flag = False
while i < len(pcd_list) and not end_flag:
    if flags[i] == 0:
        j = len(pcd_list) - 1
        while j >= 0:
            if flags[j] == 1:
                if i == j + 1:
                    end_flag = True
                    break
                flags[i] = 1
                flags[j] = 0
                del_pcd = os.path.join(pcd_dir_name, "{:s}.csv".format(str(i + 1).zfill(params["file_name_digits"])))
                mov_pcd = os.path.join(pcd_dir_name, "{:s}.csv".format(str(j + 1).zfill(params["file_name_digits"])))
                del_img = os.path.join(raw_img_dir, "{:s}.jpg".format(str(i + 1).zfill(params["file_name_digits"])))
                mov_img = os.path.join(raw_img_dir, "{:s}.jpg".format(str(j + 1).zfill(params["file_name_digits"])))
                os.remove(del_pcd)
                os.rename(mov_pcd, del_pcd)
                os.remove(del_img)
                os.rename(mov_img, del_img)
                break
            j -= 1
    i += 1