import csv
import json
import os

def compute_stats(input_filename):
    total_final = 0.0
    num_final = 0
    students = set()  # use a set for uniqueness

    with open(input_filename, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            students.add(row["student_id"])

            if row["exam_name"] == "final":
                total_final += float(row["score"])
                num_final += 1

    average_final = total_final / num_final if num_final > 0 else 0.0
    unique_students = len(students)

    return average_final, unique_students


# ---- main execution ----
average_final, unique_students = compute_stats(input_filename)

result = {
    "average_final": average_final,
    "unique_students": unique_students,
}

if os.path.exists(output_filename):
    os.remove(output_filename)

with open(output_filename, "w") as out:
    json.dump(result, out, indent=2)

print(average_final, unique_students)