# Author: Dakota Farrstrom
# Date: 08/19/2023
import pandas as pd
import requests
from flask import Flask, request, render_template

from identify import identify, main, createDF

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def form():
    if request.method == "POST":
        bs = request.form.get("bs")
        tw = request.form.get("tw")
        bsw = request.form.get("bsw")
        ca = request.form.get("ca")
        f = request.form.get("f")
        BodyStyle, TopWood, BackSideWood, Cutaway, Finish = int(bs), int(tw), int(bsw), int(ca), int(f)
        userSet = createDF(BodyStyle, TopWood, BackSideWood, Cutaway, Finish)
        message = identify(userSet)
        return message
    return render_template('form.html')


if __name__ == '__main__':
    app.run()
