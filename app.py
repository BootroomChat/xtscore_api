from flask import Flask, jsonify, request

from xt_calculator import *
from config import *

app = Flask(__name__)
with app.app_context():
    with open('static/match_stats.csv', "r") as theFile:
        reader = list(csv.DictReader(theFile))


@app.route('/calculator', methods=['POST'])
def calculator():
    if request.args.get('api_key') == api_key:
        return jsonify(calculate(reader))
    else:
        return jsonify({'Error': 'Wrong API KEY'})


if __name__ == '__main__':
    app.run(port=8080)
