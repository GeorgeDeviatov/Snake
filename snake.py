import pygame as pg
import random
pg.init()

#width,height = 1200,800
#screen = pg.display.set_mode((width,height))
def write(text,color,pos,size,screen):
    f = pg.font.SysFont('c059', size)
    font = f.render(text, True, color)
    screen.blit(font,pos)


def draw_snake(snake,size_x,size_y,screen):
    j = 0
    for block in snake:
        j+=1
        print(block,j)
        pg.draw.polygon(screen,(255,0,0),((block[0]*size_x,block[1]*size_y),
        ((block[0]+1)*size_x,block[1]*size_y),((block[0]+1)*size_x,(block[1]+1)*size_y),
        (block[0]*size_x,(block[1]+1)*size_y)))


def draw_field(x,y,size_x,size_y,screen):
    for xx in range(x+1):
        pg.draw.line(screen, (255,255,255), (xx*size_x,0), (xx*size_x,y*size_y), 2)
    
    for yy in range(y+1):
        pg.draw.line(screen, (255,255,255),(0,yy*size_y),(size_x*x,yy*size_y) )







def update(snake,direct,x,y,apple,free_tiles):
    last_block = snake[len(snake)-1]
    for cur in range(len(snake)-1,0,-1):
        print(snake,9)
        snake[cur] = snake[cur-1].copy()
    snake[0][0] += direct[0]
    snake[0][1] += direct[1]
    print(snake[0] in snake[1:len(snake)],snake)
    if snake[0] in snake[1:len(snake)]:return True,snake, apple
    
    if snake[0][0] < 0:return True, snake, apple
    
    if snake[0][0] > x-1:return True, snake, apple
    
    if snake[0][1] < 0:return True, snake, apple
    
    if snake[0][1] > y-1:return True, snake, apple
    
    if snake[0] in free_tiles:
        free_tiles.remove(snake[0])
    if snake[0] == apple:
        snake.append(last_block)
        apple = rand_apple(free_tiles)
    else:
        free_tiles.append(last_block)
        
    return False,snake,apple



def rand_apple(free_tiles):
    apple = random.choice(free_tiles)
    return apple
    
    

def game(width=1200,height=800,step_time=200):
    score = 0
    direct = [1,0]
    width,height =width+2,height+2
    screen = pg.display.set_mode((width,height))
    br = False
    clock = pg.time.Clock()
    mode = ''
    


    
    x,y = 20,20
    
    snake = [[x//2,y//2],[x//2-1,y//2]]
    
    beg_t = pg.time.get_ticks()
    
    free_tiles = []
    for xx in range(x):
        for yy in range(y):
            free_tiles.append([xx,yy])
    
    for s in snake:
        free_tiles.remove(s)
    
    apple = rand_apple(free_tiles)
    size_x,size_y = width//x,height//y
    
    while True:
        draw_snake(snake,width//x,height//y,screen)
        draw_field(x,y,width//x,height//y,screen)
        pg.draw.polygon(screen, (0,255,0), ((apple[0]*size_x,apple[1]*size_y),
        ((apple[0]+1) * size_x, apple[1]*size_y ),((apple[0]+1)*size_x,(apple[1]+1)*size_y),
        (apple[0]*size_x,(apple[1]+1)*size_y)))
        
        if pg.time.get_ticks() - beg_t >= step_time:
            end,snake,apple = update(snake,direct,x,y,apple,free_tiles)
            if end:
                mode = 'over'
                break
            beg_t = pg.time.get_ticks()
            score = (len(snake)-2)*100
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            elif event.type == pg.KEYDOWN:
                name = pg.key.name(event.key)
                if (name == 'left' or name == 'a') and direct != [1,0]:
                    direct = [-1,0]
                elif (name == 'right' or name == 'd') and direct != [-1,0]:
                    direct = [1,0]
                elif (name == 'up' or name == 'w') and direct != [0,1]:
                    direct = [0,-1]
                elif (name == 'down' or name == 's') and direct != [0,-1]:
                    direct = [0,1]
                elif name == 'e':
                    br = True
                    mode = 'menu'
        
        if br:
            break
        
        
        pg.display.flip()
        clock.tick(30)
        pg.display.set_caption('Game Snake; Score: {}'.format(str(score)))
        screen.fill((0,0,0))
    
    
    if mode == 'menu':
        draw_menu()
    elif mode == 'over':
        game_over(score,width,height,step_time)
    return


def game_over(score,width=1200,height=800,step_time=800):
    screen = pg.display.set_mode((width,height))
    clock = pg.time.Clock()
    br = False
    
    while True:
        
        write('Game over! Your score: {}'.format(str(score)), (255,0,0), (width//3,20), 40, screen)
        write('To play again press Enter!',(255,0,0),(width//4,height//3*2),35,screen)
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            elif event.type == pg.KEYDOWN:
                name = pg.key.name(event.key)
                if name == 'return':
                    br = True
        
        if br:break
        pg.display.flip()
        clock.tick(30)
        pg.display.set_caption('Game Snake; Score: {}'.format('0'))
        screen.fill((0,0,0))        
    
    game(width,height,step_time)
    return



def draw_set():
    width,height = 1200,800
    screen = pg.display.set_mode((width,height))
    clock = pg.time.Clock()
    
    questions = [['Width',1200,'1200'],['Height',800,'800'],['StepTime (speed) in s',0.1,'0.1']]
    
    buttons = []
    x,y = 200,20
    size = 100
    br = False
    cur = 0
    for apply in questions:
        buttons.append([[x+size,y],[x+size,y+size],[x+size*2,y+size],[x+size*2,y]])
        
        if x + size*4 > width:
            x = 20
            y += size + 30
        else:
            x += size * 4
    
    while True:
        
        for num in range(len(buttons)):
            write(questions[num][2],(255,0,0),(buttons[num][0][0]-size*3,buttons[num][0][1]), 35, screen)
            write(questions[num][0],(0,255,0),(buttons[num][0][0]-size*3,buttons[num][0][1]+45), 30, screen)
            pg.draw.polygon(screen,(255,255,255),buttons[num])
        
        
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            elif event.type == pg.KEYDOWN:
                name = pg.key.name(event.key)
                if name == 'return':
                    br = True
                elif name == 'backspace':
                    if len(questions[cur][2]) > 0:
                        questions[cur][2] = questions[cur][2][0:len(questions[cur][2])-1]
                else:
                    questions[cur][2] += name
            elif event.type == pg.MOUSEBUTTONDOWN:
                pos = event.pos
                for but in range(len(buttons)):
                    if pos[0] > buttons[but][0][0] and pos[0] < buttons[but][2][0]:
                        if pos[1] > buttons[but][0][1] and pos[1] < buttons[but][2][1]:
                            cur = but
                            break
        
        if br:break
        pg.display.flip()
        clock.tick(30)
        pg.display.set_caption('Settings')
        screen.fill((0,0,0)) 
    
    try:
        width = int(questions[0][2])
    except:
        width = questions[0][1]
    
    try:
        height = int(questions[1][2])
    except:
        height = questions[1][1]
    
    try:
        step_time = float(questions[2][2])*1000
    except:
        step_time = questions[2][1]*1000
    draw_menu(width,height,step_time)
    return






def draw_menu(width=1200,height=800,step_time=200):
    screen = pg.display.set_mode((width,height))
    br = False
    mode = ''
    clock = pg.time.Clock()
    while True:
        sz = width//9
        if height//4 < sz:
            sz = height//4
        write('Main Menu',(255,0,0),(width//3,20),sz,screen)
        
        sz = width//20
        if height//4<sz:
            sz = height//4
        
        write('Press Enter to play',(200,50,150),(width//4,height//3),sz,screen)
        
        sz = width//26
        if height//4<sz:
            sz = height//4
        write('Press s to go to settings',(100,40,200),(width//5,height//3*2),sz,screen)
        
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            elif event.type == pg.KEYDOWN:
                name = pg.key.name(event.key)
                if name == 'return':
                    br = True
                    mode = 'play'
                    break
                elif name == 's':
                    br = True
                    mode = 'settings'
                    break
        
        if br:
            break
        
        pg.display.flip()
        clock.tick(30)
        pg.display.set_caption('Main Menu')
        screen.fill((0,0,0))
    
    if mode == 'play':
        game(width,height,step_time)
        return
    elif mode == 'settings':
        draw_set()
        return


if __name__ == '__main__':
    draw_menu()