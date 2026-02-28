from collections import Counter
import random
from itertools import combinations
import math


def pair(hand):
    ranks=[rank for rank,suit in hand]
    c=Counter(ranks)
    if sorted(c.values())==[1,1,1,2]:
        pair1=[i for i,v in c.items() if v==2][0]
        k=sorted([i for i,v in c.items() if i!=pair1],reverse=True)
        return (2,pair1,*k)

    else:
        return None
    
def two_pair(hand):
    ranks=[rank for rank,suit in hand]
    c=Counter(ranks)
    if sorted(c.values())==[1,2,2]:
        pair2=sorted([i for i,v in c.items() if v==2],reverse=True)
        k2=[i for i,v in c.items() if v==1][0]
        return(3,pair2[0],pair2[1],k2)
    else:
        return None
    
def three(hand):
    ranks=[rank for rank,suit in hand]
    c=Counter(ranks)
    if sorted(c.values())==[1,1,3]:
        kind3=[i for i,v in c.items() if v==3 ][0]
        k3=sorted([j for j in c if j != kind3],reverse=True)
        return(4,kind3,*k3)
    else:
        return None
    
def stra(hand):
    ranks=[rank for rank,suit in hand]
    c=Counter(ranks)
    s_hand=sorted(ranks,reverse=True)
    if sorted(c.values())==[1,1,1,1,1] and sum([1 for i in range(4) if s_hand[i]==s_hand[i+1]+1 ])==4:
        return(5,s_hand[0])
    elif s_hand==[14,5,4,3,2]:
        return(5,5)
    else:
        return None
    
def flush(hand):
    suit=[s for r,s in hand]
    c_s=Counter(suit)
    if len(c_s)==1:
        ranks=sorted([r for r,s in hand],reverse=True)
        return (6,*ranks)
    else:
        return None
        
def full_house(hand):
    ranks=[r for r,s in hand]
    c=Counter(ranks)
    if sorted(c.values())==[2,3]:
        house=[i for i,v in c.items() if v==3][0]
        pair=[i for i,v in c.items() if v==2][0]
        return(7,house,pair)
    else:
        return None

def four(hand):
    ranks=[r for r,s in hand]
    c=Counter(ranks)
    if sorted(c.values())==[1,4]:
        four4=[i for i,v in c.items() if v==4][0]
        k=[i for i in c.keys() if i !=four4][0]
        return(8,four4,k)
    else:
        return None
    
def str_flush(hand):
    ranks=sorted([r for r,s in hand],reverse=True)
    suits=[s for r,s in hand]
    c_r=Counter(ranks)
    c_s=Counter(suits)
    if len(c_s.values())==1 and sum([1 for i in range(4) if ranks[i]-1==ranks[i+1]])==4:
        return(9,ranks[0])
    elif len(c_s.values())==1 and ranks==[14,5,4,3,2]:
        return(9,5)
    else:
        return None
    
def hand_rank(hand):
    for i in [str_flush,four,full_house,flush,stra,three,two_pair,pair]:
        res= i(hand)
        if res:
            return res
        
    ranks=sorted([i for i,v in hand],reverse=True)
    return (1,*ranks)   

def best_five(all):
    five=combinations(all,5)
    best=None
    card_type=[]
    for i in five :
        rank=hand_rank(i)
        if  best is None or best<=rank:
            best=rank
            card_type=i
    return best,card_type 
# 分點＋牌型


def start_game(num,cards):
    random.shuffle(cards)
    players={}
    for p in range(num):
        players[f"player{p+1}"]=[cards.pop(),cards.pop()]
    return players


def simulate(hand,desk,cards):

    current_hand={}

    for i in range(len(hand)):
        current_hand[f"player{i+1}"]=hand[f"player{i+1}"]+desk

    num=5-len(desk)
    p=list(combinations(cards,num))

    length = math.comb(len(cards), num)

    players_win={}
    human=len(hand)

    for z in range(human):
        players_win[f"player{z+1}"]=[0,0]


    for k in range(length):
        res={}
        for j in range(len(hand)):
            seven=current_hand[f"player{j+1}"]+list(p[k])
            res[f"player{j+1}"]= best_five(seven)

        winner=max(res,key=lambda w : res[w][0])
        high=[i for i,v in res.items() if v[0]==res[winner][0]]
        for a in range(len(high)):
            players_win[high[a]][0]+=1 / len(high)

    for f in range(human):
        players_win[f"player{f+1}"][1]= players_win[f"player{f+1}"][0] / length

    return players_win



deck=[i for i in range(2,15)]
flower=['♠','♥','♣','♦']
cards=[]
for i in flower:
    for j in deck:
        cards.append((j,i))

num=0

while 2>num or num>10:
    num=int(input("請輸入玩家人數(2~10人):"))
    if 2>num or num>10:
        print(f"輸入錯誤,請重新輸入")

# money=int(input("請輸入共同入場籌碼："))

s=start_game(num,cards)

desk=[cards.pop() for i in range(3)]
print(f"桌牌:{desk}")

win_rate=simulate(s,desk,cards)
for i,v in win_rate.items():
    rate=v[1]
    print(f"{i}|手牌:{s[i]},勝率:{rate:.2%}")
print("-"*30)

desk.append(cards.pop())
print(f"桌牌:{desk}")

win_rate=simulate(s,desk,cards)
for i,v in win_rate.items():
    rate=v[1]
    print(f"{i}|手牌:{s[i]},勝率:{rate:.2%}")
print("-"*30)

desk.append(cards.pop())
print(f"桌牌:{desk}")

win_rate=simulate(s,desk,cards)
for i,v in win_rate.items():
    rate=v[1]
    print(f"{i}|手牌:{s[i]},勝率:{rate:.2%}")


# {每位玩家:最佳分點＋牌}
res={}
for i in range(num):
    seven=s[f"player{i+1}"]+desk
    res[f"player{i+1}"]= best_five(seven)

winner=max(res,key=lambda p : res[p][0])

print("-"*30)

high=[i for i,v in res.items() if v[0]==res[winner][0]]
if len(high)>1:
    print(f"有{len(high)}人平手")

for i in high:
    print(f"贏家是{i},分點:{res[i][0]},牌型:{sorted(res[i][1])}")


