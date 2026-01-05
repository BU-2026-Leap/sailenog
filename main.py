import csv
import os
import json

from pathlib import Path
full_base_path = Path(__name__).resolve().parent
input_filename = full_base_path / "test_scores.csv"
output_filename = "output.json"

if os.path.exists(output_filename):
    os.remove(output_filename)

total_final = 0
average_final = 0.0
unique_students = 0
students = []

with open(input_filename) as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row)
    #if unique

        # TODO: compute average final score
        if row['exam_name'] == 'final':
            total_final += float(row['score'])
            unique_students += 1

        # TODO: unique student count
        if row['student_id'] not in students:
            students.append(row['student_id'])

average_final = total_final/unique_students
print(average_final)
print(unique_students)

if os.path.exists(output_filename):
    os.remove(output_filename)

result = {
    "average_final": average_final,
    "unique_students": unique_students,
}

with open(output_filename, "w") as out:
    json.dump(result, out, indent=2)

