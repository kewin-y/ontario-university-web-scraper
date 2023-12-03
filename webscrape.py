# Web scraper to find data on Ontario post secondary institutions

# Python modules
from bs4 import BeautifulSoup
import requests 
import json
import re
import codecs
# import pandas as pd

urls = ["a", "b", "c", "d-e", "f-g", "h", "i", "j-l", "m", "n-p", "q-s", "t-z"]
portal = "https://www.ontariouniversitiesinfo.ca/programs/search/?search=&group="

def get_program_links(url):
    # Just an example: there are many other programs in this website
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

    # Uncleaned program summary details
    psd = [detail.text for detail in program_summary_soup.find_all("dd")]
    # Same thing but for the titles
    pst = [title.text for title in program_summary_soup.find_all("dt")]

    # Clean up tabs and newlines 
    # Replace all tabs and newlines w/ spaces, remove trailing and leading whitespaces
    program_summary_details = [re.sub(r'\s+', ' ', text).rstrip().lstrip() for text in psd]

    # Remove tabs and newlines for the titles
    program_summary_titles = [text.replace("\t","").replace("\n","") for text in pst]

    # Add to dictionary
    program_summary = dict(zip(program_summary_titles, program_summary_details))
    program_summary = {"Name" : soup.find("h1", class_="template-heading").text, **program_summary}

    # for detail_title in program_summary:
    #     program_summary[detail_title] = "Bruh"

    # 💀
    program_requirements_div = soup.find(string=re.compile("Prerequisites")).parent.parent

    program_requirements = [re.sub(r'\s+', ' ', text).rstrip().lstrip() for text in ([req.text for req in program_requirements_div.find_all("li")])]

    program_summary["Prerequisites"] = program_requirements
    program_summary["Link"] = soup.find(class_="program-apply").get("href")

    return program_summary

if __name__ == "__main__":
    pl = []

    for url in urls:
        pl += get_program_links(portal + url)
    
    program_links = ["https://www.ontariouniversitiesinfo.ca" + end_url for end_url in pl]

    # Get the program details of one program using its link
    programs = []
    for link in program_links:
        programs.append(get_program_summary(link))

    print(len(programs))

    program_json = json.dumps(programs, indent = 2, ensure_ascii=False)

    with open("programs.json", "w") as f:
        f.write(program_json)
