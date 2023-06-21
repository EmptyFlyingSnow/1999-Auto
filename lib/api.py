import os


def get_screen_shot():
    Path = os.getcwd().replace("\\", '/')
    print(f"{Path}/screenshot.png")
    PATH='/'.join(Path.split("/")[:-1])
    print(PATH)
    os.system("adb shell screencap /sdcard/screenshot.png")
    """adb shell screencap /sdcard/screenshot.png: 这个命令在安卓设备上执行屏幕截图，并将截图保存在/sdcard/screenshot.png路径下。这个命令通过adb shell调用执行，在设备的shell环境中运行。"""
    # print(f"{Path}/screenshot.png")
    os.system(f"adb pull /sdcard/screenshot.png {PATH}\screenshot.png")
    """adb pull /sdcard/screenshot.png {Path}\screenshot.png: 这个命令用于将安卓设备上的文件（这里是截图）复制到本地路径。adb pull命令将设备上的文件复制到本地电脑，/sdcard/screenshot.png是设备上截图的路径，{Path}\screenshot.png是将截图复制到本地时的保存路径。"""
    # print(f"{Path}/screenshot.png")
    ans = os.system("adb shell rm /sdcard/screenshot.png")
    """adb shell rm /sdcard/screenshot.png: 这个命令在安卓设备上删除之前保存的截图文件。它通过adb shell调用执行，在设备的shell环境中运行，将screenshot.png文件从设备的/sdcard/路径下删除。"""
    return PATH
    

get_screen_shot()
