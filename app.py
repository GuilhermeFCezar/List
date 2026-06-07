import os
import sqlite3
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

# Configuração do caminho absoluto para o banco de dados (Evita perda de dados)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "presentes.db")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Cria a tabela se ela não existir
    c.execute(
        """CREATE TABLE IF NOT EXISTS itens
                 (id INTEGER PRIMARY KEY, nome TEXT, disponivel INTEGER, doador TEXT, telefone TEXT)"""
    )

    # Verifica se a tabela está vazia para colocar os presentes iniciais
    c.execute("SELECT COUNT(*) FROM itens")
    if c.fetchone()[0] == 0:
        itens_iniciais = [
            "Jogo de Panelas",
            "Liquidificador",
            "Fritadeira Elétrica (Airfryer)",
            "Faqueiro Completo",
            "Jogo de Pratos (Raso/Fundo)",
            "Jogo de Copos de Vidro",
            "Jogo de Toalhas de Banho",
            "Kit de Panos de Prato",
            "Assadeiras de Vidro (Marinex)",
            "Garrafa Térmica + Coador",
            "Kit de Utensílios de Silicone",
            "Aparelho de Jantar",
            "Varal de Chão",
            "Mimos de Decoração / Almofadas",
            "Jogo de Cama (Casal)",
        ]
        for item in itens_iniciais:
            c.execute(
                "INSERT INTO itens (nome, disponivel, doador, telefone) VALUES (?, 1, '', '')",
                (item,),
            )
        conn.commit()
    conn.close()


@app.route("/")
def index():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Busca todos os itens cadastrados
    c.execute("SELECT id, nome, disponivel, doador FROM itens")
    itens = c.fetchall()
    conn.close()
    return render_template("index.html", itens=itens)


@app.route("/escolher/<int:id>", methods=["POST"])
def escolher(id):
    nome = request.form.get("nome")
    telefone = request.form.get("telefone")

    if nome and telefone:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        # Segurança extra: Verifica se o item ainda está disponível antes de atualizar
        c.execute("SELECT disponivel FROM itens WHERE id=?", (id,))
        item_status = c.fetchone()

        if item_status and item_status[0] == 1:
            c.execute(
                "UPDATE itens SET disponivel=0, doador=?, telefone=? WHERE id=?",
                (nome, telefone, id),
            )
            conn.commit()
        conn.close()

    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)