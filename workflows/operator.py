from enum import Enum
from typing import List, Optional

from workflows.blog_post_generator import get_blog_post_generator
from workflows.investment_report_generator import get_investment_report_generator


class WorkflowType(Enum):
    BLOG_POST = "generate-blog-post-on"
    INVESTMENT_REPORT = "generate-investment-report"


def get_available_workflows() -> List[str]:
    return [w.value for w in WorkflowType]


def get_workflow(
    workflow_id: Optional[str] = None,
    wf_type: Optional[WorkflowType] = None,
    debug_mode: bool = True,
):
    if wf_type == WorkflowType.INVESTMENT_REPORT or workflow_id == WorkflowType.INVESTMENT_REPORT.value:
        return get_investment_report_generator(debug_mode=debug_mode)
    else:
        return get_blog_post_generator(debug_mode=debug_mode)
