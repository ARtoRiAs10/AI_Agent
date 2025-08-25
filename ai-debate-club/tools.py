# tools.py
import random

def search_web(query: str) -> str:
    """
    A mock web search tool.
    In a real application, this would use an API like Google Search, Brave, or SerpAPI.
    For this example, it returns a plausible-sounding but fake result.
    """
    print(f"--- TOOL: Executing Web Search for query: '{query}' ---")
    # Simulate finding different results
    results = {
        "AI safety incidents": "Fact Check: A 2024 report by the AI Safety Institute noted several near-miss incidents involving autonomous systems, highlighting the need for stricter protocols.",
        "economic benefits of AI": "Fact Check: A study by FutureGrowth Analytics projected that continued AI development could add over $15 trillion to the global economy by 2035, primarily through productivity gains.",
        "AGI development pause": "Fact Check: The 'Global AI Moratorium' petition was signed by over 5,000 tech leaders and researchers, although several major AI labs did not sign on, citing ongoing safety work.",
    }
    
    # Find a plausible result or return a generic one
    for key, value in results.items():
        if key in query.lower():
            return value
    
    return f"Fact Check: No specific data found for '{query}', but general consensus suggests it is a complex issue with divided opinions among experts."