from flask import Flask


app = Flask(__name__)


def debug():
  app.run(debug=True, host='0.0.0.0', port=52000)
