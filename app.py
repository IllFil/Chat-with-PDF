from flask import Flask, request, jsonify
from flask_cors import CORS
from query_data import query_rag
import os

app = Flask(__name__)
CORS(app)


@app.route('/query', methods=['POST'])
def query():
    query_text = request.form.get('query')
    file = request.files.get('file')

    # Print debug information
    print(f"Received query: {query_text}")
    if file:
        print(f"Received file: {file.filename}")
        file_path = os.path.join("data", file.filename)
        print(f"Saving file to: {file_path}")

        try:
            file.save(file_path)
            print("File saved successfully.")
        except Exception as e:
            print(f"Error saving file: {e}")
            return jsonify({'error': 'Failed to save file'}), 500
    else:
        file_path = None

    try:
        response = query_rag(query_text, file_path)
        return jsonify({'response': response})
    except Exception as e:
        print(f"Error processing query: {e}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
