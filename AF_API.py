from selenium import webdriver
import time
from fake_useragent import UserAgent
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import colorama



a=open("Times.txt","r").read().replace(" ","").replace("\n","").split(";")[0].split(",") #the list itself


WRITERATE1=int(a[0])
WRITERATE2=int(a[1])
WRITERATE3=int(a[2])
WRITERATE4=int(a[3])
WRITERATE5=int(a[4])
WRITERATESTD=int(a[5])
CurrentWait=WRITERATESTD

colorama.init()

def debug(string="Hello World!", type="Debug", color=colorama.Fore.MAGENTA):
    print(color+"["+type+"] "+string+colorama.Style.RESET_ALL)
    
ua=UserAgent()
profile = webdriver.FirefoxProfile()
options = webdriver.FirefoxOptions()
options.add_argument("--headless")
profile.set_preference("general.useragent.override", ua.ie) #Using the IE UserAgent because it is not blocked
driver=webdriver.Firefox(profile,options=options)
debug("WebDriver Started Succesfully!")
def login(email,password):
    driver.get("https://af.articleforge.com/users/sign_in")
    emailfield=driver.find_element_by_id("user_email")
    passwordfield=driver.find_element_by_id("user_password")
    enterbutton=driver.find_element_by_xpath("/html/body/div/section[2]/div/div/form/div[4]/button")
    emailfield.send_keys(email)
    passwordfield.send_keys(password)
    enterbutton.click()
    debug("Logged In As: "+colorama.Fore.YELLOW+email+" "+("*"*len(password)),"Data",colorama.Fore.GREEN)

def changeswitches():
    pass

def createnewarticle():
    driver.get("https://af.articleforge.com/new_article")
    #bulkswitch=driver.find_element_by_id("bulk_switcher")
    #bulkswitch.click()
    debug("New Article Page Opened!")

def additem(articlearray):
    debug("Adding Article Information...")
    keyword=driver.find_element_by_id("keyword")
    keyword.send_keys(articlearray[0])
    a=open("tmp.txt","r").read().split(",")
    open("tmp.txt","w").write(a[0]+","+a[1]+","+articlearray[0])
    
    subkeywords=driver.find_element_by_id("sub_keywords")
    for item in articlearray[1:-1]:
        
        subkeywords.send_keys(item[1:] if item[0]==" " else item)
        subkeywords.send_keys(Keys.RETURN)
    debug("Article Information Added!")
        
    

        
def defineoptions(lenght=1,titles=False,headings=False,autogen=False,language="en"):
    html = driver.find_element_by_tag_name('html')
    html.send_keys(Keys.END)
#    wait = WebDriverWait(driver,10)
#    wt = wait.until(ec.visibility_of_element_located((By.ID, 'switch_title')))
    select=Select(driver.find_element_by_id("select_length"))
    if lenght==1:
        select.select_by_value("Very Short")
    if lenght==2:
        select.select_by_value("Short")
    if lenght==3:
        select.select_by_value("Medium")
    if lenght==4:
        select.select_by_value("Long")
    if lenght==5:
        select.select_by_value("Very Long")
        
    lanselect=Select(driver.find_element_by_id("language"))
    lanselect.select_by_value(language)
    
    debug("Changed lenght to "+str(lenght))
    
    if titles:
        driver.find_element_by_xpath('//*[@id="switch_title"]/parent::div').click()
        debug("Titles enabled!")
    if headings:
        driver.find_element_by_xpath('//*[@id="use_outline"]/parent::div').click()
        debug("Headings enabled!")
        if autogen:
            try:
                time.sleep(3)
                driver.find_element_by_xpath('//*[@id="auto_outline"]/parent::div').click()
                debug("Auto-generate enabled!")
            except:
                debug("Couldn't enable Auto-generation","Warning",colorama.Fore.YELLOW)
                
    driver.find_element_by_id("create_article_button").click() #START THE PROGRAM
    debug("Started Article Generation!")
def waitforcompletion(articlearray,lenght=1):
    print(articlearray)
    debug("Waiting For Query To Get Listed...")
    wait = WebDriverWait(driver,180)
    jid=wait.until(ec.visibility_of_element_located((By.XPATH ,'//h5[contains(text(),"Processing Query: '+articlearray[0]+'")]/parent::div/parent::div/parent::div')))
    debug("Query Listed! Waiting For Start...")
    jobid=jid.get_attribute("id").split("_")[1]
    debug("Found job id: "+colorama.Fore.YELLOW+jobid,"Data",colorama.Fore.GREEN)
    wait = WebDriverWait(driver,600)
    progress = wait.until(ec.visibility_of_element_located((By.XPATH ,"//div[@id='job_"+jobid+"']/div[2]/div/div")))
    debug("Query Started!")
    progperc=progress.get_attribute("style").replace("width: ","").replace("%","")
    i=0
    while not progperc=="100":

        if i==0:
            debug("REMEMBER: The first percentage check is longer depending on the lenght of the article!","Warning",colorama.Fore.YELLOW)
            if lenght==1:
                CurrentWait=WRITERATE1
            elif lenght==2:
                CurrentWait=WRITERATE2
            elif lenght==3:
                CurrentWait=WRITERATE3
            elif lenght==4:
                CurrentWait=WRITERATE4
            elif lenght==5:
                CurrentWait=WRITERATE5
        else:
            CurrentWait=WRITERATESTD

        time.sleep(CurrentWait)

        progperc=progress.get_attribute("style").replace("width: ","").replace("%","").split(";")[0]
        debug("Progress: "+progperc+"%","Info",colorama.Fore.CYAN)
        
        a=open("tmp.txt","r").read().split(",")
        open("tmp.txt","w").write(a[0]+","+progperc+","+a[2])

        i+=1