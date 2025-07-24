
from flask import Blueprint, Flask, request, jsonify
from secret import option
from googleapiclient.discovery import build
import time
import threading

apiBluePrint = Blueprint('api', __name__, url_prefix='/api')
class youth_status:
    def __init__(self):
        self.youth_view = {}
        # YouTube API 키 입력
        self.API_KEY = option.youtube_API_KEY
        self.timer={"seconds": 0, "minute": 0}

    def check_timer(self):
        while True:
            if self.timer["seconds"] == 0 and self.timer["minute"] == 0:
                self.youth_view = self.get_playlist_videos("PLJZ8JY7xrUd4iI7EyraoIr2sAYT_Iyy-n")
                self.timer["seconds"] = 0
                self.timer["minute"] = 60
                
            self.timer["seconds"] -= 1


            if self.timer["seconds"] < 0:
                self.timer["seconds"] += 60
                self.timer["minute"] -= 1
            print(self.timer["minute"], self.timer["seconds"])

            time.sleep(1)
    # YouTube Data API 클라이언트 생성

    def get_youtube_client(self):

        youtube = build("youtube", "v3", developerKey=self.API_KEY)

        return youtube


    def get_playlist_videos(self,playlist_id):
        youtube = self.get_youtube_client()
        temp_videos = {}
        video_info_map = {}
        video_ids = []
        videos={}
        next_page_token = None
        
        while True:
            request = youtube.playlistItems().list(
                part="snippet",
                playlistId=playlist_id,
                maxResults=50,  # 한 번에 가져올 수 있는 최대 개수
                pageToken=next_page_token
            )
            response = request.execute()


            for item in response.get('items', []):

                video_id=item['snippet']['resourceId']['videoId']
                title=item['snippet']['title']
                video_ids.append(video_id)
                video_info_map[video_id] = title

            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break

        for i in range(0, len(video_ids), 50):
            chunk = video_ids[i:i + 50]
            starts_request = youtube.videos().list(
                part = "statistics",
                id = ','.join(chunk)
            )
            starts_response = starts_request.execute()

            for item in starts_response.get('items', []):
                video_id = item['id']
                title = video_info_map[video_id]
                views = int(item["statistics"]["viewCount"])
                temp_videos[title] = views




        #temp_videos=dict(sorted(temp_videos.items(), key=lambda item:item[1]))  # 조회수 기준으로 정렬
        videos["timer"] = self.timer
        videos["videos"]=temp_videos

        for title, views in temp_videos.items():
            print(f"{title}: {views} views")

        return videos




apiApp = Flask(__name__)



host = "127.0.0.1" if option.testMode else "0.0.0.0"




@apiBluePrint.route('/youth_view', methods=['GET'])
def get_youth_view():
    return jsonify(youth_status_instance.youth_view)

if option.testMode:
    origins = ["http://localhost:49494","http://127.0.0.1:49494","https://changpop.party"]
else:
    origins = ["*"]

from flask_cors import CORS
CORS(apiApp, origins=origins, supports_credentials=True, methods=["GET", "POST", "OPTIONS"], allow_headers=["Content-Type"])

if __name__ == '__main__':
    
    apiApp.register_blueprint(apiBluePrint)
    youth_status_instance = None
    if youth_status_instance is None:
        youth_status_instance = youth_status()
        timer_thread = threading.Thread(target=youth_status_instance.check_timer)
        timer_thread.daemon = True  # 메인 스레드가 종료되면 이 스레드도 종료
        timer_thread.start()  # 스레드 시작
    
    apiApp.run(debug=option.testMode, host=host, port=option.apiport,use_reloader=False)