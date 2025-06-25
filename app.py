from flask import Flask, render_template, request
from fuzzy_model import evaluar_calidad_cafe

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None

    if request.method == "POST":
        acidez = float(request.form["acidez"])
        cafeina = float(request.form["cafeina"])
        humedad = float(request.form["humedad"])
        aroma = float(request.form["aroma"])

        calidad, categoria = evaluar_calidad_cafe(acidez, cafeina, humedad, aroma)
        resultado = {
            "calidad": calidad,
            "categoria": categoria
        }

    return render_template("index.html", resultado=resultado)

if __name__ == "__main__":
    app.run(debug=True)
