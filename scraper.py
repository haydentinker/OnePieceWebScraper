import requests
from bs4 import BeautifulSoup
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
characters_page=requests.get(character_URL+character_table[0][0].get('href'))
soup=BeautifulSoup(characters_page.content, "html.parser")
character_information=soup.find_all('div',class_='pi-item')
character_map={
    "Japanese_name":character_information[0].find('div',class_='pi-data-value').text,
    "Romanized_name":character_information[1].find('div',class_='pi-data-value').text,
    "English_name":character_information[2].find('div',class_='pi-data-value').text,
    "Debut":character_information[3].find('div',class_='pi-data-value').text,
    "Affiliations":character_information[4].find('div',class_='pi-data-value').text,
    "Occupations":character_information[5].find('div',class_='pi-data-value').text,
    #Ignoring Status because spoilers
    "Birthday":character_information[7].find('div',class_='pi-data-value').text
    #Don't need VA so will leave off the rest
}
print(character_map)
text=character_information[2].find('div',class_='pi-data-value').text.split('(VIZ')
print(text[0])
print(character_information[4].find('div',class_='pi-data-value').text)
