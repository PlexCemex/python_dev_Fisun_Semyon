# python_dev_Fisun_Semyon
Летняя практика в Farpost 2025

Generate fake dat

```shell
python3 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
flask --app flaskr init-db

```

Then run webserver

```shell
flask --app flaskr run --debug
```

Then goto your browser and test, for example:
http://127.0.0.1:5000/api/comments?login=nrusso
http://127.0.0.1:5000/api/general?login=nrusso

Discription:
Из добавленного, не прописанного в ТЗ, я добавил таблицу комментариев в authors.sql. 
Я сделал это потому что надо выводить куда юзер писал комментарий, а из требований задания это сделать было невозможно.