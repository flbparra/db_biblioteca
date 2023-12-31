from service.connectBD import getDB
from flask import jsonify, request
import json
import mysql.connector


def create_new_book(IDLivro, Titulo, Autor, Descricao, Categoria, DataAquisicao, EstadoConservacao, LocalizacaoFisica, URICapaLivro):
    
    conexao = getDB()
    cursor = conexao.cursor()
    query = "INSERT INTO Livros(IDLivro, Titulo, Autor, Descricao, Categoria, DataAquisicao, EstadoConservacao, LocalizacaoFisica, URICapaLivro) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    
    cursor.execute(query,(IDLivro, Titulo, Autor, Descricao, Categoria, DataAquisicao, EstadoConservacao, LocalizacaoFisica, URICapaLivro))
    conexao.commit()
    livro_cadastrado = get_book_id(IDLivro)
    livro_cadastrado = livro_cadastrado.get_json()

    #------------------------------------------------------------------------------
    # Script para adicionar Livro também na tabela Item
    adicionarEmItem = "INSERT INTO Item(Tipo, IDLivro, StatusItem) VALUES (%s, %s, %s)"
    cursor.execute(adicionarEmItem,("Livro", IDLivro, "Disponivel"))
    conexao.commit()
    conexao.close()

    return jsonify({"mensage" : "Livro cadastrado com sucesso", "livro" :livro_cadastrado}), 200


def get_book_id(IDLivro): 
    conexao = getDB()
    cursor = conexao.cursor()
    
    cursor.execute(f"SELECT IDLivro, Titulo, Autor, Descricao, Categoria, DataAquisicao, EstadoConservacao, LocalizacaoFisica, URICapaLivro FROM Livros WHERE IDLivro ={IDLivro}")
    infoBook = []
    
    for row in cursor:
        IDLivro, Titulo, Autor, Descricao, Categoria, DataAquisicao, EstadoConservacao, LocalizacaoFisica, URICapaLivro = row
        infoBook.append({
            "IDLivro": IDLivro,
            "Titulo": Titulo,
            "Autor": Autor,
            "Descricao": Descricao,
            "Categoria": Categoria,
            "DataAquisicao": DataAquisicao,
            "EstadoConservacao": EstadoConservacao,
            "LocalizacaoFisica": LocalizacaoFisica,
            "URICapaLivro": URICapaLivro
        })
           
    conexao.close()
    return jsonify(infoBook)

def get_all_books():
    conexao = getDB()
    cursor = conexao.cursor()
    
    cursor.execute("SELECT IDLivro, Titulo, Autor, LocalizacaoFisica, Categoria, URICapaLivro FROM Livros")
    allBooks = []
    
    for row in cursor:
        IDLivro, Titulo, Autor, LocalizacaoFisica, Categoria, URICapaLivro = row
        allBooks.append({
            "IDLivro": IDLivro,
            "Titulo": Titulo,
            "Autor": Autor,
            "LocalizacaoFisica": LocalizacaoFisica,
            "Categoria": Categoria,
            "URICapaLivro": URICapaLivro
        })
    conexao.close()
    return jsonify({"Livros cadastrados no Sistema": allBooks})

def delete_book(IDLivro):
    
    conexao = getDB()
    cursor = conexao.cursor()
    
    try:
        #verifica se o id existe no banco
        
        cursor.execute(f"SELECT IDLivro FROM Livros WHERE IDLivro = {IDLivro}")
        livro_exite = cursor.fetchone()
        
        if not livro_exite:
            return jsonify({"message" : "Livro não encontrado"}), 404
        
        cursor.execute(f"DELETE FROM Item WHERE IDLivro = {IDLivro}")
        cursor.execute(f"DELETE FROM Livros WHERE IDLivro = {IDLivro}")
        conexao.commit()
        
        return jsonify({"message" : "Livro deletado com sucesso!"}), 200
    
    except mysql.connector.Error as erro:
        return jsonify({"error - livro não encontrado" : str(erro)}), 500
    

def update_book(IDLivro):
    
    conexao = getDB()
    cursor = conexao.cursor()
    
    cursor.execute(f"SELECT IDLivro FROM Livros WHERE IDLivro = {IDLivro}")
    livro_exite = cursor.fetchone()
        
    if not livro_exite:
        conexao.close()
        return jsonify({"message" : "Livro não encontrado"}), 404
        
    livro_data = request.json
        
    query = "UPDATE Livros SET Titulo=%s, Autor=%s, Descricao=%s, Categoria=%s, DataAquisicao=%s, EstadoConservacao=%s, LocalizacaoFisica=%s, URICapaLivro=%s WHERE IDLivro=%s"
        
    cursor.execute(query,(livro_data.get('Titulo'),
            livro_data.get('Autor'),
            livro_data.get('Descricao'),
            livro_data.get('Categoria'),
            livro_data.get('DataAquisicao'),
            livro_data.get('EstadoConservacao'),
            livro_data.get('LocalizacaoFisica'),
            livro_data.get('URICapaLivro'),
            IDLivro))
        
    conexao.commit()
    conexao.close()
    return jsonify({"message" : "Livro atualizado"})


"""

BUSCAS DOS LIVROS: 
"""
#buscar por cartegoria - atualizado: 12/12/2023 
def get_books_category(categoria):
    conexao = getDB()
    cursor = conexao.cursor()
    
    cursor.execute("SELECT IDLivro, Titulo, Autor, LocalizacaoFisica, Categoria, URICapaLivro FROM Livros WHERE Categoria = %s", (categoria,))
    
    books_category = []
    
    for row in cursor:
        IDLivros, Titulo, Autor, LocalizacaoFisica, Categoria, URICapaLivro = row
        books_category.append({
            "IDLivros": IDLivros,
            "Titulo": Titulo,
            "Autor": Autor,
            "LocalizacaoFisica": LocalizacaoFisica,
            "Categoria": Categoria,
            "URICapaLivro": URICapaLivro
        })
    
    conexao.close()
    if books_category:    
        return jsonify({"Livros referentes a essa cartegoria: ": books_category})
    
    return jsonify({"message": f"Nenhum livro com esse author '{cartegoria}' foi encontrado."})


def get_books_titles(pesquisa):
    
    conexao = getDB()
    cursor = conexao.cursor()
    
    cursor.execute("SELECT IDLivro, Titulo, Autor, LocalizacaoFisica, Categoria, URICapaLivro FROM Livros WHERE Titulo LIKE %s", ('%' + pesquisa + '%',))

    books_titles = []
    
    for row in cursor:
        IDLivros, Titulo, Autor, LocalizacaoFisica, Categoria, URICapaLivro = row
        books_titles.append({
            "IDLivros": IDLivros,
            "Titulo": Titulo,
            "Autor": Autor,
            "LocalizacaoFisica": LocalizacaoFisica,
            "Categoria": Categoria,
            "URICapaLivro": URICapaLivro
        })

    conexao.close()
    
    if books_titles:
        return jsonify({"Livros com esse titulo disponivel": books_titles})

    return jsonify({"message": f"Nenhum livro com esse título '{pesquisa}' foi encontrado."})
    
    
def get_books_author(pesquisa):
    
    conexao = getDB()
    cursor = conexao.cursor()
    
    cursor.execute("SELECT IDLivro, Titulo, Autor, LocalizacaoFisica, Categoria, URICapaLivro FROM Livros WHERE Autor LIKE %s", ('%' + pesquisa + '%',) )
    
    books_author = []
    for row in cursor:
        IDLivros, Titulo, Autor, LocalizacaoFisica, Categoria, URICapaLivro = row
        books_author.append({
            "IDLivros": IDLivros,
            "Titulo": Titulo,
            "Autor": Autor,
            "LocalizacaoFisica": LocalizacaoFisica,
            "Categoria": Categoria,
            "URICapaLivro": URICapaLivro
        })
    
    if books_author:
        return jsonify({"Livros com esse author disponível:" : books_author})
    
    return jsonify({"message": f"Nenhum livro com esse author '{pesquisa}' foi encontrado."})
