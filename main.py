import pygame
import sys
import csv
import os
import random

# Initialize Pygame
pygame.init()

# Screen Dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Friend Finder')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
TURQUOISE = (0, 150, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)


# Fonts
question_font = pygame.font.Font(None, 36)
answer_font_button = pygame.font.Font(None, 36)
answer_font_options = pygame.font.Font(None, 30)
# Sample Questions
questions = [
    "What age do you prefer to hang out with?",
    "After school, you usually...",
    "You spent most of last summer...",
]

answers = [
    "A) Doesn't Matter   B) Same age as me   C) Older than Me   D) Younger than me",
    "A) Work             B) Sleep            C) Study           D) Hang out with friends",
    "A)Hanging out at home   B) Traveling    C) At school    D) Working",
]
# Current question index
current_question = 0

# User answers
user_answers = []

# Load previous answers from file (if any)
class_answers = []

def read_answer_file(filename):
    global class_answers
    if os.path.exists(filename):
        with open(filename, 'r', newline='') as csvfile:
            answer_reader = csv.reader(csvfile)
            next(answer_reader)  # Skip header
            for row in answer_reader:
                class_answers.append(row)

def write_answer_file(filename, name, user_answers, class_answers):
    class_answers.append([name] + user_answers)
    with open(filename, 'w', newline='') as csvfile:
        answer_writer = csv.writer(csvfile)
        header = ['name'] + [f'Q{i+1}' for i in range(len(questions))]
        answer_writer.writerow(header)
        answer_writer.writerows(class_answers)

# Read the answers file (if exists)
read_answer_file('answers.csv')

# Button Class
class Button:
    def __init__(self, text, pos, width, height, color):
        self.text = text
        self.pos = pos
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(pos, (width, height))
        self.rendered_text = answer_font_button.render(text, True, BLACK)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.rendered_text, self.rendered_text.get_rect(center=self.rect.center))

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            return True
        return False

# Create buttons for answers
buttons = [
    Button("A", (150, 300), 100, 50, RED),
    Button("B", (300, 300), 100, 50, YELLOW),
    Button("C", (450, 300), 100, 50, GREEN),
    Button("D", (600, 300), 100, 50, CYAN),
]

# Function to display the current question
def display_question(screen, question, answer):
    screen.fill(BLACK)
    question_text = question_font.render(question, True, WHITE)
    answer_text = answer_font_options.render(answer, True, WHITE)
    screen.blit(question_text, (WIDTH // 2 - question_text.get_width() // 2, 150))
    screen.blit(answer_text, (WIDTH // 2 - answer_text.get_width() // 2, 200))
    for button in buttons:
        button.draw(screen)
    pygame.display.flip()


# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        for button in buttons:
            if button.is_clicked(event):
                user_answers.append(button.text)
                current_question += 1
                if current_question >= len(questions):
                    # End of questions
                    name = "User"  # Placeholder for user name input
                    write_answer_file('answers.csv', name, user_answers, class_answers)
                    running = False
                break

    if current_question < len(questions):
        display_question(screen, questions[current_question], answers[current_question])

pygame.quit()
sys.exit()
