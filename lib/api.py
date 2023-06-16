import os


def get_screen_shot():
    Path = os.getcwd().replace("\\", '/')
    #获取文件目录位置
    # print(f"{Path}/screenshot.png")
    os.system("adb shell screencap /sdcard/screenshot.png")
    # print(f"{Path}/screenshot.png")
    os.system(f"adb pull /sdcard/screenshot.png {Path}\screenshot.png")
    # print(f"{Path}/screenshot.png")
    ans = os.system("adb shell rm /sdcard/screenshot.png")
    #看起来是保存屏幕截图，但我不会os库的函数


get_screen_shot()
