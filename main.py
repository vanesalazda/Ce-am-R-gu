import pygame
import random
import sys
import os


pygame.init()


window_width, window_height = 959, 678
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Ceļam Rīgu")

#
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Fonti
base_font = pygame.font.Font(None, 32)
large_font = pygame.font.Font(None, 64)

#Vārdnīca ar jautājumiem un atbildēm
questions = {
    "Kad dibinaja Rīgu?": "1201",
    "Kurš dibināja Rīgu?": "Bīskaps Alberts",
    "Kad dibināja rāti?": "1226",
    "Kura statuja atrodas Rīgas ģeometriskajā centrā?": "Rolanda statuja"
}
background_images = [f"{i}.webp" for i in range(1, 11)]
background_game_over = "background_1.webp"

#
current_question = ""
current_answer = ""
user_text = ""
score = 0
timer = 420 # 7 sekundes
game_over = False
current_background_image_index = 0
def set_new_question():
    global current_question, current_answer
    current_question, current_answer = random.choice(list(questions.items()))

def reset_game():
    global score, timer, game_over, current_background_image_index
    score = 0
    timer = 420
    game_over = False
    current_background_image_index = 0
    set_new_question()

def handle_input(event):
    global user_text, game_over, score, timer, current_background_image_index
    if not game_over:
        if event.key == pygame.K_RETURN:
            if user_text.lower() == current_answer.lower():
                score += 1
                set_new_question()
                user_text = ""
                timer = 420
                next_background_image()
            else:
                game_over = True
        elif event.key == pygame.K_BACKSPACE:
            user_text = user_text[:-1]
        else:
            user_text += event.unicode
    elif event.key == pygame.K_RETURN:  # Sāk spēli no sākuma
        reset_game()

def next_background_image(): #maina fonu
    global current_background_image_index, game_over
    current_background_image_index += 1
    if current_background_image_index >= len(background_images):
        game_over = True

def update_game_state(): #game over/laiks
    global timer, game_over
    if not game_over:
        timer -= 1
        if timer <= 0:
            game_over = True

def display_elements():
    window.fill(WHITE)
    if not game_over:
        background_image = pygame.image.load(os.path.join("backgrounds", background_images[current_background_image_index])).convert()
        window.blit(background_image, (0, 0))

        question_text_surface = base_font.render(current_question, True, BLACK)
        question_text_rect = question_text_surface.get_rect(center=(window_width // 2, 100))  # Adjust the Y coordinate to 150 pixels
        window.blit(question_text_surface, question_text_rect)

        input_surface = base_font.render(user_text, True, BLACK)
        input_rect = input_surface.get_rect(center=(window_width // 2, 210))  # Adjust the Y coordinate to 175 pixels
        window.blit(input_surface, input_rect)

        timer_text_surface = base_font.render("Time: " + str(timer // 60), True, BLACK)
        window.blit(timer_text_surface, (window_width - timer_text_surface.get_width() - 10, 10))
        score_text_surface = base_font.render("Score: " + str(score), True, BLACK)
        window.blit(score_text_surface, (10, 10))
    else:
        game_over_background = pygame.image.load(os.path.join("backgrounds", background_game_over)).convert()
        window.blit(game_over_background, (0, 0))
        
        game_over_text_surface = large_font.render("Game Over! Score: " + str(score), True, BLACK)
        window.blit(game_over_text_surface, ((window_width - game_over_text_surface.get_width()) // 2, (window_height - game_over_text_surface.get_height()) // 2))

# galvenais spēles loop
set_new_question()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            handle_input(event)
            
    update_game_state()
    display_elements()
    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
