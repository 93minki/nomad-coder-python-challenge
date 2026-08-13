from flask import Flask, redirect, render_template, request

from scraper import Scraper

app = Flask("JobScraper")


KEYWORDS = ["python", "javascript", "java"]


@app.route("/")
def hello_world():
    return render_template("home.html")


@app.route("/not-found")
def not_found():
    return render_template("not_found.html")


@app.route("/search")
def search():
    keyword = request.args.get("keyword")
    site_list = request.args.getlist("site")
    results = []

    if not keyword:
        return redirect("/")

    if keyword not in KEYWORDS:
        return redirect("/not-found")

    for site in site_list:
        scraper = Scraper(keyword, site)
        results.extend(scraper.search())

    return render_template(
        "search.html", site_list=site_list, results=results, keyword=keyword
    )


if __name__ == "__main__":
    app.run()
