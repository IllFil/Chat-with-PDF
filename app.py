from flask import Flask, request, jsonify, session
from flask_cors import CORS
from llm_core import main as query_main
import os
from add_to_database import main_add_to_data, clear_database
import uuid
import sqlite3
from datetime import datetime
from langchain_core.messages import HumanMessage, AIMessage
from uuid import uuid4
app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = os.urandom(24)

CORS(app, supports_credentials=True)

UPLOAD_FOLDER = 'data'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
@app.before_request
def set_session_id():
    # Generate a session ID if one doesn't exist
    if 'session_id' not in session:
        session['session_id'] = str(uuid4())
        session['history'] = []  # Initialize chat history in the session

def get_db_connection():
    conn = sqlite3.connect('instance/chat_history.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS chat_history
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     session_id TEXT,
                     timestamp DATETIME,
                     role TEXT,
                     content TEXT)''')
    conn.close()

def get_chat_history(session_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT role, content FROM chat_history WHERE session_id = ? ORDER BY timestamp", (session_id,))
    rows = cursor.fetchall()
    conn.close()

    chat_history = []
    print(f"Retrieved {len(rows)} messages from database for session {session_id}")
    for row in rows:
        if row['role'] == 'human':
            chat_history.append(HumanMessage(content=row['content']))
        elif row['role'] == 'ai':
            chat_history.append(AIMessage(content=row['content']))
    print(f"Constructed chat history: {chat_history}")
    return chat_history

def save_chat_history(session_id, messages):
    conn = get_db_connection()
    cursor = conn.cursor()
    for message in messages:
        role = 'human' if isinstance(message, HumanMessage) else 'ai'
        cursor.execute("INSERT INTO chat_history (session_id, timestamp, role, content) VALUES (?, ?, ?, ?)",
                       (session_id, datetime.now(), role, message.content))
    conn.commit()
    conn.close()
    print(f"Saved {len(messages)} messages to database for session {session_id}")


init_db()


@app.route('/query', methods=['POST'])
def query():
    query_text = request.form.get('query')
    file = request.files.get('file')

    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())

    session_id = session['session_id']
    print(f"Session ID: {session_id}")

    chat_history = get_chat_history(session_id)
    print(f"Retrieved chat history: {chat_history}")

    print(f"Received query: {query_text}")
    if file:
        filename = file.filename
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        print(f"Saving file to: {file_path}")

        try:
            # Save file
            file.save(file_path)
            print("File saved successfully.")

            # Process the file
            main_add_to_data()
            print("File processed and added to the database.")
        except Exception as e:
            print(f"Error saving or processing file: {e}")
            return jsonify({'error': 'Failed to save or process file'}), 500
    else:
        file_path = None
    try:
        response, updated_chat_history = query_main(query_text, chat_history)
        print(f"Response from query_main: {response}")
        print(f"Updated chat history: {updated_chat_history}")

        # Save only the new messages
        new_messages = updated_chat_history[len(chat_history):]
        save_chat_history(session_id, new_messages)

        return jsonify({'response': response})
    except Exception as e:
        print(f"Error processing query: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/chat_history', methods=['GET'])
def get_chat_history_route():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())

    history = get_chat_history(session['session_id'])
    return jsonify({'history': [{'query': msg.content, 'response': history[i + 1].content}
                                for i, msg in enumerate(history[::2])]})


@app.route('/clear_history', methods=['POST'])
def clear_history():
    if 'session_id' in session:
        clear_chat_history(session['session_id'])
    return jsonify({'message': 'Chat history cleared successfully'})

@app.route('/check_db', methods=['GET'])
def check_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM chat_history")
    rows = cursor.fetchall()
    conn.close()
    return jsonify({'db_contents': [dict(row) for row in rows]})

def clear_chat_history(session_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM chat_history WHERE session_id = ?", (session_id,))
    conn.commit()
    conn.close()


if __name__ == '__main__':
    app.run(debug=True)