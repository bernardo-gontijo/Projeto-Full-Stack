from flask import Flask, request, jsonify, send_file, render_template, Response
import pandas as pd
import plotly.express as px

app = Flask(__name__)
CSV_PATH = "dados.csv"
df = pd.read_csv(CSV_PATH)

@app.route("/")
def inicio():
    return render_template("index.html")

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

@app.route("/estatisticas")
def estatisticas():
    # Reagrega direto do CSV mais atual
    global df
    df = pd.read_csv(CSV_PATH)

    tipo = request.args.get("tipo", "grafico_barra")

    if tipo == "grafico_linha":
        # Número de alunos matriculados por mês
        temp = df.copy()
        temp["mes"] = pd.to_datetime(temp["data_matricula"]).dt.to_period("M").astype(str)
        contagem = temp.groupby("mes").size().reset_index(name="quantidade")
        contagem = contagem.sort_values("mes")

        fig = px.line(
            contagem, x="mes", y="quantidade", markers=True,
            title="Alunos Matriculados por Mês",
            labels={"mes": "Mês", "quantidade": "Nº de Alunos"}
        )

    elif tipo == "grafico_pizza":
        # Número de alunos por plano
        contagem = df["plano"].value_counts().reset_index()
        contagem.columns = ["plano", "quantidade"]

        fig = px.pie(
            contagem, names="plano", values="quantidade",
            title="Alunos por Plano"
        )

    else:
        # Número de alunos cadastrados por unidade
        contagem = df["unidade"].value_counts().reset_index()
        contagem.columns = ["unidade", "quantidade"]

        fig = px.bar(
            contagem, x="unidade", y="quantidade",
            title="Alunos Cadastrados por Unidade",
            labels={"unidade": "Unidade", "quantidade": "Nº de Alunos"}
        )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",  # Fundo externo transparente
        plot_bgcolor="rgba(0,0,0,0)",   # Fundo do gráfico transparente
        font_color="#FFFFFF",           # Cor do texto em branco para combinar com o modo escuro
        margin=dict(l=20, r=20, t=40, b=20),
        autosize=True
    )
        
    return Response(fig.to_json(), mimetype="application/json")

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