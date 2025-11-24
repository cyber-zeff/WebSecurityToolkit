
Web Security Toolkit
====================

A combined SQL Injection Detector + Password Strength Checker
built using:
- FastAPI (backend)
- PyQt5 (GUI frontend)
- Python 3.10+

RUN INSTRUCTIONS
----------------

1. Install dependencies:
   pip install fastapi uvicorn requests PyQt5

2. Run backend server:
   cd backend
   uvicorn main:app --reload

3. Run GUI (open another terminal for gui):
   cd gui
   python app.py

Enjoy!
