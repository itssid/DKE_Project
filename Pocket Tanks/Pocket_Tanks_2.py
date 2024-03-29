import pygame
import time
import random
import sqlite3
import numpy as np

pygame.init()

conn  = sqlite3.connect("pocket_tanks.db")
cursor = conn.cursor()

angle = 0

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width,display_height))

pygame.display.set_caption('Pocket Tanks')

icon = pygame.image.load('tanks_icon.png')       
pygame.display.set_icon(icon)

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
light_blue = (0, 153, 204)
blue = (0, 0, 153)
dark_green = (0, 102, 0)
green = (0,200,0)
pink = (255, 51, 204)
purple = (128, 0, 96)
maroon = (153, 0, 0)
brown = (204, 51, 0)
yellow = (0,150,200)
yellow = (200,200,0)
light_yellow = (255,255,0)
light_green = (0,255,0)

clock = pygame.time.Clock()

tankWidth = 40
tankHeight = 20

turretWidth = 4
wheelWidth = 4

ground_height = 35

smallfont = pygame.font.SysFont("comicsansms", 15)
medfont = pygame.font.SysFont("comicsansms", 25)
largefont = pygame.font.SysFont("comicsansms", 30)

def create_table():
    cursor.execute("CREATE TABLE IF NOT EXISTS user_shot_attr(power INTEGER,angle REAL,initial_point INTEGER,final_point INTEGER,barrier INTEGER,ememy_positon INTEGER, damage INTEGER)")

#    cursor.execute("CREATE TABLE IF NOT EXISTS computer_shot_attr(power INTEGER,angle REAL,initial_point INTEGER,final_point INTEGER,barrier INTEGER, ememy_position INTEGER)")

def user_dynamic_entry(power,angle,initial_point,final_point,barrier,ememy_positon,damage):
    cursor.execute("INSERT INTO user_shot_attr (power,angle,initial_point,final_point,barrier,ememy_positon,damage) VALUES(?,?,?,?,?,?,?)",
                   (power,angle,initial_point,final_point,barrier,ememy_positon,damage))

    conn.commit()


def selecting(user_tank,comp_tank):
    num = user_tank-comp_tank
    cursor.execute("SELECT * from user_shot_attr where barrier>400 and abs(%s-(initial_point-final_point)) < 36 ORDER BY damage DESC;" % num)
    rows = cursor.fetchall()
#    print(rows[0][0],rows[1][1])
    try:
        a,b = rows[0][0],int(rows[1][1])
    except IndexError:
        a,b = 70,12    
    return a,int(b)
    
    #for row in rows:
        #print(row[1])
#	for row in rows:
#		print "%s %s %s" % (row["power"], row["angle"], row["initial_point"])

#def computer_dynamic_entry():
 #   cursor.execute("INSERT INTO computer_shot_attr (power,angle,initial_point,final_point,barrier,ememy_positon) VALUES(?,?,?,?,?)",
   #                (power,angle,initial_point,final_point,barrier,ememy_positon))
  #  conn.commit()



def score(score):

    text = medfont.render("Score: "+str(score), True, black)
    gameDisplay.blit(text, [0,0])
    

def text_objects(text, color,size = "small"):

    if size == "small":
        textSurface = smallfont.render(text, True, color)
    if size == "medium":
        textSurface = medfont.render(text, True, color)
    if size == "large":
        textSurface = largefont.render(text, True, color)

    return textSurface, textSurface.get_rect()

def text_to_button(msg, color, buttonx, buttony, buttonwidth, buttonheight, size = "small"):
    textSurf, textRect = text_objects(msg,color,size)
    textRect.center = ((buttonx+(buttonwidth/2)), buttony+(buttonheight/2))
    gameDisplay.blit(textSurf, textRect)
   
def message_to_screen(msg,color, y_displace = 0, size = "small"):
    textSurf, textRect = text_objects(msg,color,size)
    textRect.center = (int(display_width / 2), int(display_height / 2)+y_displace)
    gameDisplay.blit(textSurf, textRect)

def tank(x,y,turPos):
    x = int(x)
    y = int(y)


    possibleTurrets = [(x-30, y-1),
					   (x-28, y-2),
                       (x-26, y-4),
                       (x-24, y-6),
                       (x-22, y-8),
                       (x-20, y-10),
                       (x-18, y-12),
                       (x-16, y-14),
                       (x-14, y-16),
                       (x-12, y-18),
                       (x-10, y-20),
                       (x-8,  y-22),
                       (x-6,  y-24),
					   (x-4,  y-26),
					   (x-2,  y-28),
					   (x-1,  y-30)
                       ]
  
    pygame.draw.circle(gameDisplay, blue, (x,y), int(tankHeight/2))
    pygame.draw.rect(gameDisplay, blue, (x-tankHeight, y, tankWidth, tankHeight))
    pygame.draw.line(gameDisplay, blue, (x,y), possibleTurrets[turPos], turretWidth)
  
    
    pygame.draw.circle(gameDisplay, black, (x-15, y+20), wheelWidth)
    pygame.draw.circle(gameDisplay, black, (x-10, y+20), wheelWidth)
    pygame.draw.circle(gameDisplay, black, (x-15, y+20), wheelWidth)
    pygame.draw.circle(gameDisplay, black, (x-10, y+20), wheelWidth)
    pygame.draw.circle(gameDisplay, black, (x-5, y+20), wheelWidth)
    pygame.draw.circle(gameDisplay, black, (x, y+20), wheelWidth)
    pygame.draw.circle(gameDisplay, black, (x+5, y+20), wheelWidth)
    pygame.draw.circle(gameDisplay, black, (x+10, y+20), wheelWidth)
    pygame.draw.circle(gameDisplay, black, (x+15, y+20), wheelWidth)

    return possibleTurrets[turPos]


def enemy_tank(x,y,turPos):
    x = int(x)
    y = int(y)


    possibleTurrets = [(x+30, y-1),
					   (x+28, y-2),
                       (x+26, y-4),
                       (x+24, y-6),
                       (x+22, y-8),
                       (x+20, y-10),
                       (x+18, y-12),
                       (x+16, y-14),
                       (x+14, y-16),
                       (x+12, y-18),
                       (x+10, y-20),
                       (x+8,  y-22),
                       (x+6,  y-24),
					   (x+4,  y-26),
					   (x+2,  y-28),
					   (x+1,  y-30)
                       ]
  
    pygame.draw.circle(gameDisplay, red, (x,y), int(tankHeight/2))
    pygame.draw.rect(gameDisplay, red, (x-tankHeight, y, tankWidth, tankHeight))

    pygame.draw.line(gameDisplay, red, (x,y), possibleTurrets[turPos], turretWidth)

    pygame.draw.circle(gameDisplay, black, (x-15, y+20), wheelWidth)
    pygame.draw.circle(gameDisplay, black, (x-10, y+20), wheelWidth)
    pygame.draw.circle(gameDisplay, black, (x-15, y+20), wheelWidth)
    pygame.draw.circle(gameDisplay, black, (x-10, y+20), wheelWidth)
    pygame.draw.circle(gameDisplay, black, (x-5, y+20), wheelWidth)
    pygame.draw.circle(gameDisplay, black, (x, y+20), wheelWidth)
    pygame.draw.circle(gameDisplay, black, (x+5, y+20), wheelWidth)
    pygame.draw.circle(gameDisplay, black, (x+10, y+20), wheelWidth)
    pygame.draw.circle(gameDisplay, black, (x+15, y+20), wheelWidth)

    return possibleTurrets[turPos]


def game_controls():


    gcont = True

    while gcont:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(purple)

        gameDisplay.fill(pink)
        message_to_screen("CONTROLS",purple,-270,size="large")
        #message_to_screen("PLAYER 1",black,-240,size="large")
        message_to_screen("FIRE: Spacebar",black,-180,size="medium")
        message_to_screen("Move Turret: W and S ",black,-150,size="medium")
        message_to_screen("Move Tank: A and D",black,-120,size="medium")
        message_to_screen("Adjust Power: Q to increase and E to decrease",black,-90,size="medium")
##      message_to_screen("PLAYER 2",black,-50,size="large")
##      message_to_screen("FIRE: J",black,-20,size="medium")
##      message_to_screen("Move Turret: UP Arrow and DOWN Arrow ",black,10,size="medium")
##      message_to_screen("Move Tank: LEFT Arrow and RIGHT Arrow",black,40,size="medium")
##      message_to_screen("Adjust Power: K to increase and L to decrease",black,70,size="medium")
        message_to_screen("Pause: P",black,150,size="medium")
        button("PLAY",150,490,150,100,dark_green,green,size="large",action="play")
        button("QUIT",550,490,150,100,maroon,red,size="large",action="quit")

        pygame.display.update()

        clock.tick(15)


def button(text, x, y, width, height, inactive_color, active_color,size,action = None):
    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    #print(click)
    if x + width > cur[0] > x and y + height > cur[1] > y:
        pygame.draw.rect(gameDisplay, active_color, (x,y,width,height))
        if click[0] == 1 and action != None:
            if action == "quit":
                pygame.quit()
                quit()

            if action == "controls":
                game_controls()

            if action == "play":
                gameLoop()
            
    else:
        pygame.draw.rect(gameDisplay, inactive_color, (x,y,width,height))

    text_to_button(text,black,x,y,width,height,size)
        


def pause():

    paused = True
    message_to_screen("Paused",black,-100,size="large")
    message_to_screen("Press C to continue playing or Q to quit",black,25,size="medium")
    pygame.display.update()
    while paused:
        for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        paused = False
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        quit()
        clock.tick(5)



def barrier(xlocation,randomHeight, barrier_width):
    pygame.draw.rect(gameDisplay, brown, [xlocation, display_height-randomHeight, barrier_width,randomHeight])
    
def explosion(x, y, size=50):

    explode = True

    while explode:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        startPoint = x,y

        colorChoices = [red, maroon, dark_green, green]

        magnitude = 1

        while magnitude < size:

            exploding_bit_x = x +random.randrange(-1*magnitude,magnitude)
            exploding_bit_y = y +random.randrange(-1*magnitude,magnitude)

            pygame.draw.circle(gameDisplay, colorChoices[random.randrange(0,4)], (exploding_bit_x,exploding_bit_y),random.randrange(1,5))
            magnitude += 1

            pygame.display.update()
            clock.tick(100)

        explode = False
        
        


def fireShell(xy,tankx,tanky,turPos,gun_power,xlocation,barrier_width,randomHeight,enemyTankX,enemyTankY,turn,initialTankX):
    fire = True
    damage = 0

    startingShell = list(xy)

    #print("FIRE!",xy)

                
    while fire:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pygame.draw.circle(gameDisplay, red, (startingShell[0],startingShell[1]),5)


        startingShell[0] -= (16 - turPos)*2

        startingShell[1] += int((((startingShell[0]-xy[0])*0.016/(gun_power/50))**2) - (turPos+turPos/(16-turPos)))

        if startingShell[1] > display_height-ground_height:
            #print("Last shell:",startingShell[0], startingShell[1])
            hit_x = int((startingShell[0]*display_height-ground_height)/startingShell[1])
            hit_y = int(display_height-ground_height)
            #print("Impact:", hit_x,hit_y)
            
            if enemyTankX + 10 > hit_x > enemyTankX - 10:
                #print("Critical Hit!")
                damage = 25
            elif enemyTankX + 15 > hit_x > enemyTankX - 15:
                #print("Hard Hit!")
                damage = 18
            elif enemyTankX + 25 > hit_x > enemyTankX - 25:
                #print("Medium Hit")
                damage = 10
            elif enemyTankX + 35 > hit_x > enemyTankX - 35:
                #print("Light Hit")
                damage = 5
            
            explosion(hit_x,hit_y)
            fire = False

        check_x_1 = startingShell[0] <= xlocation + barrier_width
        check_x_2 = startingShell[0] >= xlocation

        check_y_1 = startingShell[1] <= display_height
        check_y_2 = startingShell[1] >= display_height - randomHeight

        if check_x_1 and check_x_2 and check_y_1 and check_y_2:
            #print("Last shell:",startingShell[0], startingShell[1])
            hit_x = int((startingShell[0]))
            hit_y = int(startingShell[1])
            #print("Impact:", hit_x,hit_y)
            explosion(hit_x,hit_y)
            fire = False
            

        pygame.display.update()
        clock.tick(60)
        
##################################################################################################################

    if (turn == -1): #Storing user input into database
        user_dynamic_entry( gun_power, turPos, initialTankX, hit_x, randomHeight, enemyTankX, damage)
        turn = turn * -1
        print("initial: "+str(initialTankX)+" Drop point: "+str(hit_x) + " Turret pos:" + 
str(turPos) + " Power:" + str(gun_power)  +" Barrier: "+str(randomHeight) +" Enemy tank: "+str(enemyTankX) + " Damage: " + str(damage))

            
    return damage,turn

        
def e_fireShell(xy,tankx,tanky,turPos,gun_power,xlocation,barrier_width,randomHeight,ptankx,ptanky,turn):

    damage = 0
    currentPower = 1
    power_found = False
    turn = turn * -1
    
    while not power_found:
        currentPower += 1
        if currentPower > 100:
            power_found = True

        fire = True
        startingShell = list(xy)


        while fire:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            startingShell[0] += (16 - turPos)*2
            startingShell[1] += int((((startingShell[0]-xy[0])*0.016/(currentPower/50))**2) - (turPos+turPos/(16-turPos)))

            if startingShell[1] > display_height-ground_height:
                hit_x = int((startingShell[0]*display_height-ground_height)/startingShell[1])
                hit_y = int(display_height-ground_height)
                #explosion(hit_x,hit_y)
                if ptankx+16 > hit_x > ptankx - 16:
                    print("target acquired!")
                    power_found = True
                fire = False

            check_x_1 = startingShell[0] <= xlocation + barrier_width
            check_x_2 = startingShell[0] >= xlocation

            check_y_1 = startingShell[1] <= display_height
            check_y_2 = startingShell[1] >= display_height - randomHeight

            if check_x_1 and check_x_2 and check_y_1 and check_y_2:
                hit_x = int((startingShell[0]))
                hit_y = int(startingShell[1])
                fire = False
    

    
    fire = True
    startingShell = list(xy)
    #print("FIRE!",xy)

    while fire:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pygame.draw.circle(gameDisplay, red, (startingShell[0],startingShell[1]),5)


        startingShell[0] += (16 - turPos)*2


        gun_power = random.randrange(int(currentPower*0.90), int(currentPower*1.10))
        
        startingShell[1] += int((((startingShell[0]-xy[0])*0.016/(gun_power/50))**2) - (turPos+turPos/(16-turPos)))

        if startingShell[1] > display_height-ground_height:
            #print("last shell:",startingShell[0],startingShell[1])
            hit_x = int((startingShell[0]*display_height-ground_height)/startingShell[1])
            hit_y = int(display_height-ground_height)
            #print("Impact:",hit_x,hit_y)


            if abs(ptankx - hit_x) < 10:
                print("Critical Hit!")
                damage = 25
            elif abs(ptankx - hit_x) < 15:
                print("Hard Hit!")
                damage = 18
            elif abs(ptankx - hit_x) < 25:
                print("Medium Hit")
                damage = 10
            elif abs(ptankx - hit_x) < 35:
                print("Light Hit")
                damage = 5


            
            explosion(hit_x,hit_y)
            fire = False

        check_x_1 = startingShell[0] <= xlocation + barrier_width
        check_x_2 = startingShell[0] >= xlocation

        check_y_1 = startingShell[1] <= display_height
        check_y_2 = startingShell[1] >= display_height - randomHeight

        if check_x_1 and check_x_2 and check_y_1 and check_y_2:
            #print("Last shell:",startingShell[0], startingShell[1])
            hit_x = int((startingShell[0]))
            hit_y = int(startingShell[1])
            #print("Impact:", hit_x,hit_y)
            explosion(hit_x,hit_y)
            fire = False        

        pygame.display.update()
        clock.tick(60)
        
    return damage,turn

def power(level):
    text = medfont.render("Power: "+str(level)+"%",True, black)
    gameDisplay.blit(text, [display_width/2,0])

def game_intro():

    intro = True

    while intro:
        for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        intro = False
                    elif event.key == pygame.K_q:
                        
                        pygame.quit()
                        quit()

        gameDisplay.fill(pink)
        message_to_screen("Welcome to Pocket Tanks!",dark_green,-100,size="large")
        message_to_screen("The objective is to shoot and destroy",purple,-30,size="medium")
        message_to_screen("the enemy tank before they destroy you.",purple,10,size="medium")
        message_to_screen("The more enemies you destroy, the harder they get.",purple,50,size="medium")

        button("PLAY",150,400,150,100,dark_green,green,size="large",action="play")
        button("CONTROLS",335,400,180,100,blue,light_blue,size="large",action="controls")
        button("QUIT",550,400,150,100,maroon,red,size="large",action="quit")
        pygame.display.update()
        clock.tick(15)

def game_over():

    game_over = True

    while game_over:
        for event in pygame.event.get():
                #print(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

        gameDisplay.fill(light_blue)
        message_to_screen("Game Over",green,-100,size="large")
        message_to_screen("You died.",black,-30,size="medium")



        button("play Again", 150,500,150,50, green, light_green,size="large",action="play")
        button("controls", 350,500,100,50, yellow, light_yellow,size="large",action="controls")
        button("quit", 550,500,100,50, red, red,size="large",action ="quit")


        pygame.display.update()

        clock.tick(15)

def you_win():

    win = True

    while win:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(light_blue)
        message_to_screen("You won!",green,-100,size="large")
        message_to_screen("Congratulations!",black,-30,size="medium")



        button("play Again", 150,500,150,50, green, light_green,size="large",action="play")
        button("controls", 350,500,100,50, yellow, light_yellow,size="large",action="controls")
        button("quit", 550,500,100,50, red, red,size="large",action ="quit")


        pygame.display.update()

        clock.tick(15)


def health_bars(player_health, enemy_health):

    if player_health > 75:
        player_health_color = green
    elif player_health > 50:
        player_health_color = yellow
    else:
        player_health_color = red

    if enemy_health > 75:
        enemy_health_color = green
    elif enemy_health > 50:
        enemy_health_color = yellow
    else:
        enemy_health_color = red

    pygame.draw.rect(gameDisplay, player_health_color, (680, 25, player_health, 25))
    pygame.draw.rect(gameDisplay, enemy_health_color, (20, 25, enemy_health, 25))




def gameLoop():
    gameExit = False
    gameOver = False
    FPS = 20
    turn = -1    
    player_health = 100
    enemy_health = 100

    barrier_width = 40
    initialTankX = 0
    mainTankX = display_width * 0.9    
    mainTankY = display_height * 0.9 
    tankMove = 0
    currentTurPos = 0
    changeTur = 0
    db_power=70
    db_turret=12

    enemyTankX = display_width * 0.1
    enemyTankY = display_height * 0.9

    fire_power = 50
    power_change = 0

    xlocation = (display_width/2) 
    #randomHeight = random.randrange(display_height*0.1,display_height*0.6)
    randomHeight = random.randrange(display_height*0.3,display_height*0.6)
    
    while not gameExit:        
                
        if gameOver == True:
            #gameDisplay.fill(white)
            message_to_screen("Game Over",red,-50,size="large")
            message_to_screen("Press C to play again or Q to exit",black,50)
            pygame.display.update()
            while gameOver == True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        gameExit = True
                        gameOver = False

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_c:
                            gameLoop()
                        elif event.key == pygame.K_q:
                            gameExit = True
                            gameOver = False
         


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True

            if event.type == pygame.KEYDOWN: #Move tank Left
                if event.key == pygame.K_a:
                    tankMove = -5
                elif event.key == pygame.K_d: #Move tank right
                    tankMove = 5
                elif event.key == pygame.K_UP: #Move turret up
                    changeTur = 1
                elif event.key == pygame.K_DOWN: #Move turret down
                    changeTur = -1
                elif event.key == pygame.K_p:
                    pause()
                elif event.key == pygame.K_SPACE: #Launch attack
                    
                    damage,turn = fireShell(gun,mainTankX,mainTankY,currentTurPos,fire_power,xlocation,barrier_width,randomHeight,enemyTankX,enemyTankY,turn,initialTankX)
                    enemy_health -= damage
                    
                    db_power,db_turret = selecting(initialTankX,enemyTankX)
                    
                    damage,turn = e_fireShell(enemy_gun,enemyTankX,enemyTankY,db_turret,db_power,xlocation,barrier_width,randomHeight,mainTankX,mainTankY,turn)
                    player_health -= damage
                    
                    possibleMovement = ['f','r']
                    moveIndex = random.randrange(0,2)

                    for x in range(random.randrange(0,10)):

                        if display_width * 0.3 > enemyTankX > display_width * 0.03:
                            if possibleMovement[moveIndex] == "f":
                                enemyTankX += 5
                            elif possibleMovement[moveIndex] == "r":
                                enemyTankX -= 5

                            gameDisplay.fill(light_blue)
                            health_bars(player_health,enemy_health)
                            gun = tank(mainTankX,mainTankY,currentTurPos)

                            enemy_gun = enemy_tank(enemyTankX, enemyTankY, db_turret)
                            power(fire_power)
                            barrier(xlocation,randomHeight,barrier_width)
                            gameDisplay.fill(green, rect=[0, display_height-ground_height, display_width, ground_height])
                            pygame.display.update()

                            clock.tick(FPS)
                   
                    
                elif event.key == pygame.K_LEFT:
                    power_change = -1
                elif event.key == pygame.K_RIGHT:
                    power_change = 1

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    tankMove = 0

                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    changeTur = 0
                    
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    power_change = 0
                

        if turn == -1:
            initialTankX = mainTankX
                    
        mainTankX += tankMove

        currentTurPos += changeTur

        if currentTurPos > 15:
            currentTurPos = 15
        elif currentTurPos < 1:
            currentTurPos = 1


        if mainTankX - (tankWidth/1.5) < xlocation+barrier_width:
            mainTankX += 5

        if mainTankX + (tankWidth/2) > display_width:
            mainTankX -= 5 

        if enemyTankX + (tankWidth/2) < 0:
            enemyTankX += 5 

        gameDisplay.fill(light_blue)
        health_bars(player_health,enemy_health)
        gun = tank(mainTankX,mainTankY,currentTurPos)
        enemy_gun = enemy_tank(enemyTankX, enemyTankY, db_turret)
        fire_power += power_change

        if fire_power >= 100:
            fire_power =100
        elif fire_power <= 1:
            fire_power = 1
    
        power(fire_power)

        barrier(xlocation,randomHeight,barrier_width)
        gameDisplay.fill(green, rect=[0, display_height-ground_height, display_width, ground_height])
        pygame.display.update()
        
        
        
        if player_health < 1:
            game_over()
        elif enemy_health < 1:
            you_win()
        clock.tick(FPS)
            
    pygame.quit()
    quit()

create_table()
game_intro()
gameLoop()
cursor.close()
conn.close()
