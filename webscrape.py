# Web scraper to find data on Ontario post secondary institutions
from bs4 import BeautifulSoup
import requests
import pandas as pd
import json
from university_program import university_program

def get_program_links():
    # Just an example: there are many other programs in this website
    url = "https://ontariouniversitiesinfo.ca/programs/search/?search=&advanced=1&a_category=computer-science-1&a_lang=22&group=a-c"

    html_doc = requests.get(url)
    soup = BeautifulSoup(html_doc.text, "html.parser")

    program_headings_soup = soup.find_all("h2", class_="result-heading")

    # Find every URL and append it to a list
    program_links = []
    for heading in program_headings_soup:
        link = heading.find("a")
        if link:
            program_links.append(link.get("href"))


    # Return the list
    return program_links

def get_program_summary(program_link):
    program_html_doc = requests.get(program_link)
    soup = BeautifulSoup(program_html_doc.text, "html.parser")


    program_article_soup = soup.find("article")
    program_summary_soup = program_article_soup.find_all(class_="tabbed-subsection")[0]

    # Gross, uncleaned program summary details
    psd = [detail.text for detail in program_summary_soup.find_all("dd")]
    # Same thing but for the titles
    pst = [title.text for title in program_summary_soup.find_all("dt")]

    # Clean up tabs and newlines 
    program_summary_details = [text.replace("\t","").replace("\n","") for text in psd]
    program_summary_titles = [text.replace("\t","").replace("\n","") for text in pst]

    # print(program_summary_titles)
    # print(program_summary_details)

    program_summary = dict(zip(program_summary_titles, program_summary_details))
    program_summary["link"] = program_link

    return program_summary


if __name__ == "__main__":
    program_links = get_program_links()

    # Get the program details of one program using its link
    programs = []
    for link in program_links:
        programs.append(get_program_summary(link))

    program_json = json.dumps(programs, indent = 2)

    with open("programs.json", "w") as f:
        f.write(program_json )




