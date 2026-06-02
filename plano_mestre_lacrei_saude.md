# 📄 PLANO MESTRE DE ARQUITETURA E DESENVOLVIMENTO
## Projeto: API RESTful de Gerenciamento de Consultas Médicas - Lacrei Saúde

---

## 1. VISÃO GERAL DO SISTEMA

Este projeto visa construir uma API robusta, segura e escalável para o gerenciamento de profissionais de saúde e suas respectivas consultas. A aplicação serve como base fundamental para as operações da Lacrei Saúde, projetada para ser integrada futuramente com sistemas de pagamento e outras ferramentas internas. O foco principal é a entrega de código de alta qualidade, adoção de boas práticas de segurança, e a preparação completa do ambiente para produção, garantindo impacto social através da tecnologia.

### 1.1 Stack Tecnológica Escolhida
* **Backend Framework:** Python com Django & Django REST Framework (DRF).
* **Gerenciamento de Dependências:** Poetry.
* **Banco de Dados:** PostgreSQL.
* **Containerização:** Docker e Docker Compose.
* **CI/CD:** GitHub Actions.
* **Infraestrutura Cloud:** AWS (Ambientes de Staging e Produção).
* **Testes:** `APITestCase` do Django.
* **Documentação (Opcional/Bônus):** Swagger / drf-spectacular.

---

## 2. REQUISITOS E REGRAS DE NEGÓCIO

A API deve garantir o gerenciamento eficiente e seguro dos dados dos profissionais e suas agendas.

### 2.1 Entidades Principais
1.  **Profissionais da Saúde:**
    * Campos obrigatórios: Nome social, Profissão, Endereço, Contato.
2.  **Consultas:**
    * Campos obrigatórios: Data/Hora, Profissional vinculado (Chave Estrangeira - FK).

### 2.2 Requisitos de Segurança e Validação
* Retorno de dados estritamente em formato **JSON**.
* Sanitização robusta de inputs e validação de dados nas requisições.
* Proteção contra vulnerabilidades comuns, especialmente SQL Injection.
* Configuração rigorosa de CORS (Cross-Origin Resource Sharing).
* Implementação de Autenticação (Ex: JWT via `djangorestframework-simplejwt` ou Token nativo).
* Sistema de logs estruturados para auditoria de acessos e erros.

---

## 3. MODELAGEM DO BANCO DE DADOS (PostgreSQL)

```text
┌────────────────────────┐       ┌────────────────────────┐
│     professionals      │       │     appointments       │
├────────────────────────┤       ├────────────────────────┤
│ id (PK) UUID           │◄──────│ id (PK) UUID           │
│ social_name VARCHAR    │       │ professional_id (FK)   │
│ profession VARCHAR     │       │ appointment_date TS    │
│ address TEXT           │       │ patient_name VARCHAR   │
│ contact VARCHAR        │       │ status ENUM            │
│ created_at TS          │       │ created_at TS          │
│ updated_at TS          │       │ updated_at TS          │
└────────────────────────┘       └────────────────────────┘
```

---

## 4. ENDPOINTS DA API RESTful

A API seguirá os padrões REST para manipulação dos recursos.

### 4.1 Autenticação (`/api/auth/`)
* `POST /login/`: Retorna os tokens de acesso (ex: JWT) mediante credenciais válidas.
* `POST /refresh/`: Atualiza o token de acesso expirado.

### 4.2 Profissionais (`/api/professionals/`)
* `GET /`: Lista todos os profissionais cadastrados (com paginação).
* `POST /`: Cria um novo registro de profissional.
* `GET /{id}/`: Recupera os detalhes de um profissional específico.
* `PUT / PATCH /{id}/`: Atualiza dados de um profissional.
* `DELETE /{id}/`: Remove um profissional do sistema.

### 4.3 Consultas (`/api/appointments/`)
* `GET /`: Lista todas as consultas cadastradas (com paginação e filtros).
* `POST /`: Agenda uma nova consulta vinculando a um profissional.
* `GET /{id}/`: Recupera detalhes de uma consulta.
* `PUT / PATCH /{id}/`: Atualiza o status ou dados de uma consulta.
* `DELETE /{id}/`: Cancela/Remove uma consulta.
* `GET /by-professional/{professional_id}/`: Busca otimizada de consultas vinculadas a um ID de profissional específico.

---

## 5. ESTRUTURA DE DIRETÓRIOS DO PROJETO

```text
lacrei-saude-api/
├── .github/
│   └── workflows/
│       └── ci-cd.yml          # Pipeline do GitHub Actions (Lint, Test, Build, Deploy)
├── app/
│   ├── core/                  # Configurações do Django (settings, wsgi, asgi, urls globais)
│   ├── professionals/         # App: Modelos, Views, Serializers, Tests para Profissionais
│   ├── appointments/          # App: Modelos, Views, Serializers, Tests para Consultas
│   └── authentication/        # App: Configurações de JWT/Tokens e rotas de login
├── docker/
│   ├── entrypoint.sh          # Script de inicialização (migrations, collectstatic)
│   └── Dockerfile             # Configuração da imagem da aplicação
├── pyproject.toml             # Gerenciamento de dependências via Poetry
├── poetry.lock                # Lockfile de dependências
├── docker-compose.yml         # Orquestração do PostgreSQL e aplicação
├── manage.py                  # Entrypoint do Django
├── .env.example               # Template de variáveis de ambiente
└── README.md                  # Documentação completa do projeto
```

---

## 6. PIPELINE CI/CD (GitHub Actions)

A esteira de integração e entrega contínua garantirá a qualidade do código antes de chegar aos ambientes da AWS.

### 6.1 Etapas do Workflow (`ci-cd.yml`)
1.  **Checkout:** Clonagem do repositório.
2.  **Setup Python & Poetry:** Instalação do ambiente e gerenciador.
3.  **Linting:** Verificação de padrões de código (usando `flake8` ou `black`).
4.  **Testes:** Execução da suíte de testes Django (`python manage.py test`) cobrindo cenários de sucesso e falhas (APITestCase).
5.  **Build:** Construção da imagem Docker.
6.  **Deploy Staging (AWS):** Implantação automática quando há merge na branch `develop`.
7.  **Deploy Production (AWS):** Implantação quando há merge/release na branch `main`.

---

## 7. DOCUMENTAÇÃO E ENTREGÁVEIS

O `README.md` será o guia principal do projeto e deverá conter:

1.  **Instruções de Setup Local:** Como clonar o repositório, instalar o Poetry, configurar o `.env` e rodar as migrações localmente.
2.  **Setup via Docker:** Como utilizar o `docker-compose up` para subir a aplicação e o banco de dados com um único comando.
3.  **Execução de Testes:** Comando exato para rodar os testes utilizando o `APITestCase` com informações sobre cobertura mínima garantida.
4.  **Decisões Técnicas:** Breve justificativa sobre as escolhas arquiteturais (ex: por que JWT, qual ferramenta de linting escolhida).
5.  **Fluxo de Deploy (CI/CD):** Explicação da esteira configurada no GitHub Actions e os ambientes da AWS.
6.  **Estratégia de Rollback:** Proposta documentada de como reverter um deploy em caso de falhas críticas (ex: Blue/Green Deployment na AWS, Revert via GitHub Actions e restore de snapshots do DB).

---

## 8. BÔNUS RECOMENDADOS (Diferenciais)

* **Integração Asaas (Proposta):** Documentar no README ou criar um módulo mockado (`payments/`) demonstrando a arquitetura de split de pagamento (ex: Webhooks para recebimento de confirmação de pagamento de consultas).
* **Documentação Viva:** Implementar `drf-spectacular` ou `drf-yasg` para gerar uma interface Swagger/Redoc acessível via `/api/docs/`.

---

## 9. CRONOGRAMA DE EXECUÇÃO (5 DIAS ÚTEIS)

O planejamento foi dividido em etapas incrementais para garantir a entrega de todos os requisitos obrigatórios dentro do prazo estabelecido.

### Dia 1 — Estrutura Inicial e Ambiente

#### Objetivos

* Configuração do repositório GitHub
* Criação do projeto Django
* Configuração do Poetry
* Configuração do PostgreSQL
* Configuração do Docker e Docker Compose
* Criação da estrutura base do projeto

#### Entregáveis

* Projeto inicial funcionando
* Banco PostgreSQL conectado
* Containers Docker funcionando
* Primeiro commit estruturado

---

### Dia 2 — Desenvolvimento dos CRUDs

#### Objetivos

* Implementação da entidade Professional
* Implementação da entidade Appointment
* Criação dos serializers
* Criação dos ViewSets
* Configuração das rotas REST
* Implementação da busca de consultas por profissional

#### Entregáveis

* CRUD completo de profissionais
* CRUD completo de consultas
* Filtro por profissional funcionando

---

### Dia 3 — Segurança e Qualidade

#### Objetivos

* Implementação de autenticação JWT
* Configuração de permissões
* Configuração de CORS
* Validações de entrada
* Sanitização dos dados
* Configuração de logs de acesso e erros

#### Entregáveis

* API protegida por autenticação
* Validações implementadas
* Logs configurados
* Requisitos de segurança atendidos

---

### Dia 4 — Testes Automatizados e Documentação da API

#### Objetivos

* Implementação dos testes APITestCase
* Testes de CRUD de profissionais
* Testes de CRUD de consultas
* Testes de cenários de erro
* Configuração do Swagger (drf-spectacular)

#### Entregáveis

* Suíte de testes funcionando
* Cobertura dos cenários obrigatórios
* Documentação Swagger disponível

---

### Dia 5 — CI/CD, Deploy e Documentação Final

#### Objetivos

* Configuração do GitHub Actions
* Pipeline de Lint
* Pipeline de Testes
* Build da imagem Docker
* Deploy para ambiente Staging
* Deploy para ambiente Produção
* Finalização do README
* Revisão geral do projeto

#### Entregáveis

* Pipeline CI/CD funcional
* Deploy realizado
* README completo
* Projeto pronto para entrega

---

### Buffer de Risco

Caso alguma etapa atrase, a prioridade de entrega será:

1. CRUDs completos
2. Segurança (JWT, CORS, validações)
3. Docker + PostgreSQL
4. Testes automatizados
5. GitHub Actions
6. Deploy AWS
7. Swagger e itens bônus

Dessa forma, os requisitos obrigatórios permanecem garantidos mesmo diante de imprevistos durante o desenvolvimento.
