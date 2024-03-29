Мурзин Святослав и Юрьев Артём
|Task|Description|
|:---|----------:|
|traceroute|Утилита для определения маршрута в TCP/IP|
|metrica|Счетчик посещений сайта|

## Metrica:

Запускаем flask_server.py, что-то такое должно выйти в консоль:
```
 * Serving Flask app 'flask_server'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.0.29:5000
```

Заходим по второму адресу, он для внутренней сети, можно протестировать количество посещений с помощью подключения к этой самой внутренней сети через другое устройство, затем при обновлении страницы будет обновляться счётчик, вместе с ним и база данных.

*База данных будет создана, если её ещё нет, саму базу данных мы не посчитали нужным вкладывать в наш гит проект

[//]: # (Для взаимодействия с формами, можно пройти по адресу localhost:5000/view_info)

# Traceroute
Traceroute - консольная утилита, показывающая точный путь, который проходит пакет до места назначения. Данная утилита можешь помочь вам для выявления таких проблем как "bottle neck".
### Usage
```
sudo python3 traceroute.py *server_name*
```
Заместо server_name может быть или домен (www.mursvet.ru) или айпи-адрес (192.168.0.30)
### Вывод команды:
```
traceroute to google.com (142.250.113.100), 30 hops max, 52 byte packets 
1 10.0.0.1 (10.0.0.1) 595.45 ms
2 * * * 
3 te0-2-1-1.rcr51.b059724-0.dfw01.atlas.cogentco.com (38.88.231.249) 431.29 ms
4 be2356.ccr31.dfw01.atlas.cogentco.com (154.54.47.106) 495.89 ms
5 be2763.ccr41.dfw03.atlas.cogentco.com (154.54.28.74) 716.18 ms
5 be2764.ccr41.dfw03.atlas.cogentco.com (154.54.47.214) 511.47 ms
6 tata.dfw03.atlas.cogentco.com (154.54.12.106) 818.2 ms
7 66.110.56.139 (66.110.56.139) 715.02 ms
8 108.170.231.48 (108.170.231.48) 605.08 ms
8 142.251.248.209 (142.251.248.209) 715.9 ms
9 108.170.240.209 (108.170.240.209) 614.88 ms
9 108.170.252.131 (108.170.252.131) 708.3 ms
9 108.170.240.209 (108.170.240.209) 612.75 ms
10 108.170.228.103 (108.170.228.103) 614.4 ms
10 108.170.233.119 (108.170.233.119) 408.91 ms
11 142.250.233.171 (142.250.233.171) 739.04 ms
11 142.251.70.211 (142.251.70.211) 715.9 ms
11 142.250.233.171 (142.250.233.171) 646.04 ms
12 142.250.236.158 (142.250.236.158) 613.93 ms
...
```