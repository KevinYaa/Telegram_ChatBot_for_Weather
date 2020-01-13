import requests
import re
import numpy as np
from bs4 import BeautifulSoup


def web_Status_Verify(rq : requests) :
    if rq.status_code == requests.codes.ok :
        print('網站正常')
    else:
        print('網站異常')


def search_weather_data(search_City):
    search_weather_Url = 'https://www.cwb.gov.tw/V7/forecast/taiwan/'+search_City+'.htm'
    rq = requests.get(search_weather_Url)
    web_Status_Verify(rq)
    rq.encoding = 'utf-8'
    soup = BeautifulSoup(rq.text ,'html.parser')
    #print(soup.prettify)
    # with open('html.txt','wt',encoding='utf-8') as fout:
    #     fout.write(str(soup.prettify))

    Tables = soup.find_all('table',attrs={'class' : 'FcstBoxTable01' , 'summary' : '編排用'})

    t_head = []
    t_body = []
    t_num = []

    for i in range(0,len(Tables)) : 
        tb = Tables[i]
        t_head.append([])
        
        for thead in tb.find_all('thead'): #抓每一個table head的資料
            for tr in thead.find_all('tr') :
                for th in tr.find_all('th'):
                    #print(th.get_text())
                    t_head[i].append(th.get_text())                    
                   
        #print('------')

        j = 0
        for tbody in tb.find_all('tbody'): #抓每一個table body的資料            
            for tr in tbody.find_all('tr') :
                t_body.append([])                                
                for th in tr.find_all('th'):                    
                    t_body[j].append(th.get_text())
                    #print(th.get_text())

                for img in tr.find_all('img'):                    
                    t_body[j].append(img.attrs.get('title'))
                    #print(img.attrs.get('title')) 

                for td in tr.find_all('td'):
                    if td.get_text() == '\n':
                        continue
                    else:                       
                        t_body[j].append(td.get_text())             
                    #print(td.get_text())        
                #print('------')
                j+=1                


        t_num.append([])
        for tr in tb.find_all('tr'):           
            for td in tr.find_all('td',attrs = {'class' : 'num'}):
                #print(td.get_text())
                t_num[i].append(td.get_text())

    for i in range(0,3):
        t_body[i][1],t_body[i][2] = t_body[i][2],t_body[i][1]
    
    del t_head[2][0:1]
    del t_num[0:1]
    

    #print(t_head)
    #print(t_body)
    #print(t_num)


    return np.array(t_head),np.array(t_body),np.array(t_num)
                
            

# if __name__ == "__main__":
#     City_DIC = {
#         '基隆市':'Keelung_City','臺北市':'Taipei_City','新北市':'New_Taipei_City',
#         '桃園市':'Taoyuan_City','新竹市':'Hsinchu_City','新竹縣':'Hsinchu_County',
#         '苗栗縣':'Miaoli_County','臺中市':'Taichung_City','彰化縣':'Changhua_County',
#         '南投縣':'Nantou_County','雲林縣':'Yunlin_County','嘉義市':'Chiayi_City',
#         '嘉義縣':'Chiayi_County','宜蘭縣':'Yilan_County','花蓮縣':'Hualien_County',
#         '台東縣':'Taitung_County','台南市':'Tainan_City','高雄市':'Kaohsiung_City',
#         '屏東縣':'Pingtung_County','連江縣':'Lienchiang_County','金門縣':'Kinmen_County',
#         '澎湖縣':'Penghu_County'
#     }


#     search_weather_Url = 'https://www.cwb.gov.tw/V7/forecast/taiwan/Taipei_City.htm'


#     t_head,t_body,t_num =  search_weather_data(search_weather_Url)
    # print(t_head)
    # print(t_body)
    # print(t_num)

    