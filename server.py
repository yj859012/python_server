from flask import Flask, render_template, request, redirect, make_response
from werkzeug.utils import secure_filename
from aws import detect_labels_local_file as label
from aws import compare_faces  # compare_faces 함수도 import!

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/compare", methods=["POST"])
def compare():
    try:
        if request.method == "POST":
            # 이미지 2개 받기
            f1 = request.files["file1"]
            f2 = request.files["file2"]

            # 안전한 파일 이름 만들기
            filename1 = secure_filename(f1.filename)
            filename2 = secure_filename(f2.filename)

            # static 폴더에 저장
            path1 = "static/" + filename1
            path2 = "static/" + filename2

            f1.save(path1)
            f2.save(path2)

            # compare_faces 함수 호출
            result = compare_faces(path1, path2)

            return result
    except Exception as e:
        print(e)
        return "얼굴 비교 실패"

@app.route("/detect", methods=["POST"])
def detect():
    try:
        if request.method == "POST":
            f = request.files["file"]
            filename = secure_filename(f.filename)
            f.save("static/" + filename)
            r = label("static/" + filename)
            return r
    except:
        return "감지실패"

@app.route("/mbti", methods=["POST"])
def mbti():
    try:
        if request.method == "POST":
            mbti = request.form["mbti"]
            return f"당신의 MBTI는 {mbti}입니다"
    except:
        return "데이터 수신 실패"

@app.route("/login", methods=["GET"])
def login():
    try:
        if request.method == "GET":
            login_id = request.args["login_id"]
            login_pw = request.args["login_pw"]

            if (login_id == "nayeho") and (login_pw == "1234"):
                response = make_response(redirect("/login/success"))
                response.set_cookie("user", login_id)
                return response
            else:
                return redirect("/")
    except:
        return "로그인 실패"

@app.route("/login/success", methods=["GET"])
def login_success():
    login_id = request.cookies.get("user")
    return f"{login_id}님 환영합니다"

if __name__ == "__main__":
    app.run(host="0.0.0.0")
