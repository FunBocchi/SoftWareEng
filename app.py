from flask import Flask, render_template, request, redirect, url_for, session
import pymysql

app = Flask(__name__)
app.secret_key = 'secret_key'

# 连接MySQL数据库
conn = pymysql.connect(host='localhost', port=3306, user='root', password='123456', db='bookshare')
cursor = conn.cursor()

# 创建用户表
cursor.execute('CREATE TABLE IF NOT EXISTS users(id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(50) NOT NULL, '
               'password VARCHAR(50) NOT NULL)')


@app.route('/', methods=['GET'])
def index():
    if 'username' in session:
        return redirect(url_for('home'))
    else:
        return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    cursor.execute('SELECT * FROM users WHERE username=%s AND password=%s', (username, password))
    result = cursor.fetchone()
    if result:
        session['username'] = username
        return redirect(url_for('home'))
    else:
        return render_template('login.html', error='学号或密码不正确！')


@app.route('/home', methods=['GET'])
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    else:
        return redirect(url_for('index'))


@app.route('/home2')
def home2():
    if 'username' in session:
        return render_template('home2.html', username=session['username'])
    else:
        return redirect(url_for('index'))


@app.route("/homePage")
def homePage():
    if 'username' in session:
        return render_template("homePage.html")
    else:
        return render_template("login.html")


@app.route('/register', methods=['GET'])
def register():
    if 'username' in session:
        return redirect(url_for('home2'))
    else:
        return render_template('register.html')


@app.route('/register', methods=['POST'])
def register_user():
    username = request.form['username']
    password = request.form['password']
    user_type = request.form.get('user_type')

    if user_type == 'student':
        cursor.execute('INSERT INTO users(username, password) VALUES (%s, %s)',
                       (username, password, user_type))
        conn.commit()
    elif user_type == 'teacher':
        cursor.execute('INSERT INTO tutors(username, password) VALUES (%s, %s)',
                       (username, password, username))
        conn.commit()

    session['username'] = username

    return redirect(url_for('home2'))


@app.route('/my-circle')
def my_circle():
    if 'username' in session:
        # 查询学生姓名
        cursor = conn.cursor()
        cursor.execute('SELECT StudentName FROM users WHERE username = %s', (session.get('username'),))
        student_name = cursor.fetchone()[0]

        # 查询导师姓名和描述
        cursor.execute('SELECT tutor_name, description FROM circle_info WHERE student_name = %s', (student_name,))
        tutor_info = cursor.fetchone()

        # 查询书籍信息和评论
        book_list = []
        if tutor_info:
            tutor_name = tutor_info[0]
            cursor.execute('SELECT id, book_name, author, reading_plan FROM book_list WHERE tutor_name = %s', (tutor_name,))
            books = cursor.fetchall()
            for book in books:
                cursor.execute('SELECT content, user_name, date FROM comments WHERE book_id = %s', (book[0],))
                comments = cursor.fetchall()
                book_dict = {
                    'title': book[1],
                    'author': book[2],
                    'reading_plan': book[3],
                    'comments': comments
                }
                book_list.append(book_dict)

        # 渲染模板并返回页面
        return render_template('my-circle.html', username=session['username'], tutor_name=tutor_info[0],
                               description=tutor_info[1], book_list=book_list)
    else:
        return redirect(url_for('login'))


@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
