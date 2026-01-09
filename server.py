from fastapi import FastAPI, HTTPException, Depends, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
import database
import uvicorn
import os
import shutil
import random
import google.generativeai as genai

# Configure Gemini if API Key exists
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

app = FastAPI()

# Create uploads dir if not exists
UPLOADS_DIR = "uploads"
if not os.path.exists(UPLOADS_DIR):
    os.makedirs(UPLOADS_DIR)

app.mount("/uploads", StaticFiles(directory=UPLOADS_DIR), name="uploads")

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
    attachment_url: Optional[str] = None
    attachment_type: Optional[str] = None

class CustomApp(BaseModel):
    app_name: str
    code: str
    is_public: bool = False

# Routes

@app.get("/")
def read_root():
    return {"message": "PyPhone OS Server Running"}

@app.head("/")
def read_root_head():
    return {}

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
    database.send_message(
        username, 
        message.to_user, 
        message.content, 
        message.attachment_url, 
        message.attachment_type
    )
    return {"status": "success"}

# Ensure Admin exists
if not database.get_user("admin"):
    database.create_user("admin", "1000011", is_admin=True)

@app.get("/api/search/{query}")
def search_users(query: str):
    users = database._load_json(database.USERS_FILE)
    results = [u for u in users.keys() if query.lower() in u.lower() and u != "admin"]
    return results[:10]

@app.get("/api/friends/{username}")
def get_friends(username: str):
    user_data = database.get_user(username)
    if not user_data: return []
    return {
        "friends": user_data.get("friends", []),
        "received": user_data.get("requests_received", []),
        "sent": user_data.get("requests_sent", [])
    }

@app.patch("/api/users/{username}/settings")
def set_user_settings(username: str, settings: dict):
    success = database.update_settings(username, settings)
    if success:
        return {"status": "success"}
    else:
        raise HTTPException(status_code=404, detail="User not found")

@app.post("/api/friends/request")
def send_friend_request(req: dict):
    # expect { "from": "...", "to": "..." }
    success = database.send_friend_request(req['from'], req['to'])
    return {"status": "success" if success else "failed"}

@app.post("/api/friends/accept")
def accept_friend_request(req: dict):
    # expect { "user": "...", "friend": "..." }
    success = database.accept_friend_request(req['user'], req['friend'])
    return {"status": "success" if success else "failed"}

@app.post("/api/friends/remove")
def remove_friend(req: dict):
    # expect { "user": "...", "friend": "..." }
    success = database.remove_friend(req['user'], req['friend'])
    return {"status": "success" if success else "failed"}

@app.get("/api/admin/stats")
def get_admin_stats():
    users = database._load_json(database.USERS_FILE)
    messages = database._load_json(database.MESSAGES_FILE)
    
    total_messages = 0
    for user_msgs in messages.values():
        total_messages += len(user_msgs)
        
    return {
        "total_users": len(users),
        "total_messages": total_messages,
        "users_list": list(users.keys())
    }

@app.get("/api/admin/feedback")
def get_all_feedback():
    return database.get_feedback()

@app.post("/api/feedback")
def submit_user_feedback(req: dict):
    # expect { "username": "...", "content": "..." }
    database.send_feedback(req['username'], req['content'])
    return {"status": "success"}

@app.delete("/api/admin/feedback/{fb_id}")
def delete_feedback(fb_id: int):
    database.delete_feedback(fb_id)
    return {"status": "success"}

@app.get("/api/admin/users")
def get_users_list():
    return database.get_all_users()

@app.delete("/api/admin/users/{username}")
def delete_user(username: str):
    success = database.delete_user(username)
    return {"status": "success" if success else "failed"}

@app.get("/api/admin/apps")
def get_all_apps_for_moderation():
    # Admins see everything
    return database.get_all_custom_apps()

@app.get("/api/apps/public")
def get_public_app_store():
    return database.get_public_apps()

@app.get("/api/apps/{username}")
def get_user_personalized_apps(username: str):
    return database.get_user_apps(username)

@app.post("/api/admin/apps/visibility")
def set_app_visibility(req: dict):
    # expect { "owner": "...", "app_name": "...", "is_public": bool }
    success = database.set_app_visibility(req['owner'], req['app_name'], req['is_public'])
    return {"status": "success" if success else "failed"}

@app.post("/api/apps/{username}")
def save_app(username: str, app: CustomApp):
    database.save_custom_app(username, app.app_name, app.code, app.is_public)
    return {"status": "success"}

@app.delete("/api/apps/{username}/{app_name}")
def delete_app(username: str, app_name: str):
    success = database.delete_custom_app(username, app_name)
    return {"status": "success" if success else "failed"}

# --- NEW AI & MULTIMEDIA ENDPOINTS ---

class AIChat(BaseModel):
    message: str
    context: Optional[str] = None

@app.get("/api/ai/status")
def get_ai_status():
    return {
        "configured": GEMINI_API_KEY is not None,
        "mode": "production" if GEMINI_API_KEY else "simulation"
    }

@app.post("/api/ai/nexus")
def nexus_ai_chat(chat: AIChat):
    if not GEMINI_API_KEY:
        # Fallback to simulation
        responses = [
            "Analyzing kernel data...",
            "Interesting query. Here's what I found in the system logs.",
            "Your request has been processed. Powering up neural links.",
            "I'm sorry, I cannot perform that action outside of sandbox mode.",
            "System stability is at 99.8%. How can I assist further?",
            "Searching local databases for relevant information."
        ]
        return {"response": f"{random.choice(responses)}\n\nYou said: '{chat.message}'"}
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        system_instr = "You are Nexus AI, the core intelligence of the PyPhone Web OS. You are futuristic, concise, and helpful. You reside within a simulated operating system."
        response = model.generate_content(f"{system_instr}\n\nUser: {chat.message}")
        return {"response": response.text}
    except Exception as e:
        return {"response": f"AI Error: {str(e)}. Reverting to local buffers."}

@app.post("/api/ai/studio")
def studio_ai_assistant(chat: AIChat):
    if not GEMINI_API_KEY:
        # Fallback to simulation
        lang_info = ""
        if chat.context and "[LANG:" in chat.context:
            lang_info = f"I see you're writing in {chat.context.split(']')[0][6:]}."
        
        return {
            "response": f"{lang_info}\nBased on your request '{chat.message}', I suggest checking your loops and ensuring all imports are correct. I've optimized your logic buffers."
        }
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        system_instr = f"You are the Dev Studio AI Assistant. You help users write and debug code within the PyPhone Web OS. Context: {chat.context}"
        response = model.generate_content(f"{system_instr}\n\nUser: {chat.message}")
        return {"response": response.text}
    except Exception as e:
        return {"response": f"Code Assistant Error: {str(e)}"}

@app.post("/api/upload/{username}")
async def upload_file(username: str, file: UploadFile = File(...)):
    # 10MB Limit Enforcement
    MAX_SIZE = 10 * 1024 * 1024 # 10MB
    
    # Read a chunk to check size (fast for large files)
    contents = await file.read(MAX_SIZE + 1)
    if len(contents) > MAX_SIZE:
        raise HTTPException(status_code=413, detail="File too large (Max 10MB)")
    
    # Reset seek for saving
    await file.seek(0)
    
    # Simple file saving
    filename = f"{username}_{random.randint(1000, 9999)}_{file.filename}"
    file_path = os.path.join(UPLOADS_DIR, filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    return {
        "url": f"/uploads/{filename}",
        "type": file.content_type,
        "name": file.filename
    }

if __name__ == "__main__":
    # Use PORT environment variable if available, otherwise 8000
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=True)