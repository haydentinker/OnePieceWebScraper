import requests
from bs4 import BeautifulSoup
URL="https://onepiece.fandom.com/wiki/List_of_Canon_Characters"
all_characters_page=requests.get(URL)
soup=BeautifulSoup(all_characters_page.content, "html.parser")
print('Classes of each table:')
for table in soup.find_all('table'):
    print(table.get('class'))
table = soup.find('table', class_='wikitable sortable')
for row in table.tbody.find_all('tr'):    
    # Find all data for each column
    columns = row.find_all('td')
    if columns !=[]:
        print(columns[1].contents)
