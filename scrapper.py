from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from urllib.parse import urlparse
import time


max_images_to_retrieve = 10000
query = "hands"
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
driver_service = Service("/opt/homebrew/bin/chromedriver")
driver = webdriver.Chrome(service=driver_service, options=options)
weblink = f"https://www.google.com/search?q={query}&hl=en-US&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjSuLy81pv5AhXwADQIHaJEAkkQ_AUoAXoECAIQAw&cshid=1659014492371764&biw=2056&bih=1207&dpr=2"


def write_image_to_dataset(image_link, image_name):
    image = open(f"dataset/{image_name}.png", "wb")
    image.write(image_link.screenshot_as_png)
    image.close()

def scroll_to_bottom(driver):
    script = "window.scrollTo(0, document.body.scrollHeight);"
    driver.execute_script(script)
    time.sleep(5)


def fetch_image_urls(query, sleep_between_interactions: int = 1):
    img_num = 0
    driver.get(weblink)
    while img_num < max_images_to_retrieve:
        scroll_to_bottom(driver)
        # Fetch the image and download it as a png file.
        image_links = driver.find_elements(By.CLASS_NAME, "rg_i.Q4LuWd")
        load_more_button = driver.find_element(By.CSS_SELECTOR, ".mye4qd")
        if load_more_button:
            driver.execute_script("document.querySelector('.mye4qd').click();")
        # Iterate through each image link and download it onto the datasets folder.
        for image_link in image_links:
            print(f"Collecting image {img_num}")
            write_image_to_dataset(image_link, f"hand_{img_num}")
            img_num += 1

fetch_image_urls("hands")
driver.close()
