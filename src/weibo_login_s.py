# -*-coding:utf-8-*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def login(username, password):
    system.setProperty("webdriver.chrome.driver", "/path/to/chromedriver");
    browser = webdriver.Chrome('C:/Users/bo/AppData/Local/Temp/Rar$EXa0.634/')

    browser.get("http://weibo.com/login.php")

    user = browser.find_element_by_xpath('//*[@id="pl_login_form"]/div[3]/div[2]/div[1]/div/input')
    user.send_keys(username, Keys.ARROW_DOWN)

    passwd = browser.find_element_by_xpath('//*[@id="pl_login_form"]/div[3]/div[2]/div[2]/div/input')
    passwd.send_keys(password, Keys.ARROW_DOWN)

    # //*[@id="pl_login_form"]/div[3]/div[2]/div[3]/div/input
    browser.find_element_by_xpath('//*[@id="pl_login_form"]/div[3]/div[2]/div[6]').click()
    vcode = browser.find_element_by_xpath('//*[@id="pl_login_form"]/div[3]/div[2]/div[3]/div/input')
    if vcode:
        code = raw_input("verify code:")
        if code:
            vcode.send_keys(code, Keys.ARROW_DOWN)

    browser.find_element_by_xpath('//*[@id="pl_login_form"]/div[3]/div[2]/div[6]').click()
    print browser.find_element_by_xpath(
        "//*[@id='v6_pl_content_homefeed']/div[2]/div[3]/div[1]/div[1]/div[3]/div[1]/a[1]").get_attribute("usercard")


def test():
    username = "vcjmi41976504@126.com"
    passwd = "zx1987"
    login(username, passwd)


if __name__ == "__main__":
    test()
