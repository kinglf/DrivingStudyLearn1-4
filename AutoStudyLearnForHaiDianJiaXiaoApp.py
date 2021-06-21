# -*- coding: UTF-8 -*-

import subprocess, cv2, numpy, os, time
import random

__ADB_PATH__ = 'C:/Environment/Android/platform-tools/adb.exe' #你的adb执行路径


def cap_screen():
    out = subprocess.Popen(__ADB_PATH__ + " shell screencap -p", stdout=subprocess.PIPE)
    out = out.stdout.read().replace(b'\r\n', b'\n')
    npb = numpy.frombuffer(out, numpy.uint8)
    return cv2.imdecode(npb, cv2.IMREAD_ANYCOLOR)


def get_image_point_color(img, x, y):
    b, g, r = img[y, x]
    return r, g, b


def check_process_bar(img):
    r, g, b = get_image_point_color(img, 514, 387)
    if r > 200 or g > 200 or b > 200:
        return True
    else:
        return False


def check_play_btn(img):
    r, g, b = get_image_point_color(img, 34, 377)
    if r > 200 or g > 200 or b > 200:
        return True  # 播放按钮
    else:
        return False  # 暂停按钮或其他


def click(x, y):
    adb_cmd = __ADB_PATH__ + " shell input tap " + str(x) + " " + str(y)
    os.system(adb_cmd)


def show(img):
    cv2.namedWindow("Image")
    cv2.imshow("Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def get_play_status():
    while True:
        click(random.randint(-10, 10) + 260, random.randint(-10, 10) + 240)
        time.sleep(0.2)
        img = cap_screen()
        is_bar = check_process_bar(img)
        if is_bar:
            break
    print('进度条截图:', is_bar)
    is_wait_play = check_play_btn(img)
    print('播放按钮状态', is_wait_play)
    if is_wait_play:
        click(34, 377)
        print('开始播放:', time.strftime('%Y-%m-%d %H:%M:%S'))


while True:
    get_play_status()
    time.sleep(random.randint(30, 60))
