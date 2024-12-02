from crewai import Task
from textwrap import dedent
from tools.search_tool import SearchTools
from tools.askUser_tool import AskUserTools

class RetrievalTasks:
    def __tip_section(self):
        return "If you do your BEST WORK, I'll give you a $10,000 commission!"

    def generate_search_queries(self, agent, argument):
        return Task(description=dedent(f'''
        **Task**: Generate Search Queries  
        **Description**: Formulate precise and relevant search queries to find counterarguments, 
                         examples, and supporting information to counter the provided argument using internet resources.
                         Your final output must be a list formatted as a numbered list of search queries that can be used 
                         to retrieve relevant information.

        **Parameters**:  
        - Argument: {argument}

        **Note**: Focus on accuracy and relevance while creating queries. Ensure the queries are designed to fetch 
                  legal examples, laws, or precedents. {self.__tip_section()}
        '''),
        agent=agent,
        expected_output=dedent('''
                A list of 3 distinct search queries, each designed to 
                uncover a different angle or perspective on the argument. 
                Format the output as a python list of search queries.
            '''))

    def retrieve_information(self, agent,argument):
        return Task(description=dedent(f'''
        **Task**: Retrieve Relevant Information from the internet using Search Queries 
        **Description**: Use the output of previous agent to extract data from the internet. Use the tool output to collect examples,
                         legal statutes, case precedents, and other supporting materials for the counterargument. Your final output must be
                         well-cited with website links and a comprehensive report of relevant information retrieved from the internet.

        **Parameters**:
        - Argument to be countered: {argument}

        **Note**: Ensure all retrieved information is accurate, well-documented, and credible. If you do your BEST WORK and CITE sources
                  with actual links from tool output, I will give you a $10,000 commission!.
        '''),
        tools=[SearchTools.search_internet],  
        agent=agent,
        expected_output=dedent('''
                A comprehensive report containing all relevant information retrieved from the internet with website links. 
                The report should be well-cited and include examples, legal statutes, case precedents, and other supporting materials 
                for the counterargument. Format the output as a multi-paragraph text report with citations.
            '''))

    def formulate_counterargument(self, agent, argument):
        return Task(description=dedent(f'''
        **Task**: Formulate Counterargument  
        **Description**: Use the retrieved information to construct a comprehensive counterargument. Include examples and 
                         cite sources to support your argument effectively. Your final output must be a well-structured, logical
                         and factually correct (with citation) counterargument that directly addresses the original argument provided.
                                       
        **Parameters**:
        - Argument to be countered: {argument}

        **Note**: Ensure the counterargument is logical, clear, real and directly addresses the original argument provided. {self.__tip_section()}
        '''), 
        agent=agent,
        expected_output=dedent('''A well-structured, logical, and factually correct counterargument that directly addresses the original argument. 
                The counterargument should include examples and cite sources to support the argument effectively.'''))

    def evaluate_counterargument(self, agent, argument):
        return Task(description=dedent(f'''
        **Task**: Evaluate Counterargument  
        **Description**: Assess the validity of the counterargument provided by the Legal Researcher. Check if it is comprehensive 
                         and aligned with the original argument's context. If the counterargument is valid, approve it else disapprove it.
                         Your final output must be a SINGLE word which is "YES" if counterargument is valid and "NO" if it is not valid.  

        **Parameters**:  
        - Argument to be countered: {argument}

        **Note**: Ensure the counterargument is comprehensive and aligned with the original argument's context. {self.__tip_section()}
        '''),
        agent=agent,
        expected_output=dedent('''return a SINGLE word as output. It should be "YES" if counterargument is valid and "NO" if it is not valid.'''))

    def request_additional_information(self, agent, argument):
        return Task(description=dedent(f'''
        **Task**: Request Additional Information  
        **Description**: Identify information needed to counter argument and request additional specifics from the user to address these gaps.
                         Use the askUser tool to ask user specific questions to gather the necessary information. Clearly communicate what 
                         information is needed and ask specific question to user to improve the counterargument. You may or may not use the
                         Old or incorrect counter argument. Your final output must be the additional information provided by the user.

        **Parameters**:  
        - Argument to be countered: {argument}

        **Note**:{self.__tip_section()}
        '''),
        tools=[AskUserTools.ask_user], 
        agent=agent,
        expected_output=dedent('''The additional information provided by the user to improve the counterargument. '''))

    def refine_counterargument(self, agent, argument):
        return Task(description=dedent(f'''
        **Task**: Refine/Reformulate the Counterargument  
        **Description**: MODIFY or REFORMULATE the provided counterargument using additional specifics or feedback from the user to ensure it is 
                         legally sound and tailored to the case. You may or may not use the Old or incorrect counter argument. Your final output 
                         must be a refined counterargument that addresses all aspects of the original argument.

        **Parameters**:  
        - Argument to be countered: {argument}

        **Note**: Strive for precision and clarity in the refined argument. Ensure it meets all case-specific requirements. {self.__tip_section()}
        '''),
        agent=agent,
        expected_output=dedent('''A refined counterargument that addresses all aspects of the original argument. Ensure the argument is legally sound 
                and tailored to the case.'''))


    # def task_name(self, agent):
    #     return Task(
    #         description=dedent(
    #             f"""
    #         Take the input from task 1 and do something with it.
                                       
    #         {self.__tip_section()}

    #         Make sure to do something else.
    #     """
    #         ),
    #         expected_output="The expected output of the task",
    #         agent=agent,
    #     )
