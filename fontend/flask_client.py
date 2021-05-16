from flask import Flask, send_file

app = Flask(__name__)


@app.route('/index')
def index():
    # 首页
    return send_file('templates/index.html')


@app.route('/video')
def video():
    # 电影
    return send_file('templates/video.html')


@app.route('/movies/classification/')
def classification():
    # 电影分类
    return send_file('templates/classification.html')


@app.route('/<username>/home/history')
def history(username):
    # 历史记录
    return send_file('templates/html/history.html')


@app.route('/top100/')
def top100():
    return send_file('templates/top100.html')


@app.route('/top100/<cursor>')
def pager_top100(cursor):
    return send_file('templates/top100.html')


@app.route('/login')
def login():
    # 登录
    return send_file('templates/login.html')


@app.route('/register')
def register():
    # 注册
    return send_file('templates/register.html')


@app.route('/<username>/home/profile')
def profile(username):
    # 个人中心
    return send_file('templates/html/profile.html')

@app.route('/<username>/home/video')
def my_video(username):
    # 个人中心
    return send_file('templates/html/myvideo.html')


@app.route('/<username>/home/fans')
def fans(username):
    # 个人中心
    return send_file('templates/html/fans.html')


@app.route('/<username>/home/attention')
def attention(username):
    # 个人中心
    return send_file('templates/html/attention.html')


@app.route('/<username>/movies/release')
def video_release(username):
    # 上传视频
    return send_file('templates/release.html')


@app.route('/<username>/space')
def space(username):
    # 个人空间
    return send_file('templates/space.html')


@app.route('/<username>/attention')
def attention_user(username):
    # 关注的用户
    return send_file('templates/attention_user.html')


@app.route('/<username>/fans')
def fans_user(username):
    # 关注ta的用户
    return send_file('templates/fans_user.html')


@app.route('/movie/<int:m_id>')
def movies_detail(m_id):
    # 电影详情页
    return send_file('templates/detail.html')


@app.route('/movie/player/<int:m_id>')
def player(m_id):
    # 电影播放页
    return send_file('templates/player.html')


@app.route('/movie/shortplayer/<int:m_id>')
def shortplayer(m_id):
    # 电影播放页
    return send_file('templates/shortplayer.html')


@app.route('/404')
def error():
    # error
    return send_file('templates/html/pages-error-404.html')


if __name__ == '__main__':
    app.run(debug=True)
