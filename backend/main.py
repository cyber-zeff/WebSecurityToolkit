
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

# Encryption/Decryption route
from typing import Optional

class CipherInput(BaseModel):
    text: str
    key: Optional[str] = None
    shift: Optional[int] = None
    algorithm: str # "caesar" or "vigenere"
    mode: str # "encrypt" or "decrypt"

def caesar_cipher(text, shift, mode):
    result = ""
    if mode == "decrypt":
        shift = -shift
    
    for char in text:
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - start + shift) % 26 + start)
        else:
            result += char
    return result

def vigenere_cipher(text, key, mode):
    result = ""
    key_index = 0
    key = key.upper()
    
    for char in text:
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - ord('A')
            if mode == "decrypt":
                shift = -shift
            
            start = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - start + shift) % 26 + start)
            key_index += 1
        else:
            result += char
    return result

@app.post("/cipher")
def cipher_tool(data: CipherInput):
    if data.algorithm.lower() == "caesar":
        if data.shift is None:
            return {"error": "Shift is required for Caesar cipher"}
        return {"result": caesar_cipher(data.text, data.shift, data.mode)}
    
    elif data.algorithm.lower() == "vigenere":
        if not data.key:
            return {"error": "Key is required for Vigenere cipher"}
        return {"result": vigenere_cipher(data.text, data.key, data.mode)}
    
    return {"error": "Invalid algorithm"}
