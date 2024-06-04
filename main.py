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
bar = pygame.Rect(screen_width // 2 - 80 // 2, screen_height - 16 - 30, 80, 16)
pygame.draw.rect(screen, BLUE,bar)

# 공 생성
ball_radius = 8
ball = pygame.Rect(screen_width // 2 - ball_radius, bar.top - ball_radius * 2, ball_radius * 2, ball_radius * 2)
ball_dx = 5
ball_dy = -5
pygame.draw.circle(screen, YELLOW, ball.center, ball_radius)

# 게임 시작 및 종료 문구, 최고 점수 텍스트 생성 
start_text = small_font.render("press spacekey to start game", True, BLACK)
start_text_rect = start_text.get_rect(center=(screen_width // 2, screen_height // 2))
end_text = small_font.render("game over (press spacekey to retry)", True, BLACK)
end_text_rect = end_text.get_rect(center=(screen_width // 2, screen_height // 2))

# 점수 설정

def print_score():
    score_text = small_font.render(f"Score: {point}", True, BLACK)
    screen.blit(score_text, (5, 5))

def print_max_score():
    max_score_text = small_font.render(f"max score: {max_point}", True, BLACK)
    screen.blit(max_score_text, (5,40))

game_started = False
first_game = True

point = 0
max_point = 0
ball_hit_count = 0

# 게임 초기화
def reset_game():
    global bricks, bar, ball, ball_dx, ball_dy, game_started, life, point
    bricks = []
    for column_index in range(COLUMN):
        for row_index in range(ROW):
            brick_x = screen_width / 2 - (COLUMN * (brick_width + brick_spacing) / 2) + column_index * (brick_width + brick_spacing)
            brick_y = row_index * (brick_height + brick_spacing) + 35
            brick = pygame.Rect(brick_x, brick_y, brick_width, brick_height)
            bricks.append(brick)
    bar = pygame.Rect(screen_width // 2 - 80 // 2, screen_height - 16 - 30, 80, 16)
    ball = pygame.Rect(screen_width // 2 - ball_radius, bar.top - ball_radius * 2, ball_radius * 2, ball_radius * 2)
    ball_dx = 5
    ball_dy = -5
    point = 0
    ball_hit_count = 0 

reset_game()

# 새로운 벽돌을 생성하면서 벽돌을 한 칸 아래로 이동
def move_bricks_down():
    for brick in bricks:
        brick.y += brick_height + brick_spacing

    # 맨 위에 새로운 벽돌 추가
    for column_index in range(COLUMN):
        brick_x = screen_width / 2 - (COLUMN * (brick_width + brick_spacing) / 2) + column_index * (brick_width + brick_spacing)
        brick_y = 35
        new_brick = pygame.Rect(brick_x, brick_y, brick_width, brick_height)
        bricks.append(new_brick)


# 게임 시작
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if not game_started and event.key == pygame.K_SPACE:
                reset_game()
                game_started = True
                first_game = False
            
                
    if game_started:  # 게임이 시작된 상태라면
        # 바 이동
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and bar.left > 0:
            bar.move_ip(-10, 0)
        if keys[pygame.K_RIGHT] and bar.right < screen_width:
            bar.move_ip(10, 0)

        # 공 이동
        ball.x += ball_dx
        ball.y += ball_dy
        ball.left += ball_dx
        ball.top  += ball_dy

        if ball.left <= 0: # 공이 왼쪽 벽에 닿았을 경우
            ball.left = 0
            ball_dx = -ball_dx
        elif ball.left >= screen_width - ball.width: #공이 오른쪽 벽에 닿았을 경우
            ball.left = screen_width - ball.width
            ball_dx = -ball_dx
        if ball.top < 0: # 공이 천장에 닿았을 경우
            ball.top = 0
            ball_dy = -ball_dy
        elif ball.top >= screen_height: # 공이 바닥에 닿았을 경우
            game_started = False
            if max_point < point:
                max_point = point

        # 공이 벽돌에 닿았을 경우
        for brick in bricks:
            if ball.colliderect(brick):
                bricks.remove(brick)
                ball_dy = -ball_dy
                point+=1
                break
    
        # 공이 바에 닿았을 경우
        if ball.colliderect(bar):
            ball_dy = -ball_dy
            ball_hit_count += 1
            if ball_hit_count == 5:
                move_bricks_down() 
                ball_hit_count = 0
        
        # 모든 벽돌을 제거했을 경우
        if len(bricks) == 0:
            game_started = False

    # 화면 지우기
    screen.blit(background_image,(0,0))

    # 벽돌 그리기
    for brick in bricks:
        pygame.draw.rect(screen, GREEN, brick)
    
    # 공 그리기
    pygame.draw.circle(screen, YELLOW, ball.center, ball_radius)

    # 바 그리기
    pygame.draw.rect(screen, BLUE, bar)
    
    # 점수 출력
    print_score()
    print_max_score()
    
    #게임 시작 또는 종료 문구 출력
    if not game_started:
        if first_game:
            screen.blit(start_text, start_text_rect)
        else:
            screen.blit(end_text, end_text_rect)

    # 화면 업데이트
    pygame.display.flip()

    # 게임 속도 조절
    clock.tick(60)