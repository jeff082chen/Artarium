import os
from flask import *
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import pymysql
from api import *

app = Flask(__name__)
app.secret_key = os.urandom(16).hex()

# setup logging
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"
login_manager.login_view = 'login'
login_manager.login_message = 'Please Login'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = pymysql.connect(
            host = '104.199.235.116', 
            port = 3306, 
            user = 'artarium', 
            passwd = '0000', 
            db = 'artarium'
        )
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

class User(UserMixin):
    pass

@login_manager.user_loader
def user_loader(user_id):
    db = get_db()
    cur = db.cursor()
    cur.execute(
        'SELECT password FROM members WHERE member_id = %s', (user_id, )
    )
    password = cur.fetchone()
    if password is None:
        return
    user = User()
    user.id = user_id
    return user

@login_manager.request_loader
def request_loader(request):
    user_id = request.form.get('ID')
    db = get_db()
    cur = db.cursor()
    cur.execute(
        'SELECT password FROM members WHERE member_id = %s', (user_id, )
    )
    password = cur.fetchone()
    if not password:
        return
    user = User()
    user.id = user_id
    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    if request.form.get('password') == password[0]:
        user.is_authenticated = True
    return user

@app.route('/')
def index():
    db = get_db()
    slide = get_slides(db = db)
    cities = list(weather_dict.keys())
    return render_template('index.html', slide = slide, cities = cities)

@app.route('/info')
def info():
    UID = request.args.get('UID')
    db = get_db()
    info = get_info(UID, db = db)
    if info is None:
        return render_template('error.html', error = 'Not Found'), 404
    return render_template('info.html', info = info)

@app.route('/login', methods=['GET', 'POST'])
def login():
    next = request.args.get('next', None)
    if request.method == 'GET':
        return render_template("login.html", next = next)
    user_id = request.form['username']
    user_password = request.form['password']
    db = get_db()
    cur = db.cursor()
    cur.execute(
        'SELECT password FROM members WHERE member_id = %s', (user_id, )
    )
    password = cur.fetchone()
    if not password:
        errorMsg='<span style="color:#35858B">__</span><i class="fa fa-exclamation-triangle" aria-hidden="true"></i>您輸入的帳號不存在'
        return render_template('login.html', errorMsg = errorMsg)
    password = password[0]
    if user_password != password:
        errorMsg='<span style="color:#35858B">__</span><i class="fa fa-exclamation-triangle" aria-hidden="true"></i>您輸入的帳號或密碼有誤'
        return render_template('login.html', errorMsg = errorMsg)
    user = User()
    user.id = user_id
    login_user(user)
    return redirect(next or url_for('index'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    user_id = request.form['username']
    user_password = request.form['password']
    db = get_db()
    cur = db.cursor()
    cur.execute(
        'SELECT member_id FROM members WHERE member_id = %s', (user_id, )
    )
    if cur.fetchone() is not None:
        errorMsg='<span style="color:#35858B">__</span><i class="fa fa-exclamation-triangle" aria-hidden="true"></i>您輸入的帳號已存在'
        return render_template('register.html', errorMsg = errorMsg)
    cur.execute(
        'INSERT INTO members (member_id, password) VALUES (%s, %s)', (user_id, user_password)
    )
    db.commit()
    return redirect(url_for('login'))

@app.route('/favorite')
@login_required
def favorite():
    user_id = current_user.id
    db = get_db()
    favorite = get_favorite(user_id, db = db)
    return render_template('favorite.html', shows = favorite)

@app.route('/like')
@login_required
def like():
    user_id = current_user.id
    UID = request.args.get('UID')
    db = get_db()
    cur = db.cursor()
    cur.execute(
        'SELECT * FROM favorites WHERE member_id = %s AND UID = %s', (user_id, UID)
    )
    if cur.fetchone() is None:
        cur.execute(
            'INSERT INTO favorites (member_id, UID) VALUES (%s, %s)', (user_id, UID)
        )
        db.commit()
        cur.execute('UPDATE activities SET likeCount = likeCount + 1 WHERE UID = %s', (UID, ))
        db.commit()
    else:
        cur.execute('DELETE FROM favorites WHERE member_id = %s AND UID = %s', (user_id, UID))
        db.commit()
        cur.execute('UPDATE activities SET likeCount = likeCount - 1 WHERE UID = %s', (UID, ))
        db.commit()
    return redirect("/info?UID=" + UID)

@app.route('/search')
def search():
    # [('title', 'ewfwe'), ('category', '全部'), ('city', '桃園縣'), ('date', '2022-06-15')]
    title = request.args.get('title')
    category = request.args.get('category')
    city = request.args.get('city')
    date = request.args.get('date')
    db = get_db()
    search = get_search(title, category, city, date, db = db)
    return render_template('search.html', search = search)

@app.route('/popular')
def popular():
    return render_template('popular.html')

@app.route('/lucky')
def lucky():
    db = get_db()
    lucky = lucky_draw(db = db)
    return render_template('lucky.html', lucky = lucky)

@app.route('/comment', methods = ['POST'])
@login_required
def comment():
    user_id = current_user.id
    UID = request.form['UID']
    comment = request.form['content']
    db = get_db()
    leave_reply(UID, user_id, comment, db = db)
    return redirect("/info?UID=" + UID)

@app.route('/delete_comment')
@login_required
def delete_comment():
    user_id = current_user.id
    UID = request.args.get('UID')
    comment_id = request.args.get('comment_id')
    db = get_db()
    delete_reply(UID, user_id, comment_id, db = db)
    return redirect("/info?UID=" + UID)

@app.route('/team', methods=['GET', 'POST'])
@login_required
def team():
    db = get_db()
    if request.method == 'GET':
        UID = request.args.get('UID')
        teams = get_team(UID, db = db)
        return render_template('team.html', teams = teams, UID = UID)
    UID = request.form['UID']
    contact = request.form['contact']
    place = request.form['place']
    member_id = current_user.id
    send_team(UID, member_id, contact, place, db = db)
    return redirect("/team?UID=" + UID)

@app.route('/delete_team')
@login_required
def delete_team():
    user_id = current_user.id
    UID = request.args.get('UID')
    team_id = request.args.get('team_id') 
    db = get_db()
    cancel_team(UID, team_id, user_id, db = db)
    return redirect("/team?UID=" + UID)

@app.route('/restaurant')
def restaurant():
    UID = request.args.get('UID')
    longitude = request.args.get('longitude')
    latitude = request.args.get('latitude')
    db = get_db()
    restaurants = get_restaurant(latitude, longitude, 0.5, db = db)
    return render_template('restaurant.html', restaurants = restaurants, longitude = longitude, latitude = latitude, UID = UID)

@app.route('/weather')
def weather():
    UID = request.args.get('UID')
    longitude = request.args.get('longitude')
    latitude = request.args.get('latitude')
    db = get_db()
    weather_info = get_weather(longitude, latitude, db = db)
    return render_template('weather.html', weather_info = weather_info, UID = UID)

@app.errorhandler(404)
def not_found(e):
    return render_template('error.html', error = 'Not Found'), 404

@app.errorhandler(500)
def not_found(e):
    return render_template('error.html', error = 'Internal Server Error'), 500

if __name__ == '__main__':
    app.run(debug = True, port = 8090)
    #app.run(debug = True, host = '0.0.0.0', port = 8090)
