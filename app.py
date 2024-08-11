from flask import Flask, request, jsonify
from flask_cors import CORS
from query_data import main
import os
from add_to_database import main_add_to_data
app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Ensure the upload directory exists
UPLOAD_FOLDER = 'data'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/query', methods=['POST'])
def query():
    query_text = request.form.get('query')
    file = request.files.get('file')

    # Print debug information
    print(f"Received query: {query_text}")
    if file:
        filename = file.filename
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        print(f"Saving file to: {file_path}")
        main_add_to_data()

        try:
            # Save file
            file.save(file_path)
            print("File saved successfully.")
        except Exception as e:
            print(f"Error saving file: {e}")
            return jsonify({'error': 'Failed to save file'}), 500
    else:
        file_path = None

    try:
        response = main(query_text)
        return jsonify({'response': response})
    except Exception as e:
        print(f"Error processing query: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
