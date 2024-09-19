from dataclasses import dataclass

@dataclass
class CommonError:
    code: int
    message: str