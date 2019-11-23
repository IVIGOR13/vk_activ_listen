#
# Author: Igor Ivanov
# 2019
#
import csv
import plotly.figure_factory as ff
import requests
from bs4 import BeautifulSoup

data = []
users = {}

with open("activity.csv") as file_obj:
  reader = csv.DictReader(file_obj, delimiter=',')
  for i, line in enumerate(reader):
      r = requests.get('https://vk.com/' + line["id"])
      r.encoding = 'utf8'
      soup = BeautifulSoup(r.text, 'lxml')
      users.update({line["id"]: str(soup.find('div', class_='pp_cont').find_all('h2', class_="op_header")[0].string)})
      data.append(dict(Task=users[line["id"]], Start=line["start_time"], Finish=line["end_time"], Resource='Complete'))


colors = {
    'Complete': 'rgb(0, 255, 100)'
}

fig = ff.create_gantt(data,
                      colors=colors,
                      index_col='Resource',
                      show_colorbar=True,
                      group_tasks=True)

fig.show()