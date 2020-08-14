import pygame, random, sys

def draw_floor():
    screen.blit(floor_surface, (floor_x_pos,450))
    screen.blit(floor_surface, (floor_x_pos+screen_width,450))

def create_pipe():
    random_pipe_height = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (screen_width+12,random_pipe_height))
    top_pipe = pipe_surface.get_rect(midbottom = (screen_width+12,random_pipe_height-150))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 1.5
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 512:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe_surface = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe_surface, pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    if bird_rect.bottom >= 450:
        return False
    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird,-bird_movement*5,1)
    return new_bird

def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (50,bird_rect.centery))
    return new_bird, new_bird_rect

pygame.init()
screen_width = 288
screen_height = 512
screen = pygame.display.set_mode((screen_width,screen_height)) #devided original 576,1024 by 2
clock = pygame.time.Clock()

# Game Variables
gravity = 0.125
bird_movement = 0
game_active = True

bg_surface = pygame.image.load('assets/background-day.png').convert() # no scaline needed

floor_surface = pygame.image.load('assets/base.png').convert() # no scaline needed
floor_x_pos = 0

bird_downflap = pygame.image.load('assets/bluebird-downflap.png').convert_alpha()
bird_midflap = pygame.image.load('assets/bluebird-midflap.png').convert_alpha()
bird_upflap = pygame.image.load('assets/bluebird-upflap.png').convert_alpha()
bird_frames = [bird_downflap, bird_midflap, bird_upflap, bird_midflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (50,256))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP,150)

# bird_surface = pygame.image.load('assets/bluebird-midflap.png').convert_alpha() # no scaline needed
# bird_rect = bird_surface.get_rect(center = (50,256))

pipe_surface = pygame.image.load('assets/pipe-green.png').convert() # no scaline needed
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1200)
pipe_height = [200, 300, 400]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                if bird_rect.top + bird_movement <= 0:   
                    bird_rect.top = 0
                    bird_movement = 0
                else: 
                    bird_movement = 0
                    bird_movement -= 4
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (50,256)
                bird_movement = 0
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
        if event.type == BIRDFLAP:
            if bird_index < 3:
                bird_index += 1
            else:
                bird_index = 0
            bird_surface, bird_rect = bird_animation()

    # Boundry
    if bird_rect.top + bird_movement <= 0:
            bird_rect.top = 0
            bird_movement = 0
    
    if game_active:
        # Bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.top += bird_movement
        screen.blit(bg_surface, (0,0))
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)

        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

    # Floor
    floor_x_pos -= 0.5
    draw_floor()
    if floor_x_pos <= -screen_width:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120)