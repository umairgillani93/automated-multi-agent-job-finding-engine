from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import TavilySearchTool, ScrapeWebsiteTool
from typing import List
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class JobDiscoveryAgents():
    """JobDiscoveryAgents crew"""

    ollama_llm = LLM(
    model="ollama/llama2:latest",
    base_url="http://localhost:11434"
    )
    # requires TAVILY_API_KEY in .env
    scrape_tool = ScrapeWebsiteTool()

    @agent
    def job_scraper(self) -> Agent:
        return Agent(
            config=self.agents_config['job_scraper'],
            llm=self.ollama_llm,
            tools=[self.search_tool], # The agent now has "eyes" on the web
            verbose=True,
            max_iter=3,
            allow_delegation=False
        )

    @task
    def job_search_task(self) -> Task:
        return Task(
            config=self.tasks_config['job_search_task'],
        )

    @agent
    def data_cleaner_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['data_cleaner'],
            llm=self.ollama_llm,
            tools=[self.scrape_tool], # The agent now has "eyes" on the web
            verbose=True,
            max_iter=3,
            allow_delegation=False
        )

    @task
    def data_cleaner_task(self) -> Task:
        return Task(
            config=self.tasks_config['data_cleaning_task'],
        )


    @crew
    def crew(self) -> Crew:
        """Creates the JobDiscoveryAgents crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )

