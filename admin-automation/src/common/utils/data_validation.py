import json
import csv
from functools import wraps
from common.utils.custom_errors import DateError, FileError


def handle_errors(fn):
    """
    Catches validation and TSV‐parsing errors and returns
    a proper API Gateway response dict.
    """

    @wraps(fn)
    def wrapper(event, context):
        try:
            return fn(event, context)
        except (DateError, FileError) as e:
            return {"statusCode": 400, "body": json.dumps({"message": str(e)})}
        except (UnicodeDecodeError, csv.Error) as e:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Invalid TSV format", "detail": str(e)}),
            }

    return wrapper
