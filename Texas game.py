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
    five_cards=[]
    for i in five :
        rank=hand_rank(i)
        if  best is None or best<=rank:
            best=rank
            five_cards =i
    return best,five_cards 
# 分點＋牌型


def start_game(num,cards):
    random.shuffle(cards)
    players={}
    for p in range(num):
        players[f"player{p+1}"]=[cards.pop(),cards.pop()]
    return players

def star_chips(num):
    player_chip={}
    for i in range(num):
        money=int(input("請輸入最初籌碼量："))
        player_chip[f"player{i}"].append(money)

    return player_chip

# def simulate(hand,desk,cards):

#     current_hand={}

#     for i in range(len(hand)):
#         current_hand[f"player{i+1}"]=hand[f"player{i+1}"]+desk

#     num=5-len(desk)
#     p=list(combinations(cards,num))

#     length = math.comb(len(cards), num)

#     players_win={}
#     human=len(hand)

#     for z in range(human):
#         players_win[f"player{z+1}"]=[0,0]


#     for k in range(length):
#         res={}
#         for j in range(len(hand)):
#             seven=current_hand[f"player{j+1}"]+list(p[k])
#             res[f"player{j+1}"]= best_five(seven)

#         winner=max(res,key=lambda w : res[w][0])
#         high=[i for i,v in res.items() if v[0]==res[winner][0]]
#         for a in range(len(high)):
#             players_win[high[a]][0]+=1 / len(high)

#     for f in range(human):
#         players_win[f"player{f+1}"][1]= players_win[f"player{f+1}"][0] / length

#     return players_win

def simulate(hand,desk,cards,interactions=10000):

    current_hand={}

    for i in range(len(hand)):
        current_hand[f"player{i+1}"]=hand[f"player{i+1}"]+desk

    num=5-len(desk)
   

    length = math.comb(len(cards), num)

    players_win={}
    human=len(hand)

    for z in range(human):
        players_win[f"player{z+1}"]=[0,0]

    use_random=length>interactions

    if not use_random:
        p=list(combinations(cards,num))
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

    else:

        for k in range(interactions):  
            res={}
            for j in range(len(hand)):
                seven=current_hand[f"player{j+1}"]+list(random.sample(cards,num))
                res[f"player{j+1}"]= best_five(seven)

            winner=max(res,key=lambda w : res[w][0])
            high=[i for i,v in res.items() if v[0]==res[winner][0]]
            for a in range(len(high)):
                players_win[high[a]][0]+=1 / len(high)

        for f in range(human):
            players_win[f"player{f+1}"][1]= players_win[f"player{f+1}"][0] / interactions

    return players_win

def display(cards):
    rank_map={11:"J",12:"Q",13:"K",14:"A"}
    rank_display=[]
    for i,v in cards:
        rank_display.append(rank_map.get(i,str(i))+v)
    
    return rank_display

def type(point_record):
    
    point_map={1:"單張",2:"一對",3:"兩對",4:"三條",5:"順子",6:"同花",7:"葫蘆",8:"四條",9:"同花順"}
    card_type=[]
    card_type=point_map.get(point_record[0])

    return card_type

def chips(player_chips,total_pot,quit_list):
    num=len(player_chips)
    current_chips={}
    for i in range(num):
        current_chips[f"player{i+1}"]=[0]
    
    name=list(current_chips.keys())
    
    for i in name:
        if i in quit_list:
            name.remove(i)

    
    pot=0
    high_chips=0
    state=0
    # while sum(1 for i in range(len(money)-1) if money[i]==money[i+1])!=(len(money)-1) or money.count(0)>0:
    while True:
        
        
        if state==0:
            for i in name:
                action=int(input(f"{i} 請輸入數字1~3: 1:check,2:加碼,3:棄牌 :"))
                if action==1:
                    current_chips[i][0]+=0
                elif action==2:
                    add_money=int(input("要加到多少？"))
                    current_chips[i][0]+=add_money
                    position=name.index(i)
                    name=name[position:]+name[:position]
                    # current_chips={k: current_chips[k]  for k in new_name }
                    high_chips=add_money
                    state=2
                    pot+=add_money
                    break

                elif action==3:
                    quit_list.append(i)
                    position=name.index(i)
                    del name[position]
                    if len(name)==1:
                        pot=sum(i[0] for i in current_chips.values())
                        for i,v in player_chips.items():
                            v[0]-=current_chips[i][0]

                        player_chips[name[0]][0]+=(pot+total_pot)
                        # print(f"此局{name[0]}獲勝")
                        return player_chips,False,name[0],pot,quit_list
    

            else:
                break
        


        else:
            for i in name[1:]:
                action=int(input(f"{i} 請輸入數字1~3: 1:加碼,2:跟注,3:棄牌 :"))
                
                if action==1:
                    add_money=int(input("要加到多少？"))
                    current_chips[i][0]+=add_money
                    position=name.index(i)
                    name=name[position:]+name[:position]
                    # current_chips={k: current_chips[k]  for k in name }
                    high_chips=add_money
                    
                    break

                elif action==2:
                    current_chips[i][0]+=(high_chips-current_chips[i][0])
                    pot+=(high_chips-current_chips[i][0])
                elif action==3:
                    quit_list.append(i)
                    position=name.index(i)
                    del name[position]
                    if len(name)==1:
                        pot=sum(i[0] for i in current_chips.values())
                        for i,v in player_chips.items():
                            v[0]-=current_chips[i][0]

                        player_chips[name[0]][0]+=(pot+total_pot)
                        # print(f"此局{new_name[0]}獲勝")
                        return player_chips,False,name[0],pot,quit_list

            else:
                break


    for i,v in player_chips.items():
        v[0]-=current_chips[i][0]

    pot=sum(i[0] for i in current_chips.values())

    return player_chips,True,name[0],pot,quit_list

# ________________________________________________________________________

game_state=True
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

player_chips={}
for i in range(num):
    money=int(input(f"player{i+1},請輸入入場籌碼："))
    player_chips[f"player{i+1}"]=[money]
    

s=start_game(num,cards)
desk=[]

win_rate=simulate(s,desk,cards)
for i,v in win_rate.items():
    rate=v[1]
    print(f"{i}|手牌：{display(s[i])},勝率：{rate:.2%}")
print("-"*30)

quit_list=[]
total_pot=0
# 第一次下注
c,q,w,t,o=chips(player_chips,total_pot,quit_list)
for i,v in c.items():
    print(f"{i}目前籌碼：{v}")
print("-"*30)
total_pot+=t
game_state=q
quit_list=o

if game_state==True:
    desk=[cards.pop() for i in range(3)]
    print(f"桌牌:{display(desk)}")

    win_rate=simulate(s,desk,cards)
    for i,v in win_rate.items():
        rate=v[1]
        current_card=s[i]+desk
        cards_type=type(best_five(current_card)[0])
        print(f"{i}|手牌:{display(s[i])},最佳牌型：{cards_type},勝率:{rate:.2%}")
    print("-"*30)

    # 第二次下注
    c,q,w,t,o=chips(player_chips,total_pot,quit_list)
    for i,v in c.items():
        print(f"{i}目前籌碼：{v}")
    print("-"*30)
    total_pot+=t
    game_state=q
    quit_list=o

    if game_state==True:

        desk.append(cards.pop())
        print(f"桌牌:{display(desk)}")

        win_rate=simulate(s,desk,cards)
        for i,v in win_rate.items():
            rate=v[1]
            current_card=s[i]+desk
            cards_type=type(best_five(current_card)[0])
            print(f"{i}|手牌:{display(s[i])},最佳牌型：{cards_type},勝率:{rate:.2%}")
        print("-"*30)

        # 第三次下注
        c,q,w,t,o=chips(player_chips,total_pot,quit_list)
        for i,v in c.items():
            print(f"{i}目前籌碼：{v}")
        print("-"*30)
        total_pot+=t
        game_state=q
        quit_list=o

        if game_state==True:

            desk.append(cards.pop())
            print(f"桌牌:{display(desk)}")

            win_rate=simulate(s,desk,cards)
            for i,v in win_rate.items():
                rate=v[1]
                current_card=s[i]+desk
                cards_type=type(best_five(current_card)[0])
                print(f"{i}|手牌:{display(s[i])},最佳牌型：{cards_type},勝率:{rate:.2%}")

            # 第四次下注
            c,q,w,t,o=chips(player_chips,total_pot,quit_list)
            for i,v in c.items():
                print(f"{i}目前籌碼：{v}")
            print("-"*30)
            total_pot+=t
            game_state=q
            quit_list=o
                
            if game_state==True:
            
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
                    # print(f"贏家是{i},分點:{res[i][0]},牌型:{display(sorted(res[i][1]))}")
                    print(f"贏家是{i},牌型:{type(res[i][0])},最佳五張牌:{display(sorted(res[i][1]))}")
                    player_chips[i][0]+=(total_pot/len(high))

                for i,v in player_chips.items():
                    print(f"{i}目前籌碼量：{v}")

            else:
                print(f"遊戲結束:{w}獲勝")
        else:
            print(f"遊戲結束:{w}獲勝")
    else:
        print(f"遊戲結束:{w}獲勝")
else:
    print(f"遊戲結束:{w}獲勝")