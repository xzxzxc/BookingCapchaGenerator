from selenium import webdriver
from urllib.request import urlretrieve
from time import sleep

startUrl = 'https://booking.uz.gov.ua/en/?from=2200001&to=2218000&date=2019-08-12&time=00%3A00&url=train-list'

driver = webdriver.Chrome()
driver.get(startUrl)

items_count = 1
audios_count = 5

for i in range(0, items_count):
    img = driver.find_element_by_css_selector('div.input > img')
    imgUrl = img.get_attribute("src")
    urlretrieve(imgUrl, "res/{i}.png".format(i=i))
    button = driver.find_element_by_css_selector('button.listen')

    for j in range(0, audios_count):        
        button.click()
        sleep(0.25)
        audio = driver.find_element_by_css_selector('audio > source.wav')
        audioUrl = audio.get_attribute("src")
        urlretrieve(imgUrl, "res/{i}_{j}.wav".format(i=i, j=j))
    
driver.close()
    