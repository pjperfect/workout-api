# Workout API

A RESTful Flask API backend for a workout tracking application used by personal
trainers. The API tracks workouts and their associated exercises, with full
validation at the table, model, and schema level.

---

## Tech Stack

- **Flask 2.2.2** — web framework
- **Flask-SQLAlchemy 3.0.3** — ORM (SQLite by default)
- **Flask-Migrate** — database migrations via Alembic
- **Marshmallow 3.20.1** — serialization and schema validation
- **uv** — fast Python package manager

---

## Database Schema

```
Table exercises {
  id integer [primary key]
  name varchar [unique, not null]
  category varchar [not null]
  equipment_needed boolean [not null]
}

Table workouts {
  id integer [primary key]
  date date [not null]
  duration_minutes integer [not null]
  notes text
}

Table workout_exercises {
  id integer [primary key]
  workout_id integer [not null, ref: > workouts.id]
  exercise_id integer [not null, ref: > exercises.id]
  reps integer
  sets integer
  duration_seconds integer
}
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/pjperfect/workout-api.git
cd workout-api
```

### 2. Install dependencies with `uv`

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh

uv venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
uv sync
```

### 3. Apply database migrations

```bash
cd server
export FLASK_APP=app.py
flask db upgrade
```

> `flask db init` and `flask db migrate` have already been run and the
> `migrations/` folder is committed to the repo. You only need `flask db upgrade`
> to apply the schema to your local database.

### 4. Seed the database

```bash
python seed.py
```

This creates 5 exercises, 3 workouts, and 7 workout exercises.

---

## Running the Server

```bash
flask run -p 5555
```

The API runs at `http://127.0.0.1:5555` by default.

---

## API Endpoints

### Workouts

| Method   | Path             | Description                                |
| -------- | ---------------- | ------------------------------------------ |
| `GET`    | `/workouts`      | List all workouts                          |
| `GET`    | `/workouts/<id>` | Get a single workout with its exercises    |
| `POST`   | `/workouts`      | Create a new workout                       |
| `DELETE` | `/workouts/<id>` | Delete a workout and its workout exercises |

#### POST `/workouts`

```json
// Request body
{ "date": "2024-01-15", "duration_minutes": 60, "notes": "Morning session" }

// 201 response
{ "id": 1, "date": "2024-01-15", "duration_minutes": 60, "notes": "Morning session", "workout_exercises": [] }
```

---

### Exercises

| Method   | Path              | Description                                  |
| -------- | ----------------- | -------------------------------------------- |
| `GET`    | `/exercises`      | List all exercises                           |
| `GET`    | `/exercises/<id>` | Get a single exercise                        |
| `POST`   | `/exercises`      | Create a new exercise                        |
| `DELETE` | `/exercises/<id>` | Delete an exercise and its workout exercises |

#### POST `/exercises`

```json
// Request body
{ "name": "Bench Press", "category": "strength", "equipment_needed": true }

// 201 response
{ "id": 1, "name": "Bench Press", "category": "strength", "equipment_needed": true }
```

---

### Workout Exercises

| Method | Path                                                               | Description                  |
| ------ | ------------------------------------------------------------------ | ---------------------------- |
| `POST` | `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` | Add an exercise to a workout |

#### POST `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises`

```json
// Request body
{ "sets": 4, "reps": 10 }

// 201 response
{ "id": 1, "workout_id": 1, "exercise_id": 1, "sets": 4, "reps": 10, "duration_seconds": null }
```

---

## Project Structure

```
workout-api/
├── server/
│   ├── app.py          # App entry-point and all endpoints
│   ├── models.py       # SQLAlchemy models with constraints and validations
│   ├── schemas.py      # Marshmallow schemas with validations
│   ├── seed.py         # Database seed script
│   └── migrations/     # Flask-Migrate generated migrations
│       └── README      # Migration usage instructions
├── pyproject.toml      # uv dependencies
└── README.md
```

---

## Validations

### Table Constraints

- `exercises.name` must be unique
- `workouts.duration_minutes` must be greater than 0
- `workout_exercises.reps` must be greater than 0 if provided
- `workout_exercises.sets` must be greater than 0 if provided

### Model Validations

- Exercise `name` cannot be empty
- Exercise `category` must be one of: `strength`, `cardio`, `flexibility`, `balance`
- Workout `duration_minutes` must be greater than 0
- Workout `date` is required
- WorkoutExercise `reps` must be positive if provided
- WorkoutExercise `sets` must be positive if provided

### Schema Validations

- Exercise `name` cannot be empty
- Exercise `category` must be one of the valid categories
- Workout `duration_minutes` must be greater than 0
- WorkoutExercise `reps` must be positive if provided
- WorkoutExercise `sets` must be positive if provided
