import functools
from flask import (
    Blueprint,flash,g,redirect,render_template,request,session,url_for 
)
from werkzeug.security import check_password_hash,generate_password_hash
from flaskr.db import get_db

bp=Blueprint('auth',__name__,url_prefix='/auth')

@bp.route('/register',methods=('GET','POST'))
def register():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        db=get_db()
        error=None

        if not username:
            error="Username is required"
        elif not password:
            error="Passward is required"
        elif db.execute('SELECT id FROM user WHERE username=?',(username,)).fetchone() is not None:
            error="User {} is already registered".format(username)
        
        if error is None:
            db.execute('INSERT INTO user VALUES(username,passward)',(username,generate_password_hash(password)))
            db.commit()
            return redirect(url_for('auth.login'))
        flash(error)
    return render_template('auth/register.html')

@bp.route('/login',methods=('GET','POST'))
def login():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        error=None
        db=get_db()
        user=db.execute('SELECT * FROM user WHERE username=?',(username)).fetchone()
        if user is None:
            error='Username is not existed'
        elif check_password_hash(user['password'],password):
            error='Password is not accurate'
        
        if error is None:
            session.clear()
            session['user_id']=user['id']
            return redirect(url_for('index'))
        flash(error)
    return redirect(url_for('auth.login'))

@bp.before_app_request
def load_logged_in_user():
    user_id=session['user_id']
    db=get_db()
    
    if user_id is None:
        g.user=None
    else:
        g.user=db.execute('SELECT * FROM user WHERE id=?',(user_id,)).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view


