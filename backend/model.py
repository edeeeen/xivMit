#################################################################
#                     Pydantic Models                           #
#################################################################
from pydantic import BaseModel, Field, RootModel
from typing import Optional, List, Dict



####################### Templates #######################

# Base model for templtes
class TemplateBase(BaseModel):
    name: str = Field(..., description="Template Name.")
    fight: str = Field(..., description="A string representing a 'fight' identifier (e.g., 'M5S')")
    user: str = Field(..., description="The name of the user who created the template")
    description: Optional[str] = Field(None, description="An optional description for the template")
    bookmarks: int = Field(0, ge=0, description="The number of bookmarks for the template (non-negative)")
    views: int = Field(0, ge=0, description="The number of views for the template (non-negative)")

# create model
class TemplateCreate(TemplateBase):
    id: str = Field(..., description="A unique identifier for the template")

# return model
class TemplateResponse(TemplateCreate):
    pass

####################### Encounters #######################

# base model for an encounter, defining common fields
class EncounterBase(BaseModel):
    shorthand: str = Field(..., description="A short identifier for the encounter (e.g., 'M5S')")
    boss: str = Field(..., description="The name of the boss/fight")
    imgLink: str = Field(..., description="Link to an image associated with the encounter")
    category: str = Field(..., description="The category/tier of the encounter (e.g., 'Cruiserweight')")

# return model
class EncounterResponse(EncounterBase):
    id: int = Field(..., description="The auto-generated database ID for the encounter")
    pass

# Model for individual fights
class EncounterDetail(BaseModel):
    shorthand: str
    boss: str
    imgLink: str

# This defines a dictionary where keys are strings and values are lists of EncounterDetail objects
class CategorizedEncounterResponse(RootModel[Dict[str, List[EncounterDetail]]]):   
    pass