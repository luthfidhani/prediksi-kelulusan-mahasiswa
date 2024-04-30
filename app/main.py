import os
import joblib
import pandas as pd
from flask import Flask, render_template, request


app = Flask(__name__)

model = joblib.load(os.path.join(os.path.dirname(__file__), "model_logistik.pkl"))


def predict(jumlah_semester, jenjang):
    df = pd.DataFrame({"Jumlah_Semester": [jumlah_semester], "jenjang": [jenjang]})
    return model.predict(df)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        jumlah_semester = int(request.form["jumlah_semester"])
        jenjang = request.form["jenjang"]

        data = {
            "jumlah_semester": jumlah_semester,
            "jenjang": jenjang,
            "prediction": predict(jumlah_semester, jenjang)[0],
        }

        return render_template("index.html", data=data)
    return render_template("index.html", data=None)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
