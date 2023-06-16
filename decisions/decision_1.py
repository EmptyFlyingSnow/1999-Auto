# 本方法在默认方法进行改进，有合卡的能力，但是决策同样是没buff续buff，没事干就续buff/debuff。
# 测试中
from plugins.Turn import Turn
import cards.aname as cards_arrow


def move(t:Turn,p:int):
    while(True):
        p -= 1
        if (p == -1):
            break
        t.card[p+1] = t.card[p]
        t.data[p+1] = t.data[p]
    # print(t.card[0][0])
    t.data[0] = 0
    t.card[0] = ('无卡牌',0)
    pass

# 与前一个合成
def upgrade(t:Turn,p:int):
    if is_same(t,p,p-1):
        move(t,p-1)
        t.data[p] += 3
        t.card[p] = (t.card[p][0],t.card[p][1]+1)
    pass
def is_same(t:Turn,a:int,b:int):
    if t.card[a][0] == t.card[b][0] and t.card[a][1] == t.card[b][1] and t.card[a][0] != '无卡牌':
        return True
    return False

def use(t:Turn,id:int):
    click = id
    wait = 0.8
    move(t,id)
    hec = 0
    if id < 6:
        if is_same(t,id,id+1):
            upgrade(t,id+1)
            wait += 1
            id = id+1
            hec += 1
    if id < 6:
        if is_same(t,id,id+1):
            upgrade(t,id+1)
            wait += 1
            id = id+1
            hec += 1
    if id >= 0:
        if is_same(t,id-1,id):
            upgrade(t,id)
            wait += 1
            hec += 1

    return (click,wait,f'合成 {hec}')

def find_best(t:Turn):
    b = -114514#啊这……
    ret = 0
    # print(t.data)
    for i in range(0,7):#遍历权重，找出最大值
        if t.data[i] > b:
            b = t.data[i]
            ret = i
    print(f"选择使用{t.card[ret][0]} star : {t.card[ret][1]} at {ret}")
    if t.card[ret][0] in cards_arrow.buff:#如果是对应效果卡，重置周期（处理略显草率，不具有普适性，但简单能用）
        t.buff = 2
    if t.card[ret][0] in cards_arrow.debuff:
        t.debuff = 2
    if t.card[ret][0] in cards_arrow.heal:
        t.heal = 2
    return ret
    

def pri_test(t:Turn):
    t.data = [0,0,0,0,0,0,0,0]#某些情况下会有八张手牌
    for i in range(0,7):
        if t.card[i][0] == '无卡牌':
            t.data[i] -= 10000
    for i in range(0,7):#遍历手牌
        for j in range(i+1,7):#当前比较手牌为j和i
            if is_same(t,i,j) and t.card[i][1] < 3:#如果是相似卡且星级小于3
                value = 1#权值设为1
                if t.card[i][0] in cards_arrow.dps_aoe:#如果是高输出aoe卡牌
                    value *= 1.2
                if t.card[i][0] in cards_arrow.aoe:#如果是aoe卡
                    value *= 1.1
                if t.card[i][0] in cards_arrow.buff:#如果是buff卡
                    value *= 1.5
                for k in range(i+1,j):#遍历i和j之间的卡牌
                    t.data[k] += int(((7-j+i)*(7-j+i)) * value)#增加其间的手牌权值，i和j的差值越小，增加的越多（吧？）
    for i in range(0,7):
        if t.card[i][0] in cards_arrow.limit_aoe:#以下部分，分别根据卡牌的属性予以适当权值调整
                t.data[i] += 25
    for i in range(0,7):
        if t.card[i][0] in cards_arrow.limit_one:
                t.data[i] += 23
    for i in range(0,7):#三星卡
        if t.card[i][1] == 3:
                t.data[i] += 6
    for i in range(0,7):
        if t.card[i][1] == 2:
                t.data[i] += 3
    for i in range(0,7):
        if t.card[i][0] in cards_arrow.buff:
            if t.buff <= 0:#如果buff周期<1，即现在没有buff
                t.data[i] += 50
            else:
                t.data[i] -= 10
    for i in range(0,7):
        if t.card[i][0] in cards_arrow.debuff:
            if t.debuff <= 0:#如果debuff周期<1，即现在没有debuff
                t.data[i] += 50
            else:
                t.data[i] -= 10
    for i in range(0,7):
        if t.card[i][0] in cards_arrow.dps_aoe:
            t.data[i] += 4
    for i in range(0,7):
        if t.card[i][0] in cards_arrow.dps_attack:
            t.data[i] += 2
    for i in range(0,7):
        if t.card[i][0] in cards_arrow.attack:
            t.data[i] -= 1
    for i in range(0,7):
        if t.card[i][0] in cards_arrow.heal:
            if t.heal <= 0:
                t.data[i] += 3
            else:
                t.data[i] -= 5

def normal_cards_upgrade(t:Turn):
    pri_test(t)#计算手牌权重
    print(t.card)
    print(t.data)
    a1 = use(t,find_best(t))
    pri_test(t)#打出手牌后重新计算权重
    print(t.card)
    print(t.data)
    a2 = use(t,find_best(t))
    pri_test(t)
    print(t.card)
    print(t.data)
    a3 = use(t,find_best(t))
    return (a1,a2,a3)#返回使用的三张手牌






