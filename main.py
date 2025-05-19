import time
from flask import Flask,render_template, make_response,request,redirect,url_for,jsonify
import random
import secret.option as option
import os
from gevent.pywsgi import WSGIServer
import datetime
import threading

project_root = os.path.dirname(__file__)
template_path = os.path.join(project_root, 'templates')
app = Flask(__name__, template_folder=template_path)


host = ""
listpath=f"{os.path.dirname(os.path.abspath(__file__))}/list.txt"
listpath1201=f"{os.path.dirname(os.path.abspath(__file__))}/list10201201.txt"
kesapath=f"{os.path.dirname(os.path.abspath(__file__))}/list_kesa.txt"
kesapath1201=f"{os.path.dirname(os.path.abspath(__file__))}/kesalist10201201.txt"
if option.testMode:
    host="127.0.0.1"
else:
    host="0.0.0.0"

@app.route('/youthyouthsheet', methods=['GET','POST'])
def youthyouthsheet():
    return redirect("https://docs.google.com/spreadsheets/d/1eVphTP9FaDgKn4W0x03rQBDrYMF2ibANxEpaz1dFNvU/edit?gid=1280611118#gid=1280611118")

def getFileContent(htmlFileName,cpoplink=None):
    hfn = open(f"{os.path.dirname(os.path.abspath(__file__))}/templates/{htmlFileName}.html","r",encoding="UTF-8")
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
    #xlsx파일 대신 csv파일 불러오기
    import csv
    with open(f'{os.path.dirname(os.path.abspath(__file__))}/오늘의 추천곡.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            print(row)
            print(row[0])
            if row[0]==datetime.datetime.now().strftime("%Y-%m-%d"):
                text=f"""<br>오늘의 추천곡<br><div class="player">
    <iframe width="560" height="315" src="https://www.youtube.com/embed/{row[1]}?autoplay=0"
        title="YouTube video player" frameborder="0"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        allowfullscreen></iframe><br>
</div><br>{row[2]}"""
                break



    return render_template("main.html",text=text)


@app.route('/ads.txt', methods=['GET','POST'])
def adstxt():
    with open(f"{os.path.dirname(os.path.abspath(__file__))}/ads.txt","r",encoding="UTF-8") as f:
        return f.read()


@app.route('/list', methods=['GET','POST'])
def cpoplist():
    returnstr=""
    text=""
    with open(listpath,"r",encoding="UTF-8") as f:
        text=f.readlines()

    for i in text:
        if i.startswith("finding"):
            break
        returnstr+=f'<a href="changpop?video_id={i[0:11]}&mode=read"'+"</a>"+i+"<br>"

    with open(listpath1201,"r",encoding="UTF-8") as f:
        text=f.readlines()
        

    for i in text:
        if "?si=" in i:
            i=i[0:11]+i[32:]
        
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

def get_document(video_id,mode="read",version="recent"):

    text=""
    try:
        text+=getFileContent(f"changpop/{video_id}/{version}")
    except:
        
        text+="존재하지 않는 문서입니다."
    if mode=="read":
        text+=f'<a href="changpop?video_id={video_id}&mode=edit&type=document">수정</a>'
    return text


def get_lyric(video_id,mode="read"):
    text=""
    try:
        text+=getFileContent(f"changpop/{video_id}/lyric")
    except:
        text+="가사가 작성되지 않았습니다."
    if mode=="read":
        text+=f'<a href="changpop?video_id={video_id}&mode=edit&type=lyric">수정</a>'
    return text

import secret.youthyouth.getview as getview


youth_status_list = ""

#1시간마다 조회수 체크
def check_view():
    global youth_status_list
    while True:
        playlist_id = "PLJZ8JY7xrUd4iI7EyraoIr2sAYT_Iyy-n"

        videos = getview.get_playlist_videos(playlist_id)

        value=""
        for video in videos:
            value+=video[0]+" "+str(video[1])+"<br>"
        
        youth_status_list = value
        time.sleep(3600)







@app.route('/youth_status', methods=['GET','POST'])
def youth_status():
    global youth_status_list
    text=getFileContent("youth_status")

    if youth_status_list=="":
        value = "로딩중입니다."
    else:
        value = youth_status_list


    return render_template("main.html",text=value)


@app.route('/changpop', methods=['GET','POST'])
def changpop_info():
    video_id=request.args.get("video_id")
    mode=request.args.get("mode")
    ver=request.args.get("version")
    type=request.args.get("type")
    after=""
    if mode=="edit":

        if request.method == 'POST':
            #파일 저장
            after=request.form['text']

            keyword=["a href","img","video","iframe","audio","script"]
            #미디어 차단
            for i in keyword:
                if i in after:
                    return redirect(f"changpop?video_id={video_id}&mode=edit&type={type}")

            if type=="document":
                #파일의 세부 변경사항을 저장하기
                before=get_document(video_id,mode)
            elif type=="lyric":
                before=get_lyric(video_id,mode)
            
            if before==after:
                pass
            else:
                count=0

                #폴더의 파일 개수 확인
                if type=="document":
                    #파일의 세부 변경사항을 저장하기
                    try:
                        file_list=os.listdir(f"templates/changpop/{video_id}")
                        file_list_py = [file for file in file_list if file.endswith(".html")]
                        count=len(file_list_py)

                        with open(f"templates/changpop/{video_id}/V{count}.html","w",encoding="UTF-8") as f:
                            f.write(before)
                    except:
                        count=1
                        os.mkdir(f"templates/changpop/{video_id}")

                    with open(f"templates/changpop/{video_id}/recent.html","w",encoding="UTF-8") as f:
                        f.write(after)
                    
                elif type=="lyric":
                    with open(f"templates/changpop/{video_id}/lyric.html","w",encoding="UTF-8") as f:
                        f.write(after)



            #읽기모드 페이지로 url 변경
            return redirect(f"changpop?video_id={video_id}&mode=read")
        
            
        if request.method == 'GET':

            #html input text로 수정할 수 있게
            after+=f"""<form action="changpop?video_id={video_id}&mode=edit&type={type}" method="post">
            """
            if type=="document":
                after+=f'''<textarea name="text" rows="10" cols="50">{get_document(video_id,mode)}</textarea>'''
            
            elif type=="lyric":
                after+=f'''<textarea name="text" rows="10" cols="50">{get_lyric(video_id,mode)}</textarea>'''
            after+="""<input type="submit" value="수정"> </form>"""

    elif mode=="read":
        print(ver)
        after=get_video(video_id)
        if ver==None:
            after+=get_document(video_id,mode)
            after+="<br><br><br>가사<br>"
            after+=get_lyric(video_id,mode)
            print(after)
        else:
            text=get_document(video_id,mode,version=ver)

            if text=="존재하지 않는 문서입니다.":
                return redirect(f"changpop?video_id={video_id}&mode=read")
            else:
                after+=text
            after+=get_lyric(video_id,mode)
    elif mode=="version":
        versions = os.listdir(f"templates/changpop/{video_id}")
        return render_template(f"main.html",text=versions)
    else:
        return redirect(f"changpop?video_id={video_id}&mode=read")
    
    return render_template(f"main.html",text=after)


@app.route('/changpop_kesa', methods=['GET'])
def changpopkesa_info():
    video_id=request.args.get("video_id")
    text=get_document(video_id)
    
    return render_template(f"main.html",text=text)

@app.route('/prompt', methods=['GET','POST'])
def promptlist():
    text=getFileContent(f"prompt")

    return render_template(f"main.html",text=text)

@app.route('/contest', methods=['GET','POST'])
def contestlist():
    text=getFileContent(f"contest")

    return render_template(f"main.html",text=text)


@app.route('/kesa_list', methods=['GET','POST'])
def cpopkesalist():
    returnstr=""
    text=""
    with open(kesapath,"r",encoding="UTF-8") as f:
        text=f.readlines()

    for i in text:
        if i.startswith("finding"):
            break
        returnstr+=f'<a href="changpop?video_id={i[0:11]}&mode=read"'+"</a>"+i+"<br>"

    with open(kesapath1201,"r",encoding="UTF-8") as f:
        text=f.readlines()

    for i in text:
        if "?si=" in i:
            i=i[0:11]+i[32:]
        returnstr+=f'<a href="changpop?video_id={i[0:11]}&mode=read"'+"</a>"+i+"<br>"
        

    return render_template("main.html",text=returnstr)


@app.route('/recommand', methods=['GET'])
def recommandlist():

    text=""

    import csv
    with open(f'{os.path.dirname(os.path.abspath(__file__))}/오늘의 추천곡.csv', 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        for row in reader:
            print(row)
            if datetime.datetime.strptime(row[0],"%Y-%m-%d") < datetime.datetime.now():
                for value in row:

                    text+=f"{value} "
                text+="<br>"
                

    return render_template("main.html",text=text)



@app.route('/changdcup', methods=['GET','POST'])
def changdcuplist():
    text=getFileContent("changdcup")

    return render_template("main.html",text=text)




problemList={}

@app.route('/quiz', methods=['GET','POST'])
def cpopquiz():
    global problemList
    returnstr=''
    id=0
    resp = make_response(redirect('quiz'))

    if request.method == 'POST':
        if 'testid' in request.cookies.keys():
            testid=request.cookies.get('testid')

            if testid==0:
                id = str(random.randint(100000000000,999999999999))

                while id in problemList:
                    id = str(random.randint(100000000000,999999999999))
            elif testid in problemList.keys():
                print(123123123213)
                submit=request.form['text']
                submit=submit.replace(" ","")
                submit=submit.replace(",","")
                submit=submit.lower()
                answer=problemList[testid].replace(" ","")
                answer=answer.replace(",","")
                answer=answer.lower()
                if submit==answer:
                    returnstr="정답입니다."
                else:
                    returnstr="오답입니다."

                returnstr+=f"\n정답 : {problemList[testid]}"

                resp.delete_cookie('testid')
                del problemList[testid]
                return render_template("main.html",text=returnstr)
            else:
                return redirect('quiz')
        else:
            print(1111111111111111111111)
            return make_response(redirect('quiz'))

            
    if request.method == 'GET':
        print("asdfdasfasf")
        result = "finding"

        while result=="finding" or result[0]=="lostmedia" or result[0]=="finding":
            with open(listpath,"r",encoding="UTF-8") as f:
                plist = f.readlines()
                result = random.choice(plist)
                result = result.replace("\n","")
                result = result.split("...")
        returnstr=getFileContent("random",result[0])

        returnstr=returnstr.replace("youtube-video-link",result[0])
        returnstr=returnstr.replace("upload-date","")
        returnstr=returnstr.replace("artist-name","")
        returnstr=returnstr.replace("cpop-name","")

        returnstr+=getFileContent(f"quiz")

        id = str(random.randint(100000000000,999999999999))

        while id in problemList:
            id = str(random.randint(100000000000,999999999999))
        print(result)
        problemList[id]=result[3]

    resp = make_response(render_template("main.html",text=returnstr))
    if id!=0:
        resp.set_cookie('testid',str(id))
    return resp


if __name__ == '__main__':
    youth_thread = threading.Thread(target=check_view)
    youth_thread.start()
    if option.testMode:
        app.run(debug=True, host=host, port=option.port)
    else:
        # Debug/Development
        # app.run(debug=True, host="0.0.0.0", port="5000")
        # Production
        


        http_server = WSGIServer(('', option.port), app)
        http_server.serve_forever()