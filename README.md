
# Task Manager System

A simple task manager system built with Flask for the backend, SQLite for the database, and React for the frontend. This system helps manage daily, weekly, and monthly tasks with reminders and daily progress analysis.

## Features
- [x] Create, Read, Update, and Delete tasks
- [ ] Categorize tasks into Daily, Weekly, and Monthly
- [x] Set reminders for tasks with due dates
- [x] Receive daily summaries of pending tasks
- [x] Analyze daily progress

## Technologies Used
- **Backend:** Python, Flask, SQLAlchemy
- **Database:** SQLite
- **Scheduler:** APScheduler
- **Frontend:** React

## Setup Instructions

### Backend Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd task-manager
   ```
2. Create a virtual environment:
   ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows use .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the Flask app:
   ```bash
      python app.py
   ```

## License

This project is licensed under the MIT License.


