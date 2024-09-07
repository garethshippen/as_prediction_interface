from flask import Flask, render_template, request
from model import predict

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():
    name = request.form.get("name")
    age = float(clean(request.form.get("age")))
    sex = float(request.form.get("sex"))
    ethnicity = request.form.get("ethnicity")
    height = float(clean(request.form.get("height")))
    weight = float(clean(request.form.get("weight")))
    sbp = float(clean(request.form.get("sbp")))
    dbp = float(clean(request.form.get("dbp")))
    egfr = float(clean(request.form.get("egfr")))
    mcv = float(clean(request.form.get("mcv")))
    chol = float(clean(request.form.get("chol")))
    trig = float(clean(request.form.get("trig")))
    hdl = float(clean(request.form.get("hdl")))
    ldl = float(clean(request.form.get("ldl")))
    hcl = float(request.form.get("hcl"))
    cvd = float(request.form.get("cvd"))
    asthma = float(request.form.get("asthma"))
    hf = float(request.form.get("hf"))
    af = float(request.form.get("af"))
    ob = float(request.form.get("ob"))
    mi = float(request.form.get("mi"))

    diag = predict(age, sex, ethnicity, height, weight, sbp,
                dbp, egfr, mcv, chol, trig,
                hdl, ldl, hcl, cvd, asthma, hf, af, ob, mi)

    if diag == 1:
        diagnosis = "severe"
    else:
        diagnosis = "moderate"

    if name == "":
        name = "Patient"

    return render_template("diagnosis.html", diagnosis = diagnosis, name = name)

def clean(x):
    return x if x != "" else 0