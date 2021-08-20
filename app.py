from pymongo import MongoClient

from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.moviestar


# HTML 화면 보여주기
@app.route('/')
def home():
    return render_template('index.html')


# API 역할을 하는 부분
# DB에 있는 모든 배우의 정보를 클라이언트에 넘겨줌.
@app.route('/api/list', methods=['GET'])
def show_stars():
    # 배우들을 좋아요가 많은 순으로 정렬
    actors = list(db.mystar.find({}, {'_id': False}).sort('like', -1))

    return jsonify({'movie_stars': actors})

# 클라이언트한테 배우의 이름을 받아서 해당하는 배우의 좋아요를 DB에서 1을 증가시킴.
@app.route('/api/like', methods=['POST'])
def like_star():
    actor_name = request.form['actor_name']
    actor = db.mystar.find_one({'name': actor_name})
    current_like = actor['like']
    #현재 좋아요 + 1
    new_like = current_like + 1
    #db에 업데이트
    db.mystar.update_one({'name': actor_name}, {'$set': {'like': new_like}})

    return jsonify({'msg': '좋아요 완료'})

# 클라이언트한테 배우의 이름을 받아서 해당하는 배우 삭제
@app.route('/api/delete', methods=['POST'])
def delete_star():
    actor_name = request.form['actor_name']
    
    db.mystar.delete_one({'name': actor_name})
    return jsonify({'msg': '삭제 완료'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)