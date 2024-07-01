import pygame
import sys
import csv

# 1. Set up pygame for user interface
#    - Game window, ask questions, options for users to answer
pygame.init()
game_window = pygame.display.set_mode((800, 600))
#    - Have users press keys to submit answers seems simplest (A, B, C, D)
def answer_input():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        return 'A'
    elif keys[pygame.K_b]:
        return 'B'
    elif keys[pygame.K_c]:
        return 'C'
    elif keys[pygame.K_d]:
        return 'D'
        
# 2. Store answers (CSV)
def write_answer_file(filename, name, user_answers, class_answers):
    class_answers.append([name] + user_answers)
    with open(filename, 'w', newline='') as csvfile:
        answer_writer = csv.writer(csvfile)
        answer_writer.writerow(['name', '1_answer', '2_answer'])  # Add more depending on #of questions
        answer_writer.writerows(class_answers)  #Writes in any existing answers

def read_answer_file(filename):
    answer_list = []
    with open(filename, 'r', newline='') as csvfile:
        answer_reader = csv.reader(csvfile)
        for row in answer_reader:
            answer_list.append(row)  #Creates a list we can accesss if needed
            
# 3. Compare them
# 4. Display comparison to users
# 5. Run the quiz

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


