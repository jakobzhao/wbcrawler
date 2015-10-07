# -*-coding:utf-8-*-
import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def login(username, password):
    # system.setProperty("webdriver.chrome.driver", "/path/to/chromedriver");
    # browser = webdriver.Chrome('C:/Users/bo/AppData/Local/Temp/Rar$EXa0.634/')
    chromedriver = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
    os.environ["webdriver.chrome.driver"] = chromedriver
    browser = webdriver.Chrome(chromedriver)
    browser.get("http://weibo.com/login.php")

    user = browser.find_element_by_xpath("//*[@id='pl_login_form']/div[5]/div[1]/div/input")
    user.send_keys(username, Keys.ARROW_DOWN)

    passwd = browser.find_element_by_xpath("//*[@id='pl_login_form']/div[5]/div[2]/div/input")
    passwd.send_keys(password, Keys.ARROW_DOWN)

    vcode = browser.find_element_by_xpath("//*[@id='pl_login_form']/div[5]/div[3]/div/input")
    if vcode:
        code = raw_input("verify code:")
        if code:
            vcode.send_keys(code, Keys.ARROW_DOWN)

    browser.find_element_by_xpath("//*[@id='pl_login_form']/div[5]/div[6]/div[1]/a/span").click()

    print browser.find_element_by_xpath(
        "//*[@id='v6_pl_content_homefeed']/div[2]/div[3]/div[1]/div[1]/div[3]/div[1]/a[1]").get_attribute("usercard")


def test():
    username = "jakobzhao@gmail.com"
    passwd = "atozinc328"
    login(username, passwd)


if __name__ == "__main__":
    test()
