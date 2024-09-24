from dataclasses import dataclass
from typing import Optional

from errors.common_error import CommonError


@dataclass
class CommonResult:
    is_success: bool
    error: Optional[CommonError] = None
