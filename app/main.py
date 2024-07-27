import os

from flask import Flask, render_template, request

from utils import data_validation, is_smt_valid, is_file_allowed
from vars import jalur, prodi, jenis_kelamin
from predictor import Predictor

app = Flask(__name__)
predictor = Predictor()

def prepare_data():
    return {
        "vars": {
            "jalur": jalur,
            "prodi": prodi,
            "jenis_kelamin": jenis_kelamin,
        },
        "request": None,
        "prediction": [None],
        "error_message": None
    }

@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")

@app.route("/predict", methods=["GET", "POST"])
def predict():
    data = prepare_data()

    if request.method == "POST":
        try:
            validated_data = data_validation(request.form)
            data["request"] = validated_data.model_dump()
            prediction_response = predictor.predict(validated_data)
            data["prediction"] = prediction_response.prediction
        except ValueError as e:
            data["error_message"] = str(e)

    return render_template("predict.html", data=data)

@app.route("/result", methods=["GET", "POST"])
def result():
    data = prepare_data()

    if request.method == "POST":
        
        if request.files:
            data["prediction_type"] = "batch"
            file = request.files.get("file")
            if file.filename == "":
                data["error_message"] = "No file selected"
                return render_template("predict.html", data=data)
            elif not is_file_allowed(file.filename):
                data["error_message"] = "Filename must be an Excel file (.xlsx or .xls) and the file name must not be 'prediction_result'"
                return render_template("predict.html", data=data)
            else:
                file_path = os.path.join("app/static/temp", file.filename)
                file.save(file_path)
                try:
                    result_file_path = predictor.batch_prediction(file_path)
                except Exception as e:
                    data["error_message"] = str(e)
                    return render_template("predict.html", data=data)
                finally:
                    os.remove(file_path)
                data["prediction"] = result_file_path
            
            return render_template("result.html", data=data)

        else:
            try:
                validated_data = data_validation(request.form)
                if not is_smt_valid(validated_data):
                    data["request"] = validated_data.model_dump()
                    data["error_message"] = "Semester values not met"
                else:
                    prediction_response = predictor.predict(validated_data).model_dump()
                    prediction_response["prediction_type"] = "realtime"
                    return render_template("result.html", data=prediction_response)
            except ValueError as e:
                data["error_message"] = str(e)

    return render_template("predict.html", data=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
