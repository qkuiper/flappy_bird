import pygame, sys

def draw_floor():
    screen.blit(floor_surface, (floor_x_pos,450))
    screen.blit(floor_surface, (floor_x_pos+screen_width,450))

pygame.init()
screen_width = 288
screen_height = 512
screen = pygame.display.set_mode((screen_width,screen_height)) #devided original 576,1024 by 2
clock = pygame.time.Clock()

# Game Variables
gravity = 0.125
bird_movement = 0

bg_surface = pygame.image.load('assets/background-day.png').convert()
# bg_surface = pygame.transform.scale2x(bg_surface) no scaling needed

floor_surface = pygame.image.load('assets/base.png').convert()
# floor_surface = pygame.transform.scale2x(floor_surface) no scaling needed
floor_x_pos = 0

bird_surface = pygame.image.load('assets/bluebird-midflap.png').convert()
# bird_surface = pygame.transform.scale2x(bird_surface) no scaling needed
bird_rect = bird_surface.get_rect(center = (50,256))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement -= 6

    bird_movement += gravity
    bird_rect.centery += bird_movement
    screen.blit(bg_surface, (0,0))
    screen.blit(bird_surface, bird_rect)
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -screen_width:
        floor_x_pos = 0


    pygame.display.update()
    clock.tick(120)