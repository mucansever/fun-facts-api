from typing import Annotated

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends

from app.adapter.api.v1.contract import DailyFunFactDto
from app.adapter.api.v1.error_handler import handle_errors
from app.domain.service import get_daily_fun_fact_service, DailyFunFactService
from app.util import logger


router = APIRouter(prefix="/v1/fun-facts")

@router.get("/today", response_model=DailyFunFactDto)
@handle_errors
async def get_todays_fun_fact(service: Annotated[DailyFunFactService, Depends(get_daily_fun_fact_service)]):
    logger.info("Retrieving today's fun fact")
    fact = await service.get_todays_fun_fact()

    if not fact:
        raise HTTPException(status_code=404, detail="Fun fact not found")
    return DailyFunFactDto.from_model(fact)

@router.get("/recent", response_model=list[DailyFunFactDto])
@handle_errors
async def get_recent_fun_facts(service: Annotated[DailyFunFactService, Depends(get_daily_fun_fact_service)]):
    logger.info("Retrieving recent fun facts")
    facts = await service.get_last_n_fun_facts(10)
    return [DailyFunFactDto.from_model(fact) for fact in facts]
