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

def simulate(hand,desk,cards,quit_list,interactions=10000):

    current_hand={}

    for i in range(len(hand)):
        current_hand[f"player{i+1}"]=hand[f"player{i+1}"]+desk

    for i in quit_list:
        if i in current_hand:
            del current_hand[i]


    num=5-len(desk)
   

    length = math.comb(len(cards), num)

    players_win={}
    human=len(current_hand)

    for z in current_hand:
        players_win[z]=[0,0]

    use_random=length>interactions

    if not use_random:
        p=list(combinations(cards,num))
        for k in range(length):
            res={}
            for j in current_hand:
                seven=current_hand[j]+list(p[k])
                res[j]= best_five(seven)

            winner=max(res,key=lambda w : res[w][0])
            high=[i for i,v in res.items() if v[0]==res[winner][0]]
            for a in high:
                players_win[a][0]+=(1 / len(high))

        for f in current_hand:
            players_win[f][1]= players_win[f][0] / length

    else:

        for k in range(interactions):  
            res={}
            for j in current_hand:
                seven=current_hand[j]+list(random.sample(cards,num))
                res[j]= best_five(seven)

            winner=max(res,key=lambda w : res[w][0])
            high=[i for i,v in res.items() if v[0]==res[winner][0]]
            for a in high:
                players_win[a][0]+=(1 / len(high))

        for f in current_hand:
            players_win[f][1]= players_win[f][0] / interactions

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

def distribute_pot(current_chip,quit_list):
    
    s_current_chip=sorted(current_chip.items(),key=lambda x :x[1])
    
    side_pot=[]
    prev=0
    diff_list=[]


    for i,v in s_current_chip:
        diff=v-prev
        if i not in quit_list and diff >0:
            attend=[a for a,b in s_current_chip if a not in quit_list and b-v>=0]
            side_pot.append({"pot":diff*len(attend),"players":attend,"bet":v})
            prev=v

    for i in quit_list:
        money=current_chip[i]
        for a in side_pot:
            if money <= a["bet"]:
                a["pot"]+=money
                break
            elif money>a["bet"]:
                a["pot"]+=a["bet"]
                money-=a["bet"]
    

    return side_pot

def merge_pot(total_pot,quit_list):

    new_total_pot=[{"pot":i["pot"],"players":i["players"]} for i in total_pot]
    merged={}

    for i in quit_list:
        for v in new_total_pot:
            if i in v["players"]:
                v["players"].remove(i)

    for i in new_total_pot:
        key=tuple(sorted(i["players"]))
        if key not in merged:
            merged[key]={"pot":i["pot"],"players":i["players"],"bet":None}
        else:
            merged[key]["pot"]+=i["pot"]    
   

    return list(merged.values())

def chips(player_chips,total_pot,quit_list,dealer,bb,all_in):

    num=len(player_chips)
    current_chips={i:0 for i in player_chips.keys()}
    
    name=list(current_chips.keys())
    
    pos=name.index(dealer)
    star_pos=(pos+2)%len(name)
    name=name[star_pos:]+name[:star_pos]

    name=[i for i in name if i not in quit_list]
    name=[i for i in name if i not in all_in]

    if len(name)==1:
        return player_chips,True,all_in,total_pot,quit_list
    
    else:
        pot=0
        high_chips=0
        call_chips=0
        state=0
        quit_pos=0
        raise_gap=bb
        state_allin=False
        # while sum(1 for i in range(len(money)-1) if money[i]==money[i+1])!=(len(money)-1) or money.count(0)>0:
        while True:
            
            if state==0:
                
                for i in list(name):
                    while True:

                        choose=int(input(f"{i} 請輸入數字1~3: 1:check,2:bet（最低bet）'{raise_gap}', 3:棄牌, 4:all in  :"))
                        if choose==1:
                            action=1
                            break
                        elif choose==2:
                                mini=raise_gap+high_chips
                                add_money=int(input(f"要加到多少？(最低{mini}): "))
                                if add_money<mini:
                                    print("加碼不足最低加碼量，請重新選擇")
                                    continue
                                
                                elif add_money>player_chips[i]:
                                    print("玩家籌碼不足，請重新選擇")
                                    print(f"{i}籌碼剩餘{player_chips[i]}")
                                    continue

                                elif add_money==player_chips[i]:
                                    print(f"此加碼用了{i}所有剩餘籌碼,等同於all in")
                                    action=4
                                    break
                                else:
                                    action=2
                                    break

                        elif choose==3:
                            action=3
                            break
                        elif choose==4:
                            action=4
                            break


                    if action==1:
                        continue
                    elif action==2:
                        
                        current_chips[i]+=(add_money-current_chips[i])
                        position=name.index(i)
                        name=name[position:]+name[:position]
                        # current_chips={k: current_chips[k]  for k in new_name }
                        raise_gap=add_money-high_chips
                        high_chips=add_money
                        call_chips=add_money
                        state=2
                        
                        break

                    elif action==3:
                        quit_list.append(i)
                        name.remove(i)
                    elif action==4:
                        all_in.append(i)
                        
                        all=player_chips[i]
                        print(f"{i}|all_in|本輪加到:{all}籌碼")

                        state_allin=True

                        complete_raise=(raise_gap+high_chips)
                            
                        if (all-current_chips[i])>=complete_raise:
                            
                            state=1
                            raise_gap=all-high_chips
                            current_chips[i]=all
                            position=name.index(i)
                            name=name[position:]+name[:position]
                            high_chips=all
                            call_chips=all
                            name.remove(i)
                            break
                        else:
                            
                            if all>call_chips:
                                
                                state=1
                                current_chips[i]=all
                                call_chips=all
                                position=name.index(i)
                                name=name[position:]+name[:position]
                                name.remove(i)
                                break
                            else:
                                
                                current_chips[i]=all
                                name.remove(i)



                else:
                    break
            
            elif state==1:
                for i in list(name):
                    while True:
                        choose=int(input(f"{i} 請輸入數字1~3: 1:加碼（最低加碼）'{raise_gap+high_chips}',2:跟注(再加碼{call_chips-current_chips[i]}) ,3:棄牌,4:all in :"))
                        if choose==1:
                                mini=raise_gap+high_chips
                                add_money=int(input(f"要加到多少？(最低{mini})"))
                                if add_money<mini:
                                    print("加碼不足最低加碼量，請重新選擇")
                                    continue
                                
                                elif add_money>player_chips[i]:
                                    print("玩家籌碼不足，請重新選擇")
                                    print(f"{i}籌碼剩餘{player_chips[i]}")
                                    continue

                                elif add_money==player_chips[i]:
                                    print(f"此加碼用了{i}所有剩餘籌碼,等同於all in")
                                    action=4
                                    break
                                else:
                                    action=1
                                    break

                        elif choose==2:
                            if call_chips>player_chips[i]:
                                print("玩家籌碼不足跟注籌碼,系統判定為all in")
                                action=4
                                break
                            elif call_chips==player_chips[i]:
                                print("玩家所有籌碼與跟注相同,系統判定為all in")
                                action=4
                                break
                            else:
                                action=2
                                break
                        elif choose==3:
                            action=3
                            break
                        elif choose==4:
                            action=4
                            break
                    
                    if action==1:
                        
                        current_chips[i]+=(add_money-current_chips[i])
                        position=name.index(i)
                        name=name[position:]+name[:position]
                        raise_gap=add_money-high_chips
                        # current_chips={k: current_chips[k]  for k in new_name }
                        high_chips=add_money
                        call_chips=add_money
                        state=2
                        
                        break

                    elif action==2:
                        current_chips[i]+=(call_chips-current_chips[i])
                        
                    elif action==3:
                        quit_list.append(i)
                        name.remove(i)
                    elif action==4:
                        all_in.append(i)
                        
                        all=player_chips[i]
                        print(f"{i}|all_in|本輪加到:{all}籌碼")

                        state_allin=True

                        complete_raise=(raise_gap+high_chips)
                            
                        if (all-current_chips[i])>=complete_raise:
                            
                            state=1
                            raise_gap=all-high_chips
                            current_chips[i]=all
                            position=name.index(i)
                            name=name[position:]+name[:position]
                            high_chips=all
                            call_chips=all
                            name.remove(i)
                            break
                        else:
                            
                            if all>call_chips:
                            
                                state=1
                                current_chips[i]=all
                                call_chips=all
                                position=name.index(i)
                                name=name[position:]+name[:position]
                                name.remove(i)
                                break
                            else:
                                
                                current_chips[i]=all
                                name.remove(i)
                            
                else:
                    break


            elif state==2:
                for i in list(name[1:]):
                    while True:
                        choose=int(input(f"{i} 請輸入數字1~3: 1:加碼（最低加碼）'{raise_gap+high_chips}',2:跟注(再加碼{call_chips-current_chips[i]}) ,3:棄牌,4:all in :"))
                        if choose==1:
                            mini=raise_gap+high_chips
                            add_money=int(input(f"要加到多少？(最低{mini})"))
                            if add_money<mini:
                                print("加碼不足最低加碼量，請重新選擇")
                                continue
                            
                            elif add_money>player_chips[i]:
                                print("玩家籌碼不足，請重新選擇")
                                print(f"{i}籌碼剩餘{player_chips[i]}")
                                continue

                            elif add_money==player_chips[i]:
                                print(f"此加碼用了{i}所有剩餘籌碼,等同於all in")
                                action=4
                                break
                            else:
                                action=1
                                break

                        elif choose==2:
                            if call_chips>player_chips[i]:
                                print("玩家籌碼不足跟注籌碼,系統判定為all in")
                                action=4
                                break
                            elif call_chips==player_chips[i]:
                                print("玩家所有籌碼與跟注相同,系統判定為all in")
                                action=4
                                break
                            else:
                                action=2
                                break
                        elif choose==3:
                            action=3
                            break
                        elif choose==4:
                            action=4
                            break
                    
                    if action==1:
                        
                        current_chips[i]+=(add_money-current_chips[i])
                        position=name.index(i)
                        name=name[position:]+name[:position]
                        raise_gap=add_money-high_chips
                        # current_chips={k: current_chips[k]  for k in new_name }
                        high_chips=add_money
                        call_chips=add_money
                        state=2
                        
                        break

                    elif action==2:
                        current_chips[i]+=(call_chips-current_chips[i])
                        
                    elif action==3:
                        quit_list.append(i)
                        name.remove(i)
                    elif action==4:
                        all_in.append(i)
                        
                        all=player_chips[i]
                        print(f"{i}|all_in|本輪加到:{all}籌碼")

                        state_allin=True

                        complete_raise=(raise_gap+high_chips)
                            
                        if (all-current_chips[i])>=complete_raise:
                            
                            state=1
                            raise_gap=all-high_chips
                            current_chips[i]=all
                            position=name.index(i)
                            name=name[position:]+name[:position]
                            high_chips=all
                            call_chips=all
                            name.remove(i)
                            break
                        else:
                            
                            if all>call_chips:
                                
                                state=1
                                current_chips[i]=all
                                call_chips=all
                                position=name.index(i)
                                name=name[position:]+name[:position]
                                name.remove(i)
                                break
                            else:
                                
                                current_chips[i]=all
                                name.remove(i)
                else:
                    break




        if num-len(quit_list)==1:
            for i in player_chips:
                player_chips[i]-=current_chips[i]
            pot=sum(i for i in current_chips.values())
            all_add=0
            for a in total_pot:
                all_add+=a["pot"]
            all_win=pot+all_add
            player_chips[name[0]]+=(all_win)
            print("-"*30)
            print(f"本輪結束：{name[0]} 獲勝")
            return player_chips,False,name[0],all_win,quit_list
        else:

            for i in player_chips:
                player_chips[i]-=current_chips[i]

            if state_allin==True:
                current_pot=distribute_pot(current_chips,quit_list)
                total_pot.extend(current_pot)

            else:
                p=sum(i for i in current_chips.values())
                current_pot={"pot":p,"players":name,"bet":high_chips}
                total_pot.append(current_pot)

            s_total_pot=sorted(total_pot,key=lambda x:len(x["players"]),reverse=True)
            
            total_pot=merge_pot(s_total_pot,quit_list)
            

            return player_chips,True,all_in,total_pot,quit_list

def first_chips(player_chips,total_pot,quit_list,dealer,sb,bb,all_in):
    
    num=len(player_chips)
    current_chips={i:0 for i in player_chips.keys()}
    
    name=list(current_chips.keys())
    

    pos=name.index(dealer)

    star_pos=(pos+1)%len(name)
    name=name[star_pos:]+name[:star_pos]
    
    sb_player=name[0]
    bb_player=name[1]
    
    sb_all_in=False
    bb_all_in=False
    state_allin=False

    if player_chips[sb_player]>sb:
        current_chips[sb_player]=sb
        print(f"已自動放置[小盲]{sb_player}:{sb}")
    else:
        if player_chips[sb_player]==sb:
            print(f"{sb_player} 總籌碼和小盲一樣,系統判定all in")
        else:
            print(f"{sb_player} 總籌碼比小盲少,系統判定all in")

        all_in.append(sb_player)      
        all=player_chips[sb_player]
        print(f"{sb_player}|all_in|本輪加到:{all}籌碼")
        state_allin=True
        current_chips[sb_player]=all
        sb_all_in=True
        

    if player_chips[bb_player]>bb:
        current_chips[bb_player]=bb
        print(f"已自動放置[大盲]{bb_player}:{bb}")
    else:
        if player_chips[bb_player]==bb:
            print(f"{bb_player} 總籌碼和大盲一樣,系統判定all in")
        else:
            print(f"{bb_player} 總籌碼比大盲少,系統判定all in")

        all_in.append(bb_player)      
        all=player_chips[bb_player]
        print(f"{bb_player}|all_in|本輪加到:{all}籌碼")
        state_allin=True
        current_chips[bb_player]=all
        bb_all_in=True


    pos=name.index(dealer)
    star_pos=(pos+3)%len(name)
    name=name[star_pos:]+name[:star_pos]

    if sb_all_in==True:
        name.remove(sb_player)
    if bb_all_in==True:
        name.remove(bb_player)


    print("-"*40)
    pot=0
    high_chips=bb
    raise_gap=bb
    state=0
    call_chips=bb
    
    # while sum(1 for i in range(len(money)-1) if money[i]==money[i+1])!=(len(money)-1) or money.count(0)>0:
    while True:
        
        if state==0:
            for i in list(name):
                while True:
                    
                    choose=int(input(f"{i} 請輸入數字1~3: 1:加碼（最低加碼）'{raise_gap+high_chips}',2:跟注(再加碼{call_chips-current_chips[i]}),3:棄牌,4:all in :"))
                    if choose==1:
                        mini=raise_gap+high_chips
                        add_money=int(input(f"要加到多少？(最低{mini}): "))
                        if add_money<mini:
                            print("加碼不足最低加碼量，請重新選擇")
                            continue
                        
                        elif add_money>player_chips[i]:
                            print("玩家籌碼不足，請重新選擇")
                            print(f"{i}籌碼剩餘{player_chips[i]}")
                            continue

                        elif add_money==player_chips[i]:
                            print(f"此加碼用了{i}所有剩餘籌碼,等同於all in")
                            action=4
                            break
                        else:
                            action=1
                            break

                    elif choose==2:
                        if call_chips>player_chips[i]:
                            print("玩家籌碼不足跟注籌碼,系統判定為all in")
                            action=4
                            break
                        elif call_chips==player_chips[i]:
                            print("玩家所有籌碼與跟注相同,系統判定為all in")
                            action=4
                            break
                        else:
                            action=2
                            break
                    elif choose==3:
                        action=3
                        break
                    elif choose==4:
                        action=4
                        break

      # 分隔方便觀看 # 分隔方便觀看 # 分隔方便觀看 # 分隔方便觀看 # 分隔方便觀看 # 分隔方便觀看 # 分隔方便觀看
                            
                if action==1:

                    current_chips[i]+=(add_money-current_chips[i])
                    position=name.index(i)
                    name=name[position:]+name[:position]
                    # current_chips={k: current_chips[k]  for k in new_name }
                    raise_gap=add_money-high_chips
                    high_chips=add_money
                    call_chips=add_money
                    state=2
                    break

                elif action==2:
                    current_chips[i]+=(high_chips-current_chips[i])
                
                    
                elif action==3:
                    quit_list.append(i)
                    name.remove(i)
                    
                elif action==4:
                    all_in.append(i)
                    
                    all=player_chips[i]
                    print(f"{i}|all_in|本輪加到:{all}籌碼")

                    state_allin=True

                    complete_raise=(raise_gap+high_chips)
                        
                    if (all-current_chips[i])>=complete_raise:
                        
                        state=1
                        raise_gap=all-high_chips
                        current_chips[i]=all
                        position=name.index(i)
                        name=name[position:]+name[:position]
                        high_chips=all
                        call_chips=all
                        name.remove(i)
                        break
                    else:
                        
                        if all>call_chips:
                            
                            state=1
                            current_chips[i]=all
                            call_chips=all
                            position=name.index(i)
                            name=name[position:]+name[:position]
                            name.remove(i)
                            break
                        else:
                            
                            current_chips[i]=all
                            name.remove(i)
                            

                
            else:
                break
        


        elif state==1:
            for i in list(name):
                while True:
                    choose=int(input(f"{i} 請輸入數字1~3: 1:加碼（最低加碼）'{raise_gap+high_chips}',2:跟注(再加碼{call_chips-current_chips[i]}) ,3:棄牌,4:all in :"))
                    if choose==1:
                        mini=raise_gap+high_chips
                        add_money=int(input(f"要加到多少？(最低{mini})"))
                        if add_money<mini:
                            print("加碼不足最低加碼量，請重新選擇")
                            continue
                        
                        elif add_money>player_chips[i]:
                            print("玩家籌碼不足，請重新選擇")
                            print(f"{i}籌碼剩餘{player_chips[i]}")
                            continue

                        elif add_money==player_chips[i]:
                            print(f"此加碼用了{i}所有剩餘籌碼,等同於all in")
                            action=4
                            break
                        else:
                            action=1
                            break

                    elif choose==2:
                        if call_chips>player_chips[i]:
                            print("玩家籌碼不足跟注籌碼,系統判定為all in")
                            action=4
                            break
                        elif call_chips==player_chips[i]:
                            print("玩家所有籌碼與跟注相同,系統判定為all in")
                            action=4
                            break
                        else:
                            action=2
                            break
                    elif choose==3:
                        action=3
                        break
                    elif choose==4:
                        action=4
                        break
                
                if action==1:
                    
                    current_chips[i]+=(add_money-current_chips[i])
                    position=name.index(i)
                    name=name[position:]+name[:position]
                    raise_gap=add_money-high_chips
                    # current_chips={k: current_chips[k]  for k in new_name }
                    high_chips=add_money
                    call_chips=add_money
                    state=2
                    
                    break

                elif action==2:
                    current_chips[i]+=(call_chips-current_chips[i])
                    
                    
                elif action==3:
                    quit_list.append(i)
                    name.remove(i)
                elif action==4:
                    all_in.append(i)
                    
                    all=player_chips[i]
                    print(f"{i}|all_in|本輪加到:{all}籌碼")

                    state_allin=True

                    complete_raise=(raise_gap+high_chips)
                        
                    if (all-current_chips[i])>=complete_raise:
                        
                        state=1
                        raise_gap=all-high_chips
                        current_chips[i]=all
                        position=name.index(i)
                        name=name[position:]+name[:position]
                        high_chips=all
                        call_chips=all
                        name.remove(i)
                        break
                    else:
                        
                        if all>call_chips:
                            
                            state=1
                            current_chips[i]=all
                            call_chips=all
                            position=name.index(i)
                            name=name[position:]+name[:position]
                            name.remove(i)
                            break
                        else:
                            
                            current_chips[i]=all
                            name.remove(i)
                        
            else:
                break


        elif state==2:
            for i in list(name[1:]):
                while True:
                    choose=int(input(f"{i} 請輸入數字1~3: 1:加碼（最低加碼）'{raise_gap+high_chips}',2:跟注(再加碼{call_chips-current_chips[i]}) ,3:棄牌,4:all in :"))
                    if choose==1:
                        mini=raise_gap+high_chips
                        add_money=int(input(f"要加到多少？(最低{mini})"))
                        if add_money<mini:
                            print("加碼不足最低加碼量，請重新選擇")
                            continue
                        
                        elif add_money>player_chips[i]:
                            print("玩家籌碼不足，請重新選擇")
                            print(f"{i}籌碼剩餘{player_chips[i]}")
                            continue

                        elif add_money==player_chips[i]:
                            print(f"此加碼用了{i}所有剩餘籌碼,等同於all in")
                            action=4
                            break
                        else:
                            action=1
                            break

                    elif choose==2:
                        if call_chips>player_chips[i]:
                            print("玩家籌碼不足跟注籌碼,系統判定為all in")
                            action=4
                            break
                        elif call_chips==player_chips[i]:
                            print("玩家所有籌碼與跟注相同,系統判定為all in")
                            action=4
                            break
                        else:
                            action=2
                            break
                    elif choose==3:
                        action=3
                        break
                    elif choose==4:
                        action=4
                        break
                
                if action==1:
                    
                    current_chips[i]+=(add_money-current_chips[i])
                    position=name.index(i)
                    name=name[position:]+name[:position]
                    raise_gap=add_money-high_chips
                    # current_chips={k: current_chips[k]  for k in new_name }
                    high_chips=add_money
                    call_chips=add_money
                    state=2
                    
                    break

                elif action==2:
                    current_chips[i]+=(call_chips-current_chips[i])
                    
                elif action==3:
                    quit_list.append(i)
                    name.remove(i)
                elif action==4:
                    all_in.append(i)
                    
                    all=player_chips[i]
                    print(f"{i}|all_in|本輪加到:{all}籌碼")

                    state_allin=True

                    complete_raise=(raise_gap+high_chips)
                        
                    if (all-current_chips[i])>=complete_raise:
                        
                        state=1
                        raise_gap=all-high_chips
                        current_chips[i]=all
                        position=name.index(i)
                        name=name[position:]+name[:position]
                        high_chips=all
                        call_chips=all
                        name.remove(i)
                        break
                    else:
                        
                        if all>call_chips:
                            
                            state=1
                            current_chips[i]=all
                            call_chips=all
                            position=name.index(i)
                            name=name[position:]+name[:position]
                            name.remove(i)
                            break
                        else:
                            
                            current_chips[i]=all
                            name.remove(i)
            else:
                break




    if num-len(quit_list)==1:
        for i in player_chips:
            player_chips[i]-=current_chips[i]
        pot=sum(i for i in current_chips.values())
        all_add=0
        for a in total_pot:
            all_add+=a["pot"]
        all_win=pot+all_add
        player_chips[name[0]]+=(all_win)
        print("-"*30)
        print(f"本輪結束：{name[0]} 獲勝")
        return player_chips,False,name[0],all_win,quit_list
    else:

        for i in player_chips:
            player_chips[i]-=current_chips[i]

        if state_allin==True:
            current_pot=distribute_pot(current_chips,quit_list)
            total_pot.extend(current_pot)

        else:
            p=sum(i for i in current_chips.values())
            current_pot={"pot":p,"players":name,"bet":high_chips}
            total_pot.append(current_pot)

        s_total_pot=sorted(total_pot,key=lambda x:len(x["players"]),reverse=True)
        
        total_pot=merge_pot(s_total_pot,quit_list)
        

        return player_chips,True,all_in,total_pot,quit_list

# ________________________________________________________________________

num=0

while 2>num or num>10:
    num=int(input("請輸入玩家人數(2~10人):"))
    if 2>num or num>10:
        print(f"輸入錯誤,請重新輸入")
        continue

player_chips={}
for i in range(num):
    money=int(input(f"player{i+1},請輸入入場籌碼："))
    player_chips[f"player{i+1}"]=money

dealer=input(f"請輸入莊家位(player1~{num})：")
dealer_name_list=[i for i in player_chips]
dealer_pos=dealer_name_list.index(dealer)
dealer_name_list=dealer_name_list[dealer_pos:]+dealer_name_list[:dealer_pos]

chip_state=True
circle=0
while chip_state==True:
    if circle !=0:
        dealer=dealer_name_list[1]
        print("--------------------新一輪開始--------------------")
        print(f"本輪莊家位：{dealer}")
        print("")
        dealer_name_list=dealer_name_list[1:]+dealer_name_list[:1]


    sb=int(input("請輸入小盲籌碼："))
    bb=int(input("請輸入大盲籌碼："))

    print("-"*30)

    game_state=True
    deck=[i for i in range(2,15)]
    flower=['♠','♥','♣','♦']
    cards=[]
    for i in flower:
        for j in deck:
            cards.append((j,i))

    s=start_game(num,cards)
    desk=[]
    quit_list=[]
    all_in=[]

    win_rate=simulate(s,desk,cards,quit_list)
    for i,v in win_rate.items():
        rate=v[1]
        print(f"{i}|手牌：{display(s[i])},勝率：{rate:.2%}")


    total_pot=[]
    print("")
    print("---------------下注時段---------------")
    print("第一輪下注:")
    c,q,w,t,o=first_chips(player_chips,total_pot,quit_list,dealer,sb,bb,all_in)
    total_pot=t
    all_in=w
    game_state=q

    quit_list=o

    print("")
    print("---------------籌碼資訊---------------")

    if game_state==True:
        round=1
        for i in total_pot:
            if round==1:
                print(f"主牌池籌碼：{i["pot"]},參與玩家：{sorted(i["players"])}")
                round+=1
            else:
                print(f"邊池籌碼:{i["pot"]},參與玩家：{sorted(i["players"])}")

        print("")

        for i,v in c.items():
            print(f"{i}目前籌碼：{v}")

        print("")
        print("---------------牌面資訊---------------")
        

        desk=[cards.pop() for i in range(3)]
        print(f"桌牌:{display(desk)}")

        win_rate=simulate(s,desk,cards,quit_list)
        for i,v in win_rate.items():
            rate=v[1]
            current_card=s[i]+desk
            cards_type=type(best_five(current_card)[0])
            print(f"{i}|手牌:{display(s[i])},最佳牌型：{cards_type},勝率:{rate:.2%}")
        print("")
        print("---------------下注時段---------------")

        print("第二輪下注: ")
        c,q,w,t,o=chips(player_chips,total_pot,quit_list,dealer,bb,all_in)
        total_pot=t
        
        game_state=q
        all_in=w
        quit_list=o

        if game_state==True:
            round=1
            print("")
            print("---------------籌碼資訊---------------")
            for pot in total_pot:
                if round==1:
                    print(f"主牌池籌碼：{pot["pot"]},參與玩家：{sorted(pot["players"])}")
                    round+=1
                else:
                    print(f"邊池籌碼:{pot["pot"]},參與玩家：{sorted(pot["players"])}")
            print("")
            for i,v in c.items():
                print(f"{i}目前籌碼：{v}")
            print("")
            print("---------------牌面資訊---------------")

            desk.append(cards.pop())
            print(f"桌牌:{display(desk)}")

            win_rate=simulate(s,desk,cards,quit_list)
            for i,v in win_rate.items():
                rate=v[1]
                current_card=s[i]+desk
                cards_type=type(best_five(current_card)[0])
                print(f"{i}|手牌:{display(s[i])},最佳牌型：{cards_type},勝率:{rate:.2%}")
            print("")
            print("---------------下注時段---------------")

            print("第三輪下注:")
            c,q,w,t,o=chips(player_chips,total_pot,quit_list,dealer,bb,all_in)
            total_pot=t
            game_state=q
            all_in=w
            quit_list=o 

            if game_state==True:
                print("")
                print("---------------籌碼資訊---------------")
                round=1
                for pot in total_pot:
                    if round==1:
                        print(f"主牌池籌碼：{pot["pot"]},參與玩家：{sorted(pot["players"])}")
                        round+=1
                    else:
                        print(f"邊池籌碼:{pot["pot"]},參與玩家：{sorted(pot["players"])}")
                print("")
                for i,v in c.items():
                    print(f"{i}目前籌碼：{v}")
                print("")
                print("---------------牌面資訊---------------")

                desk.append(cards.pop())
                print(f"桌牌:{display(desk)}")

                win_rate=simulate(s,desk,cards,quit_list)
                for i,v in win_rate.items():
                    rate=v[1]
                    current_card=s[i]+desk
                    cards_type=type(best_five(current_card)[0])
                    print(f"{i}|手牌:{display(s[i])},最佳牌型：{cards_type},勝率:{rate:.2%}")
                print("")
                print("---------------下注時段---------------")

                print("第四輪下注:")
                c,q,w,t,o=chips(player_chips,total_pot,quit_list,dealer,bb,all_in)
                total_pot=t
                all_in=w
                game_state=q
                quit_list=o
                    
                if game_state==True:
                    print("")
                    print("---------------籌碼資訊---------------")
                    round=1
                    for pot in total_pot:
                        if round==1:
                            print(f"主牌池籌碼：{pot["pot"]},參與玩家：{sorted(pot["players"])}")
                            round+=1
                        else:
                            print(f"邊池籌碼:{pot["pot"]},參與玩家：{sorted(pot["players"])}")
                    print("")
                    for i,v in c.items():
                        print(f"{i}目前籌碼：{v}")
                    print("-"*20+"最終牌型比大小"+"-"*20)
                
                    # {每位玩家:最佳分點＋牌}
                    
                    remain_players=s
                    for i in quit_list:
                        if i in remain_players:
                            del remain_players[i]
                    res={}
                    for i in remain_players:
                        seven=remain_players[i]+desk
                        res[i]= best_five(seven)

                    
                    # in_game={}
                    # for f in total_pot:
                    #     win=None
                    #     for pp in f["players"]:
                    #         in_game[pp]=res[pp]
                    #     winner=max(in_game,key=lambda gg : in_game[gg][0])
                    #     high=[i for i,v in in_game.items() if v[0]==in_game[winner][0]]
                    #     if len(high)>1:
                    #         print(f"有{len(high)}人平手")
                    round=1
                    for f in total_pot:
                        in_game={i:res[i] for i in f["players"]}
                        winner=max(in_game,key=lambda gg:in_game[gg][0])
                        high=[i for i,v in in_game.items() if v[0]==in_game[winner][0]]
                        
                        
                        if round==1:
                            for i in high:
                                print(f"-----主牌池 籌碼{f["pot"]}-----")
                                if len(high)>1:
                                    print(f"有{len(high)}人平手")

                                print(f"贏家是{i},牌型:{type(res[i][0])},最佳五張牌:{display(sorted(res[i][1]))}")
                                print(f"贏得籌碼{(f["pot"]/len(high))}")
                                player_chips[i]+=(f["pot"]/len(high))
                                

                        else:
                            for i in high:
                                print(f"-----邊池{round-1}  籌碼{f["pot"]}-----")
                                if len(high)>1:
                                    print(f"有{len(high)}人平手")
                                    
                                print(f"贏家是{i},牌型:{type(res[i][0])},最佳五張牌:{display(sorted(res[i][1]))}")
                                print(f"贏得籌碼{(f["pot"]/len(high))}")
                                player_chips[i]+=(f["pot"]/len(high))
                        round+=1


                    print("")

                    for i,v in player_chips.items():
                        print(f"{i}目前籌碼量：{v}")
                    print("")
                    circle+=1
                    switch=sum( 1 for i in player_chips if player_chips[i]==0)
                    if switch!=0:
                        chip_state=False
                        print("有玩家籌碼已歸零,遊戲結束")

                else:
                    for i,v in c.items():
                        print(f"{i}目前籌碼：{v}")
                    print("-"*30)
                    circle+=1
                    switch=sum( 1 for i in player_chips if player_chips[i]==0)
                    if switch!=0:
                        chip_state=False
                        print("有玩家籌碼已歸零,遊戲結束")
            else:
                for i,v in c.items():
                    print(f"{i}目前籌碼：{v}")
                print("-"*30)
                circle+=1
                switch=sum( 1 for i in player_chips if player_chips[i]==0)
                if switch!=0:
                    chip_state=False
                    print("有玩家籌碼已歸零,遊戲結束")
        else:
            for i,v in c.items():
                print(f"{i}目前籌碼：{v}")
            print("-"*30)
            circle+=1
            switch=sum( 1 for i in player_chips if player_chips[i]==0)
            if switch!=0:
                chip_state=False
                print("有玩家籌碼已歸零,遊戲結束")
    else:
        for i,v in c.items():
            print(f"{i}目前籌碼：{v}")
        print("-"*30)
        circle+=1
        switch=sum( 1 for i in player_chips if player_chips[i]==0)
        if switch!=0:
            chip_state=False
            print("有玩家籌碼已歸零,遊戲結束")