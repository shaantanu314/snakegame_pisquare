import pygame
import random
import math

pygame.init()

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
screen_width = 900
screen_height = 600
snake_x = 45
snake_y = 45
snake_size = 40
snake_width = 10
velocity_x = 0
velocity_y = 0
food_x = random.randint(40,screen_width-40)
food_y = random.randint(40,screen_height-40)
score = 0
block_size=50
fps = 30
disp_new_level = False
curr_velocity = 10

#apple image

appleImg = pygame.image.load("apple.png")

# CURRENT LEVEL
current_level = 1


gameWindow = pygame.display.set_mode((screen_width,screen_height))

clock = pygame.time.Clock()
pygame.display.set_caption("snake game")
pygame.display.update()

exit_game = False
game_over = False

font = pygame.font.SysFont(None, 50, bold=False, italic=False)

f = open("level/level1.txt")
line_map =""
for line in f:
    line_map += line.rstrip()
map = line_map.split(",")
f.close()


def text_disp(text,color,x,y):
    screen_text = font.render(text, True , color)
    gameWindow.blit(screen_text , [x,y])

# map characteristics
map_points = []

# snake length logic
snake_list = []
snake_length = 1

def get_current_time():

    return pygame.time.get_ticks()


def set_map():
    global map_points
    map_points = []
    iter = 0
    for block in map:
        if block == '1':
            block_x = iter%(screen_width/block_size)
            block_y = iter/(screen_width/block_size)
            block_x *= block_size
            block_y *= block_size
            point = [block_x,block_y,block_x,block_y+block_size,block_x+block_size,block_y,block_x+block_size,block_y+block_size]
            map_points.append(point)
        iter+=1

def plot_snake(gameWindow ,  color , snake_list, snake_size ):
    iter = 0
    for x,y in snake_list:
        iter %= 4
        # for gradient in snake colour
        pygame.draw.rect(gameWindow, (255-iter*25,255-iter*25,0) , [x , y, snake_size, snake_size])
        iter += 1

def collide(x1,x2,y1,y2,radius):
    if(math.sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2))<=radius):
        return True
    return False

def check_snake(snake_list):
    global exit_game
    global map_points
    global food_x
    global food_y
    global score
    global snake_length

    head_x = snake_list[-1][0]
    head_y = snake_list[-1][1]
    head_coordinates = [[head_x,head_y],[head_x,head_y+snake_size],[head_x+snake_size,head_y],[head_x+snake_size,head_y+snake_size]]

    # check food status

    for x,y in head_coordinates:
        if collide(x,food_x,y,food_y,20):
            score += 10
            snake_length += 5
            coincide_food = 1
            while coincide_food:
                coincide_food=False
                food_x = random.randint(40,screen_width-40)
                food_y = random.randint(40,screen_height-40)
                
                for x1,y1,x2,y2,x3,y3,x4,y4 in map_points:
                    if collide(x1,food_x,y1,food_y,40) or collide(x2,food_x,y2,food_y,40) or collide(x3,food_x,y3,food_y,40) or collide(x4,food_x,y4,food_y,40):                
                        coincide_food = True
            break


    # check self-kill
    for x,y in snake_list[0:len(snake_list)-2]:
        if(x== head_x and y==head_y):
            exit_game = True     

    # check boundary pass    
    if snake_x<0 or snake_x>screen_width-snake_size or snake_y<0 or snake_y>screen_height-snake_size:
        exit_game = True

    #check block collision

    for x1,y1,x2,y2,x3,y3,x4,y4 in map_points:
        for  hx,hy in head_coordinates:
            if collide(x1,hx,y1,hy,17) or collide(x2,hx,y2,hy,17) or collide(x3,hx,y3,hy,17) or collide(x4,hx,y4,hy,17):                
                exit_game = True


def plot_map(gameWindow):
    global map
    iter = 0
    for block in map:
        if block == '1':
            block_x = iter%(screen_width/block_size)
            block_y = iter/(screen_width/block_size)
            block_x *= block_size
            block_y *= block_size
           # print((str(block_x)+","+str(block_y)))
            pygame.draw.rect(gameWindow, black , [block_x -2, block_y -2, block_size -2, block_size -2])
        iter += 1

set_map()

while not exit_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_game = True
        
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                velocity_x = -curr_velocity
                velocity_y = 0
            if event.key == pygame.K_RIGHT:
                velocity_x = curr_velocity
                velocity_y = 0
            if event.key == pygame.K_UP:
                velocity_y = -curr_velocity
                velocity_x = 0
            if event.key == pygame.K_DOWN:
                velocity_y = curr_velocity
                velocity_x = 0
    

    
    snake_x += velocity_x
    snake_y += velocity_y            
    
    clock.tick(fps)

    gameWindow.fill(white)

    head = []
    head.append(snake_x)
    head.append(snake_y)
    snake_list.append(head)

    if len(snake_list)>snake_length:
        del snake_list[0]

    check_snake(snake_list)
    text_disp(" Score "+ str(score) , red , 5,5)
    plot_map(gameWindow)
    gameWindow.blit(appleImg, (food_x-20,food_y-20))
    plot_snake(gameWindow , black , snake_list, snake_size)

    if score > current_level*40 and current_level<3:

        current_level +=1
        f = open("level/level"+str(current_level)+".txt")
        line_map =""
        for line in f:
            line_map += line.rstrip()
        map = []
        map = line_map.split(",")
        f.close()
        set_map()
        disp_new_level = True
        start_time = get_current_time()
        fps = 10
        curr_velocity = 2

    if disp_new_level:
        screen_text = font.render("new level", True , (0,0,0))
        gameWindow.blit(screen_text,[screen_width/2,10])
        if get_current_time() - start_time > 500:
            fps=30
            curr_velocity = 10
            disp_new_level = False

    pygame.display.update()

pygame.quit()
quit()