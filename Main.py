import csv
from collections import defaultdict


def read_student_answers_from_csv(file_path):
    students = []
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            students.append({
                "name": row["Name"],
                "answers": row["Answers"].split(",")  # Assuming answers are comma-separated
            })
    return students


csv_file_path = "student_answers.csv"  # change to CSV file name or just use this name
students = read_student_answers_from_csv(csv_file_path)


def calculate_similarity_score(student1, student2):
    return sum([1 for a, b in zip(student1["answers"], student2["answers"]) if a == b])


#Find matches
def find_top_matches(students, N=5):
    similarity_scores = defaultdict(dict)
    for i in range(len(students)):
        for j in range(i + 1, len(students)):
            similarity_score = calculate_similarity_score(students[i], students[j])
            similarity_scores[students[i]["name"]][students[j]["name"]] = similarity_score
            similarity_scores[students[j]["name"]][students[i]["name"]] = similarity_score

    top_matches = {}
    for student in students:
        sorted_matches = sorted(similarity_scores[student["name"]].items(), key=lambda x: x[1], reverse=True)
        top_matches[student["name"]] = [match[0] for match in sorted_matches[:N]]

    return top_matches
