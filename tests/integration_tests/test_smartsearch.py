from typing import Type

from langchain_cloudsway.smartsearch import SmartsearchTool
from langchain_tests.integration_tests import ToolsIntegrationTests


class TestSmartsearchToolIntegration(ToolsIntegrationTests):
    @property
    def tool_constructor(self) -> Type[SmartsearchTool]:
        return SmartsearchTool

    @property
    def tool_constructor_params(self) -> dict:
        # SmartsearchTool does not require constructor arguments
        return {}

    @property
    def tool_invoke_params_example(self) -> dict:
        """
        Returns a dictionary representing the "args" of an example tool call.
        """
        return {
            "query": "2024 global AI summit highlights",
            "count": 2,
            "setLang": "en"
        }