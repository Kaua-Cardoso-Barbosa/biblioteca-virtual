from flask import Flask, render_template, request, redirect
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'chave_secreta_livro'

livros = []

@app.route('/')
def index():
    return render_template(('index.html'))



@app.route('/catalogo')
def catalogo():
    for livro in livros:
        if len(livro) > 4 and livro[4]:
            data_devolucao = datetime.strptime(livro[5], '%Y-%m-%d')
            if datetime.now() > data_devolucao:
                dias_atraso = (datetime.now() - data_devolucao).days
                multa = 10 + (0.01 * dias_atraso)
                livro[6] = f"R${multa:.2f}"
    return render_template('catalogo.html', livros=livros)


@app.route('/adicionar_livro', methods=['GET', 'POST'])
def adicionar_livro():
    if request.method == 'POST':
        titulo = request.form['titulo']
        autor = request.form['autor']
        ano = request.form['ano']
        codigo = len(livros)

        livros.append([codigo, titulo, autor, ano, None, None, None])
        return redirect('/')
    else:
        return render_template('adicionar_livro.html')


@app.route('/editar_livro/<int:codigo>', methods=['GET', 'POST'])
def editar_livro(codigo):
    if request.method == 'POST':
        titulo = request.form['titulo']
        autor = request.form['autor']
        ano = request.form['ano']

        if len(livros[codigo]) > 4:
            livros[codigo] = [codigo, titulo, autor, ano] + livros[codigo][4:]
        else:
            livros[codigo] = [codigo, titulo, autor, ano]
        return redirect('/')
    else:
        livro = livros[codigo]
        return render_template('editar_livro.html', livro=livro)


@app.route('/emprestar_livro/<int:codigo>')
def emprestar_livro(codigo):
    data_emprestimo = datetime.now()
    data_devolucao = data_emprestimo + timedelta(days=7)

    livros[codigo][4] = data_emprestimo.strftime('%Y-%m-%d')
    livros[codigo][5] = data_devolucao.strftime('%Y-%m-%d')  #
    livros[codigo][6] = "Sem multa"

    return redirect('/')


@app.route('/devolver_livro/<int:codigo>')
def devolver_livro(codigo):
    livros[codigo] = livros[codigo][:4]
    return redirect('/')


@app.route('/apagar_livro/<int:codigo>')
def apagar_livro(codigo):
    del livros[codigo]
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)