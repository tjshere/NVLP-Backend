# EF Toolkit API Testing Guide

This guide will help you test the new EF Toolkit API endpoints before committing to GitHub.

## Prerequisites

1. Make sure migrations are applied:
   ```bash
   python manage.py migrate
   ```

2. Install the requests library (if not already installed):
   ```bash
   pip install requests
   ```

## Method 1: Using the Test Script (Recommended)

1. Start the Django development server:
   ```bash
   python manage.py runserver
   ```

2. In a new terminal, run the test script:
   ```bash
   python test_ef_toolkit_api.py
   ```

The script will:
- Register/login a test user
- Test all Pomodoro Timer endpoints (create, read, update, list)
- Test all Task Chunking endpoints (create with nested steps, read, update, list)

## Method 2: Manual Testing with curl

### Step 1: Register/Login to get a token

```bash
# Register a new user
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "testpass123"}'

# Or login if user exists
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "testpass123"}'
```

Save the `access_token` from the response.

### Step 2: Test Pomodoro Timer Endpoints

Replace `YOUR_TOKEN` with the access token from Step 1.

```bash
# Create a Pomodoro timer
curl -X POST http://localhost:8000/api/pomodoro-timers/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "work_duration": 25,
    "break_duration": 5,
    "long_break_duration": 15,
    "cycles_to_long_break": 4,
    "current_status": "Working"
  }'

# List all timers (replace TIMER_ID with the ID from create response)
curl -X GET http://localhost:8000/api/pomodoro-timers/ \
  -H "Authorization: Bearer YOUR_TOKEN"

# Retrieve a specific timer
curl -X GET http://localhost:8000/api/pomodoro-timers/1/ \
  -H "Authorization: Bearer YOUR_TOKEN"

# Update a timer
curl -X PATCH http://localhost:8000/api/pomodoro-timers/1/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"current_status": "Paused"}'

# Delete a timer
curl -X DELETE http://localhost:8000/api/pomodoro-timers/1/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Step 3: Test Task Chunking Endpoints

```bash
# Create a task chunking with nested steps
curl -X POST http://localhost:8000/api/task-chunkings/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "main_task_title": "Complete Django Project",
    "is_complete": false,
    "steps": [
      {
        "step_description": "Set up virtual environment",
        "is_step_complete": true,
        "order": 1
      },
      {
        "step_description": "Create models",
        "is_step_complete": false,
        "order": 2
      }
    ]
  }'

# List all task chunkings
curl -X GET http://localhost:8000/api/task-chunkings/ \
  -H "Authorization: Bearer YOUR_TOKEN"

# Retrieve a specific task chunking (includes nested steps)
curl -X GET http://localhost:8000/api/task-chunkings/1/ \
  -H "Authorization: Bearer YOUR_TOKEN"

# Update a task chunking with new steps
curl -X PUT http://localhost:8000/api/task-chunkings/1/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "main_task_title": "Complete Django Project",
    "is_complete": false,
    "steps": [
      {
        "step_description": "Set up virtual environment",
        "is_step_complete": true,
        "order": 1
      },
      {
        "step_description": "Create models",
        "is_step_complete": true,
        "order": 2
      },
      {
        "step_description": "Test API",
        "is_step_complete": false,
        "order": 3
      }
    ]
  }'

# Delete a task chunking
curl -X DELETE http://localhost:8000/api/task-chunkings/1/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Method 3: Using Django's Test Client

You can also write Django unit tests. Create a test file:

```python
# core/tests_ef_toolkit.py
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from .models import PomodoroTimerModel, TaskChunkingModel, TaskStepModel

User = get_user_model()

class EFToolkitAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
    
    def test_create_pomodoro_timer(self):
        url = '/api/pomodoro-timers/'
        data = {
            'work_duration': 25,
            'break_duration': 5,
            'current_status': 'Working'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_task_chunking_with_steps(self):
        url = '/api/task-chunkings/'
        data = {
            'main_task_title': 'Test Task',
            'steps': [
                {'step_description': 'Step 1', 'order': 1},
                {'step_description': 'Step 2', 'order': 2}
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TaskStepModel.objects.count(), 2)
```

Run tests with:
```bash
python manage.py test core.tests_ef_toolkit
```

## Expected Behavior

✅ **All endpoints should:**
- Require authentication (return 401 if no token)
- Only show data belonging to the authenticated user
- Return proper JSON responses

✅ **Pomodoro Timer:**
- Create: Returns 201 with timer data
- List: Returns 200 with array of user's timers
- Retrieve: Returns 200 with single timer
- Update: Returns 200 with updated timer
- Delete: Returns 204 (no content)

✅ **Task Chunking:**
- Create: Returns 201 with task and nested steps
- List: Returns 200 with array of user's tasks (with steps)
- Retrieve: Returns 200 with single task and nested steps
- Update: Returns 200 with updated task and steps (replaces all steps)
- Delete: Returns 204 (cascades to delete steps)

## Troubleshooting

- **401 Unauthorized**: Make sure you're including the Bearer token in the Authorization header
- **404 Not Found**: Check that the server is running and the URL is correct
- **400 Bad Request**: Check the JSON payload format matches the serializer requirements
- **500 Server Error**: Check Django server logs for detailed error messages

## Quick Checklist Before Committing

- [ ] All migrations applied (`python manage.py migrate`)
- [ ] No syntax errors (`python manage.py check`)
- [ ] Server starts without errors (`python manage.py runserver`)
- [ ] Can create Pomodoro timer
- [ ] Can create Task chunking with nested steps
- [ ] Can retrieve and list both resources
- [ ] Can update both resources
- [ ] Authentication is required for all endpoints
- [ ] Users can only see their own data

