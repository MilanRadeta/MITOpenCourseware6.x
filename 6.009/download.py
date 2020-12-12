import requests
import pathlib
from html.parser import HTMLParser
from bs4 import BeautifulSoup
import os

def download_files(cell, output_folder):
    for link in cell.select('a'):
        url = link['href']
        filename = url.split('/')[-1]
        if '.' in filename and 'lab_solution.py?lab=' not in filename:
            r = requests.get(url)
            with open('%s/%s' % (output_folder, filename), 'wb') as f:
                f.write(r.content)

def download_page(url, filename, output_folder):
    r = requests.get(url)
    with open('%s/%s' % (output_folder, filename), 'wb') as f:
        f.write(r.content)
    return r


root_folder = pathlib.Path(
    __file__).parent.absolute().__str__()


base_url = 'https://py.mit.edu/fall20'
r = download_page(base_url, 'home.html', root_folder)
soup = BeautifulSoup(r.content, 'html.parser')

row_index = -2
for row in soup.select('table tr'):
    row_index += 1
    col_index = -1
    folder_name = '%s/%02d' % (root_folder, row_index)
    for cell in row.select('td'):
        col_index += 1
        if col_index == 1:
            for s in cell.stripped_strings:
                if s == 'Video':
                    break
                folder_name += ' ' + s
            folder_name = folder_name.lower().replace(' ', '-')
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)

        if col_index in (1, 2, 3):
            download_files(cell, folder_name)
            
        if col_index == 3:
            for link in cell.select('a'):
                text = link.text
                url = link['href']
                filename = url.split('/')[-1]
                if '.' not in filename and ' Released' not in text:
                    download_page(url, filename + '.html', folder_name)



