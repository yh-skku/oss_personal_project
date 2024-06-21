import pygame
import random
import firebase_admin
from firebase_admin import credentials, firestore

# Firebase 인증 및 초기화
cred = credentials.Certificate("./firebase.json")
firebase_admin.initialize_app(cred)

# Firestore 데이터베이스를 가져옵니다.
db = firestore.client()
collection_name = 'scores'

pygame.init()

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

# 화면 설정
screen_width = 1000
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height)) 
pygame.display.set_caption("brick breaking")
pygame.display.set_icon(icon_image)
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
screen.blit(background_image, (0, 0))

# 프레임 및 게임 종료 조건 설정
clock= pygame.time.Clock()

# 벽돌 생성
bricks = []
COLUMN = 10
ROW = 2
brick_width = 70
brick_height = 30
brick_spacing = 20

def make_brick():
    global bricks, COLUMN, ROW, brick_width, brick_height, brick_spacing
    for column_index in range(COLUMN):
        for row_index in range(ROW):
            brick_x = screen_width / 2 - (COLUMN * (brick_width + brick_spacing) / 2) + column_index * (brick_width + brick_spacing)
            brick_y = row_index * (brick_height + brick_spacing) + 35
            block_value = random.randint(1, 5)
            brick = Brick(brick_x, brick_y, brick_width, brick_height, block_value)
            bricks.append(brick)

# 바 생성
bar = pygame.Rect(screen_width // 2 - 80 // 2, screen_height - 16 - 30, 80, 16)
pygame.draw.rect(screen, BLUE, bar)

# 공 생성
ball_radius = 8
ball = pygame.Rect(screen_width // 2 - ball_radius, bar.top - ball_radius * 2, ball_radius * 2, ball_radius * 2)
ball_dx = 5
ball_dy = -5
pygame.draw.circle(screen, YELLOW, ball.center, ball_radius)

# 게임 시작 및 종료 문구, 최고 점수 텍스트 생성 
start_text = small_font.render("press spacekey to start game", True, BLACK)
start_text_rect = start_text.get_rect(center=(screen_width // 2, screen_height // 2))
end_text = small_font.render("game over (press spacekey to restart)", True, BLACK)
end_text_rect = end_text.get_rect(center=(screen_width // 2, screen_height // 2))
quit_text = small_font.render("press q to quit game", True, BLACK)
quit_text_rect = quit_text.get_rect(center=(screen_width // 2, screen_height // 2 + 100))
save_score_text = small_font.render("Do you want to save your score? (Y/N)", True, BLACK)
save_score_text_rect = save_score_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))

# 점수 설정
def print_score():
    score_text = small_font.render(f"Score: {point}", True, BLACK)
    screen.blit(score_text, (5, 5))

def print_max_score():
    max_score_text = small_font.render(f"high score: {max_point}", True, BLACK)
    screen.blit(max_score_text, (screen_width - 180, 5))

def add_score(name, point):
    data = {
        'name': name,
        'score': point
    }
    ref = db.collection(collection_name).document()
    ref.set(data)

def get_scores():
    scores_ref = db.collection(collection_name)
    scores = scores_ref.get()
    score_list = []
    for score in scores:
        score_list.append(score.to_dict())
    return score_list

def get_high_score():
    scores = get_scores()
    if scores:
        high_score = max(score['score'] for score in scores)
        return high_score
    return 0

def draw_text_input_box(text):
    input_box = pygame.Rect(screen_width // 2 - 100, screen_height // 2, 200, 40)
    pygame.draw.rect(screen, WHITE, input_box)
    pygame.draw.rect(screen, BLACK, input_box, 2)
    text_surface = small_font.render(text, True, BLACK)
    screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))
    pygame.display.flip()

def get_text_input():
    text = ''
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return text
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
        screen.blit(background_image, (0, 0))
        screen.blit(save_score_text, save_score_text_rect)
        draw_text_input_box(text)
        pygame.display.flip()

game_started = False
first_game = True
point = 0
max_point = 0
ball_hit_count = 0
game_over = False
score_saved = False

# 게임 초기화
def reset_game():
    global bricks, bar, ball, ball_dx, ball_dy, game_started, life, point, ball_hit_count, max_point, game_over, score_saved
    bricks.clear()
    make_brick()
    bar = pygame.Rect(screen_width // 2 - 80 // 2, screen_height - 16 - 30, 80, 16)
    ball = pygame.Rect(screen_width // 2 - ball_radius, bar.top - ball_radius * 2, ball_radius * 2, ball_radius * 2)
    ball_dx = 5
    ball_dy = -5
    point = 0
    ball_hit_count = 0
    game_over = False
    score_saved = False
    max_point = get_high_score()  # 최고 점수 조회

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
        block_value = random.randint(1, 5)
        brick = Brick(brick_x, brick_y, brick_width, brick_height, block_value)
        bricks.append(brick)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if not game_started and not game_over and event.key == pygame.K_SPACE:
                reset_game()
                game_started = True
                first_game = False
            elif not game_started and event.key == pygame.K_q:
                pygame.quit()
            elif game_over and not score_saved:
                if event.key == pygame.K_y:
                    name = get_text_input()
                    add_score(name, point)
                    score_saved = True
                elif event.key == pygame.K_n:
                    score_saved = True

    if game_started:
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
        ball.top += ball_dy

        if ball.left <= 0:
            ball.left = 0
            ball_dx = -ball_dx
        elif ball.left >= screen_width - ball.width:
            ball.left = screen_width - ball.width
            ball_dx = -ball_dx
        if ball.top < 0:
            ball.top = 0
            ball_dy = -ball_dy
        elif ball.top >= screen_height:
            game_started = False
            game_over = True
            if max_point < point:
                max_point = point

        # 공이 벽돌에 닿았을 경우
        for brick in bricks:
            if ball.colliderect(brick):
                brick.block_value -= 1
                if brick.block_value <= 0:
                    bricks.remove(brick)
                    point += 1
                ball_dy = -ball_dy
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
            game_over = True

    # 화면 지우기
    screen.blit(background_image, (0, 0))

    # 벽돌 그리기
    for brick in bricks:
        pygame.draw.rect(screen, GREEN, brick)
        brick.draw_value(screen)

    # 공 그리기
    pygame.draw.circle(screen, YELLOW, ball.center, ball_radius)

    # 바 그리기
    pygame.draw.rect(screen, BLUE, bar)

    # 점수 출력
    print_score()
    print_max_score()

    # 게임 시작 또는 종료 문구 출력
    if not game_started:
        if first_game:
            screen.blit(start_text, start_text_rect)
            screen.blit(quit_text, quit_text_rect)
        else:
            screen.blit(end_text, end_text_rect)
            screen.blit(quit_text, quit_text_rect)
        if game_over and not score_saved:
            screen.blit(save_score_text, save_score_text_rect)

    # 화면 업데이트
    pygame.display.flip()

    # 게임 속도 조절
    clock.tick(60)