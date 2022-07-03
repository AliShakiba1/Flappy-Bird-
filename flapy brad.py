

import pygame 
import sys
import random
import time

pygame.init()

disp_width = 576 
disp_height  = 900
floor_x = 0 
gravity = 0.25
bird_movmet = 0
pipe_list = []
game_status = True
bird_list_index = 0 
score_s = 0 
high_score = 0 
active_score = True


def generat_pipe():
    random_pipe = random.randrange(400, 600 )
    pipe_rect_bottom = pipe_image.get_rect(midtop = (900, random_pipe))
    pipe_rect_top = pipe_image.get_rect(midbottom = (900, random_pipe - 300 ))
    return pipe_rect_top, pipe_rect_bottom


def move_pipe_rect(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    inside_pipes = [pipe for pipe in pipes if pipe.right > -50]
    return inside_pipes


def disp_pipe(pipes):
    for pipe in pipes :
        if pipe.bottom >= 900:
            main_screen.blit(pipe_image, pipe)
        else : 
            reversed_pipe = pygame.transform.flip(pipe_image,False,True)
            main_screen.blit(reversed_pipe, pipe)


def check_collison(pipes):
    global active_score
    for pipe in pipes:
        if bird_image_rect.top <= 50 or bird_image_rect.bottom >= 790:
            game_over_sound.play()
            time.sleep(3)
            active_score = True
            return False
        if bird_image_rect.colliderect(pipe):
            game_over_sound.play()
            time.sleep(3)
            return False
    return True


def brid_animition():
    new_bird = bird_list[bird_list_index]
    new_bird_rect = new_bird.get_rect(center = (100, bird_image_rect.centery))
    return new_bird,new_bird_rect


def Score(stast):
    if stast == 'active' :
        text1 = game_font.render(str(score_s), True,(255, 255, 255))
        text1_rect = text1.get_rect(center = (288,100))
        main_screen.blit(text1,text1_rect)
    if stast == 'game_over' :
        text1 = game_font.render(f'Score : {str(score_s)} ', True,(255, 255, 255))
        text1_rect = text1.get_rect(center = (288,100))
        main_screen.blit(text1,text1_rect)

        # high score 
        text1 = game_font.render(f'High Score : {str(high_score)} ', True,(255, 255, 255))
        text1_rect = text1.get_rect(center = (288,250))
        main_screen.blit(text1,text1_rect) 


def update_score():
    global score_s,high_score,active_score
    if pipe_list:
        for pipe in pipe_list:
            if 95 < pipe.centerx < 105 and active_score :
                win_sound.play()
                score_s += 1
                active_score = False
            if pipe.centerx < 0 :
                active_score = True
            
    if score_s > high_score : 
        high_score = score_s 
    return high_score



create_pipe = pygame.USEREVENT
create_flap = pygame.USEREVENT + 1
pygame.time.set_timer(create_flap, 200)
pygame.time.set_timer(create_pipe, 1200)


game_font = pygame.font.Font('assets/font/Flappy.TTF', 40 )

background_image = pygame.image.load('assets/img/bg1.png')
background_image = pygame.transform.scale2x(background_image)
floor_image = pygame.transform.scale2x(pygame.image.load('assets/img/floor.png'))
pipe_image = pygame.transform.scale2x(pygame.image.load('assets/img/pipe_red.png'))

game_over_image = pygame.transform.scale2x(pygame.image.load('assets/img/message.png'))

bird_image_mid = pygame.transform.scale2x(pygame.image.load('assets/img/red_bird_mid_flap.png'))
bird_image_up = pygame.transform.scale2x(pygame.image.load('assets/img/red_bird_up_flap.png'))
bird_image_down = pygame.transform.scale2x(pygame.image.load('assets/img/red_bird_down_flap.png'))

bird_list = [bird_image_down,bird_image_mid,bird_image_up]
bird_image = bird_list[bird_list_index]


bird_image_rect = bird_image.get_rect(center =(100, 450))

game_over_image_rect = game_over_image.get_rect(center=(288,380))


main_screen = pygame.display.set_mode((disp_width, disp_height))
clock = pygame.time.Clock()



game_over_sound = pygame.mixer.Sound('assets/sound/smb_mariodie.wav')
win_sound = pygame.mixer.Sound('assets/sound/smb_stomp.wav')



keys = pygame.key.get_pressed()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT :
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_SPACE and game_status == False :
                game_status = True
                score_s = 0 
                pipe_list.clear()
                bird_image_rect.center = (100, 450)
                bird_movmet = 0 

            if event.key == pygame.K_SPACE :
                bird_movmet = 0 
                bird_movmet -= 8
                  
        if event.type == create_pipe:
            pipe_list.extend(generat_pipe())
        if event.type == create_flap:
            bird_list_index += 1
            if bird_list_index == 3 :
                bird_list_index = 0
            bird_image, bird_image_rect = brid_animition()


    main_screen.blit(background_image, (0, 0))

    if game_status :
        game_status = check_collison(pipe_list)

        main_screen.blit(bird_image, bird_image_rect )

        pipe_list = move_pipe_rect(pipe_list)
        disp_pipe(pipe_list)

        bird_movmet += gravity
        bird_image_rect.centery += bird_movmet

        update_score()
        Score('active')
    else:
        main_screen.blit(game_over_image, game_over_image_rect)
        Score('game_over')


    main_screen.blit(floor_image, (floor_x, 810))
    main_screen.blit(floor_image, (floor_x + 576, 810))
    floor_x -= 1
    if floor_x  == -576 :
        floor_x = 0
    

    pygame.display.update()
    clock.tick(90)


pygame.quit()