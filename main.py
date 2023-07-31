from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import os
import json
import tkinter as tk
from tkinter import filedialog

# Import jmena hesla pomoci systemove promenne, tak aby nebylo v kodu videt - bude fungovat pouze pokud skript bude pusten na tomto PC
username = os.environ.get('UNOB')
password = os.environ.get('PASSWORD')

# Headless mode (bezi na pozadi)
options = Options()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)

# Otevreni pozadované stránky
driver.get("https://vav.unob.cz/departments/index")
# Shodí okno do lišty ať furt nevyskakuje stránka
driver.minimize_window()

# Najde login pole a vyplní údaje
username_pole = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
username_pole.send_keys(username)

password_pole = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "password")))
password_pole.send_keys(password)

# Klikne na login tlačítko
login_button = driver.find_element(By.CSS_SELECTOR, ".button-background")
login_button.click()

# Názvy fakult a pracovišt
nazev_1 = driver.find_elements(By.CSS_SELECTOR, "table.stripped:nth-child(2) > tbody:nth-child(1) > tr:nth-child(1)")
Fakulta_FVL = nazev_1[0].find_element(By.TAG_NAME, "th").text

nazev_2 = driver.find_elements(By.CSS_SELECTOR, "table.stripped:nth-child(4) > tbody:nth-child(1) > tr:nth-child(1)")
Fakulta_FVT = nazev_2[0].find_element(By.TAG_NAME, "th").text

nazev_3 = driver.find_elements(By.CSS_SELECTOR, "table.stripped:nth-child(6) > tbody:nth-child(1) > tr:nth-child(1)")
Fakulta_FVZ = nazev_3[0].find_element(By.TAG_NAME, "th").text

nazev_4= driver.find_elements(By.CSS_SELECTOR, "table.stripped:nth-child(9) > tbody:nth-child(1) > tr:nth-child(1)")
Ustavy_a_Centra = nazev_4[0].find_element(By.TAG_NAME, "th").text


###################################-FUNKCE-########################################### 

def ZadejKatedru(i):
    cislo = ""
    while cislo not in range(1, i):
        cislo = int(input("Zadej pořadové číslo katedry: "))
    return cislo

def ZadejCentrum(i):
    cislo = ""
    while cislo not in range(1, i):
        cislo = int(input("Zadej pořadové číslo pracoviště: "))
    return cislo

def StahniData(odkaz, radky, numbers, ulozeni):
    # Prazdny list pro temp. ulozeni dat
    data = []
    # Extrakce dat
    for i, radek in enumerate(radky):
        sloupce = radek.find_elements(By.XPATH, './/td')
        if sloupce:
            hodnost = sloupce[0].text
            jmeno = sloupce[1].text
            telefony = sloupce[2].text
            if i < len(numbers) + 1:  # Check if the index is within the range of the 'numbers' list
                id = numbers[i - 1]  # Use the next number from the 'numbers' list
                data.append({
                    'Hodnost/Tituly': hodnost,
                    'Jmeno': jmeno,
                    'Telefony': telefony,
                    'ID': id
                })
    # Zápis do JSON filu
    with open('{}'.format(ulozeni), 'w') as f:
        json.dump(data, f, indent=4)
    print('Data byla úspěšně uložena do json souboru.')

###################################-MENU-###########################################
print("Pracoviště:")
print("----------------------------------------------")
print("#1 - " + Fakulta_FVL)
print("#2 - " + Fakulta_FVT)
print("#3 - " + Fakulta_FVZ)
print("#4 - " + Ustavy_a_Centra)

cislo = ""
while cislo not in ["1", "2", "3", "4"]:
    cislo = input("Zadejte číslo pracoviště (1-4): ")

###################################-TABULKY-###########################################

# Tabulka FVL
if cislo == "1":
    i = 1
    tabulka = driver.find_element(By.CSS_SELECTOR, "table.list")
    print("[>]" + Fakulta_FVL)
    print("----------------------------------------------")
    # projití všech řádků tabulky a vypsání dat
    for radek in tabulka.find_elements(By.CSS_SELECTOR, "tr"):
        bunka = radek.find_elements(By.CSS_SELECTOR,"td")
        if bunka:
            print("[{}]".format(i) + bunka[0].text, bunka[1].text)
            i += 1
    cislo_katedry = ZadejKatedru(i)
    if cislo_katedry == 1:
        # Katedra kvantitativních metod  
        odkaz = driver.get("https://vav.unob.cz/department/index/121")
        radek = driver.find_elements(By.XPATH, '//table[@class="stripped list max-width"]/tbody/tr')
        StahniData(odkaz, radek)
    elif cislo_katedry == 2:
        # Katedra řízení zdrojů  
        odkaz = driver.get("https://vav.unob.cz/department/index/111")
        radek = driver.find_elements(By.XPATH, '//table[@class="stripped list max-width"]/tbody/tr')
        StahniData(odkaz, radek)
    elif cislo_katedry == 3:
        # Katedra leadershipu 
        odkaz = driver.get("https://vav.unob.cz/department/index/139")
        radek = driver.find_elements(By.XPATH, '//table[@class="stripped list max-width"]/tbody/tr')
    elif cislo_katedry == 4:
        # Katedra teorie vojenství 
        odkaz = driver.get("https://vav.unob.cz/department/index/140")
        radek = driver.find_elements(By.XPATH, '//table[@class="stripped list max-width"]/tbody/tr')
        StahniData(odkaz, radek)
    elif cislo_katedry == 5:
        # Katedra palebné podpory  
        odkaz = driver.get("https://vav.unob.cz/department/index/107")
        radek = driver.find_elements(By.XPATH, '//table[@class="stripped list max-width"]/tbody/tr')
    elif cislo_katedry == 6:
        # Katedra ženijní podpory 
        odkaz = driver.get("https://vav.unob.cz/department/index/132")
        radek = driver.find_elements(By.XPATH, '//table[@class="stripped list max-width"]/tbody/tr')
        StahniData(odkaz, radek)
    elif cislo_katedry == 7:
        # Katedra logistiky 
        odkaz = driver.get("https://vav.unob.cz/department/index/83")
        radek = driver.find_elements(By.XPATH, '//table[@class="stripped list max-width"]/tbody/tr')
    elif cislo_katedry == 8:
        #  Katedra vševojskové taktiky 
        odkaz = driver.get("https://vav.unob.cz/department/index/110")
        radek = driver.find_elements(By.XPATH, '//table[@class="stripped list max-width"]/tbody/tr')
        StahniData(odkaz, radek)
    elif cislo_katedry == 9:
        # Katedra zpravodajského zabezpečení 
        odkaz = driver.get("https://vav.unob.cz/department/index/186")
        radek = driver.find_elements(By.XPATH, '//table[@class="stripped list max-width"]/tbody/tr')

# Tabulka FVT
elif cislo == "2":
    i = 1
    tabulka = driver.find_element(By.CSS_SELECTOR, "table.stripped:nth-child(4)")
    print("[#]" + Fakulta_FVT)
    print("----------------------------------------------")
    # projití všech řádků tabulky a vypsání dat
    for radek in tabulka.find_elements(By.CSS_SELECTOR, "tr"):
        sloupec = radek.find_elements(By.CSS_SELECTOR,"td")
        if sloupec:
            print("[{}] ".format(i) + sloupec[0].text, sloupec[1].text)
            i += 1
    cislo_katedry = ZadejKatedru(i)
    if cislo_katedry == 1:
        # Katedra zbraní a munice 
        odkaz = driver.get("https://vav.unob.cz/department/index/81")
        radek = driver.find_elements(By.XPATH, '//table[@class="stripped list max-width"]/tbody/tr')
        StahniData(odkaz, radek, ulozeni="K201.json")
    elif cislo_katedry == 2:
        # Katedra bojových a speciálních vozidel 
        odkaz = driver.get("https://vav.unob.cz/department/index/109")
        radek = driver.find_elements(By.XPATH, '//table[@class="stripped list max-width"]/tbody/tr')
        StahniData(odkaz, radek, ulozeni="K202.json")
    elif cislo_katedry == 3:
        # Katedra ženijních technologií 
        odkaz = driver.get("https://vav.unob.cz/department/index/90")
        radek = driver.find_elements(By.XPATH, '//table[@class="stripped list max-width"]/tbody/tr')
        StahniData(odkaz, radek, ulozeni="K203.json")
    elif cislo_katedry == 4:
        # Katedra letectva 
        odkaz = driver.get("https://vav.unob.cz/department/index/86")
        radek = driver.find_elements(By.XPATH, '//table[@class="stripped list max-width"]/tbody/tr')
        StahniData(odkaz, radek, ulozeni="K205.json")
    elif cislo_katedry == 5:
        # Katedra letecké techniky  
        odkaz = driver.get("https://vav.unob.cz/department/index/73")
        radek = driver.find_elements(By.XPATH, '//table[@class="stripped list max-width"]/tbody/tr')
        StahniData(odkaz, radek, ulozeni="K206.json")
    elif cislo_katedry == 6:
        # Katedra komunikačních technologií, elektronického boje a radiolokace  
        odkaz = driver.get("https://vav.unob.cz/department/index/117")
        radek = driver.find_elements(By.XPATH, '//table[@class="stripped list max-width"]/tbody/tr')
        StahniData(odkaz, radek, ulozeni="K207.json")
    elif cislo_katedry == 7:
        # Katedra protivzdušné obrany 
        odkaz = driver.get("https://vav.unob.cz/department/index/101")
        radek = driver.find_elements(By.XPATH, '//table[@class="stripped list max-width"]/tbody/tr')
        StahniData(odkaz, radek, ulozeni="K208.json")



    elif cislo_katedry == 8:
        # Katedra informatiky a kybernetických operací  
        # Removed the driver.get() call and assigned the URL to 'odkaz' directly
        odkaz = "https://vav.unob.cz/department/index/114"

        # Open the URL
        driver.get(odkaz)

        # Find all the <tr> elements
        radek = driver.find_elements(By.XPATH, '//table[@class="stripped list max-width"]/tbody/tr')

        # Find all the <a> elements within <td> elements
        td_elements = driver.find_elements(By.XPATH, '//table[@class="stripped list max-width"]/tbody/tr/td/a')

        # Extract the numbers after "/index" in each link
        numbers = []
        for td_element in td_elements:
            href = td_element.get_attribute("href")
            index = href.rfind("/index/")
            if index != -1:
                number = href[index + len("/index/"):]
                numbers.append(number)
        
        StahniData(odkaz, radek, numbers, ulozeni="K209.json")



    elif cislo_katedry == 9:
        # Katedra vojenské geografie a meteorologie  
        odkaz = driver.get("https://vav.unob.cz/department/index/115")
        radek = driver.find_elements(By.XPATH, '//table[@class="stripped list max-width"]/tbody/tr')
        StahniData(odkaz, radek, ulozeni="K210.json")
    elif cislo_katedry == 10:
        # Katedra vojenské robotiky 
        odkaz = driver.get("https://vav.unob.cz/department/index/252")
        radek = driver.find_elements(By.XPATH, '//table[@class="stripped list max-width"]/tbody/tr')
        StahniData(odkaz, radek, ulozeni="K211.json")   
    elif cislo_katedry == 11:
        # Katedra matematiky a fyziky  
        odkaz = driver.get("https://vav.unob.cz/department/index/122")
        radek = driver.find_elements(By.XPATH, '//table[@class="stripped list max-width"]/tbody/tr')
        StahniData(odkaz, radek, ulozeni="K215.json")
    elif cislo_katedry == 12:
        # Katedra strojírenství  
        odkaz = driver.get("https://vav.unob.cz/department/index/119")
        radek = driver.find_elements(By.XPATH, '//table[@class="stripped list max-width"]/tbody/tr') 
        StahniData(odkaz, radek, ulozeni="K216.json")
    elif cislo_katedry == 13:
        # Katedra elektrotechniky 
        odkaz = driver.get("https://vav.unob.cz/department/index/100")
        radek = driver.find_elements(By.XPATH, '//table[@class="stripped list max-width"]/tbody/tr')
        StahniData(odkaz, radek, ulozeni="K217.json")

# Tabulka FVZ
elif cislo == "3":
    i = 1
    tabulka = driver.find_element(By.CSS_SELECTOR, "table.stripped:nth-child(6)")
    print("[#]" + Fakulta_FVZ)
    print("----------------------------------------------")
    # projití všech řádků tabulky a vypsání dat
    for radek in tabulka.find_elements(By.CSS_SELECTOR, "tr"):
        bunka = radek.find_elements(By.CSS_SELECTOR,"td")
        if bunka:
            print("[{}]".format(i) + bunka[0].text, bunka[1].text)
            i += 1
    cislo_katedry = ZadejKatedru(i)
    if cislo_katedry == 1:
        # Katedra epidemiologie 
        odkaz = driver.get("https://vav.unob.cz/department/index/121")
        radek = driver.find_elements(By.XPATH, '//table[@class="stripped list max-width"]/tbody/tr')
        StahniData(odkaz, radek)
    elif cislo_katedry == 2:
        # Katedra organizace vojenského zdravotnictví a managementu 
        odkaz = driver.get("https://vav.unob.cz/department/index/121")
        radek = driver.find_elements(By.XPATH, '//table[@class="stripped list max-width"]/tbody/tr')
        StahniData(odkaz, radek)
    elif cislo_katedry == 3:
        # Katedra radiobiologie 
        odkaz = driver.get("https://vav.unob.cz/department/index/121")
        radek = driver.find_elements(By.XPATH, '//table[@class="stripped list max-width"]/tbody/tr')
    elif cislo_katedry == 4:
        # Katedra toxikologie a vojenské farmacie  
        odkaz = driver.get("https://vav.unob.cz/department/index/121")
        radek = driver.find_elements(By.XPATH, '//table[@class="stripped list max-width"]/tbody/tr')
        StahniData(odkaz, radek)
    elif cislo_katedry == 5:
        # Katedra vojenské chirurgie  
        odkaz = driver.get("https://vav.unob.cz/department/index/121")
        radek = driver.find_elements(By.XPATH, '//table[@class="stripped list max-width"]/tbody/tr')
    elif cislo_katedry == 6:
        # Katedra vojenského vnitřního lékařství a vojenské hygieny  
        odkaz = driver.get("https://vav.unob.cz/department/index/121")
        radek = driver.find_elements(By.XPATH, '//table[@class="stripped list max-width"]/tbody/tr')
        StahniData(odkaz, radek)
    elif cislo_katedry == 7:
        # Katedra urgentní medicíny a vojenského všeobecného lékařství 
        odkaz = driver.get("https://vav.unob.cz/department/index/121")
        radek = driver.find_elements(By.XPATH, '//table[@class="stripped list max-width"]/tbody/tr')
    elif cislo_katedry == 8:
        # Katedra molekulární patologie a biologie  
        odkaz = driver.get("https://vav.unob.cz/department/index/121")
        radek = driver.find_elements(By.XPATH, '//table[@class="stripped list max-width"]/tbody/tr')
        StahniData(odkaz, radek)

# Tabulka Ustavu a center
elif cislo == "4":
    i = 1
    tabulka = driver.find_element(By.CSS_SELECTOR, "table.stripped:nth-child(9)")
    print("[#]" + Ustavy_a_Centra)
    print("----------------------------------------------")
    # projití všech řádků tabulky a vypsání dat
    for radek in tabulka.find_elements(By.CSS_SELECTOR, "tr"):
        bunka = radek.find_elements(By.CSS_SELECTOR,"td")
        if bunka:
            print("[{}]".format(i) + bunka[0].text, bunka[1].text)
            i += 1
    zkratka_centra = ZadejCentrum(i)
    if  zkratka_centra == 1:
        # Ústav ochrany proti zbraním hromadného ničení  
        odkaz = driver.get("https://vav.unob.cz/department/index/121")
        radek = driver.find_elements(By.XPATH, '//table[@class="stripped list max-width"]/tbody/tr')
        StahniData(odkaz, radek)
    elif zkratka_centra== 2:
        # Centrum bezpečnostních a vojenskostrategických studií 
        odkaz = driver.get("https://vav.unob.cz/department/index/121")
        radek = driver.find_elements(By.XPATH, '//table[@class="stripped list max-width"]/tbody/tr')
        StahniData(odkaz, radek)
    elif zkratka_centra == 3:
        # Centrum jazykového vzdělávání 
        odkaz = driver.get("https://vav.unob.cz/department/index/121")
        radek = driver.find_elements(By.XPATH, '//table[@class="stripped list max-width"]/tbody/tr')
    elif zkratka_centra == 4:
        # Centrum tělesné výchovy a sportu 
        odkaz = driver.get("https://vav.unob.cz/department/index/121")
        radek = driver.find_elements(By.XPATH, '//table[@class="stripped list max-width"]/tbody/tr')
        StahniData(odkaz, radek)
    elif zkratka_centra == 5:
        # Ústav zpravodajských studií 
        odkaz = driver.get("https://vav.unob.cz/department/index/121")
        radek = driver.find_elements(By.XPATH, '//table[@class="stripped list max-width"]/tbody/tr')

