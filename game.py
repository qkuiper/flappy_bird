import pygame, sys

pygame.init()
screen = pygame.display.set_mode((576,1024))
clock = pygame.time.Clock()

bg_surface = pygame.image.load('assets/background-day.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface)

floor_surface = pygame.image.load('assets/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.blit(bg_surface, (0,0))
    screen.blit(floor_surface, (0,0))

    pygame.display.update()
    clock.tick(60)