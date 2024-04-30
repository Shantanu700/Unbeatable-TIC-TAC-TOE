import pygame
import sys
import math
import random
from pygame import Rect

pygame.init()
hieght = 500
width = 500
mouse_pos = (0, 0)
rl_mouse_pos = (0, 0)
screen = pygame.display.set_mode((hieght, width))
pygame.display.set_caption("Impossible TIC TAC TOE")
icon = pygame.image.load("tic-tac-toe.png").convert_alpha()
font = pygame.font.Font('aileron/Aileron-Light.otf',20)
pygame.display.set_icon(icon)
BG_COLOR = (0, 0, 0)
BOARD_COLOR = (240, 237, 207)
X_COLOR = (11, 96, 176)
O_COLOR = (64, 162, 216)
x_pos_li = []
o_pos_li = []
pos_li: list[list[int]] = [[0,0,0],[0,0,0],[0,0,0]]
chance = 1
exp = 4
line = 0
win = (None,0)
st = "Start the game or select the player"
reset_time = 0
comp_chance = 0
vs_comp = 1
rec = 1

def plot_line(wil):
    global line,exp
    rect_surface = pygame.Surface((line,6))
    rect_surface.fill(BG_COLOR)
    rect_surface.set_colorkey(BG_COLOR)
    if wil[1] == 3:
        color = X_COLOR
    else:
        color = O_COLOR
    if wil[0][0] == 'd':
        if wil[0][-1] == '0':
            pygame.draw.rect(rect_surface, color, (0, 0, line, 6), border_radius = 50)
            rotated_surface2 = pygame.transform.rotate(rect_surface, -45)
            rotated_rect2 = rotated_surface2.get_rect(topleft = (117,117))
            screen.blit(rotated_surface2, rotated_rect2.topleft)
        else:
            pygame.draw.rect(rect_surface, color, (0, 0, line, 6), border_radius = 50)
            rotated_surface = pygame.transform.rotate(rect_surface, 45)
            rotated_rect = rotated_surface.get_rect(topright = (383,117))
            screen.blit(rotated_surface, rotated_rect.topleft)
        line += exp
        if line >= 367:
            line = 367
    elif wil[0][0] == 'r':
        pygame.draw.rect(screen, color, (110,(int(wil[0][-1])+1)*100+47, line, 6), border_radius = 50)
        line += exp
        if line >= 280:
            line = 280
    elif wil[0][0] == 'c':
        pygame.draw.rect(screen, color, ((int(wil[0][-1])+1)*100+47,110, 6, line), border_radius = 50)
        line += exp
        if line >= 280:
            line = 280
def det_win(sc_li):
    score_dict = {"col_sum0":0,"col_sum1":0,"col_sum2":0,"dai_sum0":0,"dai_sum1":0,"row_sum0":0,"row_sum1":0,"row_sum2":0}
    for index, row in enumerate(sc_li):
        score_dict["col_sum0"] += row[0]
        score_dict["col_sum1"] += row[1]
        score_dict["col_sum2"] += row[2]
        score_dict["dai_sum0"] += row[index]
        score_dict["dai_sum1"] += row[2-index]
        score_dict[f"row_sum{index}"] = sum(row)
    if 3 in score_dict.values():
        return (list(score_dict.keys())[list(score_dict.values()).index(3)],3)
    elif -3 in score_dict.values():
        return (list(score_dict.keys())[list(score_dict.values()).index(-3)],-3)
    return (None,0)
def restart():
    global chance, pos_li, win, line, st, VS, rec
    st = "Start the game or select the player"
    rec = 1
    line = 0
    pos_li = [[0,0,0],[0,0,0],[0,0,0]]
    chance = 1
    win = (None,0)
    x_pos_li.clear()
    o_pos_li.clear()
    VS = 1
def plot_x(x_li):
    for pos in x_li:
        rect_surface = pygame.Surface((65,6))
        rect_surface.fill(BG_COLOR)
        rect_surface.set_colorkey(BG_COLOR)
        pygame.draw.rect(rect_surface, X_COLOR, (0, 0, 65, 6), border_radius=50)
        pygame.draw.rect(rect_surface, X_COLOR, (0, 0, 65, 6), border_radius=50)
        rotated_surface = pygame.transform.rotate(rect_surface, 45)
        rotated_surface2 = pygame.transform.rotate(rect_surface, -45)
        rotated_rect = rotated_surface.get_rect(center=pos)
        rotated_rect2 = rotated_surface2.get_rect(center=pos)
        screen.blit(rotated_surface, rotated_rect.topleft)
        screen.blit(rotated_surface2, rotated_rect2.topleft)
def plot_o(o_li):
    for pos in o_li:
        pygame.draw.circle(screen, O_COLOR, pos, 30, 5)
def info(st):
    s = font.render(st,True,BOARD_COLOR)
    text_rect = s.get_rect()
    text_rect.center = (screen.get_width()/2,15)
    screen.blit(s,text_rect)
def bot():
    global comp_chance,chance, x_pos_li, o_pos_li, pos_li, st
    chance_line = "__"
    if chance == 1:
        if not len(o_pos_li) :
            bot_chance = (random.choice((150,350)),random.choice((150,350)))
            x_pos_li.append(bot_chance)
            pos_li[bot_chance[1]//100-1][bot_chance[0]//100-1] = chance
        elif len(o_pos_li) == 1:
            if o_pos_li == [(250,250)]:
                bot_chance = (500-x_pos_li[-1][0],500-x_pos_li[-1][1])
                x_pos_li.append(bot_chance)
                pos_li[bot_chance[1]//100-1][bot_chance[0]//100-1] = chance
            elif o_pos_li[0][1] == x_pos_li[0][1] or (abs(o_pos_li[0][0] - x_pos_li[0][0]) == 200 and abs(o_pos_li[0][1] - x_pos_li[0][0]) == 100):
                bot_chance = (x_pos_li[-1][0],500-x_pos_li[-1][1])
                x_pos_li.append(bot_chance)
                pos_li[bot_chance[1]//100-1][bot_chance[0]//100-1] = chance
            elif o_pos_li[0][0] == x_pos_li[0][0] or (abs(o_pos_li[0][0] - x_pos_li[0][0]) == 100 and abs(o_pos_li[0][1] - x_pos_li[0][0]) == 200):
                bot_chance = (500-x_pos_li[-1][0],x_pos_li[-1][1])
                x_pos_li.append(bot_chance)
                pos_li[bot_chance[1]//100-1][bot_chance[0]//100-1] = chance
            else:
                rc = random.choice((500,0))
                bot_chance = (abs(500 - rc - x_pos_li[-1][0]),abs(rc - x_pos_li[-1][1]))
                x_pos_li.append(bot_chance)
                pos_li[bot_chance[1]//100-1][bot_chance[0]//100-1] = chance
        elif len(o_pos_li) == 2:
            if not (x_pos_li[0][0] == o_pos_li[-1][0] == x_pos_li[1][0] or x_pos_li[0][1] == o_pos_li[-1][1] == x_pos_li[1][1]):
                if x_pos_li[0][0] == x_pos_li[1][0]:
                    bot_chance = (x_pos_li[0][0],250)
                    x_pos_li.append(bot_chance)
                    pos_li[bot_chance[1]//100-1][bot_chance[0]//100-1] = chance
                elif x_pos_li[0][1] == x_pos_li[1][1]:
                    bot_chance = (250,x_pos_li[0][1])
                    x_pos_li.append(bot_chance)
                    pos_li[bot_chance[1]//100-1][bot_chance[0]//100-1] = chance
                elif o_pos_li[0] == (250,250):
                    bot_chance = (500 - o_pos_li[-1][0],500 - o_pos_li[-1][1])
                    x_pos_li.append(bot_chance)
                    pos_li[bot_chance[1]//100-1][bot_chance[0]//100-1] = chance
            else:
                if abs(o_pos_li[0][0] - o_pos_li[0][1]) == 200 or abs(o_pos_li[0][0] - o_pos_li[0][1]) == 0:
                    for i in range(150,351,200):
                        for j in range(150,351,200):
                            if (i,j) not in o_pos_li and (i,j) not in x_pos_li:
                                bot_chance = (i,j)
                                break
                    x_pos_li.append(bot_chance)
                    pos_li[bot_chance[1]//100-1][bot_chance[0]//100-1] = chance
                elif abs(o_pos_li[0][0] - o_pos_li[0][1]) == 100:
                    bot_chance = (250,250)
                    x_pos_li.append(bot_chance)
                    pos_li[bot_chance[1]//100-1][bot_chance[0]//100-1] = chance
        elif len(o_pos_li) == 3:
            score_dict = {"c0":0,"c1":0,"c2":0,"d0":0,"d1":0,"r0":0,"r1":0,"r2":0}
            for index, row in enumerate(pos_li):
                score_dict["c0"] += row[0]
                score_dict["c1"] += row[1]
                score_dict["c2"] += row[2]
                score_dict["d0"] += row[index]
                score_dict["d1"] += row[2-index]
                score_dict[f"r{index}"] = sum(row)
            if 2 in score_dict.values():
                chance_line = (list(score_dict.keys())[list(score_dict.values()).index(2)])
            elif -2 in score_dict.values():
                chance_line = (list(score_dict.keys())[list(score_dict.values()).index(-2)])
            if chance_line[0] == "r":
                for r in range(150,351,100):
                    bot_chance = (r,(int(chance_line[1])+1)*100+50)
                    if bot_chance not in x_pos_li and bot_chance not in o_pos_li:
                        x_pos_li.append(bot_chance)
                        pos_li[bot_chance[1]//100-1][bot_chance[0]//100-1] = chance
            elif chance_line[0] == "c":
                for c in range(150,351,100):
                    bot_chance = ((int(chance_line[1])+1)*100+50,c)
                    if bot_chance not in x_pos_li and bot_chance not in o_pos_li:
                        x_pos_li.append(bot_chance)
                        pos_li[bot_chance[1]//100-1][bot_chance[0]//100-1] = chance
            elif chance_line[0] == "d":
                for d in range(150,351,100):
                    if chance_line[1] == "0":
                        bot_chance = (d,d)
                        if bot_chance not in x_pos_li and bot_chance not in o_pos_li:
                            x_pos_li.append(bot_chance)
                            pos_li[bot_chance[1]//100-1][bot_chance[0]//100-1] = chance
                    elif chance_line[1] == "1":
                        bot_chance = (d,500-d)
                        if bot_chance not in x_pos_li and bot_chance not in o_pos_li:
                            x_pos_li.append(bot_chance)
                            pos_li[bot_chance[1]//100-1][bot_chance[0]//100-1] = chance
        else:
            for j in range(150,351,100):
                for k in range(150,351,100):
                    bot_chance = (j,k)
                    if bot_chance not in x_pos_li and bot_chance not in o_pos_li:
                        x_pos_li.append(bot_chance)
                        pos_li[bot_chance[1]//100-1][bot_chance[0]//100-1] = chance
        st = "O's Turn"
    elif chance == -1:
        if len(x_pos_li) == 1:
            if (250,250) not in x_pos_li:
                bot_chance = (250,250)
                o_pos_li.append(bot_chance)
                pos_li[bot_chance[1]//100-1][bot_chance[0]//100-1] = chance
            else:
                bot_chance = (random.choice((150,350)),random.choice((150,350)))
                o_pos_li.append(bot_chance)
                pos_li[bot_chance[1]//100-1][bot_chance[0]//100-1] = chance
        elif len(x_pos_li) == 2:
            if (x_pos_li[0][0] == x_pos_li[1][0]) or (x_pos_li[0][1] == x_pos_li[1][1]):
                bot_chance = (x_pos_li[0][0] if x_pos_li[0][0] == x_pos_li[1][0] else 750 - (x_pos_li[0][0] + x_pos_li[1][0]), x_pos_li[0][1] if x_pos_li[0][1] == x_pos_li[1][1] else 750 - (x_pos_li[0][1] + x_pos_li[1][1]))
                if bot_chance not in o_pos_li:
                    o_pos_li.append(bot_chance)
                    pos_li[bot_chance[1]//100-1][bot_chance[0]//100-1] = chance
                else:
                    bot_chance = (random.choice((150,350)),random.choice((150,350)))
                    o_pos_li.append(bot_chance)
                    pos_li[bot_chance[1]//100-1][bot_chance[0]//100-1] = chance
            elif (abs(x_pos_li[0][0] - x_pos_li[1][0]) == 200 and abs(x_pos_li[0][1] - x_pos_li[1][1]) == 100) or (abs(x_pos_li[0][0] - x_pos_li[1][0]) == 100 and abs(x_pos_li[0][1] - x_pos_li[1][1]) == 200):
                for x_pos in x_pos_li:
                    if abs(x_pos[0] - x_pos[1]) in (0,200):
                        bot_chance = (500 - x_pos[0], 500 - x_pos[1])
                        o_pos_li.append(bot_chance)
                        pos_li[bot_chance[1]//100-1][bot_chance[0]//100-1] = chance
                        break
            elif (x_pos_li[0][0] + x_pos_li[1][0] == x_pos_li[0][1] + x_pos_li[1][1] == 500):
                rc = random.choice((350,150))
                bot_chance = [rc,250]
                random.shuffle(bot_chance)
                o_pos_li.append(tuple(bot_chance))
                pos_li[bot_chance[1]//100-1][bot_chance[0]//100-1] = chance
            elif (abs(x_pos_li[0][0] - x_pos_li[1][0]) == abs(x_pos_li[0][1] - x_pos_li[1][1]) == 100):
                if (250,250) in x_pos_li:
                    bot_chance = (500 - x_pos_li[-1][0], 500 - x_pos_li[-1][1])
                    if bot_chance not in o_pos_li:
                        o_pos_li.append(bot_chance)
                        pos_li[bot_chance[1]//100-1][bot_chance[0]//100-1] = chance
                    else:
                        while True:
                            bot_chance = (random.choice((150,350)),random.choice((150,350)))
                            if bot_chance not in x_pos_li and bot_chance not in o_pos_li:
                                o_pos_li.append(bot_chance)
                                pos_li[bot_chance[1]//100-1][bot_chance[0]//100-1] = chance
                                break
                else:
                    bot_chance = (x_pos_li[0][0] if x_pos_li[0][0] != 250 else x_pos_li[1][0],x_pos_li[1][1] if x_pos_li[1][1] != 250 else x_pos_li[0][1])
                    o_pos_li.append(bot_chance)
                    pos_li[bot_chance[1]//100-1][bot_chance[0]//100-1] = chance
        elif len(x_pos_li) == 3:
            score_dict = {"c0":0,"c1":0,"c2":0,"d0":0,"d1":0,"r0":0,"r1":0,"r2":0}
            for index, row in enumerate(pos_li):
                score_dict["c0"] += row[0]
                score_dict["c1"] += row[1]
                score_dict["c2"] += row[2]
                score_dict["d0"] += row[index]
                score_dict["d1"] += row[2-index]
                score_dict[f"r{index}"] = sum(row)
            if -2 in score_dict.values():
                chance_line = (list(score_dict.keys())[list(score_dict.values()).index(-2)])
            elif 2 in score_dict.values():
                chance_line = (list(score_dict.keys())[list(score_dict.values()).index(2)])
            if chance_line[0] == "r":
                for r in range(150,351,100):
                    bot_chance = (r,(int(chance_line[1])+1)*100+50)
                    if bot_chance not in x_pos_li and bot_chance not in o_pos_li:
                        o_pos_li.append(bot_chance)
                        pos_li[bot_chance[1]//100-1][bot_chance[0]//100-1] = chance
            elif chance_line[0] == "c":
                for c in range(150,351,100):
                    bot_chance = ((int(chance_line[1])+1)*100+50,c)
                    if bot_chance not in x_pos_li and bot_chance not in o_pos_li:
                        o_pos_li.append(bot_chance)
                        pos_li[bot_chance[1]//100-1][bot_chance[0]//100-1] = chance
            elif chance_line[0] == "d":
                for d in range(150,351,100):
                    if chance_line[1] == "0":
                        bot_chance = (d,d)
                        if bot_chance not in x_pos_li and bot_chance not in o_pos_li:
                            o_pos_li.append(bot_chance)
                            pos_li[bot_chance[1]//100-1][bot_chance[0]//100-1] = chance
                    elif chance_line[1] == "1":
                        bot_chance = (d,500-d)
                        if bot_chance not in x_pos_li and bot_chance not in o_pos_li:
                            o_pos_li.append(bot_chance)
                            pos_li[bot_chance[1]//100-1][bot_chance[0]//100-1] = chance
            else:
                while True:
                    bot_chance = (random.choice((150,350)),random.choice((150,350)))
                    if bot_chance not in x_pos_li and bot_chance not in o_pos_li:
                        o_pos_li.append(bot_chance)
                        pos_li[bot_chance[1]//100-1][bot_chance[0]//100-1] = chance
                        break
        elif len(x_pos_li) == 4:
            score_dict = {"c0":0,"c1":0,"c2":0,"d0":0,"d1":0,"r0":0,"r1":0,"r2":0}
            for index, row in enumerate(pos_li):
                score_dict["c0"] += row[0]
                score_dict["c1"] += row[1]
                score_dict["c2"] += row[2]
                score_dict["d0"] += row[index]
                score_dict["d1"] += row[2-index]
                score_dict[f"r{index}"] = sum(row)
            if -2 in score_dict.values():
                chance_line = (list(score_dict.keys())[list(score_dict.values()).index(-2)])
            elif 2 in score_dict.values():
                chance_line = (list(score_dict.keys())[list(score_dict.values()).index(2)])
            if chance_line[0] == "r":
                for r in range(150,351,100):
                    bot_chance = (r,(int(chance_line[1])+1)*100+50)
                    if bot_chance not in x_pos_li and bot_chance not in o_pos_li:
                        o_pos_li.append(bot_chance)
                        pos_li[bot_chance[1]//100-1][bot_chance[0]//100-1] = chance
            elif chance_line[0] == "c":
                for c in range(150,351,100):
                    bot_chance = ((int(chance_line[1])+1)*100+50,c)
                    if bot_chance not in x_pos_li and bot_chance not in o_pos_li:
                        o_pos_li.append(bot_chance)
                        pos_li[bot_chance[1]//100-1][bot_chance[0]//100-1] = chance
            elif chance_line[0] == "d":
                for d in range(150,351,100):
                    if chance_line[1] == "0":
                        bot_chance = (d,d)
                        if bot_chance not in x_pos_li and bot_chance not in o_pos_li:
                            o_pos_li.append(bot_chance)
                            pos_li[bot_chance[1]//100-1][bot_chance[0]//100-1] = chance
                    elif chance_line[1] == "1":
                        bot_chance = (d,500-d)
                        if bot_chance not in x_pos_li and bot_chance not in o_pos_li:
                            o_pos_li.append(bot_chance)
                            pos_li[bot_chance[1]//100-1][bot_chance[0]//100-1] = chance
            else:
                while True:
                    rc = random.choice((350,150))
                    bot_chance = [rc,250]
                    random.shuffle((bot_chance))
                    if tuple(bot_chance) not in o_pos_li and tuple(bot_chance) not in x_pos_li:
                        o_pos_li.append(tuple(bot_chance))
                        pos_li[bot_chance[1]//100-1][bot_chance[0]//100-1] = chance
                        break
        st = "X's Turn"
    chance *= -1
    comp_chance = 0
    return
def loop():
    global mouse_pos, chance, win, st, reset_time, VS, comp_chance, vs_comp, rec
    while True:
        screen.fill(BG_COLOR)
        human_rect = pygame.Rect(20, 40, 210, 40)
        comp_rect = pygame.Rect(270, 40, 210, 40)
        rst_rect: Rect = pygame.Rect(145, 430, 210, 40)
        human = font.render("VS human",1,X_COLOR)
        comp = font.render("VS Comp",1,O_COLOR)
        human_rect1 = human.get_rect()
        human_rect1.center = human_rect.center
        comp_rect1 = comp.get_rect()
        comp_rect1.center = comp_rect.center
        pygame.draw.rect(screen, BOARD_COLOR, human_rect, border_radius=50, width=3)
        pygame.draw.rect(screen, BOARD_COLOR, comp_rect, border_radius=50, width=3)
        pygame.draw.rect(screen, BOARD_COLOR, rst_rect, border_radius=50, width=3)
        pygame.draw.rect(screen, BOARD_COLOR, [197, 100, 6, 300], border_radius=50)
        pygame.draw.rect(screen, BOARD_COLOR, [297, 100, 6, 300], border_radius=50)
        pygame.draw.rect(screen, BOARD_COLOR, [100, 197, 300, 6], border_radius=50)
        pygame.draw.rect(screen, BOARD_COLOR, [100, 297, 300, 6], border_radius=50)
        rstrt = font.render("Restart",True,BOARD_COLOR)
        rstrt_rect = rstrt.get_rect()
        rstrt_rect.center = rst_rect.center
        screen.blit(rstrt,rstrt_rect)
        screen.blit(human,human_rect1)
        screen.blit(comp,comp_rect1)
        info(st)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if mouse_pos[0] in range(100,401) and mouse_pos[1] in range(100,401):
                    rl_mouse_pos = (math.ceil(mouse_pos[0]/100)*100-50,math.ceil(mouse_pos[1]/100)*100-50)
                    if chance == 1:
                        if rl_mouse_pos not in x_pos_li and rl_mouse_pos not in o_pos_li and not win[1] and rec:
                            x_pos_li.append(rl_mouse_pos)
                            pos_li[rl_mouse_pos[1]//100-1][rl_mouse_pos[0]//100-1] = chance
                            st = "O's Turn"
                            chance *= -1
                            if vs_comp:
                                comp_chance = 1
                    else:
                        if rl_mouse_pos not in x_pos_li and rl_mouse_pos not in o_pos_li and not win[1] and rec:
                            o_pos_li.append(rl_mouse_pos)
                            pos_li[rl_mouse_pos[1]//100-1][rl_mouse_pos[0]//100-1] = chance
                            st = "X's Turn"
                            chance *= -1
                            if vs_comp:
                                comp_chance = 1
                elif comp_rect.collidepoint(event.pos):
                    vs_comp = 1
                    comp_chance = 1
                    restart()
                elif human_rect.collidepoint(event.pos):
                    vs_comp = 0
                    comp_chance = 0
                    restart()
                elif rst_rect.collidepoint(event.pos):
                    restart()
                    st = "Start the game or select the player"
        win = det_win(pos_li)
        if win[1]:
            plot_line(win)
            if win[1] == 3:
                st = "X wins"
            else:
                st = "O wins"
        if 0 not in pos_li[0]  and 0 not in pos_li[1] and 0 not in pos_li[2]:
            if st[-1] != 's':
                if rec:
                    reset_time = pygame.time.get_ticks()
                    rec = 0
                elapsed_time = (pygame.time.get_ticks() - reset_time)//1000
                st = f"It's a draw restarting in {3-elapsed_time}"
                if elapsed_time >= 3:
                    restart()
                    rec = 1
        if comp_chance:
            if rec:
                chance_time = pygame.time.get_ticks()
                rec = 0
            elapsed_chance_time = (pygame.time.get_ticks() - chance_time)
            if elapsed_chance_time >= 500:
                bot()
                rec = 1
        plot_x(x_pos_li)
        plot_o(o_pos_li)
        pygame.display.update()
        pygame.time.Clock().tick(60)
loop()