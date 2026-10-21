"""Small helpers every client shares: status checks, model parsing and reachability."""

import requests
from pydantic import BaseModel, ValidationError

from framework.core.redaction import redact_text


class UnexpectedStatusError(AssertionError):
    """A call answered with a status the caller did not expect."""


class ContractViolationError(AssertionError):
    """A response body did not match its model."""


def expect(response: requests.Response, *statuses: int) -> requests.Response:
    """Returns the response if its status is one of `statuses`, else fails with the details."""
    if response.status_code not in statuses:
        raise UnexpectedStatusError(
            f"{response.request.method} {redact_text(response.url)} answered "
            f"{response.status_code}, expected {' or '.join(map(str, statuses))}: "
            f"{redact_text(response.text[:500])}"
        )
    return response


def parse[M: BaseModel](response: requests.Response, model: type[M]) -> M:
    """The body as `model`; a mismatch is a contract violation that names every field."""
    try:
        return model.model_validate_json(response.content)
    except ValidationError as error:
        raise ContractViolationError(
            f"{response.request.method} {redact_text(response.url)} ({response.status_code}) "
            f"does not match {model.__name__}:\n{error}"
        ) from error


def reachable(health_url: str, timeout: float = 3.0) -> bool:
    """Whether a self-hosted service answers its health check (tests skip when it does not)."""
    try:
        return requests.get(health_url, timeout=timeout).status_code == 200
    except requests.RequestException:
        return False
