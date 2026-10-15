from typing import Annotated

from fastapi import APIRouter, Depends, Response, status

from app.application.leads.create_lead import CreateLead
from app.application.leads.list_interest_options import ListInterestOptions
from app.presentation.api.v1.schemas import (
    InterestOptionOut,
    LeadCreateRequest,
    LeadCreateResponse,
)
from app.presentation.dependencies import get_create_lead, get_list_interest_options

router = APIRouter(tags=["leads"])


@router.post("/lead", status_code=status.HTTP_201_CREATED, response_model=LeadCreateResponse)
async def submit_lead(
    payload: LeadCreateRequest,
    response: Response,
    use_case: Annotated[CreateLead, Depends(get_create_lead)],
) -> LeadCreateResponse:
    result = await use_case(payload.to_lead())
    lead_id = result.lead.id
    assert lead_id is not None
    if result.duplicate:
        response.status_code = status.HTTP_200_OK
    return LeadCreateResponse(id=lead_id, duplicate=result.duplicate)


@router.get("/lead/options", response_model=list[InterestOptionOut])
async def list_lead_options(
    use_case: Annotated[ListInterestOptions, Depends(get_list_interest_options)],
) -> list[InterestOptionOut]:
    return [InterestOptionOut(value=option.value, label=option.label) for option in use_case()]
