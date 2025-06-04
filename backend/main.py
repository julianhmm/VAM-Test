from fastapi import FastAPI
from sqlmodel import select
from sqlalchemy.orm import selectinload
from .database import init_db, get_session
from .models import Contract, Asset, ContractAssetLink, ContractRead
from typing import List
import pandas as pd
from fastapi.responses import StreamingResponse
from io import BytesIO

app = FastAPI()

init_db()

@app.post("/contracts", response_model=Contract)
def create_contract(contract: Contract):
    with get_session() as session:
        session.add(contract)
        session.commit()
        session.refresh(contract)
        return contract

@app.get("/contracts", response_model=List[ContractRead])
def list_contracts():
    with get_session() as session:
        contracts = session.exec(
            select(Contract).options(selectinload(Contract.assets))
        ).unique().all()
        return contracts

@app.post("/assets", response_model=Asset)
def create_asset(asset: Asset):
    with get_session() as session:
        session.add(asset)
        session.commit()
        session.refresh(asset)
        return asset

@app.get("/assets", response_model=List[Asset])
def list_assets():
    with get_session() as session:
        assets = session.exec(select(Asset)).all()
        return assets

@app.get("/export/contracts/xlsx")
def export_contracts_xlsx():
    with get_session() as session:
        contracts = session.exec(select(Contract)).all()
        df = pd.DataFrame([c.dict() for c in contracts])
        buf = BytesIO()
        df.to_excel(buf, index=False)
        buf.seek(0)
        return StreamingResponse(buf, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": "attachment; filename=contracts.xlsx"})

@app.get("/export/assets/xlsx")
def export_assets_xlsx():
    with get_session() as session:
        assets = session.exec(select(Asset)).all()
        df = pd.DataFrame([a.dict() for a in assets])
        buf = BytesIO()
        df.to_excel(buf, index=False)
        buf.seek(0)
        return StreamingResponse(buf, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": "attachment; filename=assets.xlsx"})
