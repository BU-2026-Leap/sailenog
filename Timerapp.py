def lambda_handler(event, context):
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "text/html"
        },
        "body": build_html()
    }


def build_html():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Interval Timer</title>

    <!-- ===================== -->
    <!--        STYLES         -->
    <!-- ===================== -->
    <style>
        :root {
            --exercise-green: #2ecc71;
            --warning-red: #e74c3c;
            --rest-purple: #9b59b6;
            --neutral-gray: #ecf0f1;
            --text-dark: #2c3e50;
        }

        body {
            font-family: Arial, Helvetica, sans-serif;
            background: var(--neutral-gray);
            color: var(--text-dark);
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }

        .app {
            background: white;
            padding: 24px;
            border-radius: 8px;
            width: 320px;
            text-align: center;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        }

        .controls input {
            width: 80px;
            margin: 6px;
            padding: 4px;
        }

        .timer {
            font-size: 48px;
            margin: 20px 0;
            padding: 20px;
            border-radius: 6px;
            background: var(--exercise-green);
            color: white;
        }

        button {
            padding: 10px 16px;
            font-size: 16px;
            cursor: pointer;
        }
    </style>
</head>

<body>
<div class="app">
    <h2>Interval Timer</h2>

    <div class="controls">
        <div>
            Reps:
            <input id="reps" type="number" value="3" min="1">
        </div>
        <div>
            Exercise (sec):
            <input id="exerciseTime" type="number" value="30" min="1">
        </div>
        <div>
            Rest (sec):
            <input id="restTime" type="number" value="15" min="0">
        </div>
    </div>

    <div id="timer" class="timer">00</div>
    <div id="status">Ready</div>

    <button onclick="start()">Start</button>
</div>

<!-- ===================== -->
<!--     TIMER SCRIPT     -->
<!-- ===================== -->
<script>
    let intervalId = null;

    function start() {
        clearInterval(intervalId);

        const totalReps = parseInt(document.getElementById("reps").value);
        const exerciseTime = parseInt(document.getElementById("exerciseTime").value);
        const restTime = parseInt(document.getElementById("restTime").value);

        let currentRep = 1;
        let phase = "exercise";
        let timeLeft = exerciseTime;

        updateUI(timeLeft, phase, currentRep, totalReps);

        intervalId = setInterval(() => {
            timeLeft--;

            if (phase === "exercise" && timeLeft <= 10) {
                setTimerColor("red");
            }

            if (timeLeft < 0) {
                if (phase === "exercise" && restTime > 0) {
                    phase = "rest";
                    timeLeft = restTime;
                    setTimerColor("purple");
                } else {
                    currentRep++;
                    if (currentRep > totalReps) {
                        clearInterval(intervalId);
                        document.getElementById("status").innerText = "Done!";
                        return;
                    }
                    phase = "exercise";
                    timeLeft = exerciseTime;
                    setTimerColor("green");
                }
            }

            updateUI(timeLeft, phase, currentRep, totalReps);
        }, 1000);
    }

    function updateUI(time, phase, rep, total) {
        document.getElementById("timer").innerText = time;
        document.getElementById("status").innerText =
            phase.toUpperCase() + " | Rep " + rep + " of " + total;
    }

    function setTimerColor(state) {
        const timer = document.getElementById("timer");

        if (state === "green") {
            timer.style.background = "var(--exercise-green)";
        } else if (state === "red") {
            timer.style.background = "var(--warning-red)";
        } else if (state === "purple") {
            timer.style.background = "var(--rest-purple)";
        }
    }
</script>
</body>
</html>
"""
