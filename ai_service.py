def generate_fitness_plan(name, age, goal, fitness_level):
    plan = {
        "name": name,
        "age": age,
        "goal": goal,
        "fitness_level": fitness_level,
        "workout": [
            "Warm-up – 5 minutes",
            "Bodyweight squats – 3 sets",
            "Push-ups – 3 sets",
            "Walking or light cardio – 15 minutes",
            "Cool-down – 5 minutes"
        ],
        "tips": [
            "Drink enough water.",
            "Get enough sleep.",
            "Take rest when needed.",
            "Increase activity gradually."
        ]
    }

    return plan