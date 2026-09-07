from pydantic import BaseModel, Field

from typing_extensions import Literal


class Failure_Anaylsis_outputs(BaseModel):
    classification: Literal[
        "application_bug",
        "test_bug",
        "environment_issue",
        "flaky_test",
        "unknown",
    ]

    confidence: float = Field(
        ge=0,
        le=1,
    )

    root_cause: str

    evidence: list[str]

    recommendation: list[str]
