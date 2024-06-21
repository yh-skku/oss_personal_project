import pygame
import random
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("./firebase.json")
firebase_admin.initialize_app(cred)

# Firestore 데이터베이스를 가져옵니다.
db = firestore.client()

pygame.init()

# 색상 및 폰트 설정
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
YELLOW = (200, 200, 0)
GRAY = (128, 128, 128)
############################################################################################
########################################## PHASE2 ##########################################
PURPLE = (165, 55, 253)
ORANGE = (255, 148, 112)
BACKGROUD_COLOR = (230,230,230)
############################################################################################
############################################################################################
large_font = pygame.font.SysFont(None, 72)
small_font = pygame.font.SysFont(None, 36)

# 이미지 불러오기
icon_image = pygame.image.load("icon.jpg")
background_image = pygame.image.load("background.png")

# 벽돌 클래스 생성
class Brick(pygame.Rect):
    def __init__(self, x, y, width, height, block_value):
        super().__init__(x, y, width, height)
        self.block_value = block_value

    def draw_value(self, screen):
        value_text = small_font.render(str(self.block_value), True, BLACK)
        screen.blit(value_text, (self.x + self.width // 2 - value_text.get_width() // 2, self.y + self.height // 2 - value_text.get_height() // 2))
############################################################################################
########################################## PHASE2 ##########################################
# 아이템 클래스 생성
class Item(pygame.Rect):
    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, width, height)
        self.color = color
        self.falling = True

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self)
############################################################################################
############################################################################################

# 화면 설정
screen_width = 1000
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("brick breaking")
pygame.display.set_icon(icon_image)
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
screen.blit(background_image, (0, 0))

# 프레임 및 게임 종료 조건 설정
clock = pygame.time.Clock()

# 벽돌 생성
bricks = []
############################################################################################
########################################## PHASE2 ##########################################
double_items = []
longer_items = []
shorter_items = []

COLUMN = 10
ROW = 2
brick_width = 70
brick_height = 30
brick_spacing = 20
item_probability = 95  # 아이템이 나올 확률
############################################################################################
############################################################################################

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
bar_color = BLUE  # 바의 초기 색상

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
save_score_text = small_font.render("Save score? (Y/N)", True, BLACK)
save_score_text_rect = save_score_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
scoreboard_text = small_font.render("ScoreBoard: (L)", True, BLACK)
scoreboard_text_rect = scoreboard_text.get_rect(bottomright=(screen_width, screen_height))

# Firebase 컬렉션
collection_name = 'scores'

# 점수 설정
def print_score(point):
    score_text = small_font.render(f"Score: {point}", True, BLACK)
    screen.blit(score_text, (5, 5))

def print_max_score():
    max_score_text = small_font.render(f"high score: {max_point}", True, BLACK)
    screen.blit(max_score_text, (screen_width - 180, 5))

# 점수 추가하기
def add_score(name, point):
    data = {
        'name': name,
        'score': point
    }
    ref = db.collection(collection_name).document()
    ref.set(data)

# 전체 점수들 가져오기
def get_scores():
    scores_ref = db.collection(collection_name)
    scores = scores_ref.get()
    score_list = []
    for score in scores:
        score_list.append(score.to_dict())
    return sorted(score_list, key=lambda x: x['score'], reverse=True)

# 최고 점수
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
    put_name_text = small_font.render("Input Username", True, BLACK)
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
        screen.blit(put_name_text, save_score_text_rect)
        draw_text_input_box(text)
        pygame.display.flip()

def draw_scoreboard(scores):
    screen.blit(background_image, (0, 0))
    y_offset = 100
    screen.blit(large_font.render("Score Board", True, BLACK), (screen_width // 2 - 100, 50))
    screen.blit(small_font.render("ESC", True, BLACK), (50, 50))
    for score in scores[:15]:
        text = f"{score['name']}: {score['score']}"
        score_text = small_font.render(text, True, BLACK)
        screen.blit(score_text, (screen_width // 2 - 100, y_offset))
        y_offset += 40
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
############################################################################################
########################################## PHASE2 ##########################################
def draw_item_info():
    info_surf = pygame.Surface((250, 100))  # 정보 표시할 표면 생성
    info_surf.set_alpha(150)  # 투명도 설정
    info_surf.fill(BACKGROUD_COLOR)
    texts = [
        ("RED: Power 2x", RED),
        ("PURPLE: Size 2x", PURPLE),
        ("ORANGE: Size 1/2x", ORANGE)
    ]
    for i, (text, color) in enumerate(texts):
        text_surface = small_font.render(text, True, color)
        info_surf.blit(text_surface, (10, i * 30))
    screen.blit(info_surf, (10, screen_height - 100))

game_over = False
score_saved = False
game_started = False
first_game = True
point = 0
max_point = 0
ball_hit_count = 0
double_effect = False
longer_effect = False
shorter_effect = False
double_item_start_time = 0
longer_item_start_time = 0
shorter_item_start_time = 0
power_multiplier = 1
############################################################################################
############################################################################################

# 게임 초기화
def reset_game():
    ############################################################################################
    ########################################## PHASE2 ##########################################
    global bricks, double_items, longer_items, shorter_items, bar, ball, ball_dx, ball_dy, game_started, life, point, ball_hit_count, max_point, game_over, score_saved, double_effect, longer_effect, shorter_effect, bar_color, power_multiplier
    bricks.clear()
    double_items.clear()
    longer_items.clear()
    shorter_items.clear()
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
    # 아이템 효과 초기화
    double_effect = False 
    longer_effect = False
    shorter_effect = False
    bar_color = BLUE  # 바 색상 초기화
    power_multiplier = 1  # 파워 초기화
    ############################################################################################
    ############################################################################################

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
############################################################################################
########################################## PHASE2 ##########################################
def create_item(x, y, color):
    item_width = 20
    item_height = 20
    return Item(x, y, item_width, item_height, color)

# 게임 시작
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_l:
                draw_scoreboard(get_scores())
            elif not game_started and event.key == pygame.K_SPACE:
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
        ball.top += ball_dy

        if ball.left <= 0:  # 공이 왼쪽 벽에 닿았을 경우
            ball.left = 0
            ball_dx = -ball_dx
        elif ball.left >= screen_width - ball.width:  # 공이 오른쪽 벽에 닿았을 경우
            ball.left = screen_width - ball.width
            ball_dx = -ball_dx
        if ball.top < 0:  # 공이 천장에 닿았을 경우
            ball.top = 0
            ball_dy = -ball_dy
        elif ball.top >= screen_height:  # 공이 바닥에 닿았을 경우
            game_started = False
            game_over = True
            if max_point < point:
                max_point = point

        # 공이 벽돌에 닿았을 경우
        for brick in bricks:
            if ball.colliderect(brick):
                brick.block_value -= power_multiplier  # 파워 배율에 따라 감소
                point += 1
                if brick.block_value <= 0:
                    bricks.remove(brick)
    ############################################################################################
    ########################################## PHASE2 ##########################################        
                    # 일정확률 아이템 생성
                    if random.random() < item_probability:
                        randomNum = random.randint(1, 4)
                        
                        # 힘 2배
                        if(randomNum == 1):
                            item = create_item(brick.x + brick.width // 2, brick.y + brick.height // 2, RED)
                            double_items.append(item)    
                        # 길이 2배
                        elif(randomNum == 2):
                            item = create_item(brick.x + brick.width // 2, brick.y + brick.height // 2, PURPLE)
                            longer_items.append(item)
                        # 길이 1/2배
                        elif(randomNum == 3):
                            item = create_item(brick.x + brick.width // 2, brick.y + brick.height // 2, ORANGE)
                            shorter_items.append(item)
    ############################################################################################          
    ############################################################################################
                ball_dy = -ball_dy
                break

        # 공이 바에 닿았을 경우
        if ball.colliderect(bar):
            ball_dy = -ball_dy
            ball_hit_count += 1
            if ball_hit_count == 5:
                move_bricks_down()
                ball_hit_count = 0
############################################################################################
########################################## PHASE2 ##########################################
        # 힘 2배 아이템에 닿았을 경우
        for item in double_items:
            if item.colliderect(bar):
                double_effect = True
                double_item_start_time = time.time()
                bar_color = item.color  # 바 색상 변경
                power_multiplier *= 2  # 파워 배율 증가
                double_items.remove(item)
            elif item.top > screen_height:
                double_items.remove(item)
            else:
                item.move_ip(0, 5)
        # 길이 2배 아이템에 닿았을 경우
        for item in longer_items:
            if item.colliderect(bar):
                longer_effect = True
                bar.width = 160  # 길이 2배로 설정
                bar_color = item.color  # 바 색상 변경
                bar.x = max(0, min(screen_width - bar.width, bar.x))  # 화면 밖으로 나가지 않도록 위치 조정
                longer_item_start_time = time.time()
                longer_items.remove(item)
            elif item.top > screen_height:
                longer_items.remove(item)
            else:
                item.move_ip(0, 5)
        # 길이 1/2배 아이템에 닿았을 경우
        for item in shorter_items:
            if item.colliderect(bar):
                shorter_effect = True
                bar.width = 40  # 길이 1/2배로 설정
                bar_color = item.color  # 바 색상 변경
                bar.x = max(0, min(screen_width - bar.width, bar.x))  # 화면 밖으로 나가지 않도록 위치 조정
                shorter_item_start_time = time.time()
                shorter_items.remove(item)
            elif item.top > screen_height:
                shorter_items.remove(item)
            else:
                item.move_ip(0, 5)
        # 아이템 효과가 지속 중인지 확인
        current_time = time.time()
        if double_effect and current_time - double_item_start_time > 10:            
            double_effect = False
            power_multiplier = 1  # 파워 배율 초기화
        if longer_effect and current_time - longer_item_start_time > 10:
            bar.width = 80  # 원래 길이로 되돌림
            bar.x = max(0, min(screen_width - bar.width, bar.x))  # 화면 밖으로 나가지 않도록 위치 조정
            longer_effect = False
        if shorter_effect and current_time - shorter_item_start_time > 10:
            bar.width = 80  # 원래 길이로 되돌림
            bar.x = max(0, min(screen_width - bar.width, bar.x))  # 화면 밖으로 나가지 않도록 위치 조정
            shorter_effect = False

        # 모든 효과가 끝나면 바 색상을 BLUE로 되돌림
        if not double_effect and not longer_effect and not shorter_effect:
            bar_color = BLUE
############################################################################################
############################################################################################

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
############################################################################################
########################################## PHASE2 ##########################################
    # 바 그리기
    pygame.draw.rect(screen, bar_color, bar)

    # 아이템 그리기
    for item in double_items:
        item.draw(screen)
    for item in longer_items:
        item.draw(screen)
    for item in shorter_items:
        item.draw(screen)

    print_score(point)
    print_max_score()
    # 아이템 정보 표시
    draw_item_info()
############################################################################################
############################################################################################
    # 게임 시작 또는 종료 문구 출력
    if not game_started:
        if first_game:
            screen.blit(start_text, start_text_rect)
            screen.blit(quit_text, quit_text_rect)
            screen.blit(scoreboard_text, scoreboard_text_rect)
        else:
            screen.blit(end_text, end_text_rect)
            screen.blit(quit_text, quit_text_rect)
            screen.blit(scoreboard_text, scoreboard_text_rect)
        if game_over and not score_saved:
            screen.blit(save_score_text, save_score_text_rect)

    # 화면 업데이트
    pygame.display.flip()

    # 게임 속도 조절
    clock.tick(40)
