from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime
from pathlib import Path


class CompoundIDProjection(BaseModel):
    compound_id: str = Field(...)        

class CompoundEntry(BaseModel):
    compound: Link[Compound]
    compound_id: str
    quantity: float
    quantity_type: Literal["weight_percent", "volume_percent", "moles"]  


class InputCompoundEntry(BaseModel):
    compound_id: str
    quantity: float
    quantity_type: Literal["weight_percent", "volume_percent", "moles"]  

class InputFormulation(BaseModel):
    description: str
    formulation: list[InputCompoundEntry]
    CE: Optional[float] = Field(default=None, ge = 0, le = 100.0)
    LCE: Optional[float] = Field(default=None, ge = 0)
    cycle: Optional[int] = Field(default=None, ge = 0)
    current: Optional[float] = Field(default=None, ge = 0)
    capacity: Optional[float] = Field(default=None, ge = 0)
    
class ElementRatio(BaseModel):
    FC: float = Field(..., ge=0)
    OC: float = Field(..., ge=0)
    FO: float = Field(..., ge=0)
    InOr: float = Field(..., ge=0)
    F: float = Field(..., ge=0)
    sF: float = Field(..., ge=0)
    aF: float = Field(..., ge=0)
    O: float = Field(..., ge=0)
    sO: float = Field(..., ge=0)
    aO: float = Field(..., ge=0) 
    C: float = Field(..., ge=0)
    sC: float = Field(..., ge=0)
    aC: float = Field(..., ge=0)


class PreparationFormulationList(BaseModel):
    formulations: list[PreparationFormulation]

class PreparationFormulationListPagination(PreparationFormulationList):
    page: int = Field(ge=1, default=1)
    has_more: bool    

class UpdateFormulation(BaseModel):
    description: Optional[str] = None
    formulation: Optional[list[InputCompoundEntry]] = None 
    CE: Optional[float] = Field(default=None, ge = 0, le = 100.0)
    LCE: Optional[float] = Field(default=None, ge = 0)
    cycle: Optional[int] = Field(default=None, ge = 0)
    current: Optional[float] = Field(default=None, ge = 0)
    capacity: Optional[float] = Field(default=None, ge = 0)     




class MLFormulationList(BaseModel):
    formulations: list[MLFormulation]

class MLFormulationListPagination(MLFormulationList):
    page: int = Field(ge=1, default=1)
    has_more: bool        



