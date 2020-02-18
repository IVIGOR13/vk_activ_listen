# vk_activ_listen
Прослушиватель активности пользователя в соц. сети Вконтакте

## Команды
* exit - выход из программы

## Установка
Клонирование репозитория
```
$ git clone https://github.com/IVIGOR13/vk_activ_listen.git
```

## Монтирование
```
$ pip install beautifulsoup4
$ pip install lxml
$ pip install re
$ pip install plotly
```

В файл objects.txt занесите идентификаторы пользователей из URL адреса

## Запуск
```
$ cd vk_activ_listen
$ python vk_activ_listen.py
```

Когда вас устроит объем собранных данных в файл activity.csv введите команду "exit" чтобы прослушивание завершилось, и запустите скрипт визуализации vizual_data.py (советую открывать в Jupyter или Colaboratory)
```
$ python vk_activ_listen.py
```
