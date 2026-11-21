from decimal import Decimal, InvalidOperation
from uuid import uuid4

from flask import Flask, abort, redirect, render_template, request, url_for

app = Flask(__name__)

resultados = {}

def guardar_resultado(**datos):
    codigo = uuid4().hex
    resultados[codigo] = datos
    return redirect(url_for("ver_resultado", codigo=codigo), code=303)

@app.route("/resultado/<codigo>")
def ver_resultado(codigo):
    datos = resultados.get(codigo)

    if datos is None:
        abort(404, description="Este resultado no está disponible.")

    return render_template("resultado.html", **datos)

@app.route("/")
def inicio():
    return render_template("inicio.html")


def leer_numero(campo, minimo, maximo):
    try:
        valor = Decimal(request.form.get(campo, ""))
    except InvalidOperation:
        abort(400, description=f"Ingresa un número en el campo {campo}.")

    if not valor.is_finite() or not minimo <= valor <= maximo:
        abort(400, description=f"{campo} debe estar entre {minimo} y {maximo}.")

    return valor

@app.route("/ejercicio1", methods=["GET", "POST"])
def ejercicio1():
    if request.method == "GET":
        return render_template("ejercicio1.html")

    nota1 = leer_numero("nota1", 10, 70)
    nota2 = leer_numero("nota2", 10, 70)
    nota3 = leer_numero("nota3", 10, 70)
    asistencia = leer_numero("asistencia", 0, 100)

    promedio = (nota1 + nota2 + nota3) / 3

    if promedio >= 40 and asistencia >= 75:
        estado = "APROBADO"
    else:
        estado = "REPROBADO"

    return guardar_resultado(
        formulario="ejercicio1.html",
        detalles={"Promedio": f"{promedio:.2f}", "Estado": estado},
        nota1=nota1,
        nota2=nota2,
        nota3=nota3,
        asistencia=asistencia,
    )

@app.route("/ejercicio2", methods=["GET", "POST"])
def ejercicio2():
    if request.method == "GET":
        return render_template("ejercicio2.html")

    nombre1 = request.form.get("nombre1", "").strip()
    nombre2 = request.form.get("nombre2", "").strip()
    nombre3 = request.form.get("nombre3", "").strip()
    nombres = [nombre1, nombre2, nombre3]

    nombres_distintos = {nombre.casefold() for nombre in nombres}

    if "" in nombres:
        detalles = {"Aviso": "Completa los tres nombres."}
    elif len(nombres_distintos) < 3:
        detalles = {"Aviso": "Los tres nombres deben ser diferentes."}
    else:
        cantidad = max(len(nombre) for nombre in nombres)
        mas_largos = [nombre for nombre in nombres if len(nombre) == cantidad]

        etiqueta = "Nombre con más caracteres"
        if len(mas_largos) > 1:
            etiqueta = "Nombres empatados"

        detalles = {
            etiqueta: ", ".join(mas_largos),
            "Cantidad de caracteres": cantidad,
        }

    return guardar_resultado(
        formulario="ejercicio2.html",
        detalles=detalles,
        nombre1=nombre1,
        nombre2=nombre2,
        nombre3=nombre3,
    )

if __name__ == "__main__":
    app.run()