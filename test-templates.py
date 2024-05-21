from flask import Flask, request, render_template
import os

app = Flask(__name__)

def calculate_results(request_form):
    # unit_chosen = request_form['unit_chosen']
    age = request_form['age']
    gender = request_form['gender']
    height = request_form['height']
    weight = request_form['weight']
    sport_per_day = request_form['sport_per_day']
    goal_chosen = request_form['goal_chosen']
    activity_level = request_form['activity_level']

    h = float(height) / 100
    w = float(weight)

    bmi = w / (h ** 2)

    water_base = w * 35
    sport_hours = float(sport_per_day)
    water_from_sport = sport_hours * 750
    water_total = water_base + water_from_sport

    protein = 0
    if goal_chosen == "1":
        protein = round(w / (220.462 / 150), 1)
    elif goal_chosen == "2":
        protein = round(w / (220.462 / 120), 1)
    elif goal_chosen == "3":
        protein = round(w / (220.462 / 100), 1)

    carbs = 0
    if activity_level == "1":
        carbs = w * 4
    elif activity_level == "2":
        carbs = w * 6
    elif activity_level == '3':
        carbs = w * 8
    elif activity_level == '4':
        carbs = w * 10

    a = float(age)
    bmr = 0
    tdee = 0
    if gender.upper() in ['M', 'Ч', 'м', 'ч']:
        bmr = 66 + (13.7516 * w) + (5.033 * h) - (6.7550 * a)
        if activity_level == "1":
            tdee = bmr * 1.4
        elif activity_level == "2":
            tdee = bmr * 1.6
        elif activity_level == "3":
            tdee = bmr * 1.8
        elif activity_level == "4":
            tdee = bmr * 2
    if gender.upper() in ['F', 'f', 'Ж', 'ж']:
        bmr = 655 + (9.5634 * w) + (1.8496 * h) - (4.6756 * a)
        if activity_level == "1":
            tdee = bmr * 1.4
        elif activity_level == "2":
            tdee = bmr * 1.6
        elif activity_level == "3":
            tdee = bmr * 1.8
        elif activity_level == "4":
            tdee = bmr * 2

    # Розрахунок серцебиття
    heart_rate = 220 - int(age)

    # Визначення категорії BMR через результат BMI
    if bmi < 18.5:
        bmi_category = "Недостатня вага"
    elif 18.5 <= bmi < 24.9:
        bmi_category = "Здорова вага"
    elif 25 <= bmi < 29.9:
        bmi_category = "Надмірна вага"
    elif 30 <= bmi < 34.9:
        bmi_category = "Ожиріння"
    elif 35 <= bmi < 39.9:
        bmi_category = "Сильне ожиріння"
    else:
        bmi_category = "Надмірна вага"

    return {'bmi': bmi, 'water_total': water_total, 'protein': protein, 'carbs': carbs, 'tdee': round(tdee, 2), 'bmi_category': bmi_category, 'bmr': round(bmr, 2), 'heart_rate': heart_rate}


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        results = calculate_results(request.form)
        return render_template('result.html', **results)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
