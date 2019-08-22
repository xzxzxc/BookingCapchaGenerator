from selenium import webdriver
from urllib.request import build_opener
from PIL import Image
from time import sleep

startUrl = 'https://booking.uz.gov.ua/en/?from=2200001&to=2218000&date=2019-08-12&time=00%3A00&url=train-list'

driver = webdriver.Chrome()

items_count = 500
audios_count = 10
user_agent = driver.execute_script("return navigator.userAgent;")

driver.get(startUrl)
cookies = driver.get_cookies()

def download(url, save_path, cookies):
    opener = build_opener()
    opener.addheaders[0] = (opener.addheaders[0][0], user_agent)
    opener.addheaders.append(('Accept', '*/*'))
    opener.addheaders.append(('Accept-Encoding', 'identity;q=1, *;q=0'))
    opener.addheaders.append(('Accept-Language', 'en-US,en;q=0.9,ru;q=0.8'))
    opener.addheaders.append(('Connection', 'keep-alive'))
    opener.addheaders.append(('Cookie', "; ".join([cookie['name'] + '=' + cookie['value'] for cookie in cookies])))    
    opener.addheaders.append(('Host', 'booking.uz.gov.ua'))
    opener.addheaders.append(('Range', 'bytes=0-'))
    opener.addheaders.append(('Referer', startUrl))
    opener.addheaders.append(('Sec-Fetch-Mode', 'no-cors'))
    opener.addheaders.append(('Sec-Fetch-Site', 'same-origin'))
    r = opener.open(url)
    content = r.read()
    with open(save_path, 'wb') as out_file:
        out_file.write(content)

def save_image(element, save_path):
    # in case the image isn't isn't in the view yet
    location = element.location_once_scrolled_into_view
    size = element.size

    # saves screenshot of entire page
    driver.save_screenshot(save_path)
    # uses PIL library to open image in memory

    image = Image.open(save_path)
    points = (location['x'], location['y'], location['x'] + size['width'], location['y'] + size['height'])
    image = image.crop(points)  # defines crop points
    image.save(save_path, 'png')  # saves new cropped image

for i in range(0, items_count):
    sleep(0.5)
    img = driver.find_element_by_css_selector('div.input > img')
    save_image(img, "res/{i}.png".format(i=i))

    audio_button = driver.find_element_by_css_selector('button.listen')

    for j in range(0, audios_count):
        audio_button.click()
        sleep(0.25)
        audio = driver.find_element_by_css_selector('audio > source.wav')
        audioUrl = audio.get_attribute("src")
        download(audioUrl, "res/{i}_{j}.wav".format(i=i, j=j), cookies)

    reload_btn = driver.find_element_by_css_selector('button.reload')
    reload_btn.click()

    
driver.close()
    
