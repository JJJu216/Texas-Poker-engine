# cards=[(12, '♣'), (8, '♦')]
# rank_map={11:"J",12:"Q",13:"K",14:"A"}

# for i,v in cards:
#     rank_display=rank_map.get(i,str(i))
    
# mini=[]
# for x,y in rank_display:
#     mini.append=[x+y]
    
# print(cards)


# cards=[(12, '♣'), (8, '♦')]

# rank_map={11:"J",12:"Q",13:"K",14:"A"}
# rank_display=[]
# for i,v in cards:
#     rank_display.append((rank_map.get(i,str(i))+v))

# print(rank_display)


# for n in range(1,82):
#     i= (n-1) // 9 +1
#     j= (n-1)%9 +1
#     print(f"{i}*{j}={i*j} ",end=" ")
#     if j>=9:
#         print()

# def distribute_pot(current_chip,quit_list):

#     s_current_chip=sorted(current_chip.items(),key=lambda x :x[1])
#     print("排序",s_current_chip)
#     side_pot=[]
#     prev=0
#     diff_list=[]


#     for i,v in s_current_chip:
#         diff=v-prev
#         if i not in quit_list and diff >0:
#             attend=[a for a,b in s_current_chip if a not in quit_list and b-v>=0]
#             side_pot.append({"pot":diff*len(attend),"players":attend,"bet":v})
#             prev=v

#     for i in quit_list:
#         money=current_chip[i]
#         for a in side_pot:
#             if money <= a["bet"]:
#                 a["pot"]+=money
#                 break
#             elif money>a["bet"]:
#                 a["pot"]+=a["bet"]
#                 money-=a["bet"]

#     return side_pot

# def merge_pot(total_pot):

#     total_pot2=total_pot
#     new_total_pot=[]
#     num_players=len(total_pot[0]["players"])
#     pot=total_pot[0]["pot"]
#     player=total_pot[0]["players"]
#     for i in list(total_pot2[1:]):
#         if len(i["players"])==num_players:
#             pot+=i["pot"]
#             player=i["players"]
            
#         else:
#             num_players=len(i["players"])
#             new_total_pot.append({"pot":pot,"players":player})

#     return new_total_pot


# import random

# res=[]
# for i in range(2):
#     current_chip={}
#     for i in range(8):
#         current_chip[f"player{i+1}"]=random.randrange(50,101,50)

#     quit_list=["player5"]

#     d=distribute_pot(current_chip,quit_list)

#     res.extend(d)


# merge_pot(res)
# print(res)


# current_chip={ f"player{i+1}":1000 for i in range(4)}
# print(current_chip)
# print("-"*15)

# for i,v in current_chip.items():
#     print(i)
#     print(v)

# total_pot=[{'pot': 60, 'players': ['player1', 'player2', 'player3'], 'bet': 20},{'pot': 100, 'players': ['player1', 'player2'], 'bet': 50}]

# round=1
# for i in total_pot:
#         if round==1:
#             print(f"主牌池籌碼：{i["pot"]},參與玩家：{i["players"]}")
#             round+=1
#         else:
#             print(f"邊池籌碼:{i["pot"]},參與玩家：{i["players"]}")


# def merge_pot(total_pot,quit_list):

#     new_total_pot=[{"pot":i["pot"],"players":i["players"]} for i in total_pot]
#     merged={}

#     for i in quit_list:
#         for v in new_total_pot:
#             if i in v["players"]:
#                 v["players"].remove(i)

#     for i in new_total_pot:
#         key=tuple(sorted(i["players"]))
#         if key not in merged:
#             merged[key]={"pot":i["pot"],"players":i["players"],"bet":None}
#         else:
#             merged[key]["pot"]+=i["pot"]    
   

#     return list(merged.values())


# total_pot=[{'pot': 200, 'players': ['player1', 'player2','player3'], 'bet': 50},{'pot': 400, 'players': ['player1', 'player2','player3'], 'bet': 100},{'pot': 200, 'players': ['player1'], 'bet': 50},{'pot': 200, 'players': ['player1', 'player2','player3'], 'bet': 50}]

# quit_list=["player2"]

# s=merge_pot(total_pot,quit_list)

# print(s)

# s_total_pot=sorted(total_pot,key=lambda x:len(x["players"]),reverse=True)
        
# total_pot=merge_pot(s_total_pot,quit_list)

# print("m=",total_pot)
# total_pot=[{'pot': 750, 'players': ['player2', 'player5', 'player1', 'player3'], 'bet': None}, {'pot': 300, 'players': ['player3', 'player2', 'player1'], 'bet': None}, {'pot': 100, 'players': ['player3', 'player1'], 'bet': 100}]

# res={'player1': ((2, 3, 14, 13, 12), ((3, '♣'), (3, '♠'), (13, '♦'), (14, '♠'), (12, '♥'))), 'player2': ((1, 14, 13, 12, 8, 6), ((8, '♥'), (13, '♦'), (14, '♠'), (12, '♥'), (6, '♥'))), 'player3': ((1, 14, 13, 12, 11, 9), ((9, '♥'), (11, '♥'), (13, '♦'), (14, '♠'), (12, '♥'))), 'player5': ((1, 14, 13, 12, 6, 5), ((5, '♠'), (13, '♦'), (14, '♠'), (12, '♥'), (6, '♥')))}
# round=1


# for f in total_pot:
#     listingame=[{i:res[i]} for i in f["players"]]
#     in_game={}
#     in_game[]
#     print(in_game)
#     print("***********")
    # in_game={}
    # listingame=[{"i":res[i]} for i in f["players"]]
    # in_game.extend(listingame)
    # winner=max(in_game,key=lambda gg:in_game[gg][0])
    # high=[i for i,v in in_game.items() if v[0]==in_game[winner][0]]
    # if len(high)>1:
    #     print(f"有{len(high)}人平手")

# player_chips={'player1': 100, 'player2': 0, 'player3': 0, 'player4': 400}

# switch=sum( 1 for i in player_chips if player_chips[i]==0)

# name=[i for i in player_chips]
# print(switch)
# print(name)

name=[f"player{i+1}" for i in range(5)]
name=name[3:]+name[:3]

print(name)

s=sorted(name)

print(s)