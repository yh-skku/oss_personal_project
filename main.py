import pygame

pygame.init()

# 색상 및 폰트 설정
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
large_font = pygame.font.SysFont(None, 72)
small_font = pygame.font.SysFont(None, 36)

# 이미지 불러오기
icon_image = pygame.image.load("icon.jpg")
background_image = pygame.image.load("background.png")


# 화면 설정
screen_width = 1000
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height)) 
pygame.display.set_caption("block breaking")
pygame.display.set_icon(icon_image)
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# 프레임 및 게임 종료 조건 설정
clock= pygame.time.Clock()


# 게임 시작
def runGame():
    running = True
    screen.blit(background_image,(0,0))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        clock.tick(10)
        pygame.display.flip()
 
runGame()
pygame.quit()
