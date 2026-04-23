from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.crawl4ai import Crawl4aiTools
from agno.tools.duckduckgo import DuckDuckGoTools

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

crawler_agent = Agent(
        name="Scraper",
        model=OpenAIChat(id="openai/gpt-4o-mini", base_url=OPENROUTER_BASE_URL),
        tools=[
            Crawl4aiTools(max_length=None)],
        instructions="""
        Given a list of URLs, crawl each one.
        Extract any email addresses and phone numbers found.
        Return ONLY a JSON list of contacts, nothing else.
        Example: [{"email": "john@co.com", "phone": "555-1234", "company": "Acme", "url": "https://..."}]
        If nothing found on a page, skip it.
        Do NOT hallucinate contact info.
        """,
)


search_agent: Agent = Agent(
        name="SearchAgent",
        model=OpenAIChat(id="openai/gpt-4o-mini", base_url=OPENROUTER_BASE_URL),
        tools=[DuckDuckGoTools()],
        instructions="""
        Search for businesses in the given market.
        Return ONLY a JSON list of 5 URLs, nothing else.
        Example: ["https://site1.com", "https://site2.com"]
        """,
)
