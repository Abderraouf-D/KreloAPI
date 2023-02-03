import os
import requests as r
import bs4
from schemas import AnnonceBase
import nums_from_string 
import requests 
from json import loads , dumps , dump ,load

#TODO This is an unfinished version 

wilayas = ['Adrar', 'Chlef', 'Laghouat', 'Oum El Bouaghi', 'Batna', 'Béjaia', 'Biskra', 'Béchar', 'Blida', 'Bouira', 'Tamanrasset', 'Tébessa', 'Tlemcen', 'Tiaret', 'Tizi Ouzou', 'Alger', 'Djelfa', 'Jijel', 'Sétif', 'Saida', 'Skikda', 'Sidi Bel Abbès', 'Annaba', 'Guelma', 'Constantine', 'Médéa', 'Mostaganem', "Msila", 'Mascara', 'Ouargla', 'Oran', 'El Bayadh', 'Illizi', 'Bordj Bou Arreridj', 'Boumerdès', 'El Tarf', 'Tindouf', 'Tissemsilt', 'El Oued', 'Khenchela', 'Souk Ahras', 'Tipaza', 'Mila', 'Aïn Defla', 'Naâma', 'Ain Temouchent', 'Ghardaia', 'Relizane', 'Timimoun', 'Bordj Badji Mokhtar', 'Ouled Djellal', 'Béni Abbès', 'In Salah', 'In Guezzam', 'Touggourt', 'Djanet', "El M'Ghair", 'El Meniaa']



# get html code of tha pege
def getData(url):
    html = r.get(url)
    soup = bs4.BeautifulSoup(html.text, "html.parser")
    return soup

#get the listings from each  table row in  the current page
def getPageListings(soup):
    folder_path = "uploads"
    listings = []

    #extract the table of listings 
    rows = soup.find_all('tr', class_='Tableau1')
    
    
    #looping through each row 
    for row in rows:
        attr = row.find_all('td')[7].find("a") #getting the row field that contains the title and link to the actual liting

        listingUrl = "http://www.annonce-algerie.com/" + str(attr.get("href"))

        annonceSoup = getData(listingUrl) #get the html content ( soup ) off the listing 

        ref= nums_from_string.get_nums(annonceSoup.find('tr',class_="da_entete").find('td').text)[0] #reference of the listing ( used to check if it already exists or no)
        #check if the listing already exists in the db 
        with open('annonces_scraping_refs.json','r') as file :
             content = file.read()
        refSet = loads(content)


        if ref in  refSet :
            print("already")
            continue
        
            

        

        
        annonce = annonceSoup.find_all('table', class_='da_rub_cadre')
        annonceDetails = annonce[1]

        # extract listing fields
        attribut = annonceDetails.find_all('td', class_='da_label_field')
        attribut = [i.text for i in attribut]
        try:
            fields = annonceDetails.find_all('td', class_='da_field_text')
            an = AnnonceBase(
                utilisateur_id = -ref ,
                titre = attr.text,
                categorie = 0 ,#fields[attribut.index('Catégorie')].find_all('a')[1].text,
                type = 0,#fields[attribut.index('Catégorie')].find_all('a')[2].text,
                wilaya = wilayas.index(fields[attribut.index('Localisation')].find_all('a')[2].text),
                commune = 0 , #"""fields[attribut.index('Localisation')].find_all('a')[3].text"""
                adresse = fields[attribut.index('Adresse')].text,
                surface = nums_from_string.get_nums(fields[attribut.index('Surface')].text.replace(" ",''))[0],
                prix = nums_from_string.get_nums(fields[attribut.index('Prix')].text.replace(" ",''))[0],
                description = fields[attribut.index('Texte')].text ,
                isScraped=False ,
                photos=""
            )
            #print(an)
            
            
        except ValueError as e: 
            print("A field is missing :")
            print (e)
            
        except Exception as e : 
            print("smth went wrong :") 
            print (e)   
            
        else :
            refSet.append(ref)
            with open('annonces_scraping_refs.json', 'w') as file:
            # Write the set into the file
                dump(list(refSet), file)
            # images ...
            annoncePhotos = annonce[3]
            images = annoncePhotos.find_all('img')
            imgList =[]
            if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
            for  i , img in enumerate(images) : 
                fileUrl = "http://www.annonce-algerie.com" + str(img.get('src'))
                response = requests.get(fileUrl)
                file_path = os.path.join("uploads", fileUrl.split('/').pop())
                with open(file_path, "wb") as f:
                    f.write(response.content)
                    imgList.append(file_path)
            an.photos= ';'.join(imgList)  
            listings.append(an)
    
    return listings


# looping through pages and getting table content
def getListings():

    i = 1
    while i < 9:
        url = f"http://www.annonce-algerie.com/AnnoncesImmobilier.asp?rech_cod_cat=1&rech_cod_rub=&rech_cod_typ=&rech_cod_sou_typ=&rech_cod_pay=DZ&rech_cod_reg=&rech_cod_vil=&rech_cod_loc=&rech_prix_min=&rech_prix_max=&rech_surf_min=&rech_surf_max=&rech_age=&rech_photo=&rech_typ_cli=&rech_order_by=31&rech_page_num={i}"
        soup = getData(url)
        if (not soup):
            break
        listings = getPageListings(soup)
        print( listings)
        i += 1
 # test


getListings()
