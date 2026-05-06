from flask import Flask, render_template, request, redirect, url_for, flash
import pyodbc

app = Flask(__name__)
app.secret_key = "chave_secreta"

# CONEXÃO BANCO DE DADOS
def conectar():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=DESKTOP-BK1ILCS;"
        "DATABASE=Livraria;"
        "Trusted_Connection=yes;"
    )



# CADASTRAR LIVRO

@app.route("/", methods=["GET", "POST"])
@app.route("/cadastrolivro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":

        titulo = request.form["titulo_livro"]
        autor = request.form["autor_livro"]
        valor = float(request.form["valor_livro"])
        qtd = int(request.form["qtd_livro"])

        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("""
            INSERT INTO dbo.tblLivros (nomeLivro, autorLivro, precoLivro, qtdEstoque)
            VALUES (?, ?, ?, ?)
        """, (titulo, autor, valor, qtd))

        conexao.commit()
        conexao.close()

        flash("Livro cadastrado com sucesso!")
        return redirect(url_for("cadastro"))

    return render_template("cadastrolivro.html")



# BUSCAR LIVRO

@app.route("/buscarlivro", methods=["GET"])
def buscar():

    nome = request.args.get("titulo_livro", "")

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT idLivro, nomeLivro, autorLivro, qtdEstoque,
        CAST(precoLivro AS DECIMAL(10,2)) as preco
        FROM tblLivros
        WHERE nomeLivro LIKE ?
    """, ('%' + nome + '%',))

    livros = cursor.fetchall()
    conexao.close()

    return render_template("buscarlivro.html", livros=livros)


# ATUALIZAR LIVRO

from flask import Flask, render_template, request, redirect, url_for, flash

@app.route("/atualizar", methods=["GET", "POST"])
def atualizarlivros():
    conn = conectar()
    cursor = conn.cursor()

    livros = []
    livro_editando = None
    ja_buscou = False

    # ATUALIZAR LIVRO

    if request.method == "POST":
        try:
            cursor.execute("""
                UPDATE tblLivros
                SET nomeLivro = ?, autorLivro = ?, qtdEstoque = ?, precoLivro = ?
                WHERE idLivro = ?
            """, (
                request.form["nome"],
                request.form["autor"],
                request.form["quantidade"],
                request.form["preco"],
                request.form["id"]
            ))

            conn.commit()
            flash("Livro atualizado com sucesso!", "sucesso")

        except Exception:
            conn.rollback()
            flash("Erro ao atualizar o livro!", "erro")

        finally:
            conn.close()

        return redirect(url_for("atualizarlivros"))


# BUSCAR LIVRO

    nome = request.args.get("titulo_livro", "").strip()
    editar_id = request.args.get("editar_id")

    if nome:
        ja_buscou = True
        cursor.execute("""
            SELECT idLivro, nomeLivro, autorLivro, qtdEstoque, precoLivro
            FROM tblLivros
            WHERE nomeLivro LIKE ?
        """, (f"%{nome}%",))
        livros = cursor.fetchall()

    if editar_id:
        cursor.execute("""
            SELECT idLivro, nomeLivro, autorLivro, qtdEstoque, precoLivro
            FROM tblLivros
            WHERE idLivro = ?
        """, (editar_id,))
        livro_editando = cursor.fetchone()

    conn.close()

    return render_template(
        "atualizarlivro.html",
        livros=livros,
        livro_editando=livro_editando,
        ja_buscou=ja_buscou
    )

# RODAR APP

if __name__ == "__main__":
    app.run(debug=True)