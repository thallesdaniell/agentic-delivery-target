# agentic-delivery-target

Repositório-alvo do [agentic-delivery-lab](https://github.com/thallesdaniell/agentic-delivery-lab): uma API de tarefas pequena, em Python, onde os agentes do lab abrem os pull requests. Cada PR passa pelo mesmo CI obrigatório que qualquer mudança feita por uma pessoa, e o merge é sempre humano.

> Projeto demonstrativo. A API guarda tudo em memória e existe só para dar ao agente um código real, com testes, para trabalhar.

## O que tem aqui

- API HTTP de tarefas com FastAPI: listar, criar, consultar e concluir.
- Testes com `pytest` e lint e formatação com `ruff`.
- CI no GitHub Actions com dois checks obrigatórios, `lint` e `test`, e branch protection na `main`: nada entra sem PR e sem CI verde.

## Endpoints

| Método | Rota | O que faz |
|---|---|---|
| `GET` | `/health` | Confirma que a aplicação está no ar |
| `GET` | `/tasks` | Lista as tarefas |
| `POST` | `/tasks` | Cria uma tarefa (`{"title": "..."}`) |
| `GET` | `/tasks/{id}` | Consulta uma tarefa |
| `POST` | `/tasks/{id}/done` | Marca uma tarefa como concluída |
| `DELETE` | `/tasks/{id}` | Remove uma tarefa (204 sem corpo; 404 se não existir) |

## Executar localmente

Requisitos: [uv](https://docs.astral.sh/uv/). Ele instala o Python 3.12 se for preciso.

```sh
uv sync
uv run uvicorn tasks_api.app:app --reload
```

A API sobe em http://localhost:8000, com a documentação interativa em http://localhost:8000/docs.

## Rodar os mesmos checks do CI

```sh
uv run ruff check .
uv run ruff format --check .
uv run pytest
```

## Regras para quem contribui, pessoa ou agente

- Toda mudança entra por pull request, com `lint` e `test` verdes.
- Comportamento novo vem com teste.
- O agente do lab não tem permissão para alterar `.github/workflows/`: o CI que o avalia não pode ser mudado por ele.

## Licença

[MIT](LICENSE)
