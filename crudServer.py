import cherrypy
import banco

@cherrypy.expose
class CRUD:

    def __init__(self):
        self.banco = banco.Banco()

    def adicionar(self, **kwargs):
        chaves = {'nome', 'tipo', 'genero', 'altura', 'peso'}
        if set(kwargs.keys()).issuperset(chaves):
            if len(kwargs['nome']) > 0 and len(kwargs['tipo']) > 0 and len(kwargs['genero']) > 0 and float(kwargs['altura']) > 0 and float(kwargs['peso']) > 0:
                id = self.banco.adicionar(kwargs['nome'], kwargs['tipo'], kwargs['genero'], kwargs['altura'], kwargs['peso'])
                cherrypy.response.status = "201"
                return "<div>Pokémon inserido com ID ", str(id), ".</div>"
            else:
                raise cherrypy.HTTPError(422,'Você errou o valor de algum campo')
        else:
            raise cherrypy.HTTPError(400,"Você esqueceu de passar uma das chaves")

    def buscar(self, **kwargs):
        if 'id' in kwargs.keys():
            #print(id)
            tupla = self.banco.buscar(int(kwargs['id']))
            if tupla is not None:
                mensagem = '<div>ID: ' + str(tupla[0]) + '\nNome: ' + str(tupla[1]) + '\nTipo: ' + str(tupla[2])
                mensagem += '\nGenero: ' + str(tupla[3]) + '\nAltura: ' + str(tupla[4]) + '\nPeso: ' + str(tupla[5]) + '</div>'
                return mensagem
            else:
                raise cherrypy.HTTPError(404,'Pokémon não encontrado')
        else:
            lista = self.banco.buscarTudo()
            mensagem = '<div>Lista de pokémons:</div>'
            for tupla in lista:
                mensagem += '<div>ID: ' + str(tupla[0]) + '\nNome: ' + str(tupla[1]) + '\nTipo: ' + str(tupla[2])
                mensagem += '\nGenero: ' + str(tupla[3]) + '\nAltura: ' + str(tupla[4]) + '\nPeso: ' + str(tupla[5]) + '</div>'
            return mensagem
        
    def atualizar(self, **kwargs):
        chaves = {'id', 'nome', 'tipo', 'genero', 'altura', 'peso'}
        if set(kwargs.keys()).issuperset(chaves):
            id = int(kwargs['id'])
            if self.banco.buscar(id) is not None:
                if len(kwargs['nome']) > 0 and len(kwargs['tipo']) > 0 and len(kwargs['genero']) > 0 and float(kwargs['altura']) > 0 and float(kwargs['peso']) > 0:
                    self.banco.atualizar(id, kwargs['nome'], kwargs['tipo'], kwargs['genero'], kwargs['altura'], kwargs['peso'])
                    cherrypy.response.status = "200"
                    return "<div>Pokémon atualizado.</div>"
                else:
                    raise cherrypy.HTTPError(422, 'Você errou o valor de algum campo')
            else:
                raise cherrypy.HTTPError(404, 'Pokémon não encontrado')
        else:
            raise cherrypy.HTTPError(400, "Você esqueceu de passar uma das chaves")
        
    def remover(self, **kwargs):
            if 'id' in kwargs.keys():
                id = int(kwargs['id'])
                if self.banco.buscar(id) is not None:
                    resultado = self.banco.remover(id)
                    if resultado is not None:
                        cherrypy.response.status = "200"
                        return "<div>Pokémon com ID " + str(id) + " removido com sucesso.</div>"
                    else:
                        raise cherrypy.HTTPError(500, 'Erro ao remover Pokémon')
                else:
                    raise cherrypy.HTTPError(404, 'Pokémon não encontrado')
            else:
                raise cherrypy.HTTPError(400, "Você deve passar o ID")
            
    def adicionarEvolucao(self, idPokemon, **kwargs): # Segundo recurso
        if self.banco.buscar(int(idPokemon)) is None:
            raise cherrypy.HTTPError(404, 'Pokémon não encontrado.')
        chaves = {'nome'}
        if set(kwargs.keys()).issuperset(chaves):
            if len(kwargs['nome']) > 0:
                idEv = self.banco.adicionarEvolucao(idPokemon, kwargs['nome'])
                if idEv is not None:
                    cherrypy.response.status = "201"
                    return "<div>Evolução " + kwargs['nome'] + " inserida para o Pokémon ID " + str(idPokemon) + ".</div>"
                else:
                    raise cherrypy.HTTPError(500, 'Falha ao inserir evolução no banco.')
            else:
                raise cherrypy.HTTPError(422, 'O nome da evolução não pode ser vazio.')
        else:
            raise cherrypy.HTTPError(400, "Você esqueceu de passar o campo 'nome' da evolução.")
        
    def buscarEvolucoes(self, idPokemon, **kwargs):
        if self.banco.buscar(int(idPokemon)) is None:
            raise cherrypy.HTTPError(404, 'Pokémon não encontrado.')
        lista = self.banco.buscarEvolucoes(idPokemon)
        mensagem = '<div>Evoluções do Pokémon ID ' + str(idPokemon) + ':</div>'
        if len(lista) == 0:
            mensagem += "<div>Nenhuma evolução encontrada.</div>"
        
        for tupla in lista:
            mensagem += '<div>ID (Evolução): ' + str(tupla[0]) + ' | Nome: ' + str(tupla[2]) + '</div>'
        
        return mensagem    

def main():

    c = CRUD()
    despachante = cherrypy.dispatch.RoutesDispatcher()

    despachante.connect(name='adicionar', route='/pokedex', controller=c, 
                        action='adicionar', conditions=dict(method=['POST']))
    despachante.connect(name='buscar', route='/pokedex', controller=c, 
                        action='buscar', conditions=dict(method=['GET']))
    despachante.connect(name='buscar', route='/pokedex/:id', controller=c, 
                        action='buscar', conditions=dict(method=['GET']))
    despachante.connect(name='atualizar', route='/pokedex/:id', controller=c, 
                        action='atualizar', conditions=dict(method=['PUT']))
    despachante.connect(name='remover', route='/pokedex/:id', controller=c, 
                        action='remover', conditions=dict(method=['DELETE']))
    despachante.connect(name='adicionarEvolucao', route='/pokedex/:idPokemon/evolucoes', controller=c, 
                        action='adicionarEvolucao', conditions=dict(method=['POST']))
    despachante.connect(name='buscarEvolucoes', route='/pokedex/:idPokemon/evolucoes', controller=c, 
                        action='buscarEvolucoes', conditions=dict(method=['GET']))
    
    conf = {'/':{'request.dispatch':despachante}}
    cherrypy.tree.mount(root=None, config=conf)
    cherrypy.config.update({'server.socket_port':8080})
    cherrypy.engine.start()
    cherrypy.engine.block()

if __name__ == '__main__':
    main()