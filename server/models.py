"""
Database models.

Exercise        — a reusable exercise with a name, category, and equipment flag.
Workout         — a single workout session with a date, duration, and notes.
WorkoutExercise — join table linking a Workout to an Exercise with sets/reps/duration.
"""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import CheckConstraint

db = SQLAlchemy()

# Valid exercise categories
VALID_CATEGORIES = ["strength", "cardio", "flexibility", "balance"]


class Exercise(db.Model):
    __tablename__ = "exercises"

    # Table constraints
    __table_args__ = (
        # Exercise name must be unique — prevents duplicate exercises
        db.UniqueConstraint("name", name="uq_exercise_name"),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False, default=False)

    workout_exercises = db.relationship("WorkoutExercise", back_populates="exercise")
    workouts = db.relationship("Workout", secondary="workout_exercises", back_populates="exercises")

    # Model validation — name cannot be empty
    @validates("name")
    def validate_name(self, key, value):
        if not value or not value.strip():
            raise ValueError("Exercise name cannot be empty")
        return value.strip()

    # Model validation — category must be one of the valid options
    @validates("category")
    def validate_category(self, key, value):
        if value not in VALID_CATEGORIES:
            raise ValueError(f"Category must be one of: {', '.join(VALID_CATEGORIES)}")
        return value

    def __repr__(self):
        return f"<Exercise id={self.id} name={self.name!r} category={self.category!r}>"


class Workout(db.Model):
    __tablename__ = "workouts"

    # Table constraint — duration must be a positive number
    __table_args__ = (
        CheckConstraint("duration_minutes > 0", name="ck_workout_duration_positive"),
    )

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

    workout_exercises = db.relationship("WorkoutExercise", back_populates="workout")
    exercises = db.relationship("Exercise", secondary="workout_exercises", back_populates="workouts")

    # Model validation — duration must be a positive integer
    @validates("duration_minutes")
    def validate_duration(self, key, value):
        if value is None or value <= 0:
            raise ValueError("duration_minutes must be greater than 0")
        return value

    # Model validation — date cannot be None
    @validates("date")
    def validate_date(self, key, value):
        if value is None:
            raise ValueError("date is required")
        return value

    def __repr__(self):
        return f"<Workout id={self.id} date={self.date} duration={self.duration_minutes}>"


class WorkoutExercise(db.Model):
    __tablename__ = "workout_exercises"

    # Table constraint — reps and sets must be positive if provided
    __table_args__ = (
        CheckConstraint("reps IS NULL OR reps > 0", name="ck_workout_exercise_reps_positive"),
        CheckConstraint("sets IS NULL OR sets > 0", name="ck_workout_exercise_sets_positive"),
    )

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey("workouts.id"), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercises.id"), nullable=False)
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    workout = db.relationship("Workout", back_populates="workout_exercises")
    exercise = db.relationship("Exercise", back_populates="workout_exercises")

    # Model validation — reps must be positive if provided
    @validates("reps")
    def validate_reps(self, key, value):
        if value is not None and value <= 0:
            raise ValueError("reps must be greater than 0")
        return value

    # Model validation — sets must be positive if provided
    @validates("sets")
    def validate_sets(self, key, value):
        if value is not None and value <= 0:
            raise ValueError("sets must be greater than 0")
        return value

    def __repr__(self):
        return f"<WorkoutExercise id={self.id} workout_id={self.workout_id} exercise_id={self.exercise_id}>"