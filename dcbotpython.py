from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from parse import *

# file_userinfo = open("data/userinfo.txt","r")
dcid='voxindochim'
dcpw='dochim1212!'


options = webdriver.ChromeOptions() 
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument("start-maximized")
chrome_driver = webdriver.Chrome(options=options, executable_path='D:/chromedriver/chromedriver.exe')
chrome_driver.implicitly_wait(5)

class DRIVER():
    def __init__(self):
        options = webdriver.ChromeOptions() 
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_argument("start-maximized")
        self.chrome_driver = webdriver.Chrome(options=options, executable_path='D:/chromedriver/chromedriver.exe')
        chrome_driver.implicitly_wait(5)


# 실베 : 'https://gall.dcinside.com/board/lists?id=dcbest'
# 픞갤 : 'https://gall.dcinside.com/board/lists?id=pripara'

# 로그인 하는거
def dclogin(driver, dcid, dcpw, *redirect):
    # Parameter Memo
    # - redirect : 로그인 후 이동할 페이지
    if redirect is None:
        redirect = 'https://gall.dcinside.com/board/lists?id=dcbest'

    # 로그인페이지 불러오기
    chrome_driver.get('https://sign.dcinside.com/login?s_url='+redirect)
    chrome_driver.implicitly_wait(5)
    # 아이디 비밀번호 입력
    driver.find_element('id','id').send_keys(dcid)
    driver.find_element('id','pw').send_keys(dcpw)
    # 로그인 버튼 클릭
    driver.find_element(By.CLASS_NAME,'btn_wfull').send_keys(Keys.ENTER)
    driver.implicitly_wait(5)

# 가장 최신글의 댓글 페이지로 이동
def move_latest_post_comment(driver):
    driver.find_element(By.XPATH, "//tbody//tr[@class='ub-content us-post']//td[@class='gall_tit ub-word']//a[@class='reply_numbox']").click()
    driver.implicitly_wait(5)

# 댓글 작성
def post_comment(driver, text: str):
    driver.find_element(By.XPATH,"//div[@class='cmt_write_box clear']/div[@class='cmt_txt_cont']/div[@class='cmt_write']/textarea").send_keys(text)
    driver.find_element(By.XPATH,"//div[@class='cmt_write_box clear']/div[@class='cmt_txt_cont']/div[@class='cmt_cont_bottm clear']/div[@class='fr']/button").click()
    driver.implicitly_wait(5)

# 디시콘 팝업 열기
def open_dccon(driver):
    driver.find_element(By.XPATH,"//div[@class='cmt_write_box clear']/div[@class='cmt_txt_cont']/div[@class='cmt_cont_bottm clear']/div[@class='dccon_guidebox']/button").click()
    driver.implicitly_wait(5)
# 디시콘 달기
def post_dccon(driver, dccon_name: str, dccon_id: str):
    conlist_select_xpath="//*[@id='div_con']/div/div[2]/div[1]/div[1]/ul//button[@title='"+dccon_name+"']"
    driver.find_element(By.XPATH, conlist_select_xpath).click()
    driver.implicitly_wait(5)
    con_xpath="//*[@id='div_con']/div/div[2]/div[2]/ul/li["+dccon_id+"]/button"
    chrome_driver.find_element(By.XPATH,con_xpath).click()

#######실베 최근글 찾는거#######
latesturl= None
latestindex= None
def check_latest_dcbest(driver):
    latesturl = str(driver.find_element(By.XPATH, "//tbody//tr[@class='ub-content us-post']//td[@class='gall_tit ub-word']//a").get_attribute('href'))
    print (latesturl)
    latestindex = parse("https://gall.dcinside.com/board/view/?id=dcbest&no={}&_dcbest=1&page=1", latesturl)
    print (latestindex)
    return latesturl, latestindex
################################


if __name__=="__main__":
    print('start')