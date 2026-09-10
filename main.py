import pygame
import sys
import math
import random

# 1. تهيئة Pygame
pygame.init()

# إعدادات الشاشة
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("لعبة السهم - مع منطقة سحب ومؤشر قوة")

# الألوان
WHITE = (255, 255, 255)
GREEN = (34, 139, 34)
RED = (220, 20, 60)
YELLOW = (255, 215, 0)
BLUE = (30, 144, 255)
BROWN = (139, 69, 19)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
ROAD_GRAY = (50, 50, 50)
DOT_COLOR = (255, 255, 255)

# 2. متغيرات اللعبة الأساسية
# القوس في مكانه الأصلي (الجهة اليسرى)
bow_x, bow_y = 120, 200

arrow_x, arrow_y = bow_x, bow_y
arrow_speed_x = 0
arrow_speed_y = 0

is_aiming = False   
is_flying = False   
game_over = False   
game_won = False

# منطقة التحكم/السحب في الأسفل (Pad)
pad_center_x, pad_center_y = WIDTH // 2, 330
pad_touch_x, pad_touch_y = pad_center_x, pad_center_y

# نسبة القوة (من 0% إلى 100%)
power_percent = 0

# مراحل اللعبة
level = 1

# نص النتيجة المؤقتة
hit_text = ""
hit_text_timer = 0

# الهدف الميكانيكي للمرحلة 1
target_x = 700
target_y = 200
target_speed = 3

# البالون للمرحلة 2
balloon_x = random.randint(400, WIDTH - 100)
balloon_y = HEIGHT + 40
balloon_speed = 3

# حركة السيارة في النهاية
car_x = -150

# النقاط (تبدأ بـ 10)
score = 10
clock = pygame.time.Clock()

# زر إعادة اللعب
restart_rect = pygame.Rect(320, 230, 160, 50)

# 3. حلقة اللعبة الرئيسية
running = True
while running:
    clock.tick(60)
    screen.fill((135, 206, 235)) # السماء

    # رسم الأرضية في الأسفل
    pygame.draw.rect(screen, GREEN, (0, 350, WIDTH, 50))

    # التقاط الأحداث
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            
            if game_over or game_won:
                if restart_rect.collidepoint(mouse_x, mouse_y):
                    score = 10
                    level = 1
                    game_over = False
                    game_won = False
                    is_flying = False
                    is_aiming = False
                    arrow_x, arrow_y = bow_x, bow_y
                    pad_touch_x, pad_touch_y = pad_center_x, pad_center_y
                    power_percent = 0
                    hit_text = ""
                    car_x = -150
                    target_y = 200
                    balloon_y = HEIGHT + 40
            elif not is_flying:
                # التحقق من الضغط داخل أو بالقرب من زر السحب في الأسفل
                if math.hypot(mouse_x - pad_center_x, mouse_y - pad_center_y) < 60:
                    is_aiming = True

        elif event.type == pygame.MOUSEMOTION and is_aiming and not (game_over or game_won):
            mouse_x, mouse_y = event.pos
            dx = mouse_x - pad_center_x
            dy = mouse_y - pad_center_y
            pull_dist = math.hypot(dx, dy)
            
            if pull_dist > 80: # تحديد أقصى مسافة للسحب
                angle = math.atan2(dy, dx)
                pad_touch_x = pad_center_x + math.cos(angle) * 80
                pad_touch_y = pad_center_y + math.sin(angle) * 80
                pull_dist = 80
            else:
                pad_touch_x = mouse_x
                pad_touch_y = mouse_y

            # حساب نسبة القوة (0% - 100%)
            power_percent = int((pull_dist / 80) * 100)

            # تحريك السهم في الأعلى بناءً على سحب اللمس بالأسفل
            arrow_x = bow_x + (pad_touch_x - pad_center_x)
            arrow_y = bow_y + (pad_touch_y - pad_center_y)

        elif event.type == pygame.MOUSEBUTTONUP and is_aiming and not (game_over or game_won):
            is_aiming = False
            is_flying = True
            
            # إطلاق السهم بعكس اتجاه السحب وبقوة تتناسب مع القوة المحسوبة
            dx = pad_center_x - pad_touch_x
            dy = pad_center_y - pad_touch_y
            arrow_speed_x = dx * 0.3
            arrow_speed_y = dy * 0.3

            # إرجاع زر التحكم لمنتنصفه
            pad_touch_x, pad_touch_y = pad_center_x, pad_center_y

    # منطق اللعبة
    if not game_over and not game_won:
        
        # --- المرحلة الأولى ---
        if level == 1:
            target_y += target_speed
            if target_y - 40 <= 0 or target_y + 40 >= 350:
                target_speed *= -1

            # رسم الهدف الميكانيكي
            pygame.draw.circle(screen, BLUE, (target_x, int(target_y)), 40)
            pygame.draw.circle(screen, RED, (target_x, int(target_y)), 25)
            pygame.draw.circle(screen, YELLOW, (target_x, int(target_y)), 10)

            # الانتقال للمرحلة 2 عند الوصول إلى 70 نقطة
            if score >= 70:
                level = 2
                hit_text = "LEVEL 2 UNLOCKED!"
                hit_text_timer = 90
                is_flying = False
                arrow_x, arrow_y = bow_x, bow_y
                power_percent = 0

        # --- المرحلة الثانية ---
        elif level == 2:
            balloon_y -= balloon_speed
            if balloon_y < -50:
                balloon_y = HEIGHT + 40
                balloon_x = random.randint(400, WIDTH - 100)

            # رسم البالون
            pygame.draw.line(screen, WHITE, (balloon_x, int(balloon_y) + 25), (balloon_x, int(balloon_y) + 50), 2)
            pygame.draw.circle(screen, RED, (balloon_x, int(balloon_y)), 25)
            pygame.draw.polygon(screen, RED, [(balloon_x - 5, int(balloon_y) + 25), (balloon_x + 5, int(balloon_y) + 25), (balloon_x, int(balloon_y) + 20)])

            # الفوز عند الوصول لـ 140 نقطة
            if score >= 140:
                game_won = True

        # حركة السهم الطائر
        if is_flying:
            arrow_x += arrow_speed_x
            arrow_y += arrow_speed_y
            arrow_speed_y += 0.25 # الجاذبية

            if level == 1:
                distance = math.hypot(arrow_x - target_x, arrow_y - target_y)
                if distance <= 10:
                    score += 20
                    hit_text = "BULLSEYE! +20"
                    hit_text_timer = 60
                    is_flying = False
                    arrow_x, arrow_y = bow_x, bow_y
                    power_percent = 0
                elif distance <= 25:
                    score += 15
                    hit_text = "GREAT! +15"
                    hit_text_timer = 60
                    is_flying = False
                    arrow_x, arrow_y = bow_x, bow_y
                    power_percent = 0
                elif distance <= 40:
                    score += 10
                    hit_text = "HIT! +10"
                    hit_text_timer = 60
                    is_flying = False
                    arrow_x, arrow_y = bow_x, bow_y
                    power_percent = 0
            
            elif level == 2:
                distance = math.hypot(arrow_x - balloon_x, arrow_y - balloon_y)
                if distance <= 25: # فرقعة البالون
                    score += 10
                    hit_text = "POP! +10"
                    hit_text_timer = 60
                    is_flying = False
                    arrow_x, arrow_y = bow_x, bow_y
                    balloon_y = HEIGHT + 40
                    balloon_x = random.randint(400, WIDTH - 100)
                    power_percent = 0

            # خطأ - عدم الاصابة
            if arrow_x > WIDTH or arrow_x < 0 or arrow_y > HEIGHT or arrow_y < 0:
                score -= 5
                hit_text = "MISS! -5"
                hit_text_timer = 60
                is_flying = False
                arrow_x, arrow_y = bow_x, bow_y
                power_percent = 0
                
                if score <= 0:
                    score = 0
                    game_over = True

    # --- رسم القوس والوتر في موقعه المعتاد ---
    pygame.draw.arc(screen, BROWN, (bow_x - 20, bow_y - 40, 40, 80), -math.pi/2, math.pi/2, 5)

    if is_aiming and not (game_over or game_won):
        pygame.draw.line(screen, WHITE, (bow_x, bow_y - 40), (arrow_x, arrow_y), 2)
        pygame.draw.line(screen, WHITE, (bow_x, bow_y + 40), (arrow_x, arrow_y), 2)

        # رسم نقاط المسار المتوقع
        sim_x, sim_y = arrow_x, arrow_y
        sim_vx = (pad_center_x - pad_touch_x) * 0.3
        sim_vy = (pad_center_y - pad_touch_y) * 0.3
        
        for i in range(15):
            sim_x += sim_vx * 2
            sim_y += sim_vy * 2
            sim_vy += 0.25 * 2
            if sim_x > WIDTH or sim_y > 350:
                break
            pygame.draw.circle(screen, DOT_COLOR, (int(sim_x), int(sim_y)), 3)
    else:
        pygame.draw.line(screen, WHITE, (bow_x, bow_y - 40), (bow_x, bow_y + 40), 2)

    # --- رسم السهم ---
    if (is_aiming or is_flying) and not (game_over or game_won):
        if is_aiming:
            angle = math.atan2(pad_center_y - pad_touch_y, pad_center_x - pad_touch_x)
        else:
            angle = math.atan2(arrow_speed_y, arrow_speed_x)
        
        end_x = arrow_x + math.cos(angle) * 35
        end_y = arrow_y + math.sin(angle) * 35
        pygame.draw.line(screen, BLACK, (arrow_x, arrow_y), (end_x, end_y), 3)
        pygame.draw.circle(screen, RED, (int(end_x), int(end_y)), 4)
    elif not (game_over or game_won):
        pygame.draw.line(screen, BLACK, (bow_x - 15, bow_y), (bow_x + 20, bow_y), 3)
        pygame.draw.circle(screen, RED, (bow_x + 20, bow_y), 4)

    # --- رسم منطقة السحب ومستطيل مؤشر القوة بالأسفل ---
    if not (game_over or game_won):
        # 1. زر ودائرة السحب (Touch Pad)
        pygame.draw.circle(screen, GRAY, (pad_center_x, pad_center_y), 45, 2)
        pygame.draw.circle(screen, RED, (int(pad_touch_x), int(pad_touch_y)), 15)

        # 2. مستطيل مؤشر نسبة القوة (Power Bar)
        bar_x, bar_y, bar_w, bar_h = 50, 345, 180, 20
        pygame.draw.rect(screen, BLACK, (bar_x, bar_y, bar_w, bar_h), 2, border_radius=5)
        fill_w = int((power_percent / 100) * (bar_w - 4))
        pygame.draw.rect(screen, RED, (bar_x + 2, bar_y + 2, fill_w, bar_h - 4), border_radius=3)

        # نص النسبة المئوية للقوة
        font_p = pygame.font.SysFont(None, 24)
        p_text = font_p.render(f"Power: {power_percent}%", True, BLACK)
        screen.blit(p_text, (bar_x + 45, bar_y + 2))

    # عرض النقاط والمرحلة
    font = pygame.font.SysFont(None, 32)
    score_text = font.render(f"Score: {score}  |  Level: {level}", True, BLACK)
    screen.blit(score_text, (20, 20))

    if hit_text_timer > 0:
        hit_font = pygame.font.SysFont(None, 36)
        color = GREEN if "+" in hit_text or "UNLOCKED" in hit_text else RED
        txt_surface = hit_font.render(hit_text, True, color)
        screen.blit(txt_surface, (WIDTH // 2 - 100, 20))
        hit_text_timer -= 1

    # --- شاشة الفوز وتحريك السيارة ---
    if game_won:
        # رسم الطريق الأسود للنهاية
        pygame.draw.rect(screen, ROAD_GRAY, (0, 340, WIDTH, 60))
        pygame.draw.line(screen, YELLOW, (0, 370), (WIDTH, 370), 2)

        car_x += 5
        if car_x > WIDTH + 100:
            car_x = -150

        # رسم السيارة
        pygame.draw.rect(screen, RED, (car_x, 335, 90, 25), border_radius=5)
        pygame.draw.rect(screen, BLUE, (car_x + 20, 320, 50, 18), border_radius=3)
        pygame.draw.circle(screen, BLACK, (car_x + 20, 360), 10)
        pygame.draw.circle(screen, BLACK, (car_x + 70, 360), 10)

        go_font = pygame.font.SysFont(None, 55)
        go_text = go_font.render("VICTORY! YOU WIN!", True, GREEN)
        screen.blit(go_text, (WIDTH // 2 - 180, 120))

        pygame.draw.rect(screen, GREEN, restart_rect, border_radius=10)
        btn_font = pygame.font.SysFont(None, 32)
        btn_text = btn_font.render("PLAY AGAIN", True, WHITE)
        screen.blit(btn_text, (restart_rect.x + 15, restart_rect.y + 12))

    # --- شاشة Game Over عند الخسارة ---
    if game_over:
        s = pygame.Surface((WIDTH, HEIGHT))
        s.set_alpha(180)
        s.fill(BLACK)
        screen.blit(s, (0, 0))

        go_font = pygame.font.SysFont(None, 64)
        go_text = go_font.render("GAME OVER", True, RED)
        screen.blit(go_text, (WIDTH // 2 - 140, 140))

        pygame.draw.rect(screen, GREEN, restart_rect, border_radius=10)
        btn_font = pygame.font.SysFont(None, 32)
        btn_text = btn_font.render("RESTART", True, WHITE)
        screen.blit(btn_text, (restart_rect.x + 25, restart_rect.y + 12))

    pygame.display.flip()

pygame.quit()
sys.exit()
