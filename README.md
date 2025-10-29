# API RESTful de Pokédex com CherryPy

Este projeto implementa um servidor web simples usando **CherryPy** que expõe uma API RESTful para realizar operações CRUD (Criar, Ler, Atualizar, Deletar) em um banco de dados de Pokémons.

O servidor é estruturado em duas camadas principais:
* `crudServer.py`: A camada de API (controlador) que usa CherryPy para definir as rotas, lidar com as requisições HTTP e tratar os erros.
* `banco.py`: A camada de acesso a dados (modelo) que gerencia a conexão com um banco de dados **SQLite** (`pokedex.db`) e executa as consultas SQL.

## Recursos Principais

* **API RESTful:** Utiliza verbos HTTP (`GET`, `POST`, `PUT`, `DELETE`) para operações em dois recursos: Pokémon e Evoluções.
* **Banco de Dados SQLite:** Armazena os dados no arquivo local `pokedex.db`.
* **Gerenciamento de Recursos Aninhados:** É possível gerenciar "Evoluções" como um sub-recurso de um "Pokémon" (ex: `/pokedex/1/evolucoes`).
* **Integridade Referencial:** O banco de dados está configurado com `PRAGMA foreign_keys = ON` e utiliza chaves estrangeiras com `ON DELETE CASCADE`. Isso garante que, ao deletar um Pokémon, todas as suas evoluções associadas também sejam removidas automaticamente.
* **Tratamento de Erros:** A API retorna códigos de status HTTP apropriados (como 400, 404, 422) para solicitações inválidas ou recursos não encontrados.

## Estrutura do Banco de Dados

O `banco.py` gerencia duas tabelas:

1.  **`pokedex`**:
    * `id` (INTEGER PRIMARY KEY)
    * `nome`
    * `tipo`
    * `genero`
    * `altura`
    * `peso`

2.  **`evolucoes`**:
    * `id` (INTEGER PRIMARY KEY)
    * `idPokemon` (INTEGER, REFERENCES `pokedex(id)` ON DELETE CASCADE)
    * `nome_evolucao` (TEXT)

## Endpoints da API

O servidor (`crudServer.py`) expõe as seguintes rotas:

| Verbo HTTP | Rota | Controlador | Ação |
| :--- | :--- | :--- | :--- |
| `POST` | `/pokedex` | `adicionar` | Adiciona um novo Pokémon. |
| `GET` | `/pokedex` | `buscar` | Lista todos os Pokémon. |
| `GET` | `/pokedex/:id` | `buscar` | Busca um Pokémon específico pelo ID. |
| `PUT` | `/pokedex/:id` | `atualizar` | Atualiza um Pokémon (requer todos os campos). |
| `DELETE` | `/pokedex/:id` | `remover` | Remove um Pokémon pelo ID. |
| `POST` | `/pokedex/:idPokemon/evolucoes` | `adicionarEvolucao` | Adiciona uma nova evolução a um Pokémon. |
| `GET` | `/pokedex/:idPokemon/evolucoes` | `buscarEvolucoes` | Lista todas as evoluções de um Pokémon. |

## Como Executar

1.  Certifique-se de ter as bibliotecas `cherrypy` e `sqlite3` (geralmente inclusa no Python) instaladas.
2.  Execute o servidor:
    ```bash
    python crudServer.py
    ```
3.  O servidor estará disponível em `http://localhost:8080`.
