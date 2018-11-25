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