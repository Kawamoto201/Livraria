from flask import Flask, render_template, request

import pyodbc

app = Flask(__name__)

def conectar():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=DESKTOP-BK1ILCS;"
        "DATABASE=Livraria;"
        "Trusted_Connection=yes;"
    )
    return conexao


@app.route("/", methods=["GET","POST"])
@app.route("/cadastrolivro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":

        nl = request.form["titulo-Livro"]
        al = request.form["autor-livro"]
        pl = float(request.form["valor-livro"])
        ql = int(request.form["qtd-livro"])

        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("""
            INSERT INTO dbo.tblLivros(nomeLivro, autorLivro, precoLivro, qtdEstoque)
            VALUES (?,?,?,?)
        """, (nl, al, pl, ql))

        conexao.commit()
        conexao.close()

        return "Livro cadastrado com sucesso!"

    return render_template("cadastrolivro.html")

if __name__ == '__main__':
    app.run(debug=True)