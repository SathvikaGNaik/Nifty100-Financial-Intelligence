from dataclasses import dataclass

@dataclass
class ValidationFailure:

    rule_id: str
    severity: str
    table: str
    company_id: str
    year: str
    message: str