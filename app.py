import csv
import json

from flask import Flask, Response, request

from config import *
from xt_calculator import *

app = Flask(__name__)
with app.app_context():
    with open('static/match_stats.csv', "r") as theFile:
        reader = list(csv.DictReader(theFile))


@app.route('/calculator', methods=['POST'])
def calculator():
    if request.args.get('api_key') == api_key:
        return Response(json.dumps(calculate(reader, calculator_config=request.get_json())),
                        content_type='application/json; charset=utf-8')
    else:
        return Response({'Error': 'Wrong API KEY'}, content_type='application/json; charset=utf-8')


if __name__ == '__main__':
    app.run(port=8080)
