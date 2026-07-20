# Sistema de Gestão de Academia

Projeto full stack com **Python + Flask** no backend e **HTML, CSS, JavaScript e Plotly** no frontend. A aplicação permite o cadastro de clientes (CRUD completo), exportação de dados em CSV e visualização de gráficos interativos sobre a base de alunos.

## Funcionalidades

- Cadastro, edição, listagem e exclusão de clientes (CRUD)
- Exportação dos dados para CSV
- Dashboard com gráficos interativos (Plotly)

## Cadastro de Clientes

| Campo              | Tipo      | Descrição                                       |
|--------------------|-----------|-------------------------------------------------|
| `id`               | Integer   | Identificador único do cliente                  |
| `telefone`         | Integer   | Telefone do Cliente                             |
| `data_matricula`   | Date      | Data de matricula do cliente                    |
| `nome`             | String    | Nome completo do cliente                        |
| `unidade`          | String    | Unidade da academia onde o cliente está matriculado |
| `plano`            | String    | Plano contratado (mensal, trimestral, anual...)  |
| `idade`            | Integer   | Idade do Cliente                                 |
| `objetivo`         | String    | Objetivo do aluno (emagrecimento, hipertrofia, condicionamento...) |

## Gráficos Planejados

- Distribuição de clientes por unidade
- Distribuição por plano contratado
- Proporção de clientes por mês de matricula
- Distribuição por faixa etária


## Tecnologias

- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, JavaScript
- **Visualização:** Plotly
- **Dados:** CSV / exportação de relatórios