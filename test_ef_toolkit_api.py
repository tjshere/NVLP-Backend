#!/usr/bin/env python
"""
Quick test script for EF Toolkit API endpoints.
Run this after starting the Django server.

Usage:
    python test_ef_toolkit_api.py
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:8000"
TEST_EMAIL = "test@example.com"
TEST_PASSWORD = "testpass123"

def print_response(title, response):
    """Helper to print formatted response."""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response: {response.text}")

def test_ef_toolkit_api():
    """Test the EF Toolkit API endpoints."""
    
    # Step 1: Register a test user (or login if exists)
    print("\n🔐 Step 1: Register/Login")
    register_data = {
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD
    }
    
    # Try to register
    register_response = requests.post(f"{BASE_URL}/api/auth/register/", json=register_data)
    if register_response.status_code == 201:
        print("✓ User registered successfully")
        token = register_response.json()["access_token"]
    else:
        # Try to login instead
        print("User might already exist, trying login...")
        login_response = requests.post(f"{BASE_URL}/api/auth/login/", json=register_data)
        if login_response.status_code == 200:
            print("✓ User logged in successfully")
            token = login_response.json()["access_token"]
        else:
            print_response("❌ Login failed", login_response)
            return
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Step 2: Test Pomodoro Timer endpoints
    print("\n🍅 Step 2: Testing Pomodoro Timer API")
    
    # Create a Pomodoro timer
    pomodoro_data = {
        "work_duration": 25,
        "break_duration": 5,
        "long_break_duration": 15,
        "cycles_to_long_break": 4,
        "current_status": "Working"
    }
    create_response = requests.post(
        f"{BASE_URL}/api/pomodoro-timers/",
        json=pomodoro_data,
        headers=headers
    )
    print_response("Create Pomodoro Timer", create_response)
    
    if create_response.status_code == 201:
        timer_id = create_response.json()["id"]
        
        # Retrieve the timer
        get_response = requests.get(
            f"{BASE_URL}/api/pomodoro-timers/{timer_id}/",
            headers=headers
        )
        print_response("Retrieve Pomodoro Timer", get_response)
        
        # Update the timer
        update_data = {"current_status": "Paused"}
        update_response = requests.patch(
            f"{BASE_URL}/api/pomodoro-timers/{timer_id}/",
            json=update_data,
            headers=headers
        )
        print_response("Update Pomodoro Timer", update_response)
        
        # List all timers
        list_response = requests.get(
            f"{BASE_URL}/api/pomodoro-timers/",
            headers=headers
        )
        print_response("List Pomodoro Timers", list_response)
    
    # Step 3: Test Task Chunking endpoints
    print("\n📋 Step 3: Testing Task Chunking API")
    
    # Create a task chunking with nested steps
    task_data = {
        "main_task_title": "Complete Django Project",
        "is_complete": False,
        "steps": [
            {
                "step_description": "Set up virtual environment",
                "is_step_complete": True,
                "order": 1
            },
            {
                "step_description": "Create models",
                "is_step_complete": True,
                "order": 2
            },
            {
                "step_description": "Create serializers and views",
                "is_step_complete": False,
                "order": 3
            },
            {
                "step_description": "Test API endpoints",
                "is_step_complete": False,
                "order": 4
            }
        ]
    }
    create_task_response = requests.post(
        f"{BASE_URL}/api/task-chunkings/",
        json=task_data,
        headers=headers
    )
    print_response("Create Task Chunking with Steps", create_task_response)
    
    if create_task_response.status_code == 201:
        task_id = create_task_response.json()["id"]
        
        # Retrieve the task with steps
        get_task_response = requests.get(
            f"{BASE_URL}/api/task-chunkings/{task_id}/",
            headers=headers
        )
        print_response("Retrieve Task Chunking with Steps", get_task_response)
        
        # Update task and steps
        update_task_data = {
            "is_complete": False,
            "steps": [
                {
                    "step_description": "Set up virtual environment",
                    "is_step_complete": True,
                    "order": 1
                },
                {
                    "step_description": "Create models",
                    "is_step_complete": True,
                    "order": 2
                },
                {
                    "step_description": "Create serializers and views",
                    "is_step_complete": True,
                    "order": 3
                },
                {
                    "step_description": "Test API endpoints",
                    "is_step_complete": True,
                    "order": 4
                }
            ]
        }
        update_task_response = requests.put(
            f"{BASE_URL}/api/task-chunkings/{task_id}/",
            json=update_task_data,
            headers=headers
        )
        print_response("Update Task Chunking with Steps", update_task_response)
        
        # List all tasks
        list_tasks_response = requests.get(
            f"{BASE_URL}/api/task-chunkings/",
            headers=headers
        )
        print_response("List Task Chunkings", list_tasks_response)
    
    print("\n✅ Testing complete!")
    print("\nNote: To test DELETE endpoints, you can manually call:")
    print(f"  DELETE {BASE_URL}/api/pomodoro-timers/{{id}}/")
    print(f"  DELETE {BASE_URL}/api/task-chunkings/{{id}}/")

if __name__ == "__main__":
    print("🧪 EF Toolkit API Test Script")
    print("Make sure the Django server is running on http://localhost:8000")
    print("\nPress Enter to start testing...")
    input()
    
    try:
        test_ef_toolkit_api()
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to server.")
        print("Please make sure the Django server is running:")
        print("  python manage.py runserver")
    except Exception as e:
        print(f"\n❌ Error: {e}")

