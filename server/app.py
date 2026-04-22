"""
Application entry-point.

Creates and configures the Flask app, registers extensions,
and defines all API endpoints.
"""

from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate
from models import db, Exercise, Workout, WorkoutExercise
from schemas import ExerciseSchema, WorkoutSchema, WorkoutExerciseSchema
from marshmallow import ValidationError
from datetime import date

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)

# Schema instances
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
workout_exercise_schema = WorkoutExerciseSchema()


# ---------------------------------------------------------------------------
# Workout Endpoints
# ---------------------------------------------------------------------------


@app.route("/workouts", methods=["GET"])
def get_workouts():
    """Return a list of all workouts."""
    workouts = Workout.query.all()
    return make_response(jsonify(workouts_schema.dump(workouts)), 200)


@app.route("/workouts/<int:id>", methods=["GET"])
def get_workout(id):
    """Return a single workout with its associated exercises."""
    workout = db.session.get(Workout, id)
    if not workout:
        return make_response(jsonify({"error": "Workout not found"}), 404)
    return make_response(jsonify(workout_schema.dump(workout)), 200)


@app.route("/workouts", methods=["POST"])
def create_workout():
    """Create a new workout."""
    data = request.get_json(silent=True) or {}
    try:
        validated = workout_schema.load(data)
    except ValidationError as e:
        return make_response(jsonify({"errors": e.messages}), 422)

    workout = Workout(**validated)
    db.session.add(workout)
    db.session.commit()
    return make_response(jsonify(workout_schema.dump(workout)), 201)


@app.route("/workouts/<int:id>", methods=["DELETE"])
def delete_workout(id):
    """Delete a workout and its associated workout exercises."""
    workout = db.session.get(Workout, id)
    if not workout:
        return make_response(jsonify({"error": "Workout not found"}), 404)

    # Stretch goal — delete associated WorkoutExercises first
    WorkoutExercise.query.filter_by(workout_id=id).delete()
    db.session.delete(workout)
    db.session.commit()
    return make_response("", 204)


# ---------------------------------------------------------------------------
# Exercise Endpoints
# ---------------------------------------------------------------------------


@app.route("/exercises", methods=["GET"])
def get_exercises():
    """Return a list of all exercises."""
    exercises = Exercise.query.all()
    return make_response(jsonify(exercises_schema.dump(exercises)), 200)


@app.route("/exercises/<int:id>", methods=["GET"])
def get_exercise(id):
    """Return a single exercise with its associated workouts."""
    exercise = db.session.get(Exercise, id)
    if not exercise:
        return make_response(jsonify({"error": "Exercise not found"}), 404)
    return make_response(jsonify(exercise_schema.dump(exercise)), 200)


@app.route("/exercises", methods=["POST"])
def create_exercise():
    """Create a new exercise."""
    data = request.get_json(silent=True) or {}
    try:
        validated = exercise_schema.load(data)
    except ValidationError as e:
        return make_response(jsonify({"errors": e.messages}), 422)

    exercise = Exercise(**validated)
    db.session.add(exercise)
    db.session.commit()
    return make_response(jsonify(exercise_schema.dump(exercise)), 201)


@app.route("/exercises/<int:id>", methods=["DELETE"])
def delete_exercise(id):
    """Delete an exercise and its associated workout exercises."""
    exercise = db.session.get(Exercise, id)
    if not exercise:
        return make_response(jsonify({"error": "Exercise not found"}), 404)

    # Stretch goal — delete associated WorkoutExercises first
    WorkoutExercise.query.filter_by(exercise_id=id).delete()
    db.session.delete(exercise)
    db.session.commit()
    return make_response("", 204)


# ---------------------------------------------------------------------------
# WorkoutExercise Endpoints
# ---------------------------------------------------------------------------


@app.route(
    "/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises",
    methods=["POST"],
)
def create_workout_exercise(workout_id, exercise_id):
    """Add an exercise to a workout with sets, reps, or duration."""
    workout = db.session.get(Workout, workout_id)
    if not workout:
        return make_response(jsonify({"error": "Workout not found"}), 404)

    exercise = db.session.get(Exercise, exercise_id)
    if not exercise:
        return make_response(jsonify({"error": "Exercise not found"}), 404)

    data = request.get_json(silent=True) or {}
    try:
        validated = workout_exercise_schema.load(data)
    except ValidationError as e:
        return make_response(jsonify({"errors": e.messages}), 422)

    workout_exercise = WorkoutExercise(
        workout_id=workout_id, exercise_id=exercise_id, **validated
    )
    db.session.add(workout_exercise)
    db.session.commit()
    return make_response(jsonify(workout_exercise_schema.dump(workout_exercise)), 201)


if __name__ == "__main__":
    app.run(port=5555, debug=True)
