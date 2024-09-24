from flask import Flask,render_template, make_response,request,redirect,url_for,jsonify
import random
import secret.option as option

app = Flask(__name__)

host = ""

if option.testMode:
    host="127.0.0.1"
else:
    host="0.0.0.0"

def getFileContent(htmlFileName):
    hfn = open(f"templates/{htmlFileName}.html","r",encoding="UTF-8")
    content = hfn.read()
    hfn.close()
    return content

@app.route('/', methods=['GET','POST'])
def home():
    text=getFileContent("main")
    result = None
    with open(f"list.txt","r",encoding="UTF-8") as f:
        plist = f.readlines()
        result = random.choice(plist)
        result = result.replace("\n","")

    text=text.replace("youtube-video-link",result)
    return text

app.run(port=40109,debug=True)