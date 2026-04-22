"""
Seed script — populates the database with sample data for development.

Usage (from the server/ directory):
    python seed.py

The script clears existing data before inserting new rows
so it can be re-run safely during development.
"""

from datetime import date
from app import app
from models import db, Exercise, Workout, WorkoutExercise


def seed():
    with app.app_context():
        print("Clearing existing data ...")
        WorkoutExercise.query.delete()
        Workout.query.delete()
        Exercise.query.delete()
        db.session.commit()

        print("Creating exercises ...")
        bench_press = Exercise(name="Bench Press", category="strength", equipment_needed=True)
        squat = Exercise(name="Squat", category="strength", equipment_needed=True)
        running = Exercise(name="Running", category="cardio", equipment_needed=False)
        yoga = Exercise(name="Yoga Flow", category="flexibility", equipment_needed=False)
        plank = Exercise(name="Plank", category="balance", equipment_needed=False)

        db.session.add_all([bench_press, squat, running, yoga, plank])
        db.session.commit()

        print("Creating workouts ...")
        workout1 = Workout(date=date(2024, 1, 15), duration_minutes=60, notes="Morning strength session")
        workout2 = Workout(date=date(2024, 1, 17), duration_minutes=45, notes="Cardio and flexibility")
        workout3 = Workout(date=date(2024, 1, 20), duration_minutes=90, notes="Full body workout")

        db.session.add_all([workout1, workout2, workout3])
        db.session.commit()

        print("Linking exercises to workouts ...")
        db.session.add_all([
            WorkoutExercise(workout_id=workout1.id, exercise_id=bench_press.id, sets=4, reps=10),
            WorkoutExercise(workout_id=workout1.id, exercise_id=squat.id, sets=3, reps=12),
            WorkoutExercise(workout_id=workout2.id, exercise_id=running.id, duration_seconds=1800),
            WorkoutExercise(workout_id=workout2.id, exercise_id=yoga.id, duration_seconds=900),
            WorkoutExercise(workout_id=workout3.id, exercise_id=bench_press.id, sets=5, reps=8),
            WorkoutExercise(workout_id=workout3.id, exercise_id=squat.id, sets=4, reps=10),
            WorkoutExercise(workout_id=workout3.id, exercise_id=plank.id, duration_seconds=60),
        ])
        db.session.commit()

        print("Done! Seeded 5 exercises, 3 workouts, and 7 workout exercises.")


if __name__ == "__main__":
    seed()