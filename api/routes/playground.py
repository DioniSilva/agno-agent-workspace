from os import getenv

from agno.playground import Playground

from agents.sage import get_sage
from agents.scholar import get_scholar
from agents.searcher import search_agent
from agents.writer import writer
from agents.article_scraper import article_scraper
from teams.finance_researcher import get_finance_researcher_team
from teams.multi_language import get_multi_language_team
from workflows.blog_post_generator import get_blog_post_generator
from workflows.investment_report_generator import get_investment_report_generator
from workspace.dev_resources import dev_fastapi

######################################################
## Router for the Playground Interface
######################################################

# Agents
sage_agent = get_sage(debug_mode=True)
scholar_agent = get_scholar(debug_mode=True)
searcher_agent = search_agent()
writer_agent = writer()
article_scraper_agent = article_scraper()

# Teams
finance_researcher_team = get_finance_researcher_team(debug_mode=True)
multi_language_team = get_multi_language_team(debug_mode=True)

# Workflows
blog_post_workflow = get_blog_post_generator(debug_mode=True)
investment_report_workflow = get_investment_report_generator(debug_mode=True)

# Create a playground instance
playground = Playground(
    agents=[sage_agent, scholar_agent, searcher_agent, writer_agent, article_scraper_agent],
    teams=[finance_researcher_team, multi_language_team],
    workflows=[blog_post_workflow, investment_report_workflow]
)
app = playground.get_app()

# Register the endpoint where playground routes are served with agno.com
if getenv("RUNTIME_ENV") == "dev":
    # Try the modern API first, fallback to alternative helpers for older/newer agno versions
    try:
        playground.serve("playground:app", f"http://localhost:{dev_fastapi.host_port}")
    except AttributeError:
        try:
            # module-level helper
            from agno.playground import serve_playground_app

            serve_playground_app("playground:app", f"http://localhost:{dev_fastapi.host_port}")
        except Exception:
            # last resort: introspect Playground instance
            try:
                playground.register_app_on_platform("playground:app", f"http://localhost:{dev_fastapi.host_port}")
            except Exception:
                # give up silently (playground will still work locally without registration)
                pass

playground_router = playground.get_async_router()
