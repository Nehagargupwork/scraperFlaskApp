from flask import Flask, request, jsonify
from flaskScraper import get_keyword_rank_and_volume

app = Flask(__name__)

# Route for the homepage
@app.route('/')
def home():
    return "Hello, World!"

# Route to get rank
@app.route('/rank', methods=['GET'])
def rank():
    try:
        keyword = request.args.get('keyword')
        domain = request.args.get('domain')
        region = request.args.get('region', 'in')  # Default to 'in' if not provided

        if not keyword or not domain:
            return jsonify({'statusCode': 400, 'message': 'Keyword and domain are required'}), 400

        rank = get_keyword_rank_and_volume(keyword, domain, region)
        if rank is None:
            return jsonify({'statusCode': 500, 'message': 'Error occurred while fetching rank'}), 500

        return jsonify({'statusCode': 200, 'rank': rank})

    except Exception as e:
        return jsonify({'statusCode': 500, 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
