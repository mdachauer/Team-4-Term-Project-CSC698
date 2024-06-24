# 1. Set up a web server
#   - So everyone can take the quiz at the same time on their own computers
#   - Try "Flask"
#   - Will come back to this later ...

# 2. Set up pygame for user interface
#    - Game window, ask questions, options for users to answer
#    - Have users press keys to submit answers seems simplest (A, B, C, D)

# 2. Store answers (CSV)
# Basic function:
import csv
with open('class_answers.csv', 'w', newline='') as csvfile:
    file_writer = csv.writer(csvfile)
    file_writer.writerow(['name', '1_answer', '2_answer', '3_answer'])

# 3. Compare them
# 4. Display comparison to users


