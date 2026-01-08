from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import database
import uvicorn
import os

app = FastAPI()

# Enable CORS for Deployments
app.add_middleware(
    CORSMiddleware,
    # Allow all origins for simplicity to support any deployment URL.
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Models
class UserLogin(BaseModel):
    username: str
    password: str

class UserCreate(BaseModel):
    username: str
    password: str
    confirm_password: str

class Note(BaseModel):
    title: str
    content: str
    id: Optional[int] = None

class Message(BaseModel):
    to_user: str
    content: str

class CustomApp(BaseModel):
    app_name: str
    code: str
    is_public: bool = False

# Routes

@app.get("/")
def read_root():
    return {"message": "PyPhone OS Server Running"}

@app.post("/api/login")
def login(user: UserLogin):
    if database.verify_login(user.username, user.password):
        return {"status": "success", "username": user.username}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/api/register")
def register(user: UserCreate):
    if user.password != user.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    if len(user.password) < 1:
        raise HTTPException(status_code=400, detail="Password too short")
    
    if database.create_user(user.username, user.password):
        return {"status": "success", "username": user.username}
    else:
        raise HTTPException(status_code=400, detail="User already exists")

@app.get("/api/notes/{username}")
def get_notes(username: str):
    return database.get_notes(username)

@app.post("/api/notes/{username}")
def save_note(username: str, note: Note):
    database.save_note(username, note.title, note.content, note.id)
    return {"status": "success"}

@app.delete("/api/notes/{username}/{note_id}")
def delete_note(username: str, note_id: int):
    database.delete_note(username, note_id)
    return {"status": "success"}

@app.get("/api/messages/{username}")
def get_messages(username: str):
    return database.get_messages(username)

@app.post("/api/messages/{username}")
def send_message(username: str, message: Message):
    # Note: 'username' here is the sender
    database.send_message(username, message.to_user, message.content)
    return {"status": "success"}

@app.get("/api/apps/{username}")
def get_apps(username: str):
    return database.get_custom_apps(username)

@app.post("/api/apps/{username}")
def save_app(username: str, app: CustomApp):
    database.save_custom_app(username, app.app_name, app.code, app.is_public)
    return {"status": "success"}

if __name__ == "__main__":
    # Use PORT environment variable if available, otherwise 8000
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=True)
