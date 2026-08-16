from pydantic import BaseModel, Field

class RawObservation(BaseModel):
    problem_summary: str = Field(description="Crisp description of the core workflow bottleneck or manual chore.")
    target_persona: str = Field(description="Specific role experiencing the pain (e.g., Shopify merchant, QA engineer).")
    current_workaround: str = Field(description="Clumsy workaround or manual steps currently used.")
    urgency_level: int = Field(description="1 (mild annoyance) to 5 (costing real money/hours).")

class ObservationList(BaseModel):
    observations: list[RawObservation]

class IdeaMatrixEvaluation(BaseModel):
    concept_title: str
    target_user: str
    problem_addressed: str
    proposed_solution_hypothesis: str
    
    # 5-Point Matrix (1 to 5 each)
    frequency_score: int = Field(description="1 (rare/annual) to 5 (daily/hourly).")
    budget_desperation_score: int = Field(description="1 (free only) to 5 (wasting payroll / already paying for hacky tools).")
    distribution_access_score: int = Field(description="1 (inaccessible enterprise) to 5 (clear hangouts, easy cold outreach).")
    technical_leverage_score: int = Field(description="1 (complex multi-month build) to 5 (1-2 week MVP using modern APIs).")
    switching_friction_score: int = Field(description="1 (replaces whole tech stack) to 5 (drop-in extension/standalone hook).")
    
    total_score: int = Field(description="Sum of all 5 scores (Max 25).")
    verdict: str = Field(description="Must be 'PASS' or 'KILL'.")
    kill_reason: str | None = Field(default=None, description="Explanation if killed.")
