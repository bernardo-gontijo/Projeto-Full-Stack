from flask import Flask, request, jsonify, send_file
import pandas as pd

app = Flask(__name__)
CSV_PATH = "dados.csv"
df = pd.read_csv(CSV_PATH)

@app.route("/registros", methods=["GET"])
def listar():
    return jsonify(df.to_dict(orient="records"))

@app.route("/registros/<int:id>", methods=["GET"])
def buscar(id):
    reg = df[df["id"] == id]
    if reg.empty:
        return jsonify({"erro": "Não encontrado"}), 404
    return jsonify(reg.to_dict(orient="records")[0])

@app.route("/registros", methods=["POST"])
def criar():
    global df

    novo = request.json
    novo["id"] = int(df["id"].max()) + 1
    df = pd.concat([df, pd.DataFrame([novo])], ignore_index=True)
    df.to_csv(CSV_PATH, index=False)

    return jsonify(novo), 201

@app.route("/registros/<int:id>", methods=["PUT"])
def atualizar_registro(id):
    global df

    if id not in df["id"].values:
        return jsonify({"erro": "Não encontrado"}), 404

    dados = request.get_json()
    indice = df.index[df["id"] == id][0]

    for campo, valor in dados.items():
        if campo in df.columns and campo != "id":
            df.loc[indice, campo] = valor

    df.to_csv(CSV_PATH, index=False)
    registro_atualizado = df.loc[indice].to_dict()

    return jsonify(registro_atualizado), 200

@app.route("/registros/<int:id>", methods=["DELETE"])
def deletar_registro(id):
    global df

    if id not in df["id"].values:
        return jsonify({"erro": "Não encontrado"}), 404

    df = df[df["id"] != id].reset_index(drop=True)
    df.to_csv(CSV_PATH, index=False)

    return jsonify({"mensagem": f"Registro {id} removido com sucesso"}), 200

@app.route("/estatisticas")
def estatisticas():
    # Reagrega direto do CSV mais atual, garantindo dados frescos
    global df
    df = pd.read_csv(CSV_PATH)

    por_unidade = df["unidade"].value_counts().to_dict()
    por_plano = df["plano"].value_counts().to_dict()

    return jsonify({
        "por_unidade": por_unidade,
        "por_plano": por_plano
    })

@app.route("/exportar")
def exportar_csv():
    df.to_csv(CSV_PATH, index=False)
    return send_file(
        CSV_PATH,
        mimetype="text/csv",
        as_attachment=True,
        download_name="dados_exportados.csv"
    )



if __name__ == "__main__":
    app.run(debug=True)