import json
import os
import requests
# from langchain.tools import tool
from crewai.tools import tool
from pydantic import BaseModel, Field

# class SearchSchema(BaseModel):                                                                                                                                                                                  
#     query: str = Field(
#         description="The search query to find information on the internet for counter arguments"
#         )

class SearchTools():

    # @tool("Search the internet", args_schema= SearchSchema, return_direct=True)
    @tool("Search the internet")
    def search_internet(queries: list) -> str:

        """
        Perform an internet search using the provided queries.

        This method searches the internet using the Serper API and returns
        the top search results as a formatted string.

        Args:
            query (list): The search terms to query the internet with.

        Returns:
            str: Formatted search results or an error message.
        """

        top_result_to_return = 4
        url = "https://google.serper.dev/search"
        headers = {
                'X-API-KEY': os.environ['SERPER_API_KEY'],
                'content-type': 'application/json'
            }
        string = []

        for query in queries:
            payload = json.dumps({"q": query})
            response = requests.request("POST", url, headers=headers, data=payload)

            # check if there is an organic key
            if 'organic' not in response.json():
                # return "Sorry, I couldn't find anything about that!"
                string.append("An error occurred while searching the internet.")
            else:
                results = response.json()['organic']
                for result in results[:top_result_to_return]:
                    try:
                        string.append('\n'.join([
                            f"Title: {result['title']}", f"Link: {result['link']}",
                            f"Snippet: {result['snippet']}", "\n-----------------"
                        ]))
                    except KeyError:
                        continue  

        return '\n'.join(string)