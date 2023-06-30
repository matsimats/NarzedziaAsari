import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from time import sleep

# Zmień ścieżkę do pliku JSON
input_file = 'C:/Users/root2/Katalon/Katalon dataFiles/Generated-Excel-Files/zaktualizowane_dane.json'

# Wczytaj dane z pliku JSON
with open(input_file) as file:
    data = pd.DataFrame(json.load(file))

# Zmień adres URL, który chcesz odwiedzić
url = 'https://release.asari.pro/index.html#seekers/list'

# Zmień te wartości na prawdziwe dane logowania
email = "mateusz.konstantinow@protoss.pl"
password = "PLMQAZWSXOKN"

# Utwórz instancję przeglądarki Chrome
browser = webdriver.Chrome(ChromeDriverManager().install())

# Wejdź na stronę logowania
browser.get(url)

# Znajdź elementy formularza: pola e-mail i hasło
# UWAGA: Zastąp 'input[id="user-email"]' i 'input[id="user-password"]' właściwymi selektorami CSS dla formularza na stronie
email_input = browser.find_element(By.CSS_SELECTOR, 'input[id="user-email"]')
password_input = browser.find_element(By.CSS_SELECTOR, 'input[id="user-password"]')

# Wpisz dane logowania do odpowiednich pól
email_input.send_keys(email)
password_input.send_keys(password)

# Naciśnij klawisz Enter, aby zatwierdzić formularz
password_input.send_keys(Keys.RETURN)

# Utwórz listę, która przechowuje kliknięte elementy
clicked_elements = []

# Wejdź na stronę
browser.get(url)

for _, row in data.iterrows():
    senchatest = row['senchatest']
    # Spróbuj znaleźć element zgodnie z wartością 'senchatest'
    try:
        element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f"[{senchatest}]"))
        )
        # Jeśli element nie został jeszcze kliknięty
        if element not in clicked_elements:
            # Kliknij element i dodaj go do listy klikniętych elementów
            element.click()
            clicked_elements.append(element)
            # Wróć na stronę główną
            browser.get(url)

    except (NoSuchElementException, TimeoutException):
        print(f"Element o atrybucie '{senchatest}' nie został znaleziony.")

# Zamknij przeglądarkę
browser.quit()
