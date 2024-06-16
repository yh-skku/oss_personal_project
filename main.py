import pygame
import random
import math

pygame.init()

##########################################
#################PHASE 2##################
# 목표 변경점
# 1. 초기 블록 발사 위치 마우스로 조정, space키로 눌러 해당 위치로 발사하는 기능 # math 라이브러리 cos, sin함수로 구현
# 2. 초기 dx, dy가 고정되어 수정할수 없는 문제 고치기 위해 바에 운동량 추가하여 튕길 때 방향 변환 적용하는 기능
# 3. 블록 체력 점진적으로 증가 시스템 + 블록 처치 시 확률로 공 강화 아이템 떨어짐 -> 공 피해량 증가
##########################################
##########################################

# 색상 및 폰트 설정
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
YELLOW = (200, 200, 0)
GRAY = (128, 128, 128)
large_font = pygame.font.SysFont(None, 72)
small_font = pygame.font.SysFont(None, 36)

# 이미지 불러오기
icon_image = pygame.image.load("icon.jpg")
background_image = pygame.image.load("background.png")
powerup_image = pygame.image.load("POW_Block.webp")

# 벽돌 클래스 생성
class Brick(pygame.Rect):
    #벽돌 생성 및 초기화
    def __init__(self, x, y, width, height, block_value):
        super().__init__(x, y, width, height)
        self.block_value = block_value
    # value 벽돌에 나타내기
    def draw_value(self, screen):
        value_text = small_font.render(str(self.block_value), True, BLACK)
        screen.blit(value_text, (self.x + self.width // 2 - value_text.get_width() // 2, self.y + self.height // 2 - value_text.get_height() // 2))

# 아이템 클래스 생성
class PowerUp(pygame.Rect):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.image = powerup_image
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

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
##########################################
#################PHASE 2##################
brick_coef = 1
##########################################
##########################################

def make_brick():
    global bricks, COLUMN, ROW, brick_width, brick_height, brick_spacing
    for column_index in range(COLUMN):
        for row_index in range(ROW):
            brick_x = screen_width / 2 - (COLUMN * (brick_width + brick_spacing) / 2) + column_index * (brick_width + brick_spacing)
            brick_y = row_index * (brick_height + brick_spacing) + 35
            ##########################################
            #################PHASE 2##################
            block_value = random.randint(1*brick_coef, 5*brick_coef) # 점차 강해지는 벽돌 생성
            ##########################################
            #################PHASE 2##################
            brick = Brick(brick_x, brick_y, brick_width, brick_height, block_value)
            bricks.append(brick)


# 바 생성
bar = pygame.Rect(screen_width // 2 - 80 // 2, screen_height - 16 - 30, 80, 16)
pygame.draw.rect(screen, BLUE,bar)

# 공 생성
ball_radius = 8
ball = pygame.Rect(screen_width // 2 - ball_radius, bar.top - ball_radius * 2, ball_radius * 2, ball_radius * 2)
ball_speed = 5 # PHASE 2
ball_dx = 5
ball_dy = -5
##########################################
#################PHASE 2##################
ball_damage = 1 # 공의 충격량 설정
##########################################
##########################################
pygame.draw.circle(screen, YELLOW, ball.center, ball_radius)

# 아이템 리스트 생성
powerups = []

# 게임 시작 및 종료 문구, 최고 점수 텍스트 생성 
start_text = small_font.render("press spacekey to start game", True, BLACK)
start_text_rect = start_text.get_rect(center=(screen_width // 2, screen_height // 2))
end_text = small_font.render("game over (press spacekey to restart)", True, BLACK)
end_text_rect = end_text.get_rect(center=(screen_width // 2, screen_height // 2))
quit_text = small_font.render("press q to quit game", True, BLACK)
quit_text_rect = quit_text.get_rect(center=(screen_width // 2, screen_height // 2 + 100))

# 점수 설정

def print_score():
    score_text = small_font.render(f"Score: {point}", True, BLACK)
    screen.blit(score_text, (5, 5))

def print_max_score():
    max_score_text = small_font.render(f"high score: {max_point}", True, BLACK)
    screen.blit(max_score_text, (screen_width-180,5))

game_started = False
first_game = True
point = 0
max_point = 0
ball_hit_count = 0
##########################################
#################PHASE 2##################
bar_speed = 10
bar_direction = 0  # -1: 왼쪽, 1: 오른쪽, 0: 정지
direction_selecting = True
arrow_angle = 0
arrow_speed = 0.05
arrow_length = 50
##########################################
##########################################

# 게임 초기화
def reset_game():
    global bricks, bar, ball, ball_dx, ball_dy, game_started, life, point, ball_hit_count, direction_selecting, arrow_angle
    bricks.clear()
    make_brick()
    bar = pygame.Rect(screen_width // 2 - 80 // 2, screen_height - 16 - 30, 80, 16)
    ball = pygame.Rect(screen_width // 2 - ball_radius, bar.top - ball_radius * 2, ball_radius * 2, ball_radius * 2)
    ball_dx = 5
    ball_dy = -5
    point = 0
    ball_hit_count = 0 
    ##########################################
    #################PHASE 2##################
    direction_selecting = True
    arrow_angle = 0
    ##########################################
    ##########################################

reset_game()

# 새로운 벽돌을 생성하면서 벽돌을 한 칸 아래로 이동
def move_bricks_down():
    global bricks, COLUMN, ROW, brick_width, brick_height, brick_spacing
    for brick in bricks:
        brick.y += brick_height + brick_spacing

    # 맨 위에 새로운 벽돌 추가
    for column_index in range(COLUMN):
        brick_x = screen_width / 2 - (COLUMN * (brick_width + brick_spacing) / 2) + column_index * (brick_width + brick_spacing)
        brick_y = 35
        #################PHASE 2##################
        block_value = random.randint(1*brick_coef, 5*brick_coef)
        ##########################################
        brick = Brick(brick_x, brick_y, brick_width, brick_height, block_value)
        bricks.append(brick)

##########################################
#################PHASE 2##################
# 방향 벡터 정규화 함수
# 처음엔 그냥 쐈는데 x축으로 너무 치우쳐있을 경우 속도가 너무 빨라서 속도를 제한함
def normalize_vector(dx, dy): # 단순하게 최대 속도 고정으로 바꿈
    if dx >= 5:
        dx = 5
    if dx <= -5:
        dx = -5
    if dy >= 5:
        dy = 5
    if dy <= -5:
        dy = -5
    return dx, dy
##########################################
##########################################

# 게임 시작
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if not game_started and event.key == pygame.K_SPACE:
                ##########################################
                #################PHASE 2##################
                if direction_selecting:
                    direction_selecting = False
                    dx = arrow_length * math.cos(arrow_angle)
                    dy = -arrow_length * math.sin(arrow_angle)
                    ball_dx, ball_dy = normalize_vector(dx, dy)
                    game_started = True
                    first_game = False
                else:
                    reset_game()
                    direction_selecting = True
                ##########################################
                ##########################################
            elif not game_started and event.key == pygame.K_q:
                pygame.quit()

    ##########################################
    #################PHASE 2##################
    if direction_selecting:  # 화살표가 반원을 그리며 움직이는 모드
        arrow_angle += arrow_speed
        if arrow_angle >= math.pi:
            arrow_angle -= math.pi
    ##########################################
    ##########################################

    if game_started:  # 게임이 시작된 상태라면
        # 바 이동
        keys = pygame.key.get_pressed()
        ##########################################
        #################PHASE 2##################
        if keys[pygame.K_LEFT] and bar.left > 0:
            bar.move_ip(-bar_speed, 0)
            bar_direction = -1
        elif keys[pygame.K_RIGHT] and bar.right < screen_width:
            bar.move_ip(bar_speed, 0)
            bar_direction = 1
        else:
            bar_direction = 0
        ##########################################
        #################PHASE 2##################

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
                brick.block_value -= 1
                if brick.block_value <= 0:
                    bricks.remove(brick)
                    point+=1
                    ##########################################
                    #################PHASE 2##################
                    if random.random() < 0.1: # 10% 확률로 아이템 생성
                        powerup = PowerUp(brick.x + brick.width // 2 - 16, brick.y, 32, 32)
                        powerups.append(powerup)
                    ##########################################
                    ##########################################
                ball_dy = -ball_dy
                break
        ##########################################
        #################PHASE 2##################
        # 공이 바에 닿았을 경우
        if ball.colliderect(bar):
            ball_dy = -ball_dy
            ball_dx += bar_direction  # 바의 이동 방향에 따라 공의 속도 조정 (최대 +- 2 정도로 조정됨) -> 너무 커서 +- 1로 수정
            ball_hit_count += 1
            if ball_hit_count == 5:
                move_bricks_down() 
                ball_hit_count = 0
        ##########################################
        #################PHASE 2##################
        # 아이템 이동 및 바와 충돌 처리
        for powerup in powerups:
            powerup.y += 5  # 아이템 떨어지는 속도
            if powerup.colliderect(bar):
                powerups.remove(powerup)
                ball_damage += 1  # 공의 피해량 증가
        ##########################################
        ##########################################

    # 화면 지우기
    screen.blit(background_image,(0,0))

    # 벽돌 그리기
    for brick in bricks:
        pygame.draw.rect(screen, GREEN, brick)
        brick.draw_value(screen)
    
    # 공 그리기
    pygame.draw.circle(screen, YELLOW, ball.center, ball_radius)

    # 바 그리기
    pygame.draw.rect(screen, BLUE, bar)

    ##########################################
    #################PHASE 2##################

    # 아이템 그리기
    for powerup in powerups:
        powerup.draw(screen)

    # 방향 선택 모드일 때 화살표 그리기
    if direction_selecting:
        arrow_x = bar.centerx + arrow_length * math.cos(arrow_angle)
        arrow_y = bar.top - arrow_length * math.sin(arrow_angle)
        pygame.draw.line(screen, RED, bar.center, (arrow_x, arrow_y), 5)
    ##########################################
    #################PHASE 2##################
    
    # 점수 출력
    print_score()
    print_max_score()
    
    #게임 시작 또는 종료 문구 출력
    if not game_started and not direction_selecting:
        if first_game:
            screen.blit(start_text, start_text_rect)
            screen.blit(quit_text, quit_text_rect)
        else:
            screen.blit(end_text, end_text_rect)
            screen.blit(quit_text, quit_text_rect)

    # 화면 업데이트
    pygame.display.flip()

    # 게임 속도 조절
    clock.tick(60)