import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest

pageNumber = 1
numOfPages = 1
fileHeaders = ["Book Name", "Book Rating", "Number of Ratings"]

books = []
ratings = []
numOfRatings = []

print("Please Enter The author Link you want to scrape his/her books")
authorLink = input("Example: https://www.goodreads.com/author/list/3389.Stephen_King\n")

while pageNumber <= numOfPages:
    res = requests.get(authorLink + f"?page={pageNumber}&per_page=30")

    soup = BeautifulSoup(res.content, "lxml")
    # print(soup)

    soupedBooks = soup.find_all("span", {"itemprop": "name", "role": "heading", "aria-level": "4"})
    soupedInfo = soup.find_all("span", {"class": "greyText smallText uitext"})

    if pageNumber == 1:
        import re

        soupedNumOfPages = soup.find("div", {"style": "float: right"})
        numOfPages = int(re.findall(r'\d+', soupedNumOfPages.text)[-1])

    for i in range(len(soupedBooks)):
        soupedInfoText = soupedInfo[i].text.replace("\n", "").split("—")
        rating = soupedInfoText[0].strip()
        numOfRating = soupedInfoText[1].strip()
        books.append(soupedBooks[i].text)
        ratings.append(rating)
        numOfRatings.append(numOfRating)

    print(f"Page Number {pageNumber} scraped successfully")
    pageNumber += 1

fileList = [books, ratings, numOfRatings]
fileListUnPacked = zip_longest(*fileList)

with open('scrapedFile.csv', 'w', encoding="utf-8-sig", newline='') as f:
    wr = csv.writer(f)
    if pageNumber == 1:
        wr.writerow(fileHeaders)
    wr.writerows(fileListUnPacked)
