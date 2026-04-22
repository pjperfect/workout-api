"""
Database models.

Exercise        — a reusable exercise with a name, category, and equipment flag.
Workout         — a single workout session with a date, duration, and notes.
WorkoutExercise — join table linking a Workout to an Exercise with sets/reps/duration.
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Exercise(db.Model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False)

    # An Exercise has many WorkoutExercises
    workout_exercises = db.relationship("WorkoutExercise", back_populates="exercise")

    # An Exercise has many Workouts through WorkoutExercises
    workouts = db.relationship("Workout", secondary="workout_exercises", back_populates="exercises")

    def __repr__(self):
        return f"<Exercise id={self.id} name={self.name!r} category={self.category!r}>"


class Workout(db.Model):
    __tablename__ = "workouts"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

    # A Workout has many WorkoutExercises
    workout_exercises = db.relationship("WorkoutExercise", back_populates="workout")

    # A Workout has many Exercises through WorkoutExercises
    exercises = db.relationship("Exercise", secondary="workout_exercises", back_populates="workouts")

    def __repr__(self):
        return f"<Workout id={self.id} date={self.date} duration={self.duration_minutes}>"


class WorkoutExercise(db.Model):
    __tablename__ = "workout_exercises"

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey("workouts.id"), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercises.id"), nullable=False)
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    # WorkoutExercise belongs to a Workout
    workout = db.relationship("Workout", back_populates="workout_exercises")

    # WorkoutExercise belongs to an Exercise
    exercise = db.relationship("Exercise", back_populates="workout_exercises")

    def __repr__(self):
        return f"<WorkoutExercise id={self.id} workout_id={self.workout_id} exercise_id={self.exercise_id}>"