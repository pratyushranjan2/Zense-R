import pygame
import time
import random
pygame.init()

display_width=1000
display_height=800

white=(255,255,255)
black=(0,0,0)
light_yellow=(250, 236, 87)
light_green=(149, 245, 210)
deep_green=(7, 26, 19)

gamedisplay=pygame.display.set_mode((display_width,display_height))
carimg=pygame.image.load('lamborghini.png')
crashimg=pygame.image.load('crash.jpg')
introimg=pygame.image.load('intro.jpg')
pygame.display.set_caption('Beat the Traffic')
clock=pygame.time.Clock()
car_width=230
pygame.mixer.music.load('mainmusic.wav')
pausemusic=pygame.mixer.Sound('pausemusic.wav')

def exit():
	pygame.quit()
	quit()

def crashimage():
	gamedisplay.blit(crashimg,(140,0))

def crash():
	pygame.mixer.music.stop()
	largetext=pygame.font.SysFont("freesansbold.ttf",100)
	textsurf,textrect=text_objects("YOU CRASHED",largetext)
	textrect.center=(display_width/2,display_height/2)
	lamborghini(0,0)
	crashimage()
	gamedisplay.blit(textsurf,textrect)
	while True:
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				exit()
		button("PLAY AGAIN",100,600,150,50,black,deep_green,game_loop)
		button("QUIT",800,600,100,50,black,deep_green,exit)
		pygame.display.update()
		clock.tick(15)

def score_display(score):
	font=pygame.font.SysFont(None,45)
	text=font.render("SCORE --> "+str(score),True,white)
	gamedisplay.blit(text,(0,100))

def pause():
	pygame.mixer.music.pause()
	pygame.mixer.Sound.play(pausemusic)
	largeText=pygame.font.SysFont("freesansbold.ttf",100)
	textsurf,textrect=text_objects("PAUSED",largeText)
	textrect.center=(display_width/2,display_height/2)
	lamborghini(0,0)
	gamedisplay.blit(textsurf,textrect)
	cont_signal=0
	while True:
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				exit()
		cont_signal=button("CONTINUE",100,600,120,50,black,deep_green,None)
		if cont_signal==1:
			pygame.mixer.Sound.stop(pausemusic)
			pygame.mixer.music.unpause()
			return
		button("QUIT",800,600,100,50,black,deep_green,exit)
		pygame.display.update()
		clock.tick(15)

def text_objects(text,font):
	textsurf=font.render(text,True,white)
	return textsurf,textsurf.get_rect()

def button(msg,x,y,w,h,ic,ac,action=None):
	mouse=pygame.mouse.get_pos()
	click=pygame.mouse.get_pressed()
	if x<mouse[0]<x+w and y<mouse[1]<y+h:
		pygame.draw.rect(gamedisplay,ac,(x,y,w,h))
		if click[0]==1 and msg!="CONTINUE":
			action()
		elif click[0]==1 and msg=="CONTINUE":
			return 1
	else:
		pygame.draw.rect(gamedisplay,ic,(x,y,w,h))
	smalltext=pygame.font.Font("freesansbold.ttf",20)
	textsurf,textrect=text_objects(msg,smalltext)
	textrect.center=(x+w/2,y+h/2)
	gamedisplay.blit(textsurf,textrect)
def lamborghini(x,y):
	gamedisplay.blit(introimg,(x,y))

def instructions_display():
	font=pygame.font.SysFont(None,45)
	text1=font.render("Press G to Change Gear",True,white)
	text2=font.render("Press p to Pause Game",True,white)
	gamedisplay.blit(text1,(display_width-400,0))
	gamedisplay.blit(text2,(display_width-400,50))

def gear_display(gear):
	font=pygame.font.SysFont(None,45)
	text=font.render("GEAR --> "+str(gear),True,white)
	gamedisplay.blit(text,(0,0))

def speed(gear,alignment):
	if alignment=="horizontal":
		if gear==1:
			return 5
		elif gear==2:
			return 10
		elif gear==3:
			return 20
		elif gear==4:
			return 35
		elif gear==5:
			return 50
		else:
			return 75
	elif alignment=="vertical":
		if gear==1:
			return 10
		elif gear==2:
			return 22
		elif gear==3:
			return 46
		elif gear==4:
			return 60
		elif gear==5:
			return 80
		else:
			return 120

def car(x,y):
	gamedisplay.blit(carimg,(x,y))

def strip(strip_x,strip_y,strip_width,strip_height,colour):
    pygame.draw.rect(gamedisplay,colour,[strip_x,strip_y,strip_width,strip_height])	

def ball(x,y,radius):
    pygame.draw.circle(gamedisplay,light_green,(x,y),radius)

def gameintro():
    while True:
    	for event in pygame.event.get():
    		if event.type==pygame.QUIT:
    			exit()
    	lamborghini(0,0)
    	button("START",100,500,100,50,black,deep_green,game_loop)
    	button("QUIT",800,500,100,50,black,deep_green,exit)
    	pygame.display.update()
    	clock.tick(15)


def game_loop():
	x=display_width*0.45
	y=display_height*0.7
	x_change=0
	strip_x=450
	strip_y=500
	strip_width=60
	strip_height=500
	strip_ychange=0
	gameExit=False
	gear=1
	pygame.mixer.music.play(-1)
	ball_radius=50
	ball_startx=random.randrange(0,display_width)
	ball_starty=-ball_radius
	score=0
	while not gameExit:
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				exit()
			if event.type==pygame.KEYDOWN:
				if event.key==pygame.K_g:
					if gear<6:
						gear+=1
					else:
						gear=1
				if event.key==pygame.K_LEFT:
					x_change=-speed(gear,"horizontal")
				if event.key==pygame.K_RIGHT:
					x_change=speed(gear,"horizontal")
				if event.key==pygame.K_UP:
					strip_ychange+=speed(gear,"vertical")
					ball_starty+=gear*4
				if event.key==pygame.K_p:
					pause()
			if event.type==pygame.KEYUP:
				if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
					x_change=0
				if event.key==pygame.K_UP:
					strip_ychange=0
		x+=x_change
		strip_y+=strip_ychange
		ball_starty+=7
		gamedisplay.fill(black)
		if strip_y>display_height:
			strip_y=-strip_height
		if x>display_width-car_width or x<0:
			x-=x_change
		if ball_starty>display_width+ball_radius:
			ball_startx=random.randrange(0,display_width)
			ball_starty=-ball_radius
			score+=gear
			ball_radius+=5
			ball(ball_startx,ball_starty,ball_radius)
		if x-ball_radius<ball_startx<x+car_width+ball_radius and y-ball_radius<ball_starty<display_width-ball_radius:
			crash()
		strip(strip_x,strip_y,strip_width,strip_height,white    )
		car(x,y)
		ball(ball_startx,ball_starty,ball_radius)
		gear_display(gear)
		instructions_display()
		score_display(score)
		pygame.display.update()
		clock.tick(60)

gameintro()
game_loop()
