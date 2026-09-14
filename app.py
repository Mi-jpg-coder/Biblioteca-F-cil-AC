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
    conexao = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    return conexao
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

    cursor.execute(
        "SELECT * FROM livros ORDER BY id DESC"
    )

    livros = cursor.fetchall()

    cursor.close()
    conexao.close()

    return jsonify(livros)
    conexao = conectar_banco()

    livros = conexao.execute(
        "SELECT * FROM livros ORDER BY id DESC"
    ).fetchall()

    conexao.close()

    return jsonify([dict(livro) for livro in livros])

@app.post("/livros")
def cadastrar_livro():
    dados = request.get_json(silent=True) or {}

    titulo = str(dados.get("titulo", "")).strip()
    autor = str(dados.get("autor", "")).strip()
    ano = dados.get("ano") or None

    if not titulo or not autor:
        return jsonify({"erro": "Título e autor são obrigatórios."}), 400

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute(
        "INSERT INTO livros (Titulo, Autor, Ano) VALUES (%s, %s, %s)",
        (titulo, autor, ano)
    )

    conexao.commit()
    livro_id = cursor.lastrowid

    cursor.close()
    conexao.close()

    return jsonify({
        "id": livro_id,
        "titulo": titulo,
        "autor": autor,
        "ano": ano
    }), 201
    dados = request.get_json(silent=True) or {}

    titulo = str(dados.get("titulo", "")).strip()
    autor = str(dados.get("autor", "")).strip()
    ano = dados.get("ano") or None

    if not titulo or not autor:
        return jsonify({"erro": "Título e autor são obrigatórios."}), 400

    conexao = conectar_banco()

    cursor = conexao.execute(
        "INSERT INTO livros (titulo, autor, ano) VALUES (?, ?, ?)",
        (titulo, autor, ano)
    )

    conexao.commit()
    livro_id = cursor.lastrowid
    conexao.close()

    return jsonify({
        "id": livro_id,
        "titulo": titulo,
        "autor": autor,
        "ano": ano
    }), 201

if __name__ == "__main__":
    criar_tabela()
    app.run(port=5000, debug=True)
    