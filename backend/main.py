
from fastapi import FastAPI
from pydantic import BaseModel
import re

app = FastAPI()

# SQLi detection route
class SQLInput(BaseModel):
    text: str

@app.post("/detect_sqli")
def detect_sqli(data: SQLInput):
    patterns = [
        r"(--|#|;)",              # comment operators
        r"(\bOR\b|\bAND\b)",  # logical operators
        r"'[^']*'|\"[^\"]*\"",       # quotes
        r"(UNION|SELECT|INSERT|DELETE|DROP|UPDATE)"  # keywords
    ]
    for p in patterns:
        if re.search(p, data.text, re.IGNORECASE):
            return {"vulnerable": True, "pattern": p}
    return {"vulnerable": False}

# Password strength route
class PasswordModel(BaseModel):
    password: str

@app.post("/check_password")
def check_password(data: PasswordModel):
    pwd = data.password
    score = 0
    if len(pwd) >= 8: score += 1
    if re.search(r"[A-Z]", pwd): score += 1
    if re.search(r"[a-z]", pwd): score += 1
    if re.search(r"[0-9]", pwd): score += 1
    if re.search(r"[^A-Za-z0-9]", pwd): score += 1

    levels = {1:"Very Weak",2:"Weak",3:"Medium",4:"Strong",5:"Very Strong"}
    return {"strength": levels.get(score, "Very Weak"), "score": score}
