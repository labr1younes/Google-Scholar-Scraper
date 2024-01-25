import logging
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import json


# Make a Soup object
def get_data(myurl):
    myheaders = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0'}
    try:
        myresult = requests.get(myurl, headers=myheaders).content
        return BeautifulSoup(myresult, "lxml")
    except requests.RequestException as e:
        logging.error(f"Error fetching data from {myurl}: {e}")
        return None


# Scrape all the data in the profile
def scrape_profile(myurl):
    page = get_data(myurl)

    profileurl = myurl
    name = page.find('div', attrs={'id': 'gsc_prf_in'}).text
    job_title = page.find('div', attrs={'class': 'gsc_prf_il'}).text
    workplace = page.find('div', attrs={'id': 'gsc_prf_ivh'}).text

    # processing keywords
    key_words_a = []
    for key_word in page.find_all('a', attrs={'class': 'gsc_prf_inta gs_ibl'}):
        key_words_a.append(key_word.text)
    key_words_list = ' ,'.join(key_words_a)

    # processing "Cited by" table
    table = page.find('table', attrs={'id': 'gsc_rsb_st'})
    table_tr = table.find_all('tr')

    citations = table_tr[1].find_all('td')[1].text
    h_index = table_tr[2].find_all('td')[1].text
    i10_index = table_tr[3].find_all('td')[1].text

    return [profileurl, name, job_title, workplace, key_words_list, citations, h_index, i10_index]


# The main function
def scrape_all_pages(start_url):
    # Getting all pages
    allpages = [start_url]
    get_next_page_url(start_url, allpages)
    print("Number of Pages  = ", len(allpages))

    # Getting all profiles
    allprofiles = []
    for page in allpages:
        soup_page = get_data(page)
        allprofiles += scrape_profile_urls(soup_page)
    print("Number of Profiles  = ", len(allprofiles))

    profiles_data = []
    # Getting all Data from the profiles
    for index, profile in enumerate(allprofiles, start=1):
        fullurl = urljoin("https://scholar.google.com", profile)
        # tmpprofile = get_data(fullurl, he)
        profiles_data.append(scrape_profile(fullurl))
        print(f'\n-------[{index}]/[{len(allprofiles)}] ')

    return [len(allpages), len(allprofiles), profiles_data]


# Scrape all teh Profiles URL from a page
def scrape_profile_urls(mysoup):
    profile_urls = []
    tmp = mysoup.find_all('h3', attrs={'class': 'gs_ai_name'})

    for i in tmp:
        u = i.a.get('href')
        profile_urls.append(u)

    return profile_urls


# Scrape all the pages URLs
def get_next_page_url(mysurl, myallpages):
    mysoup = get_data(mysurl)

    page = mysoup.find('div', attrs={'class': 'gsc_pgn'})
    if not page.find('button', attrs={'class': 'gs_btnPR gs_in_ib gs_btn_half gs_btn_lsb gs_btn_srt gsc_pgn_pnx'}).get(
            'disabled'):

        url = page.find('button',
                        attrs={'class': 'gs_btnPR gs_in_ib gs_btn_half gs_btn_lsb gs_btn_srt gsc_pgn_pnx'}).get(
            'onclick')
        if url:
            newurl = bytes(url[17:-1], 'utf-8').decode('unicode-escape')
            fullurl = urljoin("https://scholar.google.com", newurl)
        else:
            return myallpages
        myallpages.append(fullurl)

        get_next_page_url(fullurl, myallpages)
    else:
        return myallpages


# Convert the list of data to a JSON file
def convert_2_json(mydata: list, myname: str):
    # Extracted data from the list
    number_of_pages, number_of_profiles, profiles_data = mydata

    # Convert list to JSON with the desired structure
    json_data = {
        "number_of_pages": number_of_pages,
        "number_of_profiles": number_of_profiles,
        "profiles": []
    }

    for profile in profiles_data:
        profile_dict = {
            "url": profile[0],
            "name": profile[1],
            "job_title": profile[2],
            "workplace": profile[3],
            "key_words": profile[4],
            "citations": profile[5],
            "h-index": profile[6],
            "i10-index": profile[7]
        }
        json_data["profiles"].append(profile_dict)

    # Write JSON data to a file
    json_file_path = f'{myname}.json'
    with open(json_file_path, 'w') as json_file:
        json.dump(json_data, json_file, indent=4)

    print(f"JSON data has been written to : {json_file_path}")


# The main
if __name__ == '__main__':
    search_url = ("https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=algeria+AI&before_author"
                  "=tCMZ_xMAAAAJ&astart=0")

    convert_2_json(scrape_all_pages(search_url), "result")
