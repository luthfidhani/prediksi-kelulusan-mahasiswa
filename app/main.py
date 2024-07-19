from flask import Flask, render_template, request
from utils import collect_data_from_form, is_smt_valid
from vars import jalur, prodi, jenis_kelamin
from predictor import Predictor
import logging

app = Flask(__name__)
predictor = Predictor()


@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")


@app.route("/predict", methods=["GET", "POST"])
def index():
    data = {
        "vars": {
            "jalur": jalur,
            "prodi": prodi,
            "jenis_kelamin": jenis_kelamin,
        },
        "request": None,
        "prediction": [None],
    }
    if request.method == "POST":
        try:
            form_data = collect_data_from_form(request.form)
        except ValueError as e:
            data["error"] = str(e)
            return render_template("predict.html", data=data)

        data["request"] = form_data.model_dump()
        prediction_response = predictor.predict(form_data)
        data["prediction"] = prediction_response.prediction

        return render_template("predict.html", data=data)
    return render_template("predict.html", data=data)


@app.route("/result", methods=["GET", "POST"])
def result():
    if request.method == "POST":
        try:
            form_data = collect_data_from_form(request.form)
        except ValueError as e:
            data = {
                "vars": {
                    "jalur": jalur,
                    "prodi": prodi,
                    "jenis_kelamin": jenis_kelamin,
                },
                "request": None,
                "prediction": [None],
                "error": str(e),
            }
            return render_template("predict.html", data=data)

        if not is_smt_valid(form_data.prodi_code, form_data.ips):
            data = {
                "vars": {
                    "jalur": jalur,
                    "prodi": prodi,
                    "jenis_kelamin": jenis_kelamin,
                },
                "request": form_data.model_dump(),
                "prediction": [None],
                "error_message": "Nilai semester tidak terpenuhi",
            }
            return render_template("predict.html", data=data)

        prediction_response = predictor.predict(form_data)
        return render_template("result.html", data=prediction_response.model_dump())
    return render_template("result.html", data=None)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
