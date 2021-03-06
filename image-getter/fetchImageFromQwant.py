import sys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import urllib
import urllib.request
import random

defaultNumberOfImage = 5

def getBrowser():
    binary = r'/usr/bin/firefox'
    cap = DesiredCapabilities().FIREFOX
    cap["marionette"] = True
    options = Options()
    options.headless = True
    options.binary = binary
    return webdriver.Firefox(capabilities=cap, firefox_options=options, executable_path=r'/usr/local/bin/geckodriver')

def selectRandomImage(images):
    selected = random.randint(0, len(images)-1)
    images[selected], images[-1] = images[-1], images[selected]
    return images

def getImage(keyword, number=defaultNumberOfImage):
    images = fetchQwantImages(keyword, number)
    # selectRandomImage(images)
    # print(images)
    return images

#mode = 0 -> recherche "coloriage + keyword"
#mode = 1 -> recherche "keyword" en monochrome & transparent
def fetchQwantImages(keyword, number=defaultNumberOfImage, mode=0):
    fetchedImages = []
    if(not mode):
        url = "https://www.qwant.com/?q="+keyword+"&t=images&color=monochrome&imagetype=transparent"
    else :
        url = "https://www.qwant.com/?q=coloriage%20"+keyword+"&t=images"
    print(url)
    browser = getBrowser()
    browser.get(url)
    counter = 0
    timeout = 10
    try:
        element_present = EC.presence_of_element_located((By.CLASS_NAME, 'result--images'))
        WebDriverWait(browser, timeout).until(element_present)
    except TimeoutException:
        browser.close()
        print("Timed out waiting for page to load")
        return (fetchedImages, ["Timed out waiting for page to load", 1])
    except Ewception:
        print("Unknown error")
        browser.close()
        return (fetchedImages, ["Unknown error", 2])
    for x in browser.find_elements_by_xpath("//div[contains(@class, 'result--images')]"):
        name = './image/' + str(keyword) + str(counter)
        url = x.find_element_by_tag_name('a').get_attribute('href')
        imgtype = url.split(".").pop()
        try :
            fetchedImages.append(saveImage(url, [name, imgtype]))
            counter = counter + 1
            if counter >= number :
                break
        except Exception as e:
            print(e)
            print( "can't get img")
    browser.close()
    return (fetchedImages, ["Success", 0])


def saveImage(url, outfile):
    print(url)
    response = urllib.request.urlopen(url)
    image = response.read()
    with open('.'.join(outfile), 'wb') as f:
        f.write(image)
    return outfile


if __name__ == '__main__':
    # first arg is keyword, second is number of image to dl, third is the mode
    print(fetchQwantImages(sys.argv[1], int(sys.argv[2]), int(sys.argv[3])))
