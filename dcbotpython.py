from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from parse import *
from datetime import datetime
import time
import random

# file_userinfo = open("data/userinfo.txt","r")
dc_id='voxindochim'
dc_pw='dochim1212!'

# 갤러리 주소 모음
gall_url={
    '갤메인' : 'https://gall.dcinside.com/board/lists?id=',
    '글보기' : 'https://gall.dcinside.com/board/view/?id=',
    '실베' : 'dcbest',
    '픞갤' : 'pripara'
    }

# options = webdriver.ChromeOptions() 
# options.add_experimental_option("excludeSwitches", ["enable-logging"])
# options.add_argument("start-maximized")
# chrome_driver = webdriver.Chrome(options=options, executable_path='D:/chromedriver/chromedriver.exe')
# chrome_driver.implicitly_wait(5)

class DRIVER():
    def __init__(self):
        self.options = webdriver.ChromeOptions() 
        self.options.add_experimental_option("excludeSwitches", ["enable-logging"])
        self.options.add_argument("start-maximized")
        self.chrome_driver = webdriver.Chrome(options=self.options, executable_path='D:/chromedriver/chromedriver.exe')
        self.chrome_driver.implicitly_wait(5)

    # 로그인 하는거
    def dclogin(self, dcid: str, dcpw: str, redirect: str):
        # Parameter Memo
        # - redirect : 로그인 후 이동할 페이지
        if redirect is None:
            redirect = 'https://gall.dcinside.com/board/lists?id=dcbest'

        # 로그인페이지 불러오기
        self.chrome_driver.get('https://sign.dcinside.com/login?s_url='+redirect)
        self.chrome_driver.implicitly_wait(5)
        # 아이디 비밀번호 입력
        self.chrome_driver.find_element('id','id').send_keys(dcid)
        self.chrome_driver.find_element('id','pw').send_keys(dcpw)
        # 로그인 버튼 클릭
        self.chrome_driver.find_element(By.CLASS_NAME,'btn_wfull').send_keys(Keys.ENTER)
        self.chrome_driver.implicitly_wait(5)

    # 가장 최신글의 댓글 페이지로 이동
    def move_latest_post_comment(self):
        self.chrome_driver.find_element(By.XPATH, "//tbody//tr[@class='ub-content us-post']//td[@class='gall_tit ub-word']//a[@class='reply_numbox']").click()
        self.chrome_driver.implicitly_wait(5)
    
    # 가장 최근 글로 이동
    def move_latest_post(self):
        num = self.chrome_driver.find_element(By.XPATH,"//tbody/tr[@class='ub-content us-post' and not(@data-type='icon_notice')]/td[@class='gall_num']").text # == .get_attribute('innerText')
        self.chrome_driver.find_element(By.XPATH,"//tbody/tr[@class='ub-content us-post' and not(@data-type='icon_notice')]/td[@class='gall_tit ub-word']//a").click()
        self.chrome_driver.implicitly_wait(5)
        print(num)

    # 댓글 달기
    def post_comment(self, text: str):
        self.chrome_driver.find_element(By.XPATH,"//div[@class='cmt_write_box clear']/div[@class='cmt_txt_cont']/div[@class='cmt_write']/textarea").send_keys(text)
        self.chrome_driver.find_element(By.XPATH,"//div[@class='cmt_write_box clear']/div[@class='cmt_txt_cont']/div[@class='cmt_cont_bottm clear']/div[@class='fr']/button").click()
        self.chrome_driver.implicitly_wait(5)

    # 디시콘 팝업 버튼 클릭
    def open_dccon(self):
        self.chrome_driver.find_element(By.XPATH,"//div[@class='cmt_write_box clear']/div[@class='cmt_txt_cont']/div[@class='cmt_cont_bottm clear']/div[@class='dccon_guidebox']/button").click()
        self.chrome_driver.implicitly_wait(5)

    # 디시콘 달기
    def post_dccon(self, dccon_name: str, dccon_id):
        self.chrome_driver.find_element(By.XPATH,"//div[@class='cmt_write_box clear']/div[@class='cmt_txt_cont']/div[@class='cmt_cont_bottm clear']/div[@class='dccon_guidebox']/button").click()
        self.chrome_driver.implicitly_wait(5)
        dccon_recent_xpath="//*[@id='div_con']/div/div[2]/div[1]/div[1]/ul//button[@class='dccon_btn recent']"
        self.chrome_driver.find_element(By.XPATH, dccon_recent_xpath).click()
        time.sleep(5)

        conlist_select_xpath="//*[@id='div_con']/div/div[@class='dccon_list_wrap clear']/div[@class='inner']/div[@class='dccon_tab_btnbox fl clear']/ul//button[@title='"+dccon_name+"']"
        print(conlist_select_xpath)
        self.chrome_driver.find_element(By.XPATH, conlist_select_xpath).click()
        self.chrome_driver.implicitly_wait(3)

        pageindex = 0
        while True:
            con_xpath="//*[@id='div_con']/div/div[@class='dccon_list_wrap clear']/div[@class='dccon_list_box dcconlist']/ul[@class='dccon_list clear page_0_index_"+str(pageindex)+"']/li["+str(dccon_id)+"]/button"
            print(con_xpath)
            exception_occured = False
            try:    
                self.chrome_driver.find_element(By.XPATH,con_xpath).click()
            except:
                pageindex+=1
                exception_occured = True
            if exception_occured == False:
                self.chrome_driver.implicitly_wait(5)
                break

    # 디씨콘 페이지 다음페이지로
    def dccon_nextpage(self):
        xpath ="//*[@id='div_con']/div/div[@class='dccon_list_wrap clear']/div[@class='dccon_list_box dcconlist']/ul//div[@class='btn_box dccon_list_paging']/button[@class='btn_next on' or @class='btn_next']"
        self.chrome_driver.find_element(By.XPATH,xpath)

    # 디씨콘 페이지 이전페이지로
    def dccon_prevpage(self):
        xpath ="//*[@id='div_con']/div/div[@class='dccon_list_wrap clear']/div[@class='dccon_list_box dcconlist']/ul//div[@class='btn_box dccon_list_paging']/button[@class='btn_prev on' or @class='btn_prev']"
        self.chrome_driver.find_element(By.XPATH,xpath)

    # 특정 페이지 요청하기
    def get_page(self, url: str):
        self.chrome_driver.get(url)
        self.chrome_driver.implicitly_wait(5)

    # 현재 페이지 URL 반환
    def current_url(self):
        return self.chrome_driver.current_url


#######실베 최근글 찾는거#######
# latesturl= None
# latestindex= None
# def check_latest_dcbest(driver):
#     latesturl = str(driver.find_element(By.XPATH, "//tbody//tr[@class='ub-content us-post']//td[@class='gall_tit ub-word']//a").get_attribute('href'))
#     print (latesturl)
#     latestindex = parse("https://gall.dcinside.com/board/view/?id=dcbest&no={}&_dcbest=1&page=1", latesturl)
#     print (latestindex)
#     return latesturl, latestindex
################################

if __name__=="__main__":
    readlogfile= open('log.txt','r')
    History=[]
    while True:
        line = readlogfile.readline().strip()
        if not line: break
        History.append(line.split('|')[2])
    readlogfile.close()
    
    History.sort(reverse=True)
    print(History)

    #### 일단 직접지정해두는데, 원래 사용자에게 입력받아야함 ####
    GALLSELECT = '실베'
    print(gall_url[GALLSELECT])
    print('start')
    driver = DRIVER()
    driver.dclogin(dcid=dc_id, dcpw=dc_pw, redirect=gall_url['갤메인']+gall_url[GALLSELECT])
    myurl=gall_url['글보기']+gall_url[GALLSELECT]+'&no='
    print(myurl)

    driver.move_latest_post()
    startindex = parse('{}&no={}&{}',driver.current_url())[1]
    
    # startindex = 1761126
    index = int(startindex)
    step = 0
    while True:
        logfile= open('log.txt','a')
        if str(index) in History:
            print(str(index))
            print(History)
            index-=1
            continue
        driver.get_page(myurl+str(index))
        currenturl = driver.current_url()
        if(currenturl!='https://gall.dcinside.com/derror/deleted/'+gall_url[GALLSELECT]+'/gallery'):
            driver.post_dccon('블루아카레이사콘돚거','21')
            step+=1

            index = int(parse('{}&no={}',currenturl)[1])
            
            nowtime = datetime.now()
            logfile.write('{}|{}|{}\n'.format( nowtime, currenturl, index ))
            History.append(index)
            print(index)
            print(History)
            time.sleep(random.uniform(5,20))
        index -= 1
        if step>=5:
            break
        logfile.close()
