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
pygame.display.set_caption("brick breaking")
pygame.display.set_icon(icon_image)
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
screen.blit(background_image,(0,0))

# 프레임 및 게임 종료 조건 설정
clock= pygame.time.Clock()

# 벽돌 생성
bricks = []
COLUMN = 10
ROW = 2
brick_width = 70
brick_height = 30
brick_spacing = 20

for column_index in range(COLUMN):
    for row_index in range(ROW):
        brick_x = screen_width / 2 - (COLUMN * (brick_width + brick_spacing) / 2) + column_index * (brick_width + brick_spacing)
        brick_y = row_index * (brick_height + brick_spacing) + 35
        brick = pygame.Rect(brick_x, brick_y, brick_width, brick_height)
        bricks.append(brick)
for brick in bricks:
    pygame.draw.rect(screen, RED, brick)

# 바 생성
bar = pygame.Rect(screen_width // 2 - 80 // 2, screen_height - 16, 80, 16)
pygame.draw.rect(screen, BLUE,bar)

# 공 생성
ball_radius = 8
ball = pygame.Rect(screen_width // 2 - ball_radius, bar.top - ball_radius * 2, ball_radius * 2, ball_radius * 2)
ball_dx = 5
ball_dy = -5
pygame.draw.circle(screen, YELLOW, ball.center, ball_radius)

# 게임 시작 문구 생성
start_text = small_font.render("press spacekey to start game", True, BLACK)
start_text_rect = start_text.get_rect(center=(screen_width // 2, screen_height // 2))

game_started = False

# 게임 시작
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if not game_started and event.key == pygame.K_SPACE:
                game_started = True
                
    if game_started:  # 게임이 시작된 상태라면
        # 바 이동
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and bar.left > 0:
            bar.move_ip(-5, 0)
        if keys[pygame.K_RIGHT] and bar.right < screen_width:
            bar.move_ip(5, 0)

        # 공 이동
        ball.x += ball_dx
        ball.y += ball_dy
        
    # 화면 지우기
    screen.blit(background_image,(0,0))

    # 벽돌 그리기
    for brick in bricks:
        pygame.draw.rect(screen, GREEN, brick)
    
    # 공 그리기
    pygame.draw.circle(screen, YELLOW, ball.center, ball_radius)

    # 바 그리기
    pygame.draw.rect(screen, BLUE, bar)
    # 게임 시작 문구 그리기
    if not game_started:
        screen.blit(start_text, start_text_rect)

    # 화면 업데이트
    pygame.display.flip()

    # 게임 속도 조절
    clock.tick(60)