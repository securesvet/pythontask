# pythontask
Мурзин Святослав и Юрьев Артем

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
