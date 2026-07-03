from duckduckgo_search import DDGS


class WebSearch:

    def __init__(self):
        pass

    # ---------------------------------------
    # Search Internet
    # ---------------------------------------

    def search(self, query, max_results=5):

        results = []

        try:

            with DDGS() as ddgs:

                for item in ddgs.text(
                    query,
                    max_results=max_results
                ):

                    results.append({
                        "title": item.get("title", ""),
                        "body": item.get("body", ""),
                        "url": item.get("href", "")
                    })

        except Exception as e:

            print(e)

        return results

    # ---------------------------------------
    # Convert Search Results to Prompt
    # ---------------------------------------

    def build_context(self, results):

        context = ""

        for i, result in enumerate(results, start=1):

            context += (
                f"\nResult {i}\n"
                f"Title: {result['title']}\n"
                f"Summary: {result['body']}\n"
                f"Source: {result['url']}\n\n"
            )

        return context