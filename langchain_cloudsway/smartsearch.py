from typing import Optional, Type
from pydantic import BaseModel, Field
import httpx
import os

from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.tools import BaseTool

class SmartsearchToolInput(BaseModel):
    """Input schema for Cloudsway smartsearch tool."""
    query: str = Field(..., description="Search keyword or question (e.g., 'Latest advances in machine learning 2024').")
    count: Optional[int] = Field(10, description="Number of results to return (1-50, recommended 3-10).")
    offset: Optional[int] = Field(0, description="Pagination offset (e.g., offset=10 means start from result #11).")
    setLang: Optional[str] = Field("en", description="Language filter (e.g., 'zh-CN', 'en', 'ja').")
    freshness: Optional[str] = Field(None, description="Filter by time period: 'Day', 'Week', 'Month', or date range like '2023-02-01..2023-05-30'.")
    sites: Optional[str] = Field(None, description="Host address to filter results from a specific website (e.g., 'baijiahao.baidu.com').")

class SmartsearchTool(BaseTool):
    """Cloudsway Smartsearch tool for LangChain.

    Setup:
        pip install -U langchain-cloudsway
        export CLOUDSWAY_SERVER_KEY="your-endpoint-accesskey"

    Usage:
        tool = SmartsearchTool()
        tool.invoke({"query": "2024 AI summit", "count": 5})
    """

    name: str = "cloudsway_smartsearch"
    description: str = (
        "Web search via Cloudsway API. Input should be a search query. "
        "Returns structured JSON results including title, url, content, and date."
    )
    args_schema: Type[BaseModel] = SmartsearchToolInput

    def _get_api_key(self) -> str:
        api_key = os.getenv("CLOUDSWAY_SERVER_KEY")
        if not api_key:
            raise ValueError("CLOUDSWAY_SERVER_KEY environment variable not set.")
        return api_key

    def _run(
        self,
        query: str,
        count: int = 10,
        offset: int = 0,
        setLang: str = "en",
        freshness: Optional[str] = None,
        sites: Optional[str] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        server_key = self._get_api_key()
        if "-" not in server_key:
            return "Error: CLOUDSWAY_SERVER_KEY format is invalid. Expected 'endpoint-accesskey'."
        endpoint, api_key = server_key.split("-", 1)
        url = f"https://searchapi.cloudsway.net/search/{endpoint}/smart"
        params = {
            'q': query,
            'count': count,
            'offset': offset,
            'setLang': setLang,  # Changed from 'mkt' to match new doc
        }
        if freshness:
            params['freshness'] = freshness
        if sites:
            params['sites'] = sites
        headers = {
            'Authorization': f'Bearer {api_key}',
            'pragma': 'no-cache',
        }
        try:
            with httpx.Client(timeout=60) as client:
                response = client.get(url, params=params, headers=headers)
                response.raise_for_status()
            return response.text
        except Exception as e:
            return f"API Error: {e}"