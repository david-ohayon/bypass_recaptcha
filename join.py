# system libraries
import os
import warnings
from time import sleep
import requests
import numpy as np
import scipy.interpolate as si

# selenium libraries
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

warnings.filterwarnings("ignore", category=DeprecationWarning)
delayTime = 2
audioToTextDelay = 10
filename = 'captcha_audio.mp3'
url = 'https://www.google.com/recaptcha/api2/demo'
googleIBMLink = 'https://speech-to-text-demo.ng.bluemix.net/'

option = webdriver.ChromeOptions()
option.add_argument('lang=en')
option.add_argument("--mute-audio")
option.add_experimental_option("excludeSwitches", ["enable-logging"])
# option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
option.add_argument(
    "user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1")


def audioToText(mp3Path):
    driver.execute_script('''window.open("","_blank");''')
    driver.switch_to.window(driver.window_handles[1])

    driver.get(googleIBMLink)

    # Upload file
    sleep(1)
    driver.execute_script("window.scrollTo(0, 1000);")
    btn = driver.find_element(By.XPATH, '//*[@id="root"]/div/input')
    btn.send_keys(mp3Path)

    # Audio to text is processing
    sleep(audioToTextDelay)

    driver.execute_script("window.scrollTo(0, 1000);")
    text = driver.find_elements(
        By.XPATH, '//*[@id="root"]/div/div[6]/div/div/div/span')
    result = " ".join([each.text for each in text])

    driver.close()
    driver.switch_to.window(driver.window_handles[0])

    return result


def saveFile(content, filename):
    with open(filename, "wb") as handle:
        for data in content.iter_content():
            handle.write(data)


# Using B-spline for simulate humane like mouse movments
def human_like_mouse_move(action, start_element):
    points = [[6, 2], [3, 2], [0, 0], [0, 2]]
    points = np.array(points)
    x = points[:, 0]
    y = points[:, 1]

    t = range(len(points))
    ipl_t = np.linspace(0.0, len(points) - 1, 100)

    x_tup = si.splrep(t, x, k=1)
    y_tup = si.splrep(t, y, k=1)

    x_list = list(x_tup)
    xl = x.tolist()
    x_list[1] = xl + [0.0, 0.0, 0.0, 0.0]

    y_list = list(y_tup)
    yl = y.tolist()
    y_list[1] = yl + [0.0, 0.0, 0.0, 0.0]

    x_i = si.splev(ipl_t, x_list)
    y_i = si.splev(ipl_t, y_list)

    startElement = start_element

    action.move_to_element(startElement)
    action.perform()

    c = 5  # change it for more move
    i = 0
    for mouse_x, mouse_y in zip(x_i, y_i):
        action.move_by_offset(mouse_x, mouse_y)
        action.perform()
        i += 1
        if i == c:
            break


driver = webdriver.Chrome(options=option)
driver.set_window_position(0, 0)
driver.set_window_size(1680, 720)
# driver.get(which_lesson(True))
driver.get(
    'https://us04web.zoom.us/wc/join/71245235928?pwd=UWZ6UUF1UHFiUXFSODBCaW9iT2xydz09')

# name
driver.find_element_by_xpath('//*[@id="inputname"]').send_keys('caca')

check_box = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "recaptcha-anchor")))
action = ActionChains(driver)
human_like_mouse_move(action, check_box)
check_box.click()

action = ActionChains(driver)
human_like_mouse_move(action, check_box)

googleClass = driver.find_elements_by_class_name('g-recaptcha')[0]
outeriframe = googleClass.find_element_by_tag_name('iframe')
outeriframe.click()

print("\n[>] Try Bypass reCAPTCHA...")

allIframesLen = driver.find_elements_by_tag_name('iframe')
audioBtnFound = False
audioBtnIndex = -1

for index in range(len(allIframesLen)):
    driver.switch_to.default_content()
    iframe = driver.find_elements_by_tag_name('iframe')[index]
    driver.switch_to.frame(iframe)
    driver.implicitly_wait(delayTime)
    try:
        audioBtn = driver.find_element_by_id('recaptcha-audio-button')
        audioBtn.click()
        audioBtnFound = True
        audioBtnIndex = index
        break
    except Exception as e:
        pass

if audioBtnFound:
    try:
        while True:
            href = driver.find_element_by_id(
                'audio-source').get_attribute('src')
            response = requests.get(href, stream=True)
            saveFile(response, filename)
            response = audioToText(f"{os.getcwd()}/{filename}")

            driver.switch_to_default_content()
            iframe = driver.find_elements_by_tag_name('iframe')[audioBtnIndex]
            driver.switch_to.frame(iframe)

            inputbtn = driver.find_element_by_id('audio-response')
            inputbtn.send_keys(response)
            inputbtn.send_keys(Keys.ENTER)

            sleep(2)
            errorMsg = driver.find_elements_by_class_name(
                'rc-audiochallenge-error-message')[0]

            if errorMsg.text == "" or errorMsg.value_of_css_property('display') == 'none':
                print("\n[>] Success")
                break

    except Exception as e:
        print(e)
        print('\n[>] Caught. Try to change proxy now.')
else:
    print('\n[>] Button not found. This should not happen.')

driver.find_element_by_xpath('//*[@id="joinBtn"]').click()
print('Joined!')
