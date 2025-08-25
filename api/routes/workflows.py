from enum import Enum
from typing import AsyncGenerator, List, Optional

from agno.workflow import Workflow
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from workflows.operator import WorkflowType, get_available_workflows, get_workflow
from utils.log import logger

######################################################
## Router for the Workflow Interface
######################################################

workflows_router = APIRouter(prefix="/workflows", tags=["Workflows"])


class Model(str, Enum):
    gemini_2_5_pro = "gemini-2.5-pro"
    gemini_2_5_flash = "gemini-2.5-flash"
    gemini_2_5_flash_lite = "gemini-2.5-flash-lite"
    gemma_3n_e2b_it = "gemma-3n-e2b-it"


@workflows_router.get("", response_model=List[str])
async def list_workflows():
    """Returns a list of all available workflow IDs."""
    return get_available_workflows()


async def workflow_response_streamer(workflow: Workflow, payload: str) -> AsyncGenerator:
    run_response = workflow.run(payload)
    for chunk in run_response:
        # If chunk is a RunResponse or similar, yield its content
        try:
            yield getattr(chunk, "content", str(chunk))
        except Exception:
            yield str(chunk)


class RunRequest(BaseModel):
    """Request model for running a workflow"""

    input: str
    stream: bool = True
    model: Model = Model.gemini_2_5_pro
    user_id: Optional[str] = None
    session_id: Optional[str] = None


@workflows_router.post("/{workflow_id}/runs", status_code=status.HTTP_200_OK)
async def run_workflow(workflow_id: WorkflowType, body: RunRequest):
    logger.debug(f"RunRequest: {body}")

    try:
        wf: Workflow = get_workflow(workflow_id=workflow_id.value, wf_type=workflow_id, debug_mode=True)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Workflow not found: {str(e)}")

    if body.stream:
        return StreamingResponse(workflow_response_streamer(wf, body.input), media_type="text/event-stream")
    else:
        # run synchronously and return last content or aggregated content
        resp_iter = wf.run(body.input)
        content_list = [getattr(r, "content", str(r)) for r in resp_iter]
        return "\n".join(content_list)
