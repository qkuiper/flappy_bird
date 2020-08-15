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
            death_sound.play()
            return False
    if bird_rect.bottom >= 450:
        death_sound.play()
        return False
    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird,-bird_movement*5,1)
    return new_bird

def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (50,bird_rect.centery))
    return new_bird, new_bird_rect

def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)),True,(255,255,255))
        score_rect = score_surface.get_rect(center = (0.5*screen_width,50))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}',True,(255,255,255))
        score_rect = score_surface.get_rect(center = (0.5*screen_width,50))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High score: {int(high_score)}',True,(255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (0.5*screen_width,425))
        screen.blit(high_score_surface, high_score_rect)

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

pygame.mixer.pre_init(frequency = 44100, size = 16, channels = 1, buffer = 512)
pygame.init()
screen_width = 288
screen_height = 512
screen = pygame.display.set_mode((screen_width,screen_height)) #devided original 576,1024 by 2
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf',30)

# Game Variables
gravity = 0.125
bird_movement = 0
game_active = True
score = 0
high_score = 0


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

game_over_surface = pygame.image.load('assets/message.png').convert_alpha()
game_over_rect = game_over_surface.get_rect(center = (0.5*screen_width,0.5*screen_height))

flap_sound = pygame.mixer.Sound('audio/wing.wav')
death_sound = pygame.mixer.Sound('audio/hit.wav')
score_sound = pygame.mixer.Sound('audio/point.wav')
score_sound_countdown = 100

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
                    flap_sound.play()
                else: 
                    bird_movement = 0
                    bird_movement -= 4
                    flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (50,256)
                bird_movement = 0
                score = 0
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
        score += 0.01
        if game_active:
            score_display('main_game')
            score_sound_countdown -= 1
            if score_sound_countdown <= 0:
                score_sound.play()
                score_sound_countdown = 100
    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')

    # Floor
    if game_active:
        floor_x_pos -= 0.5
    draw_floor()
    if floor_x_pos <= -screen_width:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120)