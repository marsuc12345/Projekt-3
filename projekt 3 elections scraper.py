import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
import pprint

url = "https://volby.cz/pls/ps2021/ps32?xjazyk=CZ&xkraj=14&xnumnuts=8103"
vystup = ""

# faze 1 v linku nize skrejpovat LINK, CISLO a NAZEV obci do slovniku

req_obce = requests.get(url)
soup_obce = bs(req_obce.text, "html.parser")

nalezene_odkazy = []
for a_elem in soup_obce.find_all("a"):
    href = urljoin(url, a_elem["href"])
    if len(href) > 70 and href not in nalezene_odkazy:
        nalezene_odkazy.append(href)
# pprint.pprint(nalezene_odkazy)

nalezene_obce = []
for elem in soup_obce.find_all("td",{"class":"overflow_name"}):
    text = elem.text
    nalezene_obce.append(text)
# print(nalezene_obce)

nalezene_cisla = []
for znak in nalezene_odkazy:
    nalezene_cisla.append(znak[59:65])              # funkcnejsi skrejp pro jine okrsky - napr. u prahy to nefachci
# print(nalezene_cisla)


# faze 2 skrejpovat hlavicku a vsechny potrebne udaje z linku vsech obci + ulozeni do .csv

hlavicka = ["kód obce","název obce","voliči v seznamu","vydané obálky","platné hlasy"]
req_hlavicka = requests.get(nalezene_odkazy[0])
soup_hlavicka = bs(req_hlavicka.text, "html.parser")
for prvek in soup_hlavicka.find_all("td", {"headers": ["t1sa1 t1sb2","t2sa1 t2sb2"]}):
    nadpis = prvek.text
    hlavicka.append(nadpis)
print(hlavicka[:-1])                                # pridat hlavicku do .csv !!!

nalezene_udaje = []
index = 0
for link in nalezene_odkazy:
    req_detaily = requests.get(link)
    soup_detaily = bs(req_detaily.text, "html.parser")
    nalezene_udaje.append(nalezene_cisla[index])
    nalezene_udaje.append(nalezene_obce[index])
    index += 1
    for elem in soup_detaily.find_all("td",{"headers":["sa2","sa3","sa6","t1sa2 t1sb3","t2sa2 t2sb3"]}):
        text = elem.text
        nalezene_udaje.append(text)
    print(nalezene_udaje[:-1])                      # pridat tisk radku do .csv !!!
    break                                           # STOP pro prvni obec kvuli delce procesu !!!


