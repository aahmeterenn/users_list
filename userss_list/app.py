from flask import Flask,render_template,request,redirect,url_for,session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "gizli_anahtar"

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100),nullable=False)
    password = db.Column(db.String(100),nullable=False)



@app.route('/',methods=['GET','POST'])
def index():
    
    return render_template("index.html")

@app.route('/kayit/',methods=['GET','POST'])
def add_user():
    if  request.method == "POST":
        username= request.form["username"]
        password=request.form["password"]
        
        new_user = User(username=username,password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("account"))
    
    return render_template("add_user.html")

@app.route('/users/',methods=['GET','POST'])
def users():
    all_users = User.query.all()
    return render_template('users.html', users=all_users)

@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']  

        user = user.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password,password):
           session['user_id'] = user.id
           return redirect(url_for('account'))
        else:
          return "Hatalı kullanıcı adı veya şifre!"
    
    return render_template('login.html')

if __name__ =="__main__":
   with app.app_context():
    db.create_all()
    app.run(debug=True)
