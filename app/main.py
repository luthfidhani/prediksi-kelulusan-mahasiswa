import os
import joblib
import pandas as pd
import numpy as np
from flask import Flask, render_template, request
from vars import jalur, prodi, jenis_kelamin

app = Flask(__name__)

model = joblib.load(os.path.join(os.path.dirname(__file__), "model_logistik.pkl"))


def is_smt_valid(prodi_code, ips):
    # cek minimal lama studi
    for _, kode, minimal_studi in prodi:
        if kode == prodi_code:
            if len(ips) < minimal_studi:
                return False

    return True


def predict(n_toefl, ipk, jumlah_semester, prodi_code, jenis_kelamin_code, jalur_code):
    if ipk <= 2:
        return ["Tidak tepat waktu"]
    df = pd.DataFrame(
        {
            "n_toefl": [n_toefl],
            "ipk": [ipk],
            "jumlah_semester": [jumlah_semester],
            "prodi_code": [prodi_code],
            "jenis_kelamin_code": [jenis_kelamin_code],
            "jalur_code": [jalur_code],
        },
    )

    return model.predict(df)


@app.route("/", methods=["GET", "POST"])
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
        asal_sma = request.form["asal_sma"]
        n_toefl = int(request.form["n_toefl"])
        prodi_code = int(request.form["prodi_code"])
        jenis_kelamin_code = int(request.form["jenis_kelamin_code"])
        jalur_code = int(request.form["jalur_code"])

        ips = []
        for i in range(1, 15):
            ip = request.form[f"ip_semester_{i}"]
            if ip:
                ips.append(float(request.form[f"ip_semester_{i}"]))
        ips = np.array(ips, dtype=float)
   
        data["request"] = {
            "asal_sma": asal_sma,
            "n_toefl": n_toefl,
            "ipk": np.mean(ips),
            "jumlah_semester": len(ips),
            "prodi_code": prodi_code,
            "jenis_kelamin_code": jenis_kelamin_code,
            "jalur_code": jalur_code,
            "ips": ips
        },

        data["prediction"] = predict(
            n_toefl=n_toefl,
            ipk=np.mean(ips),
            jumlah_semester=len(ips),
            prodi_code=prodi_code,
            jenis_kelamin_code=jenis_kelamin_code,
            jalur_code=jalur_code,
        )[0]

        return render_template("index.html", data=data)
    return render_template("index.html", data=data)

@app.route("/result", methods=["GET", "POST"])
def result():
    if request.method == "POST":
        asal_sma = request.form["asal_sma"]
        n_toefl = int(request.form["n_toefl"])
        prodi_code = int(request.form["prodi_code"])
        jenis_kelamin_code = int(request.form["jenis_kelamin_code"])
        jalur_code = int(request.form["jalur_code"])

        ips = []
        for i in range(1, 15):
            ip = request.form[f"ip_semester_{i}"]
            if ip:
                ips.append(float(request.form[f"ip_semester_{i}"]))
        ips = np.array(ips, dtype=float)

        if not is_smt_valid(prodi_code, ips):
            data = {
                "vars": {
                    "jalur": jalur,
                    "prodi": prodi,
                    "jenis_kelamin": jenis_kelamin,
                },
                "request": None,
                "prediction": [None],
            }
            data["request"] = {
                "asal_sma": asal_sma,
                "n_toefl": n_toefl,
                "ipk": np.mean(ips),
                "jumlah_semester": len(ips),
                "prodi_code": prodi_code,
                "jenis_kelamin_code": jenis_kelamin_code,
                "jalur_code": jalur_code,
                "ips": ips,
                "error_message": "Nilai semester tidak terpenuhi"
            }

            return render_template("index.html", data=data)

        data = predict(
            n_toefl=n_toefl,
            ipk=np.mean(ips),
            jumlah_semester=len(ips),
            prodi_code=prodi_code,
            jenis_kelamin_code=jenis_kelamin_code,
            jalur_code=jalur_code,
        )[0]

        return render_template("result.html", data=data)
    return render_template("result.html", data=None)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
