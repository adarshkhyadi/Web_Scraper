from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import requests

page = requests.get("https://www.cricbuzz.com/cricket-series/2697/icc-cricket-world-cup-2019/points-table")

soup = BeautifulSoup(page.text)
#print(soup.prettify())

tbl = soup.find("table",class_="table cb-srs-pnts")
#print(tbl.prettify())

col_names = [x.get_text() for x in tbl.find_all('td',class_="cb-srs-pnts-th")]
col_names[5]='pts'
#print(col_names)

team_names = [x.get_text() for x in tbl.find_all('td',class_="cb-srs-pnts-name")]
#print(team_names)

pnt_tbl = [x.get_text() for x in tbl.find_all('td',class_="cb-srs-pnts-td")]
#print(pnt_tbl)

np_pnt_tbl = (np.array(pnt_tbl)).reshape(len(team_names),7)
np_pnt_tbl = np.delete(np_pnt_tbl,6,1)
np_pnt_tbl = np_pnt_tbl.astype(int)
#print(np_pnt_tbl)

consol_tbl = pd.DataFrame(np_pnt_tbl,index=team_names,columns=col_names)
consol_tbl.columns.name = "Teams"
print(consol_tbl)

team_abr = []

for team in team_names:
    short_form = ''
    for initial in team.split(' '):
       short_form = short_form + initial[0]
    team_abr.append(short_form)


title = 'ICC Cricket World Cup 2019 Number of match won by teams'
val_ticks = [1,2,3,4,5,6,7,8,9,10]
lost_ticks=[1.4,2.4,3.4,4.4,5.4,6.4,7.4,8.4,9.4,10.4]


plt.bar(val_ticks,np_pnt_tbl[:,1],width=0.4,color='g',alpha=0.6,label='Won')
plt.bar(lost_ticks,np_pnt_tbl[:,2],width=0.4,color='r',alpha=0.6,label='Lost')
plt.yticks(val_ticks)
plt.ylabel("Matches")
plt.xticks(val_ticks,team_names,rotation='vertical')
plt.grid(True)
plt.legend()
plt.title(title)

plt.show()
    

