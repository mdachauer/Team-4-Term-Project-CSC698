import csv
import os
import sys
from collections import defaultdict
import math

import pygame

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
YELLOW = (255, 255, 100)
GREEN = (0, 255, 0)

# Fonts
question_font = pygame.font.Font(None, 40)
answer_font_button = pygame.font.Font(None, 36)
answer_font_options = pygame.font.Font(None, 40)
username_font = pygame.font.Font(None, 36)

#New this may work to split the answer text into lines based on the number of characters.
def split_text(text, Font,  max_width):
    words = text.split(' ')
    lines = []
    current_line = ""
    for word in words:
        test_line = current_line + word + ' '
        if Font.size(test_line)[0]<= max_width:
            current_line = test_line
        else:
            lines.append(current_line.strip())
            current_line = word + " "

    lines.append(current_line.strip())

    return lines


# Sample Questions
questions = [
    "What age do you prefer to hang out with?",
    "After school, you usually...",
    "You spent most of last summer...",
    "Procrastination is:",
    "Does Pineapple belong on pizza?",
    "You need to improve your:",
    "Public speaking:",
    "What are your plans after graduation? ",
    "Would you get a tattoo?",
    "Most of your homework gets done: ",
]

answers = [
    "A) Doesn't Matter   B) Same age as me   C) Older than Me   D) Younger than me",
    "A) Work             B) Sleep            C) Study           D) Hang out with friends",
    "A) Hanging out at home   B) Traveling    C) At school    D) Working",
    "A) something everyone does B) everyone does it but me   "
    "C)  a quality I'm proud of    D) Gets me in trouble with assignments ",
    "A) Yes  B) No",
    "A) grades   B) timing / organization   C) clothes    D) play list",
    "A) Not for me     B) Makes me nauseous    C) I can do it, if in a group   "
    " D) Bring it on - I love to talk ",
    "A) college or university   B) trade school    C) military     D) undecided",
    "A) maybe   B) yes my appointment is booked   C) been there done that    D) only temporary ones",
    "A) as soon as I get home   B) sometime after dinner    "
    "C) just before I fall asleep     D) With my friends",
]
#Sprites on questions
pizza = pygame.sprite.Sprite()  #Create the first sprite
pizza_image = pygame.image.load('Pizza_Friend.png')  #Load the image
pizza_X = 400  #Set X coordinate
pizza_Y = 1  #Set Y coordinate

pineapple = pygame.sprite.Sprite()  #Create the second sprite
pineapple_image = pygame.image.load('Pineapple_Friend.png')  #Load the image
pineapple_X = 10  #Set X coordinate
pineapple_Y = 10  #Set Y coordinate


#Call function to split text
formatted_answers = [split_text(answer, answer_font_options, WIDTH - 40) for answer in answers]
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
        header = ['name'] + [f'Q{i + 1}' for i in range(len(questions))]
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
    Button("A", (150, 400), 100, 50, RED),
    Button("B", (300, 400), 100, 50, YELLOW),
    Button("C", (450, 400), 100, 50, GREEN),
    Button("D", (600, 400), 100, 50, CYAN),
]

# Function to rotate and blit a sprite
def rotate_sprite(image, angle, pos_x, pos_y):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=(pos_x, pos_y)).center)
    screen.blit(rotated_image, new_rect.topleft)
    #return rotated_image

# Function to display the current question
def display_question(screen, question, answer_lines, question_num, pos_index):
    question_background = pygame.image.load('Question Background.png')
    screen.blit(question_background, question_background.get_rect())
    question_text = question_font.render(question, True, BLACK)
    screen.blit(question_text, (WIDTH // 2 - question_text.get_width() // 2, 150))
    y_offset = 250

    # Call Global variable
    #global pineapple_image
    #global pizza_image

    for line in answer_lines:
        answer_text = answer_font_options.render(line, True, BLACK)
        screen.blit(answer_text, (WIDTH // 2 - answer_text.get_width() // 2, y_offset))
        y_offset += 30

    for button in buttons:
        button.draw(screen)

    #screen.blit(pineapple_image)  # Draw the first sprite
    #screen.blit(pizza_image) # Draw the second sprite
    #pygame.display.flip()

    # Calculate angle based on the current question number
    angle = (current_question * 36) % 360  # Rotate 36 deg per question

    # Calculate new positions for sprites based on q number
    #positions = [
    #    (0, 0),
     #   (WIDTH - pineapple_image.get_width(), 0),
      #  (WIDTH - pineapple_image.get_width(), HEIGHT - pineapple_image.get_height()),
      #  (0, HEIGHT - pineapple_image.get_height())
    #]

# Rotate and blit the sprites
    rotate_sprite(pineapple_image, angle, WIDTH//2-300,HEIGHT//12)
    rotate_sprite(pizza_image, angle, WIDTH//2+300,HEIGHT//12)
    pygame.display.flip()


# Function to display the intro page:
def display_intro_page(screen, name):
    screen.fill(BLACK)
    user_input_text = username_font.render("Please enter your name:", True, WHITE)
    screen.blit(user_input_text, (WIDTH // 2 - user_input_text.get_width() // 2, HEIGHT // 2 - 50))
    user_input_box = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)
    pygame.draw.rect(screen, WHITE, user_input_box, 2)
    name_text = username_font.render(name, True, WHITE)
    screen.blit(name_text, (user_input_box.x + 10, user_input_box.y + 10))
    instructions_text = username_font.render("Then, click anywhere to start!", True, WHITE)
    screen.blit(instructions_text, (WIDTH // 2 - instructions_text.get_width() // 2, HEIGHT // 2 + 100))
    pygame.display.flip()
    
# Function to display the splash page:
def display_splash_page(screen):
    screen.fill(WHITE)
    splash_image = pygame.image.load('Friend Finder.png')
    screen.blit(splash_image,(WIDTH // 2 - splash_image.get_width() // 2, HEIGHT // 2 - splash_image.get_height() //2))
    pygame.display.flip()

# Function to display end credits page:
def display_end_credits(screen):
    screen.fill(MAGENTA)  # Fill the screen with pink color to match color theme of splash page
    end_credits_image = pygame.image.load('credits 800 x 600.png')  # Load the end credits image
    # Center the image on the screen
    screen.blit(end_credits_image, (WIDTH // 2 - end_credits_image.get_width() // 2, HEIGHT // 2 - end_credits_image.get_height() // 2))
    pygame.display.flip()
    pygame.time.delay(5000)  # Display for 5 seconds
    
# Function to read student answers from CSV
def read_student_answers_from_csv(file_path):
    students = []
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            students.append({
                "name": row["name"],
                "answers": [row[f"Q{i + 1}"] for i in range(3)]  # Adjust to match question columns
            })
    return students


def calculate_similarity_score(student1, student2):
    return sum(1 for a, b in zip(student1["answers"], student2["answers"]) if a == b)


def find_top_matches(students, current_student_name, N=5):
    similarity_scores = defaultdict(dict)
    for i in range(len(students)):
        for j in range(i + 1, len(students)):
            similarity_score = calculate_similarity_score(students[i], students[j])
            match_percentage = (similarity_score / len(students[i]["answers"])) * 100
            similarity_scores[students[i]["name"]][students[j]["name"]] = match_percentage
            similarity_scores[students[j]["name"]][students[i]["name"]] = match_percentage

    current_student_matches = similarity_scores[current_student_name]
    sorted_matches = sorted(current_student_matches.items(), key=lambda x: x[1], reverse=True)
    top_matches = sorted_matches[:N]
    return top_matches


def display_matches(screen, matches):
    dot_matrix_image = pygame.image.load('Dot Matrix Paper.png')
    screen.blit(dot_matrix_image, dot_matrix_image.get_rect())
    y_offset = 50
    title = username_font.render("Your Top Matches", True, BLACK)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 10))
    for i, (match_name, percentage) in enumerate(matches, start=1):
        match_text = question_font.render(f"{i}. {match_name}: {percentage:.2f}% match", True, BLACK)
        screen.blit(match_text, (50, y_offset))
        y_offset += 40
    thanks = username_font.render('Thanks for playing!', True, BLACK)
    screen.blit(thanks, (WIDTH // 2 - thanks.get_width() // 2, HEIGHT - match_text.get_width()))
    click = username_font.render('[Click anywhere when done]', True, BLACK)
    screen.blit(click, (WIDTH // 2 - click.get_width() // 2, 400))
    pygame.display.flip()


# Main loop
running = True
intro_page = True
name = ""
survey_complete = False
matches_displayed = False
display_splash_page(screen)
pygame.time.set_timer(pygame.USEREVENT,4000)
splash_display = True
question_num = 0
pos_index = 2
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if splash_display:
            if event.type == pygame.USEREVENT:
                splash_display = False
                pygame.time.set_timer(pygame.USEREVENT,0)

        elif intro_page:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN and name:
                intro_page = False
        elif not survey_complete:
            for button in buttons:
                if button.is_clicked(event):
                    user_answers.append(button.text)
                    current_question += 1
                    if current_question >= len(questions):
                        # End of questions
                        write_answer_file('answers.csv', name, user_answers, class_answers)
                        students = read_student_answers_from_csv('answers.csv')
                        matches = find_top_matches(students, name)
                        survey_complete = True
                    break
    if splash_display:
        display_splash_page(screen)
    elif intro_page:
        display_intro_page(screen, name)
    elif not survey_complete:
        if current_question < len(questions):
            display_question(screen, questions[current_question], formatted_answers[current_question], question_num + 1, pos_index)
    elif survey_complete and not matches_displayed:
        display_matches(screen, matches)
        pygame.time.delay(4000)
        matches_displayed = True
    elif matches_displayed:
        if event.type == pygame.MOUSEBUTTONDOWN:
            display_end_credits(screen)


pygame.quit()
sys.exit()
