from typing import Annotated

from fastapi import APIRouter, Depends, Response, status

from app.application.leads.create_lead import CreateLead
from app.presentation.api.v1.schemas import LeadCreateRequest, LeadCreateResponse
from app.presentation.dependencies import get_create_lead

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
