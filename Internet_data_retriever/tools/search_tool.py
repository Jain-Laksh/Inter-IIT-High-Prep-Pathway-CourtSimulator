import json
import os
import requests
# from langchain.tools import tool
from crewai.tools import tool
# from pydantic import BaseModel, Field

# class SearchSchema(BaseModel):                                                                                                                                                                                  
#     query: str = Field(
#         description="The search query to find information on the internet for counter arguments"
#         ) 

# class SearchTools():

#     # @tool("Search the internet", args_schema= SearchSchema, return_direct=True)
#     @tool("Search the internet")
#     def search_internet(queries: list) -> str:

#         """
#         Perform an internet search using the provided queries.

#         This method searches the internet using the Serper API and returns
#         the top search results as a formatted string.

#         Args:
#             query (list): The search terms to query the internet with.

#         Returns:
#             str: Formatted search results or an error message.
#         """

#         top_result_to_return = 4
#         url = "https://google.serper.dev/search"
#         headers = {
#                 'X-API-KEY': os.environ['SERPER_API_KEY'],
#                 'content-type': 'application/json'
#             }
#         string = []

#         for query in queries:
#             payload = json.dumps({"q": query})
#             response = requests.request("POST", url, headers=headers, data=payload)

#             if 'organic' not in response.json():
#                 string.append("An error occurred while searching the internet.")
#             else:
#                 results = response.json()['organic']
#                 for result in results[:top_result_to_return]:
#                     try:
#                         string.append('\n'.join([
#                             f"Title: {result['title']}", f"Link: {result['link']}",
#                             f"Snippet: {result['snippet']}", "\n-----------------"
#                         ]))
#                     except KeyError:
#                         continue  

#         return '\n'.join(string)
    

import json
import os
import requests
from crewai.tools import tool

class SearchTools():
    @staticmethod
    def get_serper_search_results(queries: list, top_result_to_return: int = 4) -> list:
        """
        Perform a search using Serper API.
        
        Args:
            queries (list): Search terms to query.
            top_result_to_return (int): Number of top results to return.
        
        Returns:
            list: Formatted search results or error message.
        """
        url = "https://google.serper.dev/search"
        headers = {
            'X-API-KEY': os.environ.get('SERPER_API_KEY', ''),
            'content-type': 'application/json'
        }
        string = []

        for query in queries:
            try:
                payload = json.dumps({"q": query})
                response = requests.request("POST", url, headers=headers, data=payload)
                
                # Check if API key is invalid or request failed
                if response.status_code != 200 or 'organic' not in response.json():
                    raise Exception("Serper API request failed")
                
                results = response.json()['organic']
                for result in results[:top_result_to_return]:
                    try:
                        string.append('\n'.join([
                            f"Title: {result['title']}", f"Link: {result['link']}",
                            f"Snippet: {result['snippet']}", "\n-----------------"
                        ]))
                    except KeyError:
                        continue
            
            except Exception as e:
                # If Serper fails, log the error and move to Bing search
                print(f"Serper search failed for query '{query}': {str(e)}")
                return SearchTools.get_bing_search_results(queries)
        
        return '\n'.join(string)

    @staticmethod
    def get_bing_search_results(queries: list, top_result_to_return: int = 4) -> str:
        """
        Perform a search using Bing Search API as a fallback.
        
        Args:
            queries (list): Search terms to query.
            top_result_to_return (int): Number of top results to return.
        
        Returns:
            str: Formatted search results or error message.
        """
        url = "https://api.bing.microsoft.com/v7.0/search"
        headers = {
            "Ocp-Apim-Subscription-Key": os.environ.get('BING_API_KEY', ''),
        }
        string = []

        for query in queries:
            try:
                params = {"q": query, "count": top_result_to_return}
                response = requests.get(url, headers=headers, params=params)
                
                # Check if API key is invalid or request failed
                if response.status_code != 200:
                    raise Exception("Bing Search API request failed")
                
                results = response.json().get('webPages', {}).get('value', [])
                for result in results:
                    try:
                        string.append('\n'.join([
                            f"Title: {result['name']}", f"Link: {result['url']}",
                            f"Snippet: {result['snippet']}", "\n-----------------"
                        ]))
                    except KeyError:
                        continue
            
            except Exception as e:
                # If both Serper and Bing fail, return an error message
                print(f"Bing search failed for query '{query}': {str(e)}")
                string.append(f"Search failed for query: {query}")
        
        return '\n'.join(string)

    @tool("Search the internet")
    def search_internet(queries: list) -> str:
        """
        Perform an internet search with fallback mechanism.
        
        Args:
            queries (list): Search terms to query.
        
        Returns:
            str: Formatted search results with title,link and summary.
        """
        # First try Serper search
        return SearchTools.get_serper_search_results(queries)