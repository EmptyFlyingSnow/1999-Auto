import cv2 as cv
import lib.api as api
from cards.aname import card_reflect


def read_screenshot():
    img = cv.imread("screenshot.png")
    return img

def find_image(id: str, take=True):
    if take:
        api.get_screen_shot()
    img = cv.imread("screenshot.png")#读入图片
    img_terminal = cv.imread(f'{id}.png')#读入模板图片

    # print(img_terminal.shape)
    height, width, dep = img_terminal.shape#读取图片大小、分辨率（？）

    result = cv.matchTemplate(img, img_terminal, cv.TM_SQDIFF_NORMED)
    #在img中检索terminal模板所在位置，使用cv.TM_SQDIFF_NORMED方法（？）并将结果保存在
    #result中，result为一个矩阵

    upper_left = cv.minMaxLoc(result)[2]#左上角坐标为minMaxloc方法寻找到的相似度最高点
    img = cv.imread("screenshot.png")#读入图像
    img2 = img[upper_left[1]:upper_left[1]+height,#im2为img图像中相似度最高的区域（左上角坐标点+宽高）
               upper_left[0]:upper_left[0] + width]#右下角坐标点
    return img2

def find(id: str, take=True):
    if take:
        api.get_screen_shot()
    img = cv.imread("screenshot.png")
    img_terminal = cv.imread(f'{id}.png')#读入模板图片

    # print(img_terminal.shape)
    height, width, dep = img_terminal.shape#读取模板图片大小分辨率

    result = cv.matchTemplate(img, img_terminal, cv.TM_SQDIFF_NORMED)#搜索模板图片对应位置

    upper_left = cv.minMaxLoc(result)[2]#左上角坐标为对应矩阵位置
    img = cv.imread("screenshot.png")#再读入图片（没看懂为什么要再读一遍）
    img2 = img[upper_left[1]:upper_left[1]+height,
               upper_left[0]:upper_left[0] + width]#在原图中切出相似区域
    lower_right = (upper_left[0]+width, upper_left[1]+height)#右下角坐标

    avg = (int((upper_left[0]+lower_right[0])/2),
           int((upper_left[1]+lower_right[1])/2),#返回图像中点坐标和模板图片以及
           similar(img_terminal, img2))#计算相似度最高区域的图片的相似值
    # cv.imwrite(f'{id}2.png', img2)
    return avg


def search_cards(character: list):#寻找卡牌
    img = cv.imread("screenshot.png")#读入屏幕截图
    x = 687
    y = 520
    ls = []
    star = []
    for i in range(0, 7):
        finally_y = y+i*154#卡牌大小160*209

        star_x = x-15
        s = 0
        ls.append(img[x:x+180, finally_y:finally_y+140])
        #此处切分操作，x部分为图片纵向坐标，y部分为图片横向坐标
        #实际切分过程从右往左依次进行
        cut = img[star_x:star_x+1+3, finally_y+39:finally_y+40+5]
        # print(f'{i} 1:{cut[0][0][2]}')
        if cut[0][0][2] > 200:#截取图片部分区域，并判断其最右上角RGB中B颜色
            s = 1
        # cv.imwrite(f'{i}star1.png',cut)
        cut = img[star_x:star_x+1+3, finally_y+80:finally_y+80+5]#没找着就往下一点
        # print(f'{i} 2:{cut[0][0][2]}')
        if cut[0][0][2] > 200:
            s = 2
        # cv.imwrite(f'{i}star2.png',cut)
        cut = img[star_x:star_x+1+3, finally_y+100:finally_y+100+5]#还没找着就再往下
        # print(f'{i} 3:{cut[0][0][2]}')
        if cut[0][0][2] > 200:
            s = 3
        # cv.imwrite(f'{i}star3.png',cut)
        star.append(s)#录入卡牌星级

    characters = []
    for chars in character:#循环遍历传入的字符串，据调用为t.team
        characters.append(f'{chars}1')
        characters.append(f'{chars}2')#角色卡牌命名规则为：角色名称+123
        characters.append(f'{chars}3')#应该为一个角色的三个技能
    characters.append('None')
    ccard = []
    for i in characters:#遍历所有角色的所有卡牌
        ccard.append(cv.imread(f'cards/{i}.png'))#将卡牌信息添加到ccard中

    cards = []
    for i in range(0, 7):#似乎是因为有七张手牌
        best = 0
        target = len(ccard)-1#为了排除最后加入的none
        sim_val = 0
        for j in range(0,len(ccard)-1):
            best = similar(ccard[j], ls[i])#穷举比较切分位置和角色手牌模板的相似度
            """可以考虑改成for j in range(0,target):（？），可以节约一次计算时间，但我不确定后续修改是否会影响range的结果"""
            # print(f'{i} and {characters[j]} sim = {best}')
            if best > sim_val and best > 0.55:#记录相似度最大的卡牌序号（最可能的卡牌）
                target = j
                sim_val = best
                # break
        cards.append((card_reflect[f'{characters[target]}'], star[i]))#将其加入手牌组
    # print(cards)
    return cards


def calculate(image1, image2):
    # 灰度直方图算法
    # 计算单通道的直方图的相似值
    hist1 = cv.calcHist([image1], [0], None, [256], [0.0, 255.0])
    hist2 = cv.calcHist([image2], [0], None, [256], [0.0, 255.0])
    # 计算直方图的重合度
    degree = 0
    for i in range(len(hist1)):
        if hist1[i] != hist2[i]:
            degree = degree + \
                (1 - abs(hist1[i] - hist2[i]) / max(hist1[i], hist2[i]))
        else:
            degree = degree + 1
    degree = degree / len(hist1)
    return degree


def similar(image1, image2, size=(160, 210)):#计算图片相似度
    image1 = cv.resize(image1, size)
    image2 = cv.resize(image2, size)
    sub_image1 = cv.split(image1)
    sub_image2 = cv.split(image2)
    sub_data = 0
    for im1, im2 in zip(sub_image1, sub_image2):
        sub_data += calculate(im1, im2)
    sub_data = sub_data / 3
    return sub_data


# api.get_screen_shot()
# print(search_cards(['Anan', 'Bkornblume', 'Eternity']))
# img  = cv.imread("screenshot.png")
# x = 190
# y = 778
# img = img[x:118,y:85]
# checker = cv.imread("cards/disappear.png")
# print(calculate(checker,img))
