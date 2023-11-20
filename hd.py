
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
hostname="127.0.0.1"
port=3306
username="root"
password="030904"
database="xmusic"
app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{username}:{password}@{hostname}:{port}/xmusic?charset=utf8mb4"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 创建 Comment 模型
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500))

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    song_name = db.Column(db.String(255))
    file_path = db.Column(db.String(255))


class AdvertisingID(db.Model):
    AdvertisingID = db.Column(db.Integer, primary_key=True)
    Abstract = db.Column(db.String(100))
    title = db.Column(db.String(40))
    ReleaseTime = db.Column(db.DateTime)
    content = db.Column(db.Text)
    Picture = db.Column(db.String(200))

class Admin(db.Model):
    AdmID = db.Column(db.Integer, primary_key=True)
    AdmName = db.Column(db.String(50))
    Aassword = db.Column(db.String(20))




with app.app_context():
 db.create_all()


@app.route('/library')
def index():
    songs = Song.query.all()

    return render_template('library.html', songs=songs)

@app.route('/single/<int:id>')
def single(id):
    song = Song.query.get(id)
    audio_url = song.file_path
    return render_template('single.html', song=song,audio_url=audio_url)


@app.route('/zhegeruh/XMusic/save_comment', methods=['POST'])
def save_comment():
    try:
        # 从JSON请求中获取评论文本
        data = request.get_json()
        text = data.get('text', '')

        if text:
            # 创建 Comment 对象并保存到数据库
            new_comment = Comment(text=text)
            db.session.add(new_comment)
            db.session.commit()

            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'error', 'message': 'Comment text is empty'})

    except Exception as e:
        # 处理可能出现的错误
        return jsonify({'status': 'error', 'message': str(e)})


if __name__ == '__main__':
    app.run(debug=True,port=5000)