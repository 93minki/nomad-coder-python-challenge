from flask import Flask, redirect, render_template, request

from scraper import Scraper

app = Flask("JobScraper")


KEYWORDS = ["python", "javascript", "java"]
SITES = [
    {"id": "berlinstartupjobs", "name": "Berlin Startup Jobs"},
    {"id": "web3career", "name": "Web3 Career"},
    {"id": "weworkremotely", "name": "WeWorkRemotely"},
]


@app.route("/")
def hello_world():
    return render_template("home.html")


@app.route("/not-found/")
def not_found():
    return render_template("not_found.html")


@app.route("/search/")
def search():
    keyword = (request.args.get("keyword") or "").strip().lower()

    if not keyword:
        return redirect("/")

    if keyword not in KEYWORDS:
        return redirect("/not-found/")

    return redirect(f"/search/{keyword}/")


@app.route("/search/<keyword>/")
def search_by_keyword(keyword):
    keyword = keyword.strip().lower()
    site_results = []
    total_count = 0

    if keyword not in KEYWORDS:
        return redirect("/not-found/")

    for site in SITES:
        scraper = Scraper(keyword, site["id"])
        results = scraper.search()
        site_results.append(
            {
                "id": site["id"],
                "name": site["name"],
                "results": results,
                "count": len(results),
            }
        )
        total_count += len(results)

    return render_template(
        "search.html",
        site_results=site_results,
        total_count=total_count,
        keyword=keyword,
    )


if __name__ == "__main__":
    app.run()
