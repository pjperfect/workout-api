"""
Marshmallow schemas for serialization and deserialization.

ExerciseSchema      — serializes/deserializes Exercise objects.
WorkoutSchema       — serializes/deserializes Workout objects.
WorkoutExerciseSchema — serializes/deserializes WorkoutExercise objects.
"""

from marshmallow import Schema, fields


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    category = fields.Str()
    equipment_needed = fields.Bool()


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(dump_only=True)
    exercise_id = fields.Int(dump_only=True)
    reps = fields.Int(allow_none=True)
    sets = fields.Int(allow_none=True)
    duration_seconds = fields.Int(allow_none=True)

    # Nested exercise data when serializing a WorkoutExercise
    exercise = fields.Nested(ExerciseSchema, dump_only=True)


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date()
    duration_minutes = fields.Int()
    notes = fields.Str(allow_none=True)

    # Nested workout exercises including exercise details
    workout_exercises = fields.List(
        fields.Nested(WorkoutExerciseSchema), dump_only=True
    )
