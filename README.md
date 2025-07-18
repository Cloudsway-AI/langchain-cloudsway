# langchain-cloudsway

This package contains the LangChain integration with Cloudsway.

## Installation

```bash
pip install -U langchain-cloudsway
```

## Configuration

Set your Cloudsway API credentials as an environment variable:

```bash
export CLOUDSWAY_SERVER_KEY="your-endpoint-accesskey"
```

The value should be in the format:  
`endpoint-accesskey` 
 
To get your token and subscribe to a plan, please register at [console.cloudsway.ai](https://console.cloudsway.ai/).

## Tool

`SmartsearchTool` provides web search via the Cloudsway API.

```python
from langchain_cloudsway.smartsearch import SmartsearchTool

tool = SmartsearchTool()
result = tool.invoke({
    "query": "2024 global AI summit highlights",
    "count": 5,
    "setLang": "en"
})
print(result)
```

---

## License

This project is open-sourced under the MIT License. See [LICENSE](./LICENSE) for details.

---
