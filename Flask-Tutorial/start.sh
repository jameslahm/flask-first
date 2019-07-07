nginx 
export FLASK_APP='main'
flask init-db
uwsgi --ini uwsgi.ini
