from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selene.driver import SeleneDriver
from webdriver_manager.chrome import ChromeDriverManager
import re
import time
import urllib.request
import random
from PIL import Image
import os


def download(path, title):
    urllib.request.urlretrieve(path, "{0}".format(title))


def main():
    ranking_url = "https://3ds.pokemon-gl.com/battle/usum/"
    options = Options()
    options.add_argument('--headless')
    driver = SeleneDriver.wrap(webdriver.Chrome(executable_path=ChromeDriverManager().install(), chrome_options=options))
    driver.get(ranking_url)
    ranking = driver.find_elements_by_class_name("pokemon-ranking-item")
    pattern = r"\(.+?\)"
    reg = re.compile(pattern)
    ranking_img_paths = [reg.search(elem.find_element_by_tag_name("img").get_attribute("style")).group()[2:-2] for elem in ranking]
    ranking_pokemon_names = [elem.find_element_by_class_name("name").text for elem in ranking]
    for path, name in zip(ranking_img_paths, ranking_pokemon_names):
        file_name = os.path.join("data", name)
        download(path, file_name)
        row = Image.open(file_name)
        resize_img = row.resize((200, 200))
        crops = []
        crops.append(resize_img.crop((0, 0, 100, 100)))
        crops.append(resize_img.crop((100, 0, 200, 100)))
        crops.append(resize_img.crop((0, 100, 100, 200)))
        crops.append(resize_img.crop((100, 100, 200, 200)))
        output = Image.new('RGBA', (200, 200), (255, 255, 255))
        output.paste(crops[0], (100, 100))
        output.paste(crops[1], (0, 100))
        output.paste(crops[2], (100, 0))
        output.paste(crops[3], (0, 0))
        output.save(file_name, "PNG", quality=100, optimize=True)
    driver.quit()


if __name__ == "__main__":
    main()
