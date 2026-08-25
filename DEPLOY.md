# Deploy do SGJP

## Requisitos

- Docker
- Docker Compose

## 1. Clonar o projeto

```bash
git clone <repositorio>
cd SGJP
```

## 2. Criar o .env

Copie o arquivo de exemplo:

```bash
cp .env.example .env
```

Preencha as credenciais de produção.

## 3. Subir os containers

```bash
docker compose up -d
```

## 4. Executar as migrations

```bash
docker compose exec web flask db upgrade
```

## 5. Criar administrador

```bash
docker compose exec web python seed.py
```