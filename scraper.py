import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}


class Scraper:
    def __init__(self, keyword, site):
        self.keyword = keyword
        self.site = site
        if site == "berlinstartupjobs":
            self.url = f"https://berlinstartupjobs.com/skill-areas/{keyword}/"
        elif site == "web3career":
            self.url = f"https://web3.career/{keyword}-jobs"
        elif site == "weworkremotely":
            self.url = f"https://weworkremotely.com/remote-jobs/search?utf8=%E2%9C%93&term={keyword}"
        else:
            raise ValueError(f"Invalid site: {site}")

    def search(self):
        response = requests.get(self.url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        if self.site == "berlinstartupjobs":
            return self.get_berlinstartupjobs_jobs(soup)
        elif self.site == "web3career":
            return self.get_web3career_jobs(soup)
        elif self.site == "weworkremotely":
            return self.get_weworkremotely_jobs(soup)
        else:
            raise ValueError(f"Invalid site: {self.site}")

    def get_berlinstartupjobs_jobs(self, soup):
        jobs = soup.select("ul.jobs-list-items > li")
        results = []

        for job in jobs:
            info = job.select_one("h4.bjs-jlid__h > a")
            title = info.get_text(strip=True) if info else "Title None"
            job_url = info.get("href") if info else "URL None"
            company_name = job.select_one("a.bjs-jlid__b")

            results.append(
                {
                    "title": title,
                    "company_name": company_name.get_text(strip=True)
                    if company_name
                    else "CompanyName None",
                    "job_url": job_url,
                }
            )
        return results

    def get_web3career_jobs(self, soup):
        jobs = soup.select("tr.table_row")
        results = []
        for job in jobs:
            info = job.select_one("div.job-title-mobile > a")
            title = info.get_text(strip=True) if info else "Title None"
            href = info.get("href") if info else None
            job_url = f"https://web3.career{href}" if href else "URL None"
            company = job.select_one("div.job-company-location h3")
            results.append(
                {
                    "title": title,
                    "company_name": company.get_text(strip=True)
                    if company
                    else "CompanyName None",
                    "job_url": job_url,
                }
            )
        return results

    def get_weworkremotely_jobs(self, soup):
        jobs = soup.select("li.new-listing-container")
        results = []
        for job in jobs:
            title_el = job.select_one("span.new-listing__header__title__text")
            info = job.select_one("a[href^='/remote-jobs/']")
            company = job.select_one("p.new-listing__company-name")
            title = title_el.get_text(strip=True) if title_el else "Title None"
            href = info.get("href") if info else None
            job_url = f"https://weworkremotely.com{href}" if href else "URL None"
            results.append(
                {
                    "title": title,
                    "company_name": company.get_text(strip=True)
                    if company
                    else "CompanyName None",
                    "job_url": job_url,
                }
            )
        return results
