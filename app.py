import os
import sqlite3
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "presentes.db")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Adicionada a coluna 'imagem' no banco de dados
    c.execute(
        """CREATE TABLE IF NOT EXISTS itens
                 (id INTEGER PRIMARY KEY, nome TEXT, imagem TEXT, disponivel INTEGER, doador TEXT, telefone TEXT)"""
    )

    c.execute("SELECT COUNT(*) FROM itens")
    if c.fetchone()[0] == 0:
        # Lista agora contém (Nome do Item, Link da Imagem)
        # Usei imagens genéricas do site Unsplash para você testar
        itens_iniciais = [
            ("Jogo de Panelas", "https://images.unsplash.com/photo-1584990347449-a6e81cbce126?w=200&q=80"),
            ("Liquidificador Imperial", "https://images.unsplash.com/photo-1585237672814-8f85a8129dd6?w=200&q=80"),
            ("Airfryer (Estrela da Morte)", "https://images.unsplash.com/photo-1628840042765-356cda07504e?w=200&q=80"),
            ("Faqueiro Completo", "https://images.unsplash.com/photo-1581428982868-e410dd047a90?w=200&q=80"),
            ("Jogo de Pratos Negros", "https://images.unsplash.com/photo-1610055106191-4cf106daaa20?w=200&q=80"),
            ("Taças de Vinho Elegantes", "https://images.unsplash.com/photo-1584916201218-f4242ceb4809?w=200&q=80"),
            ("Jogo de Cama (Casal)", "https://images.unsplash.com/photo-1522771731478-44bf10cb334f?w=200&q=80"),
        ]
        for nome, imagem in itens_iniciais:
            c.execute(
                "INSERT INTO itens (nome, imagem, disponivel, doador, telefone) VALUES (?, ?, 1, '', '')",
                (nome, imagem),
            )
        conn.commit()
    conn.close()


@app.route("/")
def index():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Agora buscamos a imagem também
    c.execute("SELECT id, nome, imagem, disponivel, doador FROM itens")
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