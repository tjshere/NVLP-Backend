# Manual Testing Steps - EF Toolkit API

Follow these steps to manually test your API endpoints.

## Step 1: Start the Server

Open Terminal 1:
```bash
cd /Users/aug/Documents/GitHub/NVLP-Backend
source venv/bin/activate
python manage.py runserver
```

You should see:
```
Starting development server at http://127.0.0.1:8000/
```

**Keep this terminal running!**

---

## Step 2: Get an Authentication Token

Open Terminal 2 (new terminal window):

### Option A: Register a new user
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "testpass123"}'
```

### Option B: Login (if user already exists)
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "testpass123"}'
```

**Copy the `access_token` from the response!** It looks like:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "expires_in_minutes": 30
}
```

---

## Step 3: Test Pomodoro Timer API

Replace `YOUR_TOKEN` with the actual token you copied.

### 3a. Create a Pomodoro Timer
```bash
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
```

**Expected:** Status 201, returns timer data with an `id` field.

**Copy the `id` from the response!** (e.g., `"id": 1`)

### 3b. List All Your Timers
```bash
curl -X GET http://localhost:8000/api/pomodoro-timers/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Expected:** Status 200, returns an array with your timer(s).

### 3c. Get a Specific Timer (replace `1` with your timer ID)
```bash
curl -X GET http://localhost:8000/api/pomodoro-timers/1/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Expected:** Status 200, returns the timer details.

### 3d. Update a Timer (replace `1` with your timer ID)
```bash
curl -X PATCH http://localhost:8000/api/pomodoro-timers/1/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"current_status": "Paused"}'
```

**Expected:** Status 200, returns updated timer.

### 3e. Delete a Timer (replace `1` with your timer ID)
```bash
curl -X DELETE http://localhost:8000/api/pomodoro-timers/1/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Expected:** Status 204 (no content).

---

## Step 4: Test Task Chunking API

### 4a. Create a Task Chunking with Nested Steps
```bash
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
      },
      {
        "step_description": "Create serializers and views",
        "is_step_complete": false,
        "order": 3
      }
    ]
  }'
```

**Expected:** Status 201, returns task with nested `steps` array.

**Copy the `id` from the response!**

### 4b. List All Your Tasks
```bash
curl -X GET http://localhost:8000/api/task-chunkings/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Expected:** Status 200, returns array with tasks and their steps.

### 4c. Get a Specific Task (replace `1` with your task ID)
```bash
curl -X GET http://localhost:8000/api/task-chunkings/1/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Expected:** Status 200, returns task with all nested steps.

### 4d. Update a Task with New Steps (replace `1` with your task ID)
```bash
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
        "step_description": "Create serializers and views",
        "is_step_complete": true,
        "order": 3
      },
      {
        "step_description": "Test API endpoints",
        "is_step_complete": false,
        "order": 4
      }
    ]
  }'
```

**Expected:** Status 200, returns updated task with new steps (old steps replaced).

### 4e. Delete a Task (replace `1` with your task ID)
```bash
curl -X DELETE http://localhost:8000/api/task-chunkings/1/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Expected:** Status 204 (no content). Steps are also deleted (cascade).

---

## Step 5: Test Authentication Requirements

### Test without token (should fail):
```bash
curl -X GET http://localhost:8000/api/pomodoro-timers/
```

**Expected:** Status 401 (Unauthorized)

### Test with invalid token (should fail):
```bash
curl -X GET http://localhost:8000/api/pomodoro-timers/ \
  -H "Authorization: Bearer invalid_token_here"
```

**Expected:** Status 401 (Unauthorized)

---

## Quick Test Checklist

- [ ] Server starts without errors
- [ ] Can register/login and get token
- [ ] Can create Pomodoro timer (201)
- [ ] Can list Pomodoro timers (200)
- [ ] Can retrieve specific Pomodoro timer (200)
- [ ] Can update Pomodoro timer (200)
- [ ] Can create Task chunking with nested steps (201)
- [ ] Can list Task chunkings (200)
- [ ] Can retrieve Task chunking with steps (200)
- [ ] Can update Task chunking with new steps (200)
- [ ] Unauthenticated requests return 401

---

## Tips

1. **Pretty print JSON responses:**
   Add `| python -m json.tool` to any curl command:
   ```bash
   curl -X GET http://localhost:8000/api/pomodoro-timers/ \
     -H "Authorization: Bearer YOUR_TOKEN" | python -m json.tool
   ```

2. **Save token to a variable (bash):**
   ```bash
   TOKEN="your_token_here"
   curl -X GET http://localhost:8000/api/pomodoro-timers/ \
     -H "Authorization: Bearer $TOKEN"
   ```

3. **Use Postman or Insomnia:**
   Instead of curl, you can use GUI tools:
   - Import the endpoints
   - Set Authorization header: `Bearer YOUR_TOKEN`
   - Test all endpoints visually

---

## Common Issues

**401 Unauthorized:**
- Make sure you copied the full token (it's long!)
- Token might have expired (register/login again)
- Check the Authorization header format: `Bearer TOKEN` (with space)

**404 Not Found:**
- Make sure server is running on port 8000
- Check the URL path is correct
- Make sure migrations are applied: `python manage.py migrate`

**400 Bad Request:**
- Check JSON format is valid
- Make sure all required fields are included
- Check field types match (e.g., `order` should be integer)

**500 Server Error:**
- Check Terminal 1 (server) for error messages
- Make sure database is set up correctly
- Check that all models are properly migrated

