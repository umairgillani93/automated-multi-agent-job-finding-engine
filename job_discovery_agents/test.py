from tavily import TavilyClient
tavily = TavilyClient(api_key="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")
response = tavily.search(query="Senior AI Engineer jobs in Saudi Arabia", max_results=3)
print(response) # This is exactly what the LLM receives
