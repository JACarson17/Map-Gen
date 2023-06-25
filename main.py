import pygame
from generator.constants import WIDTH, HEIGHT, FPS
from generator.generator import Generator

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

def main():
    run = True
    clock = pygame.time.Clock()

    generator = Generator(WIN)
    while run:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                generator.generate()
        generator.update()
    pygame.quit()

if __name__ == '__main__':
    main()