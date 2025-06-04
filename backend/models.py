from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
import datetime

class ContractAssetLink(SQLModel, table=True):
    contract_id: Optional[int] = Field(default=None, foreign_key="contract.id", primary_key=True)
    asset_id: Optional[int] = Field(default=None, foreign_key="asset.id", primary_key=True)

class Contract(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    contract_date: datetime.date
    supplier: str
    description: str
    end_date: datetime.date
    auto_extend: bool = False
    notice_period_days: int
    assets: List["Asset"] = Relationship(back_populates="contracts", link_model=ContractAssetLink)

class Asset(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    vendor: str
    purchase_date: datetime.date
    eol: datetime.date
    info: str
    contracts: List[Contract] = Relationship(back_populates="assets", link_model=ContractAssetLink)
