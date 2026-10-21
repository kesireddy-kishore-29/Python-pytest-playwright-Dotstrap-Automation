"""The UI flagship app's (sut-ui) item API, used to seed hybrid tests."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

ItemStatus = Literal["active", "paused", "archived"]


class AppItem(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, populate_by_name=True)

    id: str = Field(pattern=r"^itm_")
    name: str
    status: ItemStatus
    owner: str
    created_at: str = Field(alias="createdAt")


class AppItemList(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    items: list[AppItem]
