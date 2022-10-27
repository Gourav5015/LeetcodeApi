from selenium import webdriver
from bs4 import BeautifulSoup
import os
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
class LeetCodeApi():
    def __init__(self,username):
        self.level={}
        self.name=details=None
        self.username=None
        self.rank=None
        self.url="https://leetcode.com/"+username
        self.soup=None
        self.status=0
        self.__fetch()
        while(True and self.status<3):
            if (self.soup.title.get_text()!="Page Not Found - LeetCode"):
                try:
                    questions=self.soup.find_all(class_="space-y-2")
                    for i in questions[:3]:
                        q_types=i.find_all("span")
                        self.level[i.find(class_="w-[53px] text-label-3 dark:text-dark-label-3").get_text().upper()]=[int(q_types[0].get_text().strip("/")),int(q_types[1].get_text().strip("/"))]
                    totalQuestions=totalSolved=0
                    for i in self.level.values():
                        totalSolved+=i[0]
                        totalQuestions+=i[1]
                    self.level["TOTAL"]=[totalSolved,totalQuestions]
                    details=(self.soup.find_all(class_="flex items-center"))
                    self.name=details[1].get_text().upper()
                    self.username=details[2].get_text()
                    self.rank=int((self.soup.find(class_="ttext-label-1 dark:text-dark-label-1 font-medium")).get_text().replace(",",""))
                    break
                except:
                    self.status+=1
                    self.__fetch()
            else :
                self.url=None
                break
        if self.status==3:
            self.level={}
            self.name=details=None
            self.username=None
            self.rank=None
            self.url=None

    def __fetch(self):
        options=webdriver.ChromeOptions()
        options.headless=True
        browser= webdriver.Chrome(options=options,service=Service(ChromeDriverManager().install()))
        browser.get(self.url)
        data={}
        count=0
        while(True):
            current_data=browser.execute_script("return window.onload=(function(){return document.getElementsByTagName('html')[0].innerHTML})()")
            if (current_data != data):
                data=current_data
                count=0
            else :
                if (count==10):
                    break 
                count+=1
        self.soup=BeautifulSoup(data,'html.parser')

    def getTotalQuestions(self,level="TOTAL"):
        level=level.upper() 
        value= self.level.get(level,None)
        if value==None:
            return None
        return value[1]
    def getQuestionsSolved(self,level="TOTAL"):
        level=level.upper() 
        value= self.level.get(level,None)
        if value==None:
            return None
        return value[0]
    def getPercentageQuestionsSolved(self,level="TOTAL"):
        level=level.upper() 
        value= self.level.get(level,None)
        if value==None:
            return None
        return round((value[0]/value[1])*100,2)
    def changeUseranme(self,username):
        self.__init__(username)
    def getName(self):
        return self.name
    def getProfileURL(self):
        return self.url
    def getRank(self):
        return self.rank
    def getUsername(self):
        return self.username
    def stats(self):
        return self.level
