#!/usr/bin/env python3
# encoding: utf-8
import lunchbot

from flask import Flask
app = Flask(__name__)


@app.route("/")
def index():
    return "Lunchbot running!"


@app.route("/lunch")
def get_lunch():
    lunchbot.main()
    return "", 204


if __name__ == "__main__":
    app.run()
