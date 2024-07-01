# Let's assume we have a list of students and their answers to some questions
# Not sure how to import CSV file yet
from collections import defaultdict

students = [
    {"name": "Alice", "answers": ["A", "B", "A", "C"]},
    {"name": "Bob", "answers": ["A", "A", "C", "C"]},
    {"name": "Charlie", "answers": ["B", "B", "A", "C"]},
    {"name": "David", "answers": ["A", "B", "A", "C"]}
]

# Create a dictionary to store the similarity scores between each pair of students
# Error fix attend import defaultdict above in line 3

similarity_scores = defaultdict(dict)

# Calculate the similarity scores
# Would the difference score be an important feature?
for i in range(len(students)):
    for j in range(i+1, len(students)):
        # The similarity score is the number of answers that the two students have in common
        similarity_score = sum([1 for a, b in zip(students[i]["answers"], students[j]["answers"]) if a == b])
        similarity_scores[students[i]["name"]][students[j]["name"]] = similarity_score
        similarity_scores[students[j]["name"]][students[i]["name"]] = similarity_score

# Now sort the students by their similarity scores
sorted_students = sorted(similarity_scores.items(), key=lambda x: sum(x[1].values()), reverse=True)

# print the sorted list of students
for student in sorted_students:
    print(f"Name: {student[0]}, Similarity Score: {sum(student[1].values())}")
