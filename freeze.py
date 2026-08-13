from flask_frozen import Freezer

from main import KEYWORDS, app

app.config["FREEZER_DESTINATION"] = "docs"
app.config["FREEZER_REMOVE_EXTRA_FILES"] = False

freezer = Freezer(app)


@freezer.register_generator
def search_by_keyword():
    for keyword in KEYWORDS:
        yield {"keyword": keyword}


if __name__ == "__main__":
    freezer.freeze()
