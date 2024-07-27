from vars import prodi_dict
from models import PredictionRequest


def data_validation(request_form):
    data = {
        "asal_sma": request_form["asal_sma"],
        "toefl": int(request_form["toefl"]),
        "penghasilan_orang_tua": int(request_form["penghasilan_orang_tua"]),
        "prodi": request_form["prodi"],
        "jenis_kelamin": request_form["jenis_kelamin"],
        "jalur_masuk": request_form["jalur"],
        "ip_semester_1": float(request_form["ip_semester_1"] if request_form["ip_semester_1"] != "" else 0.0),
        "ip_semester_2": float(request_form["ip_semester_2"] if request_form["ip_semester_2"] != "" else 0.0),
        "ip_semester_3": float(request_form["ip_semester_3"] if request_form["ip_semester_3"] != "" else 0.0),
        "ip_semester_4": float(request_form["ip_semester_4"] if request_form["ip_semester_4"] != "" else 0.0),
        "ip_semester_5": float(request_form["ip_semester_5"] if request_form["ip_semester_5"] != "" else 0.0),
        "ip_semester_6": float(request_form["ip_semester_6"] if request_form["ip_semester_6"] != "" else 0.0),
        "ip_semester_7": float(request_form["ip_semester_7"] if request_form["ip_semester_7"] != "" else 0.0),
        "ip_semester_8": float(request_form["ip_semester_8"] if request_form["ip_semester_8"] != "" else 0.0),
        "ip_semester_9": float(request_form["ip_semester_9"] if request_form["ip_semester_9"] != "" else 0.0),
        "ip_semester_10": float(request_form["ip_semester_10"] if request_form["ip_semester_10"] != "" else 0.0),
        "ip_semester_11": float(request_form["ip_semester_11"] if request_form["ip_semester_11"] != "" else 0.0),
        "ip_semester_12": float(request_form["ip_semester_12"] if request_form["ip_semester_12"] != "" else 0.0),
        "ip_semester_13": float(request_form["ip_semester_13"] if request_form["ip_semester_13"] != "" else 0.0),
        "ip_semester_14": float(request_form["ip_semester_14"] if request_form["ip_semester_14"] != "" else 0.0),
    }
    return PredictionRequest(**data)


def is_smt_valid(data):
    return True if data.jumlah_semester >= prodi_dict[data.prodi]["minimum_semester"] else False


def is_file_allowed(filename):
    return (
        True
        if "prediction_result.xlsx" not in filename.lower()
        and filename.lower().endswith((".xlsx", ".xls"))
        else False
    )
