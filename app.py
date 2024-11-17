from flask import Flask, request, jsonify
from supabase import create_client, Client
from datetime import datetime, timezone
from flask_cors import CORS
from flask import Flask, request, jsonify
from scripts.openai_llm import query_llm

# Flask App Initialization
app = Flask(__name__)
CORS(app)

# Supabase Configuration
SUPABASE_URL = "https://yrkwqczomqvparsfkbeg.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlya3dxY3pvbXF2cGFyc2ZrYmVnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzE4MDA1MDYsImV4cCI6MjA0NzM3NjUwNn0.wZdLE9_mP7xYZKlk956b14ZUJ1opTAFCmqkV0h3vBRI"

# Initialize Supabase Client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/api/data', methods=['GET'])
def fetch_data():
    """Fetch all data from the Supabase table."""
    try:
        response = supabase.table("dictionary_json").select("*").execute()
        data = response.data

        # Format timestamps
        for i in range(len(data)):
            dt_obj = datetime.fromisoformat(data[i]["created_at"])
            data[i]["created_at"] = dt_obj.strftime("%B %d, %Y %I:%M %p")
            if data[i]["updated_at"] is not None:
                dt_obj = datetime.fromisoformat(data[i]["updated_at"])
                data[i]["updated_at"] = dt_obj.strftime("%B %d, %Y %I:%M %p")

        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/data', methods=['POST'])
def create_or_update_data():
    """Insert or update data based on action type."""
    try:
        payload = request.json
        key = payload.get("key")
        value = payload.get("value", "")
        action = payload.get("action")

        if not key or not action:
            return jsonify({"error": "Key and action are required"}), 400

        all_keys = set(i['key'] for i in supabase.table("dictionary_json").select("key").execute().data)

        if action == "insert":
            if key in all_keys:
                return update_data({"key": key, "value": value})
            return insert_data({"key": key, "value": value})
        elif action == "update":
            if key not in all_keys:
                return jsonify({"error": "Key not found for update"}), 404
            return update_data({"key": key, "value": value})
        elif action == "delete":
            if key not in all_keys:
                return jsonify({"error": "Key not found for deletion"}), 404
            return delete_data(key)

        return jsonify({"error": "Invalid action"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/api/query_llm', methods=['POST'])
def handle_llm_query():
    try:
        data = request.json
        user_input = data.get("user_input", "")
        if not user_input:
            return jsonify({"error": "User input is required"}), 400

        # Call the LLM parsing function
        response = query_llm(user_input)

        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    


def insert_data(data):
    """Insert new record."""
    try:
        created_at = datetime.now(timezone.utc).isoformat()
        response = supabase.table("dictionary_json").insert({
            "key": data['key'],
            "value": data['value'],
            "created_at": created_at,
            "updated_at": None
        }).execute()
        return jsonify({"message": "insert", "data": response.data}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def update_data(data):
    """Update existing record."""
    try:
        updated_at = datetime.now(timezone.utc).isoformat()
        response = supabase.table("dictionary_json").update({
            "value": data["value"],
            "updated_at": updated_at
        }).eq("key", data["key"]).execute()
        return jsonify({"message": "update", "data": response.data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def delete_data(key):
    """Delete record."""
    try:
        response = supabase.table("dictionary_json").delete().eq("key", key).execute()
        return jsonify({"message": "delete"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)