from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()

    c.execute('''
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL
    )
    ''')

    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    c.execute("SELECT * FROM posts ORDER BY id DESC")
    posts = c.fetchall()
    conn.close()

    return render_template('index.html', posts=posts)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        conn = sqlite3.connect('blog.db')
        c = conn.cursor()
        c.execute(
            "INSERT INTO posts(title, content) VALUES (?, ?)",
            (title, content)
        )
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/post/<int:id>')
def post(id):
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    c.execute("SELECT * FROM posts WHERE id=?", (id,))
    post = c.fetchone()
    conn.close()

    return render_template('view.html', post=post)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
