# cards=[(12, '♣'), (8, '♦')]
# rank_map={11:"J",12:"Q",13:"K",14:"A"}

# for i,v in cards:
#     rank_display=rank_map.get(i,str(i))
    
# mini=[]
# for x,y in rank_display:
#     mini.append=[x+y]
    
# print(cards)


cards=[(12, '♣'), (8, '♦')]

rank_map={11:"J",12:"Q",13:"K",14:"A"}
rank_display=[]
for i,v in cards:
    rank_display.append((rank_map.get(i,str(i))+v))

print(rank_display)
