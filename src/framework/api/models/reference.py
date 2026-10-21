"""The API flagship's reference service, as its OpenAPI document describes it (`/openapi.yaml`).
Only the operations this repository calls; strict, like the provider's own schemas.
"""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

Region = Literal["in", "eu", "us"]


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, populate_by_name=True)


class Token(_Strict):
    access_token: str = Field(alias="accessToken", min_length=20)
    token_type: Literal["Bearer"] = Field(alias="tokenType")
    expires_in: int = Field(alias="expiresIn", ge=1)
    account_id: str = Field(alias="accountId", pattern=r"^acc_")


class Account(_Strict):
    id: str = Field(pattern=r"^acc_")
    handle: str
    display_name: str = Field(alias="displayName")
    region: Region
    role: Literal["user", "admin"]
    created_at: datetime = Field(alias="createdAt")


class Balance(_Strict):
    balance: int = Field(ge=0)
    currency: Literal["credits"]
    account_id: str = Field(alias="accountId", pattern=r"^acc_")


class Purchase(_Strict):
    id: str = Field(pattern=r"^pur_")
    pack_id: Literal["pack-10", "pack-50"] = Field(alias="packId")
    credits: int = Field(ge=1)
    balance_after: int = Field(alias="balanceAfter", ge=0)
    created_at: datetime = Field(alias="createdAt")


class FieldError(_Strict):
    field: str
    message: str


class Problem(_Strict):
    """RFC 7807 problem details: every error the service returns."""

    type: str
    title: str
    status: int = Field(ge=400, le=599)
    detail: str | None = None
    instance: str | None = None
    correlation_id: str | None = Field(default=None, alias="correlationId")
    errors: list[FieldError] | None = None
