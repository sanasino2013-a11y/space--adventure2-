import pygame
import random

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("مغامرة الفضاء الكبرى - النسخة المحسنة")
clock = pygame.time.Clock()

# الألوان
WHITE = (255, 255, 255)
BLACK = (10, 10, 30)
BLUE = (0, 150, 255)
LIGHT_BLUE = (100, 200, 255)
RED = (255, 69, 0)
YELLOW = (255, 215, 0)
ORANGE = (255, 165, 0)

font_title = pygame.font.SysFont("Arial", 40, bold=True)
font_score = pygame.font.SysFont("Arial", 24, bold=True)

# نجوم الخلفية
stars = [[random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT), random.randint(1,3)] for _ in range(50)]

def reset_game():
    return {
        "player_x": SCREEN_WIDTH // 2 - 25,
        "player_y": SCREEN_HEIGHT - 80,
        "player_width": 50,
        "player_height": 40,
        "player_speed": 7,
        "obstacles": [],
        "obstacle_speed": 3,
        "score": 0,
        "game_over": False,
        "particles": [] # للانفجار
    }

game_data = reset_game()
running = True

while running:
    screen.fill(BLACK)
    
    # رسم وتحريك النجوم
    for star in stars:
        star[1] += star[2]  # كل نجمة بسرعة مختلفة
        if star[1] > SCREEN_HEIGHT:
            star[1] = 0
            star[0] = random.randint(0, SCREEN_WIDTH)
        pygame.draw.circle(screen, WHITE, (star[0], star[1]), star[2])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_data["game_over"]:
                game_data = reset_game()

    if not game_data["game_over"]:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and game_data["player_x"] > 0:
            game_data["player_x"] -= game_data["player_speed"]
        if keys[pygame.K_RIGHT] and game_data["player_x"] < SCREEN_WIDTH - game_data["player_width"]:
            game_data["player_x"] += game_data["player_speed"]

        # توليد نيازك - صعوبة متدرجة
        spawn_rate = max(15, 40 - game_data["score"] // 500) # كل ما تجيب نقاط يزيد العدد
        if random.randint(1, spawn_rate) == 1:
            obs_width = random.randint(30, 70)
            obs_x = random.randint(0, SCREEN_WIDTH - obs_width)
            game_data["obstacles"].append(pygame.Rect(obs_x, -40, obs_width, 30))

        game_data["score"] += 1
        if game_data["score"] % 600 == 0:
            game_data["obstacle_speed"] += 0.5

        player_rect = pygame.Rect(game_data["player_x"], game_data["player_y"], game_data["player_width"], game_data["player_height"])

        # تحديث النيازك والتصادم
        for obs in game_data["obstacles"][:]:
            obs.y += game_data["obstacle_speed"]
            if player_rect.colliderect(obs):
                game_data["game_over"] = True
                # اعمل انفجار
                for _ in range(25):
                    game_data["particles"].append([player_rect.centerx, player_rect.centery, random.randint(-6,6), random.randint(-6,6), 30])

        # تنظيف النيازك اللي خرجت (أحسن من remove جوه اللوب)
        game_data["obstacles"] = [obs for obs in game_data["obstacles"] if obs.y <= SCREEN_HEIGHT]

        # رسم اللاعب بشكل سفينة أحلى
        pygame.draw.polygon(screen, BLUE, [
            (player_rect.centerx, player_rect.y),
            (player_rect.x, player_rect.bottom),
            (player_rect.right, player_rect.bottom)
        ])
        pygame.draw.rect(screen, LIGHT_BLUE, (player_rect.centerx - 7, player_rect.y + 15, 14, 12), border_radius=3)
        # نار المحرك
        pygame.draw.polygon(screen, ORANGE, [
            (player_rect.centerx - 10, player_rect.bottom),
            (player_rect.centerx + 10, player_rect.bottom),
            (player_rect.centerx, player_rect.bottom + random.randint(5,15))
        ])

        # رسم النيازك
        for obs in game_data["obstacles"]:
            pygame.draw.rect(screen, RED, obs, border_radius=6)
            pygame.draw.rect(screen, (180, 30, 0), (obs.x+5, obs.y+5, obs.width-10, 5), border_radius=2)

        score_surface = font_score.render(f"النقاط: {game_data['score'] // 10}", True, YELLOW)
        screen.blit(score_surface, (20, 20))

    else:
        # انفجار
        for p in game_data["particles"]:
            p[0] += p[2]
            p[1] += p[3]
            p[4] -= 1
            if p[4] > 0:
                pygame.draw.circle(screen, YELLOW, (int(p[0]), int(p[1])), 4)

        over_text = font_title.render("انتهت اللعبة!", True, RED)
        restart_text = font_score.render("اضغط R لإعادة المحاولة", True, WHITE)
        final_score_text = font_score.render(f"النتيجة: {game_data['score'] // 10}", True, YELLOW)

        screen.blit(over_text, (SCREEN_WIDTH // 2 - over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 60))
        screen.blit(final_score_text, (SCREEN_WIDTH // 2 - final_score_text.get_width() // 2, SCREEN_HEIGHT // 2))
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()