"""
Marshmallow schemas for serialization and deserialization.

ExerciseSchema        — serializes/deserializes Exercise objects.
WorkoutSchema         — serializes/deserializes Workout objects.
WorkoutExerciseSchema — serializes/deserializes WorkoutExercise objects.
"""

from marshmallow import Schema, fields, validates, ValidationError

VALID_CATEGORIES = ["strength", "cardio", "flexibility", "balance"]


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    category = fields.Str(required=True)
    equipment_needed = fields.Bool(required=True)

    # Schema validation — name cannot be empty
    @validates("name")
    def validate_name(self, value):
        if not value or not value.strip():
            raise ValidationError("Exercise name cannot be empty")

    # Schema validation — category must be one of the valid options
    @validates("category")
    def validate_category(self, value):
        if value not in VALID_CATEGORIES:
            raise ValidationError(
                f"Category must be one of: {', '.join(VALID_CATEGORIES)}"
            )


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(dump_only=True)
    exercise_id = fields.Int(dump_only=True)
    reps = fields.Int(allow_none=True)
    sets = fields.Int(allow_none=True)
    duration_seconds = fields.Int(allow_none=True)

    exercise = fields.Nested(ExerciseSchema, dump_only=True)

    # Schema validation — reps must be positive if provided
    @validates("reps")
    def validate_reps(self, value):
        if value is not None and value <= 0:
            raise ValidationError("reps must be greater than 0")

    # Schema validation — sets must be positive if provided
    @validates("sets")
    def validate_sets(self, value):
        if value is not None and value <= 0:
            raise ValidationError("sets must be greater than 0")


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(required=True)
    notes = fields.Str(allow_none=True)

    workout_exercises = fields.List(
        fields.Nested(WorkoutExerciseSchema), dump_only=True
    )

    # Schema validation — duration must be positive
    @validates("duration_minutes")
    def validate_duration(self, value):
        if value <= 0:
            raise ValidationError("duration_minutes must be greater than 0")
