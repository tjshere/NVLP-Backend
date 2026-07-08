# NVLP Backend

The API and intelligence layer for NVLP, the Neurodivergent Learning Platform.

Every screen the student sees is driven from here: authentication, courses, tasks, quiz results, and the adaptive engine that quietly rewires the experience around how each student actually learns. If the frontend is the face of NVLP, this is the nervous system.

## What it does

- **Adaptive Rules Engine.** A library of 47 clinically informed neuro-adaptive rules that map real-time signals to concrete interventions. Sensory overload detected? The platform dims visuals and lowers audio. Math anxiety detected? Timers disappear. The engine covers ten neuro-profiles: Autism, ADHD, Dyslexia, Dyscalculia, Dyspraxia, Auditory Processing, Gifted/2e, Anxiety, Sensory Processing, and Executive Function support.
- **AI Assistants.** Two OpenAI-powered companions with distinct jobs. Lucas handles academic scaffolding ("explain fractions using pizza"), Dani handles executive function ("I'm overwhelmed, break this down for me").
- **Executive Function Toolkit.** APIs for Pomodoro focus sessions and task chunking, so overwhelming assignments become sequences of small wins.
- **Course Platform.** Courses, lessons, quiz scoring, and XP progression.
- **Authentication.** JWT-based auth with email login and flexible superuser support.

## Tech stack

- Python with Django 5.2 and Django REST Framework
- JWT authentication via SimpleJWT
- OpenAI API for the assistant layer
- SQLite in development, PostgreSQL in production
- Docker and Google Cloud Run ready, served with Gunicorn and WhiteNoise

## Running locally

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in the project root with your configuration:

```
OPENAI_API_KEY=your-key-here
```

Then set up the database and start the server:

```bash
python manage.py migrate
python manage.py runserver
```

The API serves on `http://127.0.0.1:8000`. Production settings live in `config/settings/production.py` and require `SECRET_KEY` to be set in the environment; the server refuses to start without it.

## Project layout

- `core/` — users, courses, tasks, and the primary API surface
- `adaptive_engine/` — the neuro-adaptive rules library and signal handling
- `assistants/` — Lucas and Dani, conversation history, and OpenAI integration
- `config/` — Django settings split by environment

## Related repositories

- [NVLP-Frontend](https://github.com/tjshere/NVLP-Frontend) — the React client that students actually touch.

## License

This is proprietary software. The source is public to look at, not to take. See [LICENSE](LICENSE) for the full terms; for licensing inquiries, get in touch.
