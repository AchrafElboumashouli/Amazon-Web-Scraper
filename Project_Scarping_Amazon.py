import requests
from bs4 import BeautifulSoup
import csv

def scrape_amazon_prices(search_query):
    url = f"https://www.amazon.fr/s?k={search_query}&crid=KHIE3AB1F6FC&sprefix=sm%2Caps%2C148&ref=nb_sb_ss_ts-doa-p_1_2"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
        }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        products = soup.find_all('div', {'data-component-type': 's-search-result'})
        
        product_data = []
        
        for product in products:
            product_name = product.find('h2').text.strip()
            price_element = product.find('span', {'class': 'a-price-whole'})
            if price_element:
                price = price_element.text.strip()+"€"
            else:
                price = "Prix non disponible"
            
            product_link = "https://www.amazon.fr" + product.find('a', {'class': 'a-link-normal'})['href']
            
            product_data.append({
                'name': product_name,
                'price': price,
                'link': product_link
            })
        
        return product_data
    else:
        print(f"Erreur lors de la requête HTTP : {response.status_code}")
        return None
        

# RUN MAIN FUNCTION

print("This script is running directly")
#smartphones
search_query = input('Entrez le nom du produit que vous souhaitez Scarper sur Amazon: ')
products = scrape_amazon_prices(search_query)
afficher = input('Voulez-vous afficher les résultats dans la console? (Y/N): ')
    
if products:
    with open(f'products_{search_query}.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Nom', 'Prix', 'Lien'])
        for product in products:
            writer.writerow([product['name'], product['price'], product['link']])
            if afficher == 'Y' or afficher == 'y':
                print(f"Nom: {product['name']}")
                print(f"Prix: {product['price']}")
                #print(f"Lien: {product['link']}")
                print("-" * 50)

print(f"Les données ont été enregistrées dans le fichier products_{search_query}.csv")