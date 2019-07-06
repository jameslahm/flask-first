### Flask Tutorial
---
my first flask project

#### 本机测试：
* windows:
    
```    
    pip install -e .

    set FLASK_APP='flaskr'
  
    flask init-db
  
    flask run
```
* linux:
```
    pip install -e .
    
    export FLASK_APP='flaskr'
    
    flask init-db
    
    flask run
```


#### DOCKER部署：
```
docker build -t flask-nginx-uwsgi .
docker run -d -p 18080:80 \
    -v /data:/web/instance/flaskr.sqlite flask-nginx-uwsgi
```

