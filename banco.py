import sqlite3

class Banco:

    def __init__(self):
        self.conexao = sqlite3.connect("pokedex.db", check_same_thread=False)
        cursor = self.conexao.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;") # Habilita o suporte a Chaves Estrangeiras (e o ON DELETE CASCADE), sem isso quando deletava um pokémon as evoluções continuavam existindo
        cursor.execute("CREATE TABLE IF NOT EXISTS pokedex(id INTEGER PRIMARY KEY, nome, tipo, genero, altura, peso)")
        self.conexao.commit()
        cursor.execute("CREATE TABLE IF NOT EXISTS evolucoes(id INTEGER PRIMARY KEY, idPokemon INTEGER REFERENCES pokedex(id) ON DELETE CASCADE, nome_evolucao TEXT)")
        self.conexao.commit()
        cursor.close()

    def adicionar(self, nome, tipo, genero, altura, peso):
        cursor = self.conexao.cursor()
        cursor.execute('INSERT INTO pokedex(nome, tipo, genero, altura, peso) VALUES(?,?,?,?,?)', (nome,tipo,genero,altura,peso))
        if(cursor.rowcount > 0):
            id = cursor.lastrowid
        else:
            id = None
        self.conexao.commit()
        cursor.close()
        return id
    
    # retorna uma tupla contendo todos os campos, na mesma ordem de criação do banco
    def buscar(self, id):
        cursor = self.conexao.cursor()
        cursor.execute('SELECT * FROM pokedex WHERE id = ?', (id,))
        retorno = cursor.fetchone()
        cursor.close()
        return retorno
    
    def buscarTudo(self):
        cursor = self.conexao.cursor()
        cursor.execute('SELECT * FROM pokedex')
        retorno = cursor.fetchall()
        cursor.close()
        return retorno
    
    def remover(self, id):
        cursor = self.conexao.cursor()
        cursor.execute('DELETE FROM pokedex WHERE id = ?', (id,))
        if(cursor.rowcount > 0): 
            id = cursor.lastrowid
        else:
            id = None
        self.conexao.commit()
        cursor.close()
        return id

    def atualizar(self, id, nome, tipo, genero, altura, peso):
        cursor = self.conexao.cursor()
        cursor.execute('UPDATE pokedex SET nome = ?, tipo = ?, genero = ?, altura = ?, peso = ? WHERE id = ?', (nome,tipo,genero,altura,peso,id))
        self.conexao.commit()
        cursor.close()
        return id
    
    def adicionarEvolucao(self, idPokemon, nomeEvolucao):
        try:
            cursor = self.conexao.cursor()
            cursor.execute('INSERT INTO evolucoes(idPokemon, nome_evolucao) VALUES(?,?)', (idPokemon, nomeEvolucao))
            if(cursor.rowcount > 0):
                id = cursor.lastrowid
            else:
                id = None
            self.conexao.commit()
            cursor.close()
            return id
        except: 
            return None 

    def buscarEvolucoes(self, idPokemon):
        cursor = self.conexao.cursor()
        cursor.execute('SELECT * FROM evolucoes WHERE idPokemon = ?', (idPokemon,))
        retorno = cursor.fetchall()
        cursor.close()
        return retorno