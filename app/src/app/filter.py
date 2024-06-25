from datetime import datetime, timezone
from typing import Any, Optional

from dateparser import parse


class Filter:
    date_from: Optional[datetime] = None

    def __init__(self, from_: Optional[str], error_codes: list[str], error_only: bool):
        self.date_from = _parrse_datetime(from_)
        self.error_codes = error_codes
        self.error_only = error_only

    def match(self, record: Any) -> bool:
        at = datetime.fromisoformat(record["eventTime"])

        if self.error_only:
            if "errorCode" not in record:
                return False

        if not self.error_codes == []:
            if not any(record.get("errorCode") == code for code in self.error_codes):
                return False

        if self.date_from is not None:
            if not self.date_from <= at:
                return False

        return True

    def match_s3_object(self, s3_object: dict[str, Any]) -> bool:
        at = s3_object["LastModified"]

        if self.date_from is not None:
            if not self.date_from <= at:
                return False

        return True


def _parrse_datetime(date_string: Optional[str]) -> Optional[datetime]:
    if date_string is None:
        return None
    result = parse(date_string)
    assert result is not None
    return result.astimezone(timezone.utc)
