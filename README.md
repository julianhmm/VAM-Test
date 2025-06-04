# Vertrags Asset Manager

This repository contains a minimal prototype for managing contracts and assets.

## Setup

Install requirements:

```bash
pip install -r requirements.txt
```

## Run backend

```bash
uvicorn backend.main:app --reload
```

## Run frontend

```bash
streamlit run frontend/app.py
```

The backend stores data in a local SQLite database `vam.db`.
