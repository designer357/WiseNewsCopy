# -*- encoding:utf-8 -*-
__author__ = 'MC'
"""
This is a typical and simple application for web crawl, it support the continual processing even if it suspend the previous
crawl, and also record the missing part in log.
"""
import requests
from bs4 import BeautifulSoup
import os
import re
import shutil
global mycookie
global myheaders
global filename
filename="Urls.txt"
mycookie="JSESSIONID=03359AAC608165C8F2EBC9B435AA59AD; cookiee=20111116"
myheaders = {"Request-Line":"POST /cicpa2_web/PersonIndexAction.do HTTP/1.1",
            "Accept": "text/html, application/xhtml+xml, image/jxr, */*",
            "Accept-Encoding":"gzip, deflate",
            "Connection":	"Keep-Alive",
            "Host": "cmispub.cicpa.org.cn",
            "Referer": "http://cmispub.cicpa.org.cn/cicpa2_web/PersonIndexAction.do",
            "Content-Type":	"application/x-www-form-urlencoded",
            "Accept-Language":"zh-CN",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
            "Cookie": mycookie
            }
#url2="http://cmispub.cicpa.org.cn/cicpa2_web/003/0000010F849E97154EF70F0C2ED53B11.shtml"
def Page(page):
    url="http://cmispub.cicpa.org.cn/cicpa2_web/PersonIndexAction.do?isStock=00&method=indexQuery&pageNum="+str(page)+"&pageSize=15&perCode=0&queryType=2"
    #r = requests.get(url2, headers=myheaders)
    #r.encoding = "gbk"
    r = requests.get(url, headers=myheaders)

    listcontent = r.text
    #print(listcontent)
    return listcontent

def GetAllUrls():
    Pages=6624
    interval=500
    for tab in range(3313,Pages):
        print("The "+str(tab+1)+" Page is Processing......")
        beautiful_content = BeautifulSoup(Page(tab+1))


        """
        Temp = beautiful_content.findAll(name='td', attrs={'align': re.compile(r"center")})
        pattern=re.compile(r"<.*?>")
        print(Temp)
        print(len(Temp))
        Temp_company=[]
        Temp_name=[]
        for tab in range(int(len(Temp)/4)):
            Temp_company.append(pattern.sub('',str(Temp[tab*4+1])).strip())
            Temp_name.append(pattern.sub('',str(Temp[tab*4+3])).strip())
        print(Temp_company)
        print(Temp_name)
        """

        Temp = beautiful_content.findAll(name='a', attrs={'href': re.compile(r"javascript:viewDetail.*")})
        Temp_url=[]
        pattern_url=re.compile(r"\'\w*\'")
        for each in Temp:
            Temp_url.append(pattern_url.findall(str(each)))
        #print(Temp_url)
        #if (tab)%interval==0:
            #I=int(tab/interval)+1
        #with open(os.getcwd()+"/The "+str(I)+"th_500_urls.txt","a")as fout:
        try:
            with open(os.getcwd()+"urls2.txt","a")as fout:
                for each in Temp_url:
                    fout.write(each[1].replace('\'','')+'\t'+"http://cmispub.cicpa.org.cn/cicpa2_web/07/"+each[0].replace('\'','')+".shtml\n")
        except:
            pass
def GetAllContents():
    count=0
    label_index=[]
    with open("Label.txt")as fin:
        label_index=fin.readlines()

    with open(filename)as fin:
        for eachline in fin:
            val=eachline.split("\t")
            if int(label_index[count].strip())==0:
                pass
            else:
                print("The "+ eachline + " has processed...................................")
                count += 1
                continue

            r=requests.get(str(val[1]).strip(),headers=myheaders)
            r.encoding="gbk"
            beautiful_content=BeautifulSoup(r.text)

            Temp = beautiful_content.findAll(name='td', attrs={'class': re.compile(r".*")})

            Temp2=[]
            pattern=re.compile(r"<.*?>")
            try:
                for each in Temp:
                    Temp2.append(pattern.sub('',str(each)).strip()+":\t")
                outfilename=Temp2[28].strip().replace(':','')+'_'+str(Temp2[2].strip().replace(':',''))
                for tab in range(len(Temp2)):
                    A=Temp2[tab]
                    if r"信息" in A and not "(" in A:
                        Temp2[tab]="\n------------------------------------------------------- \t"+Temp2[tab]+'------------------------------------------------------\n'
                Temp2.pop(-1)
                Temp2.pop(-1)
                Path=(os.path.join(os.getcwd(),"DataInfo")+'\\'+outfilename+".txt")
                with open(str(Path),"w")as fout:
                    for each in Temp2:
                        fout.write(each)
                label_index[count]='1\n'
                if count%100==0:
                    with open(os.getcwd()+"/Label.txt","w")as fout:
                        fout.writelines(label_index)
                count += 1
                print("The "+str(count)+" data is complete!")
                #print(label_index)
            except:
                with open(os.getcwd()+"/Error.txt","a")as ferrorout:
                    ferrorout.write(eachline)
                    ferrorout.write('\n')
                with open(os.getcwd()+"/Label.txt","w")as fout:
                    fout.writelines(label_index)
    with open(os.getcwd()+"/Label.txt","w")as fout:
        fout.writelines(label_index)
import time
start=time.clock()
if not os.path.isfile(os.getcwd()+'/Label.txt'):
    with open(filename)as fin,open(os.getcwd()+'/Label.txt',"w")as fout:
        for eachline in fin:
            fout.write('0')
            fout.write('\n')

GetAllContents()
end=time.clock()
print("Success!"+"-----------------------------------------------------"+str(end-start)+" s")

