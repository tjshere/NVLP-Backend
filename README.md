# NVLP - Neurodivergent Learning Platform (Backend)

The backend infrastructure for an adaptive learning platform designed to support neurodivergent students (Autism, ADHD, Dyslexia, Dyscalculia, etc.). This system uses AI and real-time sensory tracking to modify the learning experience dynamically.

### 🚀 Current Status: Phase 2 Complete (Intelligence & Infrastructure)
* **Authentication:** Secure Email-based Login (JWT).
* **AI Assistants:** "LUCAS" (Academic) and "DANI" (Emotional Support) powered by OpenAI GPT-4o.
* **Adaptive Engine:** A "Nervous System" seeded with **47 Clinical Neuro-Adaptive Rules**.
* **Supported Neuro-Profiles:** The system currently holds logic for **10 specific learner profiles**:
  * Autistic
  * ADHD
  * Dyslexic
  * Dyscalculia
  * Dyspraxia
  * Auditory Processing
  * Gifted / Twice-Exceptional (2e)
  * Anxiety
  * Sensory Processing
  * Executive Function (EF) Support
* **EF Toolkit:** APIs for Pomodoro Timers and Task Chunking.

---

## 🛠️ Tech Stack
* **Language:** Python 3.14
* **Framework:** Django 5.2 + Django REST Framework
* **AI Engine:** OpenAI API (GPT-4o Mini)
* **Database:** SQLite (Dev) / PostgreSQL (Prod)
* **Deployment:** Docker + Google Cloud Run (Ready)

---

## ⚡ Key Features

### 1. The Adaptive Rules Engine
The platform contains a library of **47 Neuro-Adaptive Rules** seeded from clinical data.
* **Trigger:** "Sensory Overload Detected" -> **Action:** `AI_SENSORY_REDUCE` (Dims visuals, lowers audio).
* **Trigger:** "Math Anxiety Detected" -> **Action:** `AI_NO_TIMER` (Removes countdowns).

### 2. Intelligent Chat Assistants
* **LUCAS:** Helps with academic scaffolding (e.g., "Explain fractions using pizza").
* **DANI:** Helps with executive function (e.g., "I'm overwhelmed, break this task down").

### 3. Executive Function (EF) Tools
Built-in tools to support student workflow:
* **Pomodoro Timer API:** Tracks focus intervals.
* **Task Chunking API:** Breaks large assignments into micro-steps.

---

## 💻 Local Setup (For Developers)

**1. Clone the Repository**
```bash
git clone [https://github.com/tjshere/NVLP-Backend.git](https://github.com/tjshere/NVLP-Backend.git)
cd NVLP-Backend