from flask import Flask, jsonify
from xt_calculator import *

app = Flask(__name__)
with app.app_context():
    with open('{}/static/match_stats.csv'.format(app.config['PROJECT_ROOT']), "r") as theFile:
        reader = csv.DictReader(theFile)


@app.route('/calculator', methods=['POST'])
def calculator():
    return jsonify(calculate(reader))


if __name__ == '__main__':
    app.run()
