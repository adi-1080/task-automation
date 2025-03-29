from pydantic import BaseModel, Field, RootModel
from typing import Dict, List, Optional

class BudgetBreakdown(RootModel):
    """
    Flexible budget breakdown structure using RootModel
    Example: {"materials": 5000, "labor": 3000}
    """
    root: Dict[str, float] = Field(
        ...,
        example={"materials": 5000, "labor": 3000},
        description="Key-value pairs of budget categories and amounts"
    )

class BudgetEstimate(BaseModel):
    """
    Detailed budget estimation for a subtask
    """
    amount: float = Field(
        ...,
        gt=0,
        example=8000.0,
        description="Total estimated amount for this subtask"
    )
    breakdown: BudgetBreakdown = Field(
        ...,
        description="Detailed cost breakdown by category"
    )
    currency: str = Field(
        "INR",
        example="INR",
        description="Currency code (ISO 4217)"
    )

class SubtaskAssignment(BaseModel):
    """
    Detailed breakdown of a subtask with budget estimation
    """
    subtask: str = Field(
        ...,
        example="Venue Setup",
        description="Description of the subtask"
    )
    department: str = Field(
        ...,
        example="logistics",
        description="Department responsible for this subtask"
    )
    instructions: str = Field(
        ...,
        example="Arrange chairs and audio equipment",
        description="Specific actions needed to complete the subtask"
    )
    estimated_time: str = Field(
        ...,
        example="2 days",
        description="Human-readable time estimate"
    )
    estimated_budget: BudgetEstimate = Field(
        ...,
        description="Detailed budget estimation for this subtask"
    )

class TotalBudget(BaseModel):
    """
    Consolidated budget for the entire task
    """
    amount: float = Field(
        ...,
        gt=0,
        example=30000.0,
        description="Total estimated budget for all subtasks"
    )
    breakdown: BudgetBreakdown = Field(
        ...,
        example={"venue": 10000, "catering": 20000},
        description="Budget distribution by department/category"
    )

class TaskRequest(BaseModel):
    """
    Input structure for task analysis request
    """
    task: str = Field(
        ...,
        example="Organize college fest",
        description="Main task description to analyze"
    )
    departments: List[str] = Field(
        ...,
        example=["logistics", "finance", "marketing"],
        description="Available departments for task assignment"
    )
    currency: Optional[str] = Field(
        "INR",
        example="USD",
        description="Preferred currency for budget estimates"
    )

class TaskResponse(BaseModel):
    """
    Complete task breakdown with budget analysis
    """
    main_task: str = Field(
        ...,
        example="Organize college fest",
        description="Original task description"
    )
    currency: str = Field(
        ...,
        example="INR",
        description="Currency used for all budget estimates"
    )
    assignments: List[SubtaskAssignment] = Field(
        ...,
        description="List of subtasks with detailed assignments"
    )
    total_budget: TotalBudget = Field(
        ...,
        description="Consolidated budget for the entire task"
    )

class ErrorResponse(BaseModel):
    """
    Standard error response format
    """
    success: bool = Field(False, example=False)
    error: str = Field(
        ...,
        example="Invalid department specified",
        description="Error description"
    )
    details: Optional[Dict] = Field(
        None,
        example={"invalid_departments": ["security"]},
        description="Additional error context"
    )