from flask import Flask, request, jsonify
from flask_cors import CORS
from query_data import query_rag

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

@app.route('/query', methods=['POST'])
def query():
    data = request.get_json()
    query_text = data.get('query')
    if not query_text:
        return jsonify({'error': 'Query text is required'}), 400
    try:
        response = query_rag(query_text)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
