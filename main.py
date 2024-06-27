# 1. Set up a web server
#   - So everyone can take the quiz at the same time on their own computers
#   - Try "Flask"
#   - Will come back to this later ...

# 2. Set up pygame for user interface
#    - Game window, ask questions, options for users to answer
#    - Have users press keys to submit answers seems simplest (A, B, C, D)

# 2. Store answers (CSV)
import csv
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


