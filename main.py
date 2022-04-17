import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest
import re

pageNumber = 1
numOfPages = 1
fileHeaders = ["Book Name", "Book Rating", "Number of Ratings", "Description"]

books = []
ratings = []
numOfRatings = []
descriptions = []
links = []

print("Please Enter The author Link you want to scrape his/her books")
# authorLink = input("Example: https://www.goodreads.com/author/list/3389.Stephen_King\n")

print("Establishing connection")

while pageNumber <= 1:
    authorLink = "https://www.goodreads.com/author/list/984651._"
    res = requests.get(authorLink + f"?page={pageNumber}&per_page=30")

    if pageNumber == 1:
        print("Connection established")

    soup = BeautifulSoup(res.content, "lxml")

    soupedBooks = soup.find_all("span", {"itemprop": "name", "role": "heading", "aria-level": "4"})
    soupedInfo = soup.find_all("span", {"class": "greyText smallText uitext"})

    for a in soup.find_all('a', {"class": "bookTitle"}, href=True):
        links.append("https://www.goodreads.com/" + a['href'])

    if pageNumber == 1:
        soupedNumOfPages = soup.find("div", {"style": "float: right"})
        numOfPages = int(re.findall(r'\d+', soupedNumOfPages.text)[-1])

    for i in range(len(soupedBooks)):
        soupedInfoText = soupedInfo[i].text.replace("\n", "").split("—")
        rating = soupedInfoText[0].strip()
        numOfRating = soupedInfoText[1].strip()

        books.append(soupedBooks[i].text)
        ratings.append(rating)
        numOfRatings.append(numOfRating)

        bookRes = requests.get(links[i])
        bookSoup = BeautifulSoup(bookRes.content, "lxml")
        soupedDesc = bookSoup.find("div", {"id": "descriptionContainer"})
        sdes = "No description"

        if soupedDesc is not None:
            des2 = soupedDesc.select_one("div div span:nth-of-type(2)")
            if des2 is not None:
                sdes = soupedDesc.select_one("div div span:nth-of-type(2)").text
                # descriptions.append(soupedDesc.select_one("div div span span").text)
            else:
                sdes = soupedDesc.select_one("div div span:nth-of-type(1)").text
                # descriptions.append(soupedDesc.select_one("div div span").text)

        descriptions.append(sdes)

        if len(descriptions) % 10 == 0:
            print(f"{len(descriptions)} books scraped")

    print(f"Page Number {pageNumber} scraped successfully")
    pageNumber += 1

fileList = [books, ratings, numOfRatings, descriptions]
fileListUnPacked = zip_longest(*fileList)

flag = True
with open('scrapedFile.csv', 'w', encoding="utf-8-sig", newline='') as f:
    wr = csv.writer(f)
    if flag:
        wr.writerow(fileHeaders)
        flag = False
    wr.writerows(fileListUnPacked)
