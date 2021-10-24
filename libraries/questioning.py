import urllib.request
import json
import random
from Levenshtein import distance


categoriesPerPage = 20


def areSimilar(s1, s2):
    dist = distance(str(s1).lower(), str(s2).lower())
    return dist < (len(s1) * 0.4)  # Can be 40% wrong


# Gets a random question
def getQuestion(difficulty=0, category=0):
    urlPath = getQuestionUrl(difficulty=difficulty, category=category)
    with urllib.request.urlopen(urlPath) as url:
        try:
            data = json.loads(url.read().decode())
            questionDict = random.choice(data)
            q = str(questionDict["question"])
            a = str(questionDict["answer"]).title()
            if len(q) > 2 and len(a) > 2:
                return q, a
            else:
                return getQuestion(difficulty=difficulty, category=category)
        except Exception as e:
            pass


# Using a category is not recommended


def getQuestionUrl(difficulty=0, category=0):
    url = "http://jservice.io/api/clues"
    if difficulty > 0 or category > 0:  # either is filled
        url = url + "?"
        if difficulty > 0 and category > 0:  # both are filled
            url = (
                url
                + "value="
                + str(round(difficulty) * 100)
                + "&category="
                + str(category)
            )
        elif difficulty > 0:
            url = url + "value=" + str(round(difficulty) * 100)
        else:
            url = url + "category=" + str(category)
    return url


# Scans a section of all categories for a specific category.
# Returns its id or 0 if not found or -1 if there are no categories on the page


def scanCategoryPage(catString, page=0):
    urlPath = (
        "http://jservice.io/api/categories?count="
        + str(categoriesPerPage)
        + "&offset="
        + str(page)
    )
    with urllib.request.urlopen(urlPath) as url:
        try:
            data = json.loads(url.read().decode())
            for cat in data:
                if "title" in cat and "id" in cat:
                    if areSimilar(cat["title"], catString):
                        return int(cat["id"])
        except Exception as e:
            return -1
    return 0


# Do not use.
# Why? because it might take forever


def scanForCategory(catString):
    page = 0
    cat = 0
    while cat == 0:
        cat = scanCategoryPage(catString, page=page)
        page += 1
        if cat <= -1:
            break
    return cat


# Gets a category page in a nice, formatted string


def getCategoryPage(page=0):
    pageStr = "Categories on this page:\n```"

    urlPath = (
        "http://jservice.io/api/categories?count="
        + str(categoriesPerPage)
        + "&offset="
        + str(page)
    )
    with urllib.request.urlopen(urlPath) as url:
        try:
            data = json.loads(url.read().decode())
            titles = []
            for cat in data:
                if "title" in cat:
                    titles.append(cat["title"])
            pageStr = pageStr + ", ".join(titles)
        except:
            pass
    return page + "```"


print(scanForCategory("mixed bag"))
print(getQuestion(difficulty=1))
