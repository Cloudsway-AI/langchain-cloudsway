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

### Basic Usage

```python
from langchain_cloudsway.smartsearch import SmartsearchTool

tool = SmartsearchTool()
result = tool.invoke({
    "query": "cloudsway.ai",
    "count": 5,
    "setLang": "en"
})
print(result)
```

### Available Parameters

The SmartsearchTool supports the following parameters:

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| query (q) | Yes | String | The search query string. Cannot be empty. |
| count | No | Short | Number of search results to return. Default: 10, Maximum: 50. Accepted values: 10, 20, 30, 40, 50. |
| freshness | No | String | Filter results by time period: "Day", "Week", "Month", or a date range like "2023-02-01..2023-05-30". |
| offset | No | Short | Zero-based offset indicating how many results to skip. Default: 0. |
| setLang | No | String | Language code for results (recommended to use 4-letter codes like "en-US"). Default: "en". |
| sites | No | String | Host address to filter results from a specific website (e.g., "baijiahao.baidu.com"). |

### Advanced Usage Examples

```python
# Search with freshness filter
result = tool.invoke({
    "query": "latest AI research",
    "count": 20,
    "freshness": "Week", 
    "setLang": "en-US"
})

# Search within a specific site
result = tool.invoke({
    "query": "machine learning tutorial",
    "sites": "github.com"
})

# Paginated search
result = tool.invoke({
    "query": "climate change",
    "count": 10,
    "offset": 10  # Get second page of results
})
```

## Response Structure

The API returns a JSON response with the following structure:

```json
{
    "queryContext": {
        "originalQuery": "your search query"
    },
    "webPages": {
        "value": [
            {
                "name": "Page Title",
                "url": "https://example.com/page",
                "displayUrl": "https://example.com/page",
                "snippet": "Description of the page content...",
                "datePublished": "2025-07-14T00:00:00.0000000",
                "dateLastCrawled": "2025-07-15T02:48:00.0000000Z",
                "siteName": "Example Website",
                "thumbnailUrl": "https://example.com/thumbnail.jpg",
                "score": 0.95
            },
            // Additional results...
        ]
    }
}
```

### Response Fields

- **queryContext**: Contains information about the search query
  - **originalQuery**: The search term used in the request

- **webPages.value**: Array of search result objects, each containing:
  - **name**: Title of the webpage
  - **url**: URL of the webpage
  - **displayUrl**: URL displayed for the result
  - **snippet**: Brief description of the webpage content
  - **datePublished**: Publication date (when available)
  - **dateLastCrawled**: Date when the page was last indexed
  - **siteName**: Name of the website (when available)
  - **thumbnailUrl**: URL to thumbnail image (when available)
  - **score**: Relevance score (when available)

## Error Handling

The API may return the following status codes:

- **200**: Successful request
- **429**: Rate limit exceeded (QPS limit reached)

For higher QPS limits, please contact Cloudsway support.

## License

This project is open-sourced under the MIT License. See [LICENSE](./LICENSE) for details.