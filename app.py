from flask import Flask, render_template, request
import os
import matplotlib.pyplot as plt
import pandas as pd

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    suggestions = ""
    if request.method == 'POST':
        name = request.form['name']
        mood = request.form['mood']
        sleep = request.form['sleep']
        screen = int(request.form['screen'])

        # Save to CSV
        with open("mood_log.csv", "a") as f:
            f.write(f"{name},{mood},{sleep},{screen}\n")

        suggestions_list = []

        if mood.lower() == "sad":
            suggestions_list.extend([
                "Go for a walk.",
                "Listen to calming music.",
                "Try journaling.",
                "Drink water.",
                "Talk to a friend or family member."
            ])
        if mood.lower() == "stressed":
            suggestions_list.extend([
                "Practice deep breathing exercises.",
                "Try meditation or yoga.",
                "Take a short break and relax."
            ])
        if mood.lower() == "angry":
            suggestions_list.extend([
                "Take a few deep breaths.",
                "Count to ten before responding.",
                "Engage in physical activity to release tension."
            ])
        if sleep.lower() == "no":
            suggestions_list.append("Get 7–8 hours of sleep.")
        elif sleep.lower() == "yes":
            suggestions_list.append("Maintain a consistent sleep schedule.")

        # Screen time suggestions
        if screen >= 8:
            suggestions_list.extend([
                "Limit screen time to 1-2 hours per day.",
                "Engage in offline activities like reading or exercising."
            ])
        elif 6 <= screen < 8:
            suggestions_list.append("Consider reducing screen time to improve your mood.")
        elif 4 <= screen < 6:
            suggestions_list.extend([
                "Consider taking regular breaks from screens.",
                "Engage in hobbies that do not involve screens."
            ])
        elif 2 <= screen < 4:
            suggestions_list.extend([
                "Try to reduce screen time gradually.",
                "Engage in social activities or outdoor exercises."
            ])
        else:
            suggestions_list.append("Great job! Keep up the minimal screen time.")

        if mood.lower() == "happy":
            suggestions_list.extend([
                "Share your happiness with others.",
                "Engage in activities that bring you joy.",
                "Practice gratitude for the positive moments."
            ])

        suggestions = "<br>".join(suggestions_list)

    return render_template("index.html", suggestions=suggestions)

# Route to show graphs
@app.route('/graph')
def show_graph():
    if not os.path.exists("mood_log.csv"):
        return "No data available yet."

    df = pd.read_csv("mood_log.csv", names=["Name", "Mood", "Sleep", "Screen"])

    # Mood pie chart
    mood_counts = df["Mood"].value_counts()
    plt.figure(figsize=(5, 4))
    mood_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90)
    plt.title("Mood Distribution")
    plt.ylabel("")
    plt.savefig("static/mood_pie.png")
    plt.close()

    # Screen time bar chart
    plt.figure(figsize=(5, 4))
    df["Screen"].plot(kind='hist', bins=6, color='skyblue', edgecolor='black')
    plt.title("Screen Time Distribution")
    plt.xlabel("Hours")
    plt.savefig("static/screen_bar.png")
    plt.close()

    # Sleep distribution
    sleep_counts = df["Sleep"].value_counts()
    plt.figure(figsize=(5, 4))
    sleep_counts.plot(kind='bar', color='lightgreen')
    plt.title("Sleep Quality")
    plt.savefig("static/sleep_bar.png")
    plt.close()

    return render_template("graph.html")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)