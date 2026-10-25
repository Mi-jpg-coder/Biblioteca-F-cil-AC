from flask import Flask, request, jsonify
import mysql.connector
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR.parent / "frontend"

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "1234"
DB_NAME = "biblioteca"

app = Flask(
    __name__,
    static_folder=str(FRONTEND_DIR),
    static_url_path=""
)


def conectar_banco():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )


def criar_tabela():
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS livros (
            id INT PRIMARY KEY AUTO_INCREMENT,
            Titulo VARCHAR(150) NOT NULL,
            Autor VARCHAR(150) NOT NULL,
            Ano INT
        )
    """)

    conexao.commit()
    cursor.close()
    conexao.close()


@app.get("/")
def pagina_inicial():
    return app.send_static_file("index.html")


@app.get("/livros")
def listar_livros():
    conexao = conectar_banco()
    cursor = conexao.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT
                id AS id,
                Titulo AS titulo,
                Autor AS autor,
                Ano AS ano
            FROM livros
            ORDER BY id DESC
        """)

        livros = cursor.fetchall()
        return jsonify(livros)

    finally:
        cursor.close()
        conexao.close()


@app.post("/livros")
def cadastrar_livro():
    dados = request.get_json(silent=True) or {}

    titulo = str(dados.get("titulo", "")).strip()
    autor = str(dados.get("autor", "")).strip()
    ano_recebido = dados.get("ano")

    if not titulo or not autor:
        return jsonify({
            "erro": "Título e autor são obrigatórios."
        }), 400

    try:
        ano = int(ano_recebido) if str(
            ano_recebido or ""
        ).strip() else None
    except (TypeError, ValueError):
        return jsonify({
            "erro": "Informe um ano válido."
        }), 400

    conexao = conectar_banco()
    cursor = conexao.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO livros (Titulo, Autor, Ano)
            VALUES (%s, %s, %s)
            """,
            (titulo, autor, ano)
        )

        conexao.commit()
        livro_id = cursor.lastrowid

        return jsonify({
            "id": livro_id,
            "titulo": titulo,
            "autor": autor,
            "ano": ano
        }), 201

    finally:
        cursor.close()
        conexao.close()


@app.put("/livros/<int:livro_id>")
def editar_livro(livro_id):
    dados = request.get_json(silent=True) or {}

    titulo = str(dados.get("titulo", "")).strip()
    autor = str(dados.get("autor", "")).strip()
    ano_recebido = dados.get("ano")

    if not titulo or not autor:
        return jsonify({
            "erro": "Título e autor são obrigatórios."
        }), 400

    try:
        ano = int(ano_recebido) if str(
            ano_recebido or ""
        ).strip() else None
    except (TypeError, ValueError):
        return jsonify({
            "erro": "Informe um ano válido."
        }), 400

    conexao = conectar_banco()
    cursor = conexao.cursor()

    try:
        cursor.execute(
            """
            UPDATE livros
            SET Titulo = %s, Autor = %s, Ano = %s
            WHERE id = %s
            """,
            (titulo, autor, ano, livro_id)
        )

        conexao.commit()

        if cursor.rowcount == 0:
            cursor.execute(
                "SELECT id FROM livros WHERE id = %s",
                (livro_id,)
            )

            if cursor.fetchone() is None:
                return jsonify({
                    "erro": "Livro não encontrado."
                }), 404

        return jsonify({
            "mensagem": "Livro atualizado com sucesso!"
        })

    finally:
        cursor.close()
        conexao.close()


@app.delete("/livros/<int:livro_id>")
def excluir_livro(livro_id):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    try:
        cursor.execute(
            "DELETE FROM livros WHERE id = %s",
            (livro_id,)
        )

        conexao.commit()

        if cursor.rowcount == 0:
            return jsonify({
                "erro": "Livro não encontrado."
            }), 404

        return jsonify({
            "mensagem": "Livro excluído com sucesso!"
        })

    finally:
        cursor.close()
        conexao.close()


if __name__ == "__main__":
    criar_tabela()
    app.run(host="127.0.0.1", port=5000, debug=True)
