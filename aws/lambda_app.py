from aws.s3_data_fetcher import S3DataFetcher
from common.exam_data_processor import ExamDataProcessor
from common.contracts import read_and_compute

def build_html(stats):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Student Score Summary</title>

    <style>
        body {{
        
        
            font-family: Arial, sans-serif;
            margin: 40px;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin-top: 20px;
        }}
        th, td {{
            border: 1px solid #ccc;
            padding: 8px;
        }}
        th {{
            background-color: #f4f4f4;
        }}
        input {{
            margin-right: 10px;
        }}
    </style>
</head>

<body>
<main>
    <h1>Student Scores</h1>

    <section>
        <ul>
            <li>
                <strong>Average Score:</strong>
                <span id="avgScore">{stats.average_final:.2f}</span>
            </li>
            <li>
                <strong>Unique Students:</strong>
                <span id="studentCount">{stats.unique_students}</span>
            </li>
        </ul>
    </section>

    <section>
        <h2>Add Student Grade</h2>

        <input type="text" id="studentName" placeholder="Student name" />
        <input type="number" id="studentScore" placeholder="Final score" />
        <button onclick="addGrade()">Add</button>
    </section>

    <section>
        <h2>Grade Data</h2>

        <table>
            <thead>
                <tr>
                    <th>Student</th>
                    <th>Final Score</th>
                </tr>
            </thead>
            <tbody id="gradeTable"></tbody>
        </table>
    </section>
</main>

<script>
    // Initial dataset seeded from server-side computation
    const grades = [];

    function recalculate() {{
        const uniqueStudents = new Set(grades.map(g => g.name));
        const total = grades.reduce((sum, g) => sum + g.score, 0);
        const average = grades.length ? (total / grades.length) : 0;

        document.getElementById("studentCount").innerText = uniqueStudents.size;
        document.getElementById("avgScore").innerText = average.toFixed(2);
    }}

    function renderTable() {{
        const table = document.getElementById("gradeTable");
        table.innerHTML = "";

        grades.forEach(g => {{
            const row = document.createElement("tr");
            row.innerHTML = `<td>${{g.name}}</td><td>${{g.score}}</td>`;
            table.appendChild(row);
        }});
    }}

    function addGrade() {{
        const name = document.getElementById("studentName").value.trim();
        const score = parseFloat(document.getElementById("studentScore").value);

        if (!name || isNaN(score)) {{
            alert("Please enter a valid name and score.");
            return;
        }}

        grades.push({{ name, score }});

        document.getElementById("studentName").value = "";
        document.getElementById("studentScore").value = "";

        renderTable();
        recalculate();
    }}
</script>
</body>
</html>
"""

def lambda_handler(event, context):
    print("Starting lambda!")

    result = read_and_compute(
        S3DataFetcher("bulead2026-exam-scores", "test_scores.csv"),
        ExamDataProcessor()
    )

    print(result)

    return {
        'statusCode': 200,
        'headers': {"Content-Type": "text/html; charset=utf-8"},
        'body': build_html(result)
    }