from flask import Flask, request, render_template

from service.livros import create_new_book, get_book_id, get_all_books, delete_book, update_book, get_books_category, get_books_titles, get_books_author

from service.material import create_new_material, get_material_id, get_all_materials, delete_material, update_material, get_materials_category

from service.usuario import create_new_user, get_user_id, get_all_users, delete_user, update_user

from service.emprestimos import create_new_emprestimo, get_emprestimo, delete_emprestimo, update_emprestimo

from service.login import login, logoff

import mysql.connector


app = Flask(__name__)


"""
LOGIN
"""
# /HOME criadoe
@app.route('/')
def index():
    return render_template('template/')

@app.route('/login', methods=['POST'])
def login_this_user():
    data = request.json
    return render_template('template/', login(data))

@app.route('/logout', methods=['POST'])
# --> Faz logoff
def logout_this_user():
    return render_template('template/' ,logoof())


"""Livros: Consultas, Inserção, Edição e Delete
"""

@app.route('/books/', methods=['GET'])
def view_books():
# ---> Retorna todos os livros cadastrados no banco de dados
    return render_template( 'template/',books = get_all_books())


@app.route("/books/<int:IDLivro>", methods=["GET"])
# ---> Função para visualizar livro por id
def view_book_id(IDLivro):
    return render_template('template/', book=get_book_id(IDLivro))

@app.route("/books/<string:titulo>", methods=["GET"])
# ---> Função para visualizar livros por titulo
def view_books_title(titulo):
    return render_template('template/', books= get_books_titles(titulo))

@app.route("/books/<string:author>", methods=["GET"])
# ---> Função para visualizar livros por autores
def view_books_author(author):
    return render_template('template/', books= get_books_author(author))

@app.route("/books/<string:categoria>", methods=["GET"])
# ---> Retorna todos que tem as categorias cadastrados no banco de dados
def view_books_category(categoria):
    return render_template('template/', books= get_books_category(categoria))
    

@app.route("/books/<int:IDLivro>", methods=["POST"])
# ---> Função para criar livro
def create_book(IDLivro):
    livro_data = request.json
    return create_new_book(
        IDLivro, 
        livro_data['Titulo'], 
        livro_data['Autor'], 
        livro_data['Descricao'], 
        livro_data['Categoria'], 
        livro_data['DataAquisicao'], 
        livro_data['EstadoConservacao'],
        livro_data['LocalizacaoFisica'],
        livro_data['URICapaLivro'] 
        )

@app.route("/books/<int:IDLivro>", methods=["DELETE"])
# ---> Função para deletar livro
def delete_this_book(IDLivro):
    return delete_book(IDLivro)

@app.route("/books/<int:IDLivro>", methods=["PUT"])
# ---> Função para atualizar livro
def update_this_book(IDLivro):
    return update_book(IDLivro)



"""
MATERIAS - INSERT, CONSULTAS, DELETE, UPDATE
"""

@app.route('/materials/<int:IDMaterial>', methods=['POST'])
def create_material(IDMaterial):
    material_data = request.json
    return create_new_material(
        IDMaterial, 
        material_data['Descricao'],material_data['NumeroSerie'], material_data['DataAquisicao'],material_data['EstadoConservacao'],
        material_data['LocalizacaoFisica'],
        material_data['URIFotoMaterial'])

@app.route('/materials/<int:IDMaterial>', methods=['GET']) 
def get_material(IDMaterial):
    return render_template('template/', material= get_material_id(IDMaterial))

@app.route('/materials', methods=['GET'])
def view_materials():
    return render_template('template/', materials= get_all_materials())

@app.route('/materials/<int:IDMaterial>', methods=['GET'])
def view_material_id(IDMaterial):
    return render_template('template/', material= get_material_id(IDMaterial))

@app.route('/materials/<string:categoria>', methods=['GET'])
# Retorna materiais por cartegoria
def view_material_cartegoria(categoria):
    return render_template('template/', materials= get_materials_category(categoria))
    
@app.route('/materials/<int:IDMaterial>', methods=['DELETE'])
#somente admins podem deletar dados do banco
def delete_this_material(IDMaterial):
    return delete_material(IDMaterial)

@app.route('/materials/<int:IDMaterial>', methods=['PUT'])
# ---> Atualiza material, somente admin e chefes tem acessos
def upadate_this_material(IDMaterial):
    material_data = request.json
    return update_material(IDMaterial, material_data)



"""
USUARIOS: Chamadas para usuarios.
"""

@app.route('/user/<int:ID>', methods=['POST'])
# ---> Create new user
def create_user(ID):
    user_data = request.json
    return create_new_user(ID,
                       user_data['Nome'], 
                       user_data['Sobrenome'], 
                       user_data['Funcao'],
                       user_data['Login'], 
                       user_data['Senha'], 
                       user_data['URIFotoUsuario']
                       )
@app.route('/user/<int:ID>', methods=['GET'])
# Retorna usuarios por ID
def view_this_user(ID):
    return render_template('template/', user= get_user_id(ID))
@app.route('/users', methods=['GET'])
# --> Retorna todos os usuarios
def view_all_users():
    return render_template('template/', users= get_all_users())
@app.route('/user/<int:ID>', methods=['DELETE'])
# --> Delete a user por ID
def delete_this_user(ID):
    return delete_user(ID)
@app.route('/user/<int:ID>', methods=['PUT'])
# --> Update a user por ID (não a senha e nem o login)
def upadate_this_user(ID):
    return update_user(ID)

"""
EMPRESTIMOS: Chamadas para emprestimo.
"""

@app.route('/emprestimo', methods=['POST'])
# --> função para criar emprestimo
def create_emprestimo():
    emprestimo_data = request.json
    return create_new_emprestimo(emprestimo_data)

@app.route('/emprestimo/<int:IDUsuario>', methods=['GET'])
# --> função para consultar emprestimos de usuário
def get_all_emprestimo(IDUsuario):
    return render_template('template/', emprestimo= get_emprestimo(IDUsuario))

@app.route('/emprestimo/<int:IDItem>', methods=['DELETE'])
# --> função para deletar emprestimo
def delete_this_emprestimo(IDItem):
    return delete_emprestimo(IDItem)

@app.route('/emprestimo/<int:IDItem>', methods=['PUT'])
# --> função para renovar emprestimo
def update_this_emprestimo(IDItem):
    return update_emprestimo(IDItem)


if __name__ == '__main__':
    app.run(port=5000, host='127.0.0.1', debug=True)

