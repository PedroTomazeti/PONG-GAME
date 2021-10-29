from ursina import *
from ursina import texture
import pygame
from ursina import collider

pygame.init()
som_colisao_paddle = pygame.mixer.Sound('paddle.mp3')
som_colisao_wall = pygame.mixer.Sound('wall.mp3')
som_score = pygame.mixer.Sound('score.mp3')

score_1 = 0
score_2 = 0
timer = 1


def placar():
    print_on_screen(f'{score_1} : {score_2}',
                    position=(-.4/3, .4), scale=6, duration=2)


def reset():
    ball.x = 0
    ball.y = 0


def update():
    global dx, dy, timer, score_1, score_2
    # movimentação da raquete
    racket_1.y += held_keys['a']*time.dt*4
    racket_1.y -= held_keys['d']*time.dt*4
    racket_2.y += held_keys['right arrow']*time.dt*4
    racket_2.y -= held_keys['left arrow']*time.dt*4
    # movimento da bola
    ball.x += time.dt * dx * timer
    ball.y += time.dt * dy * timer
    # mecânica de colisão nas raquetes
    hit_info = ball.intersects()
    if hit_info.hit:
        if hit_info.entity == racket_1 or hit_info.entity == racket_2:
            dx = -dx
            som_colisao_paddle.play()
            timer += 0.3
    # mecânica de colisão nas paredes
    if abs(ball.y) > 3.8:
        dy = -dy
        som_colisao_wall.play()
    # mecânica de pontos
    if ball.x > 8:
        timer = 1
        som_score.play()
        score_1 += 1
        print_on_screen(f'{score_1} : {score_2}',
                        position=(-.4/3, .4), scale=6, duration=10)
        reset()

    if ball.x < - 8:
        timer = 1
        som_score.play()
        score_2 += 1
        print_on_screen(f'{score_1} : {score_2}',
                        position=(-.4/3, .4), scale=6, duration=2)
        reset()


app = Ursina()
placar()
racket_1 = Entity(model='quad', color=color.white,
                  position=(-6.5, 0), scale=(.2, 1.2), collider='box')
racket_2 = duplicate(racket_1, x=6.5)
ball = Entity(model='quad', color=color.white,
              position=(0, 0), scale=.4, collider='box')
dx = 1
dy = 1
window.color = color.black
print_on_screen("Player 1 controls: 'a' to go up, 'd' to go down",
                position=(-.7, -.7/2), scale=1, duration=8)
print_on_screen("Player 2 controls: 'R arrow' to go up, 'L arrow' to go down",
                position=(.1, -.7/2), scale=1, duration=8)
app.run()
