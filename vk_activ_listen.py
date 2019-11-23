#
# Author: Igor Ivanov
# 2019
#
import requests
from bs4 import BeautifulSoup
import time
import datetime
from threading import Thread
import re
import csv


class Listener(Thread):
    def __init__(self):
        Thread.__init__(self)


    def run(self):
        self.exit = False
        while(not self.exit):
            start_time = time.time()

            for id in st.objects.keys():
                now = self.get_act(self.get_html(st.link + str(id)))
                st.add(id, now)

            time.sleep(st.T-(time.time() - start_time))


    def cleanhtml(self, raw_html):
      cleanr = re.compile('<.*?>')
      cleantext = re.sub(cleanr, '', raw_html)
      return str(cleantext)


    def get_act(self, html):
        soup = BeautifulSoup(html, 'lxml')
        act = self.cleanhtml(str(soup.find('span', class_='pp_last_activity_text')))
        if act == 'Online':
            return True
        else:
            return False


    def get_html(self, url):
        r = requests.get(url)
        r.encoding = 'utf8'
        return r.text


    def close(self):
        self.exit = True



class Storage:
    def __init__(self):
        self.link = 'https://vk.com/'
        self.T = float(60)
        self.objects = {}
        self.last = {}
        self.times = {}
        self.time_start = datetime.datetime.today().strftime("%Y-%m-%d %H:%M")
        self.init_objs()
        self.filename_activity = 'activity.csv'
        self.csv_init = False


    def init_objs(self):
        with open('objects.txt', 'r', encoding="utf8") as file:
            for user in file.readlines():
                id = user.replace(' ', '').rstrip()
                r = requests.get(self.link + id)
                r.encoding = 'utf8'

                soup = BeautifulSoup(r.text, 'lxml')
                try:
                    name = str(soup.find('div', class_='pp_cont').find_all('h2', class_="op_header")[0].string)
                    if str(re.sub(re.compile('<.*?>'), '',
                                  str(soup.find('span', class_='pp_last_activity_text')))) == '':
                        print('close: ' + id + ' - ' + name)
                    else:
                        self.objects.update({id: name})

                    self.last.update({id: False})

                except:
                    print('ERROR: ' + id)


    def write_csv(self, id, start_time, end_time):
        if not self.csv_init:
            with open(self.filename_activity, "r", newline="") as file:
                if csv.DictReader(file, delimiter=',').line_num != 0:
                    self.csv_init = True

            if self.csv_init:
                with open(self.filename_activity, "w", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow(['id', 'start_time', 'end_time'])

        with open(self.filename_activity, "a", newline="") as file:
            data = [id, start_time, end_time]
            writer = csv.writer(file)
            writer.writerow(data)

    def add(self, id, online):
        if online != self.last[id]:
            time_now = datetime.datetime.today().strftime("%Y-%m-%d %H:%M")
            if self.last[id] == False:
                self.times.update({id: time_now})
                self.last[id] = True

            elif self.last[id] == True:
                self.write_csv(id, self.times[id], time_now)
                self.last[id] = False
                self.times.pop(id)


    def exit(self):
        self.time_stop = datetime.datetime.today().strftime("%Y-%m-%d %H:%M")
        for id in self.objects.keys():
            if self.last[id]:
                self.write_csv(id, self.times[id], self.time_stop)
                self.last[id] = False



if __name__ == "__main__":
    st = Storage()
    st.write_csv('1', '2', '3')
    st.write_csv('2', '3', '4')
    st.write_csv('3', '4', '5')
    l = Listener()
    l.start()

    while(True):
        command = input()
        if command == 'exit':
            st.exit()
            l.close()
            l.join()
            break
