import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

options = webdriver.ChromeOptions()

def scraper(url, deep_scrap):
    base_url = url.split(".com")[0] + ".com"

    driver = webdriver.Remote("http://ais-chrome:4444/wd/hub", DesiredCapabilities.CHROME, options=options)
    driver.get(url)
    while True:
        try:
            if not deep_scrap:
                body = driver.find_element(By.TAG_NAME, "body").text
                time.sleep(10)
                if len(body) > 0:
                    driver.quit()
                    return [body]
            else:
                links = driver.find_elements(By.TAG_NAME, "a")
                if len(links) > 0:
                    all_links = [link.get_attribute('href') for link in links]
                    filtered_links = list(set(link for link in all_links if link and not link.endswith((".com", ".com/", "/home", "/sitemap", "/.xml", "/feed.xml")) and link.startswith(base_url) and not any(word in link for word in ["login", "signup", "sign-up", "auth"])))
                    scraped_bodies = []
                    if(len(filtered_links) > 0):
                        for innerlink in filtered_links[:2]:
                            time.sleep(5)
                            driver.get(innerlink)
                            while True:
                                try:
                                    body = driver.find_element(By.TAG_NAME, "body").text
                                    if len(body) > 0:
                                        scraped_bodies.append(body)
                                        break
                                    else:
                                        time.sleep(5)
                                except:
                                    time.sleep(2)
                        if len(scraped_bodies) > 0:
                            driver.quit()
                            return scraped_bodies
                else:
                    time.sleep(5)
        except Exception as e:
            return {"error": str(e)}
