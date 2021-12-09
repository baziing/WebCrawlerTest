from alpa.model.GameDB import Game

i=Game('gamedb','detail').output('input_time','2021/11/25')
print(i)
i.to_excel('TMP1.xlsx',index=False)