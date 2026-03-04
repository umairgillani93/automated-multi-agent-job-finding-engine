from crewai import CrewTask
from typing import List, Dict
import requests
from bs4 import BeautifulSoup

class JobScraperAgent(CrewTask):
    """
    CrewAI Agent to scrape AI job postings from RemoteOK.
    """

    def run(self, query: str) -> List[Dict]:
        jobs = []
        jobs.extend(self.scrape_remoteok("https://remoteok.com/remote-ai-jobs", query))
        return jobs

    def scrape_remoteok(self, url: str, query: str) -> List[Dict]:
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers)
        soup = BeautifulSoup(resp.text, "html.parser")
        job_rows = soup.select("tr.job")
        results = []

        for row in job_rows:
            title_tag = row.select_one("td.position h2")
            company_tag = row.select_one("td.company h3")
            desc_tag = row.select_one("td.description")

            if not title_tag or not company_tag:
                continue

            title = title_tag.text.strip()
            company = company_tag.text.strip()
            description = desc_tag.text.strip() if desc_tag else ""

            if query.lower() in title.lower() or query.lower() in description.lower():
                results.append({
                    "title": title,
                    "company": company,
                    "description": description,
                    "location": "Remote",
                    "source": url
                })
        return results
