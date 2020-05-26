from fyers_api import accessToken
from fyers_api import fyersModel
import webbrowser
from selenium import webdriver
import time
import os

cwd = os.chdir("C:/fyers_algotrading")
request_token = ""
def autologin():
    global request_token
    try:
        token_path = "api_key.txt"
        key_secret = open(token_path,'r').read().split()
        appSession = accessToken.SessionModel(key_secret[0],key_secret[1])
        response = appSession.auth()
        auth_code = response["data"]["authorization_code"]
        appSession.set_token(auth_code)
        generateTokenUrl = appSession.generate_token()
        service = webdriver.chrome.service.Service('./chromedriver.exe')
        service.start()
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options = options.to_capabilities()
        driver = webdriver.Remote(service.service_url,options)
        driver.get(generateTokenUrl)
        driver.implicitly_wait(10)
        username = driver.find_element_by_xpath('/html/body/div/div[1]/div/form/div[1]/div/input')
        password = driver.find_element_by_xpath('/html/body/div/div[1]/div/form/div[2]/div/input')
        PAN = driver.find_element_by_xpath('/html/body/div/div[1]/div/form/div[4]/div/input')
        username.send_keys(key_secret[2])
        password.send_keys(key_secret[3])
        PAN.send_keys(key_secret[4])
        driver.find_element_by_xpath('/html/body/div/div[1]/div/form/div[7]/button').click()
        time.sleep(30)
        request_token=driver.current_url.split('access_token=')[1].split('&user_id')[0]
        with open('access_token.txt', 'w') as the_file:
            the_file.write(request_token)
        driver.quit()
    except Exception as e:
           print(e)
           driver.quit()

autologin()
# is_async = False
# fyers = fyersModel.FyersModel(is_async)
# profile=fyers.get_profile(token = request_token)
# print(profile)