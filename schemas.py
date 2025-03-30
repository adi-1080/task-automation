from pydantic import BaseModel, Field, RootModel, validator
from typing import Dict, List, Optional, Literal
import json

class PosterTheme(BaseModel):
    name: str = Field(..., example="Community Unity")
    description: Optional[str] = Field(None, example="People coming together")

# class PosterRequest(BaseModel):
#     theme: PosterTheme
#     style: Literal["modern", "vintage", "minimalist", "abstract"] = Field(..., example="modern")
#     color_palette: List[str] = Field(..., example=["#FF5733", "#33FF57", "#3357FF"])
#     elements: List[Literal["people", "nature", "buildings", "abstract"]] = Field(..., example=["people", "nature"])
#     mood: Literal["joyful", "serious", "inspirational", "calm"] = Field(..., example="joyful")
#     text_placement: Literal["top", "center", "bottom", "left", "right"] = Field(..., example="center")
#     additional_notes: Optional[str] = Field(None, example="Include diverse age groups")
class PosterRequest(BaseModel):
    theme: PosterTheme
    style: Literal[
        "modern", 
        "vintage", 
        "minimalist", 
        "abstract",
        "cyberpunk",
        "watercolor",
        "3d-rendered",
        "photorealistic",
        "comic-book",
        "retro"
    ] = Field(..., example="modern", description="Select from 10 artistic styles")
    
    color_palette: List[str] = Field(
        ...,
        example=["#FF5733", "#33FF57", "#3357FF"],
        description="List of HEX color codes (2-5 colors)",
        min_items=2,
        max_items=5
    )
    
    elements: List[Literal[
        "people",
        "nature",
        "buildings",
        "abstract",
        "technology",
        "animals",
        "food",
        "vehicles",
        "space",
        "music"
    ]] = Field(
        ...,
        example=["people", "technology"],
        description="Select 2-5 visual elements to include",
        min_items=2,
        max_items=5
    )
    
    mood: Literal[
        "joyful",
        "serious",
        "inspirational",
        "calm",
        "energetic",
        "mysterious",
        "futuristic",
        "romantic",
        "humorous",
        "dramatic"
    ] = Field(..., example="joyful", description="Overall emotional tone")
    
    text_placement: Literal[
        "top", 
        "center", 
        "bottom", 
        "left", 
        "right",
        "diagonal",
        "floating",
        "framed",
        "scattered"
    ] = Field(..., example="center", description="How text should be integrated")
    
    lighting: Literal[
        "natural",
        "studio",
        "neon",
        "sunset",
        "moody",
        "backlit",
        "high-contrast"
    ] = Field("natural", example="natural", description="Lighting style")
    
    composition: Literal[
        "symmetrical",
        "rule-of-thirds",
        "central",
        "diagonal",
        "grid",
        "freeform"
    ] = Field("rule-of-thirds", example="rule-of-thirds")
    
    additional_notes: Optional[str] = Field(
        None,
        example="Include QR code in bottom right",
        description="Any special requests not covered above"
    )

class CloudinaryResponse(BaseModel):
    url: str
    public_id: str
    width: int
    height: int
    format: str

class PosterResponse(BaseModel):
    original_prompt: str
    enhanced_prompt: str
    variations: List[CloudinaryResponse]

# class BudgetBreakdown(RootModel):
#     root: Dict[str, float] = Field(
#         ...,
#         example={"materials": 5000, "labor": 3000},
#         description="Key-value pairs of budget categories and amounts"
#     )

# class BudgetEstimate(BaseModel):
#     amount: float = Field(..., gt=0, example=8000.0)
#     breakdown: BudgetBreakdown
#     currency: str = Field("INR", example="INR")

# class SubtaskAssignment(BaseModel):
#     subtask: str = Field(..., example="Venue Setup")
#     department: str = Field(..., example="logistics")
#     instructions: str = Field(..., example="Arrange chairs and audio equipment")
#     estimated_time: str = Field(..., example="2 days")
#     estimated_budget: BudgetEstimate
import json

class BudgetBreakdown(RootModel):
    root: Dict[str, float] = Field(
        ...,
        example={"materials": 5000, "labor": 3000},
        description="Key-value pairs of budget categories and amounts"
    )

class BudgetEstimate(BaseModel):
    amount: float = Field(
        ..., 
        gt=0, 
        example=8000.0,
        description="Must be positive value greater than 0"
    )
    breakdown: BudgetBreakdown
    currency: str = Field("INR", example="INR")

    @validator('amount')
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError("Budget amount must be greater than 0")
        return round(v, 2)  # Ensure clean decimal values

class SubtaskAssignment(BaseModel):
    subtask: str = Field(..., example="Venue Setup")
    department: str = Field(..., example="logistics")
    instructions: str = Field(..., example="Arrange chairs and audio equipment")
    estimated_time: str = Field(..., example="2 days")
    estimated_budget: BudgetEstimate

class TotalBudget(BaseModel):
    amount: float = Field(..., gt=0, example=30000.0)
    breakdown: BudgetBreakdown

class TaskRequest(BaseModel):
    task: str = Field(..., example="Organize college fest")
    departments: List[str] = Field(..., example=["logistics", "finance"])
    currency: Optional[str] = Field("INR", example="USD")

class TaskResponse(BaseModel):
    main_task: str = Field(..., example="Organize college fest")
    currency: str = Field(..., example="INR")
    assignments: List[SubtaskAssignment]
    total_budget: TotalBudget

class ErrorResponse(BaseModel):
    success: bool = Field(False, example=False)
    error: str = Field(..., example="Invalid department specified")
    details: Optional[Dict] = Field(None, example={"invalid_departments": ["security"]})