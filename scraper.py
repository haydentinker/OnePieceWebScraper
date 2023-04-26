import requests
import csv
from bs4 import BeautifulSoup
import re

def character_scraper():
    URL="https://onepiece.fandom.com/wiki/List_of_Canon_Characters"
    all_characters_page=requests.get(URL)
    soup=BeautifulSoup(all_characters_page.content, "html.parser")
    tables = soup.find_all('table', class_='wikitable sortable')
    tables.pop()
    character_table=[]
    for table in tables:
        for row in table.tbody.find_all('tr'):    
            # Find all data for each column
            columns = row.find_all('td')
            if columns !=[]:
                character_table.append(columns[1].contents)

    character_URL="https://onepiece.fandom.com"
    with open('character.csv',mode='a')as character_file:
        character_writer=csv.writer(character_file,delimiter=',',quotechar="\"",quoting=csv.QUOTE_MINIMAL)

        character_writer.writerow(['Japanese_name','Romanized_name','English_name','Debut','Affiliations','Occupations'])
        for i in range(0,len(character_table)):
            characters_page=requests.get(character_URL+character_table[i][0].get('href'))
            soup=BeautifulSoup(characters_page.content, "html.parser")
            character_information=soup.find_all('div',class_='pi-item')
            if(len(character_information)>7):
                if(clean_string(character_information[2].find('div',class_='pi-data-value').text)!="N/A"):
                    character_map={
                        "English_name":clean_string(character_information[2].find('div',class_='pi-data-value').text),
                        "Debut":clean_string(character_information[3].find('div',class_='pi-data-value').text),
                        "Affiliations":clean_string(character_information[4].find('div',class_='pi-data-value').text),
                        "Occupations":clean_string(character_information[5].find('div',class_='pi-data-value').text),
                        #Ignoring Status because spoiler
                        #Don't need VA so will leave off the rest
                    }
                    character_writer.writerow(character_map.values())

def clean_string(input_str):
    # Remove anything within between [ ]
    input_str = re.sub('\[.*?\]', '', input_str)

    # Split on ;
    if ";" in input_str:
        split_list = input_str.split(';')

        # Remove ;
        split_list = [elem.strip().replace(';', '') for elem in split_list]

        return split_list
    return input_str


character_scraper()