import json
import os
import hashlib
from datetime import datetime

DATA_DIR = "data"
USERS_FILE = os.path.join(DATA_DIR, "users.json")
NOTES_FILE = os.path.join(DATA_DIR, "notes.json")
MESSAGES_FILE = os.path.join(DATA_DIR, "messages.json")
FEEDBACK_FILE = os.path.join(DATA_DIR, "feedback.json")
APPS_FILE = os.path.join(DATA_DIR, "custom_apps.json")

def _init_db():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    for f in [USERS_FILE, NOTES_FILE, MESSAGES_FILE, FEEDBACK_FILE, APPS_FILE]:
        if not os.path.exists(f):
            with open(f, 'w') as fp:
                json.dump({}, fp) # Default empty dict or list

def _load_json(filepath):
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def _save_json(filepath, data):
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# User Operations
def get_user(username):
    users = _load_json(USERS_FILE)
    return users.get(username)

def create_user(username, password, is_admin=False):
    users = _load_json(USERS_FILE)
    if username in users:
        return False
    users[username] = {
        "password": hash_password(password),
        "is_admin": is_admin,
        "friends": [],
        "requests_sent": [],
        "requests_received": [],
        "settings": {"clock_24h": True, "wallpaper": "neural"}
    }
    _save_json(USERS_FILE, users)
    return True

def verify_login(username, password):
    user = get_user(username)
    if user and user['password'] == hash_password(password):
        return True
    return False

def get_friends(username):
    user = get_user(username)
    return user.get("friends", []) if user else []

def send_friend_request(from_user, to_user):
    users = _load_json(USERS_FILE)
    if to_user not in users or  to_user == from_user:
        return False
    if to_user in users[from_user]['friends']:
        return False # Already friends
    
    if from_user not in users[to_user]['requests_received']:
        users[to_user]['requests_received'].append(from_user)
        users[from_user]['requests_sent'].append(to_user)
        _save_json(USERS_FILE, users)
    return True

def accept_friend_request(user, friend_to_accept):
    users = _load_json(USERS_FILE)
    if friend_to_accept in users[user]['requests_received']:
        users[user]['requests_received'].remove(friend_to_accept)
        users[user]['friends'].append(friend_to_accept)
        
        users[friend_to_accept]['requests_sent'].remove(user)
        users[friend_to_accept]['friends'].append(user)
        _save_json(USERS_FILE, users)
        return True
    return False

def remove_friend(user, friend):
    users = _load_json(USERS_FILE)
    if friend in users[user]['friends']:
        users[user]['friends'].remove(friend)
        users[friend]['friends'].remove(user)
        _save_json(USERS_FILE, users)
        return True
    return False

# Notes Operations
def get_notes(username):
    all_notes = _load_json(NOTES_FILE)
    return all_notes.get(username, [])

def save_note(username, title, content, note_id=None):
    all_notes = _load_json(NOTES_FILE)
    user_notes = all_notes.get(username, [])
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if note_id is not None:
        # Edit existing
        for note in user_notes:
            if note['id'] == note_id:
                note['title'] = title
                note['content'] = content
                note['timestamp'] = timestamp
                break
    else:
        # Create new
        new_id = len(user_notes) + 1 # Simple ID generation
        if user_notes:
             new_id = max(n['id'] for n in user_notes) + 1
             
        user_notes.append({
            "id": new_id,
            "title": title,
            "content": content,
            "timestamp": timestamp
        })
    
    all_notes[username] = user_notes
    _save_json(NOTES_FILE, all_notes)

def delete_note(username, note_id):
    all_notes = _load_json(NOTES_FILE)
    if username in all_notes:
        all_notes[username] = [n for n in all_notes[username] if n['id'] != note_id]
        _save_json(NOTES_FILE, all_notes)

# Message Operations
def get_messages(username):
    all_msgs = _load_json(MESSAGES_FILE)
    return all_msgs.get(username, [])

def send_message(from_user, to_user, content, attachment_url=None, attachment_type=None):
    all_msgs = _load_json(MESSAGES_FILE)
    
    msg_obj = {
        "from": from_user,
        "to": to_user,
        "content": content,
        "attachment_url": attachment_url,
        "attachment_type": attachment_type,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # 1. Save to Receiver's Inbox
    receiver_msgs = all_msgs.get(to_user, [])
    receiver_msgs.append(msg_obj)
    all_msgs[to_user] = receiver_msgs
    
    # 2. Save to Sender's Outbox (if different)
    if from_user != to_user:
        sender_msgs = all_msgs.get(from_user, [])
        sender_msgs.append(msg_obj)
        all_msgs[from_user] = sender_msgs
        
    _save_json(MESSAGES_FILE, all_msgs)

# User Operations
def get_all_users():
    users = _load_json(USERS_FILE)
    return [{"username": u, "is_admin": d.get("is_admin", False)} for u, d in users.items()]

def delete_user(username):
    if username == "admin": return False # Protect admin
    
    # 1. Delete user entry
    users = _load_json(USERS_FILE)
    if username in users:
        del users[username]
        _save_json(USERS_FILE, users)
    
    # 2. Delete notes
    notes = _load_json(NOTES_FILE)
    if username in notes:
        del notes[username]
        _save_json(NOTES_FILE, notes)
        
    # 3. Clean up messages (optional: delete messages *to* this user)
    msgs = _load_json(MESSAGES_FILE)
    if username in msgs:
        del msgs[username]
        _save_json(MESSAGES_FILE, msgs)
        
    # 4. Cleanup apps
    apps = _load_json(APPS_FILE)
    if username in apps:
        del apps[username]
        _save_json(APPS_FILE, apps)
        
    return True

# ... existing code ...

# Feedback
def send_feedback(username, content):
    feedbacks = _load_json(FEEDBACK_FILE)
    if not isinstance(feedbacks, list): feedbacks = [] 
    feedbacks.append({
        "id": len(feedbacks) + 1,
        "user": username,
        "content": content,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "pending"
    })
    _save_json(FEEDBACK_FILE, feedbacks)

def get_feedback():
    feedbacks = _load_json(FEEDBACK_FILE)
    if not isinstance(feedbacks, list): return []
    return feedbacks

def delete_feedback(feedback_id):
    feedbacks = _load_json(FEEDBACK_FILE)
    if not isinstance(feedbacks, list): return
    feedbacks = [f for f in feedbacks if f.get('id') != feedback_id]
    _save_json(FEEDBACK_FILE, feedbacks)

# Custom Apps Oversight
def get_all_custom_apps():
    # Returns all apps across all users
    all_users_apps = _load_json(APPS_FILE)
    results = []
    for username, apps in all_users_apps.items():
        for app in apps:
            results.append({**app, "owner": username})
    return results

def set_app_visibility(owner, app_name, is_public):
    apps = _load_json(APPS_FILE)
    if owner in apps:
        for app in apps[owner]:
            if app['name'] == app_name:
                app['is_public'] = is_public
                break
        _save_json(APPS_FILE, apps)
        return True
    return False

# Initialize
_init_db()
