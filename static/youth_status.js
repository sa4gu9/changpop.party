function youth_view() {
  var API_BASE = null;

  if (window.location.hostname === "127.0.0.1") {
    API_BASE = "http://127.0.0.1:41002";
  } else {
    API_BASE = "https://changpop.party/api";
  }

  $.ajax({
    url: `${API_BASE}/youth_view`,
    type: "GET",
    success: function (data) {
      $("#timer").text(data.timer["minute"] + ":" + data.timer["seconds"]);

      if (document.getElementById("youth_view").context == "empty") {
        if (data.timer["seconds"] != 0 && data.timer["minute"] != 0) {
          return;
        }
      }

      const video_list = Object.entries(data.videos).sort(function (a, b) {
        return b[1] - a[1];
      });

      $("#youth_view").empty(); // 기존 내용을 비우고 새로 추가

      video_list.forEach(function (element) {
        console.log(element[0] + " : " + element[1]);
        $("#youth_view").append(element[0] + " : " + element[1] + "<br>");
      });
    },
    error: function (xhr, status, error) {
      console.error("Error fetching youth view:", error);
    },
  });
}

youth_view(); // 페이지 로드 시 초기 호출
setInterval(youth_view, 5000);
