var ua = navigator.userAgent;
var ipad = ua.match(/(iPad).*OS\s([\d_]+)/),
isIphone =!ipad && ua.match(/(iPhone\sOS)\s([\d_]+)/),
isAndroid = ua.match(/(Android)\s+([\d.]+)/),
isMobile = isIphone || isAndroid;
//判断
if(location.href.indexOf("static") != -1){
    if(isMobile){
        if(location.href.indexOf("mobile") == -1){
            //跳转到手机端
            location.href = location.href.replace("static/","static/mobile/")
        }
    }else{
        if(location.href.indexOf("mobile") != -1){
            //跳转到pc端
            location.href = location.href.replace("mobile/","")
        }
    }
}
//加载每日颜色
var link = document.createElement("link");
link.rel = "stylesheet";
link.type = "text/css";
link.href = "/static/css/dailycolor.css?v=" + Date.now();
document.getElementsByTagName("head")[0].appendChild(link);
$(function(){
    //随机数判断
    if(Math.floor(Math.random()*10+1) % 2 == 0){
        $(".first-name h1").html("刘文斌");
        $(".last-name h1").html("陈晓静");
    }else{
        $(".first-name h1").html("陈晓静");
        $(".last-name h1").html("刘文斌");
    }
    $.ajax({
        url:"/getSpecialDay",
        type:"POST",
        success:function(data){
            if("None" != data){
                var color = data.split("|")[1];
                var message = data.split("|")[0];
                if(location.href.indexOf("index.html") != -1){
                    var html = "<a href='/static/message.html'><marquee bgcolor='"+color+"' style='font-size:16px;color:#fff8ac;padding-top: 5px;padding-bottom: 5px'>"+message+"</marquee></a>";
                    $("#myCarousel .active").prepend(html)
                }
            }
        }
    });
});