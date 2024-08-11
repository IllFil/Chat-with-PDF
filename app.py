from flask import Flask, request, jsonify
from flask_cors import CORS
from query_data import main as query_main
import os
from add_to_database import main_add_to_data

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'data'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/query', methods=['POST'])
def query():
    query_text = request.form.get('query')
    file = request.files.get('file')

    # Print received query and file information
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
        response = query_main(query_text)
        print(f"Response from query_main: {response}")
        return jsonify({'response': response})
    except Exception as e:
        print(f"Error processing query: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)