# Deploy do SGJP

## Requisitos

- Docker
- Docker Compose

## 1. Clonar o projeto

```bash
git clone <repositorio>
cd SGJP
```

## 2. Criar o arquivo de ambiente

Copie o arquivo de exemplo:

```bash
cp .env.example .env
```

Edite o `.env` e preencha as credenciais de produção (`SECRET_KEY`, `ADMIN_PASSWORD`, `POSTGRES_PASSWORD`, `DATABASE_URL`, etc.).

## 3. Iniciar os containers

```bash
docker compose up -d
```

## 4. Executar as migrations

```bash
docker compose exec web flask db upgrade
```

## 5. Criar o administrador inicial

```bash
docker compose exec web python seed.py
```

## 6. Verificar os containers

```bash
docker compose ps
```