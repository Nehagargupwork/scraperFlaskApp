from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from colorama import init, Fore

# Initialize colorama for colored output
init(autoreset=True)

def get_keyword_rank_and_volume(keyword='flask python', domain='geeksforgeeks.org', region='in'):
    chrome_options = Options()
    chrome_options.add_argument('--headless')  
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-infobars')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--window-size=1200,800')

    try:
        # Automatically download the correct version of ChromeDriver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

        search_url = f"https://www.google.com/search?q={keyword}&gl={region}&num=20"
        driver.get(search_url)
        sleep(3)

        all_results = driver.find_elements(By.CSS_SELECTOR, '.yuRUbf a')
        filtered_urls = []

        for result in all_results:
            try:
                parent = result.find_element(By.XPATH, './ancestor::*[contains(@class, "Wt5Tfe")]')
                if parent:
                    continue
            except NoSuchElementException:
                href = result.get_attribute('href')
                if href:
                    filtered_urls.append(href)

        print(Fore.GREEN + "Filtered results:", Fore.GREEN + str(filtered_urls))

        normalized_domain = domain.replace("www.", "")
        rank = -1

        for i, url in enumerate(filtered_urls):
            extracted_domain = url.split('/')[2].replace("www.", "")
            if extracted_domain == normalized_domain:
                rank = i + 1
                break

        driver.quit()

        if rank != -1:
            print(f"Domain '{domain}' for keyword '{keyword} found at position {rank}")
        else:
            print(f"Domain '{domain}' not found for keyword '{keyword}' in top results")


        return rank if rank != -1 else 'Not found in top results'

    except WebDriverException as e:
        print("WebDriver error:", e)
        if driver:
            driver.quit()
        return None

    except Exception as e:
        print("An error occurred:", e)
        if driver:
            driver.quit()
        return None
