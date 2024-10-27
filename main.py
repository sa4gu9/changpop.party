from flask import Flask,render_template, make_response,request,redirect,url_for,jsonify
import random
import secret.option as option

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
        
    print(result)


    text=getFileContent("random",result[0])


    if result[0]!="lostmedia":
        text=text.replace("youtube-video-link",result[0])
    text=text.replace("upload-date",result[1])
    text=text.replace("artist-name",result[2])
    text=text.replace("cpop-name",result[3])

    return render_template("main.html",text=text)

@app.route('/list', methods=['GET','POST'])
def cpoplist():
    returnstr=""
    text=""
    with open(f"list.txt","r",encoding="UTF-8") as f:
        text=f.readlines()

    for i in text:
        if i.startswith("finding"):
            break
        returnstr+=f'<a href="changpop?video_id={i[0:11]}"'+"</a>"+i+"<br>"
        

    return render_template("main.html",text=returnstr)

@app.route('/changpop', methods=['GET'])
def changpop_info():
    video_id=request.args.get("video_id")

    try:
        text=getFileContent(f"changpop/{video_id}")
    except:
        text="존재하지 않는 문서입니다."
    return render_template(f"main.html",text=text)

@app.route('/changpop_kesa', methods=['GET'])
def changpopkesa_info():
    video_id=request.args.get("video_id")

    try:
        text=getFileContent(f"changpop_kesa/{video_id}")
    except:
        text="존재하지 않는 문서입니다."
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
        returnstr+=f'<a href="changpop?video_id={i[0:11]}"'+"</a>"+i+"<br>"
        

    return render_template("main.html",text=returnstr)

@app.route('/changdcup', methods=['GET','POST'])
def changdcuplist():
    

    text=getFileContent("changdcup")


    return render_template("main.html",text=text)



app.run(port=40109,debug=option.testMode)