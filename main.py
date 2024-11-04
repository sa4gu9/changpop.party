from flask import Flask,render_template, make_response,request,redirect,url_for,jsonify
import random
import secret.option as option
import os

app = Flask(__name__)
host = ""

if option.testMode:
    host="127.0.0.1"
else:
    host="0.0.0.0"

def getFileContent(htmlFileName,cpoplink=None):
    hfn = open(f"templates/{htmlFileName}.html","r",encoding="UTF-8")
    content = hfn.readlines()
    hfn.close()

    if cpoplink=="lostmedia":
        content[8]="youtube-video-link<br>"
        del content[2:8]
    
    returnstr=""

    for line in content:
        returnstr+=line

    return returnstr

@app.route('/', methods=['GET','POST'])
def home():
    
    result = ["finding"]

    while result[0]=="finding":
        with open(f"list.txt","r",encoding="UTF-8") as f:
            plist = f.readlines()
            result = random.choice(plist)
            result = result.replace("\n","")
            result = result.split("...")
    text=getFileContent("random",result[0])


    if result[0]!="lostmedia":
        text=text.replace("youtube-video-link",result[0])
    text=text.replace("upload-date",result[1])
    text=text.replace("artist-name",result[2])
    text=text.replace("cpop-name",result[3])

    return render_template("main.html",text=text)


@app.route('/ads.txt', methods=['GET','POST'])
def adstxt():
    with open("ads.txt","r",encoding="UTF-8") as f:
        return f.read()

@app.route('/list', methods=['GET','POST'])
def cpoplist():
    returnstr=""
    text=""
    with open(f"list.txt","r",encoding="UTF-8") as f:
        text=f.readlines()

    for i in text:
        if i.startswith("finding"):
            break
        returnstr+=f'<a href="changpop?video_id={i[0:11]}&mode=read"'+"</a>"+i+"<br>"

    return render_template("main.html",text=returnstr)


def get_video(video_id):
    text=f"""<div class="player">
    <iframe width="560" height="315" src="https://www.youtube.com/embed/{video_id}?autoplay=0"
    title="YouTube video player" frameborder="0"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
    allowfullscreen></iframe><br>
    </div><br>"""

    return text

def get_document(is_kesa, video_id):

    text=""
    add_text=""
    if is_kesa:
        add_text="_kesa"
    try:
        text+=getFileContent(f"changpop{add_text}/{video_id}/recent")
    except:
        text+="존재하지 않는 문서입니다."

    return text


@app.route('/changpop', methods=['GET','POST'])
def changpop_info():
    video_id=request.args.get("video_id")
    mode=request.args.get("mode")
    after=""
    if mode=="edit":

        if request.method == 'POST':
            #파일 저장
            after=request.form['text']

            

            #파일의 세부 변경사항을 저장하기
            before=get_document(False,video_id)
            
            if before==after:
                pass
            else:
                #미디어 차단
                if "a href" in after or "img" in after or "video" in after or "iframe" in after or "audio" in after:
                    return redirect(f"changpop?video_id={video_id}&mode=edit")
                count=0

                #폴더의 파일 개수 확인
                try:
                    count=len(os.listdir(f"templates/changpop/{video_id}"))
                except:
                    count=1
                    os.mkdir(f"templates/changpop/{video_id}")


                with open(f"templates/changpop/{video_id}/V{count}.html","w",encoding="UTF-8") as f:
                    f.write(before)

                with open(f"templates/changpop/{video_id}/recent.html","w",encoding="UTF-8") as f:
                    f.write(after)


            #읽기모드 페이지로 url 변경
            return redirect(f"changpop?video_id={video_id}&mode=read")
        
            
        if request.method == 'GET':

            #html input text로 수정할 수 있게
            after+=f"""<form action="changpop?video_id={video_id}&mode=edit" method="post">
            <textarea name="text" rows="10" cols="50">{get_document(False,video_id)}</textarea>
            <input type="submit" value="수정">
            </form>"""

    elif mode=="read":
        after=get_video(video_id)
        after+=get_document(False,video_id)

        #a href로 수정버튼 추가
        after+=f'<a href="changpop?video_id={video_id}&mode=edit">수정</a>'
    
    return render_template(f"main.html",text=after)


@app.route('/changpop_kesa', methods=['GET'])
def changpopkesa_info():
    video_id=request.args.get("video_id")
    text=get_document(True,video_id)
    
    return render_template(f"main.html",text=text)

@app.route('/prompt', methods=['GET','POST'])
def promptlist():
    text=getFileContent(f"prompt")

    return render_template(f"main.html",text=text)


@app.route('/kesa_list', methods=['GET','POST'])
def cpopkesalist():
    returnstr=""
    text=""
    with open(f"list_kesa.txt","r",encoding="UTF-8") as f:
        text=f.readlines()

    for i in text:
        if i.startswith("finding"):
            break
        returnstr+=f'<a href="changpop?video_id={i[0:11]},mode=read"'+"</a>"+i+"<br>"
        

    return render_template("main.html",text=returnstr)

@app.route('/changdcup', methods=['GET','POST'])
def changdcuplist():
    text=getFileContent("changdcup")

    return render_template("main.html",text=text)


app.run(port=40109,debug=option.testMode)