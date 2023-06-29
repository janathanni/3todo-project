(function(d) {
  var config = {
    kitId: 'iyy2yam',
    scriptTimeout: 0,
    async: true
  },
  h=d.documentElement,t=setTimeout(function(){h.className=h.className.replace(/\bwf-loading\b/g,"")+" wf-inactive";},config.scriptTimeout),tk=d.createElement("script"),f=false,s=d.getElementsByTagName("script")[0],a;h.className+=" wf-loading";tk.src='https://use.typekit.net/'+config.kitId+'.js';tk.async=true;tk.onload=tk.onreadystatechange=function(){a=this.readyState;if(f||a&&a!="complete"&&a!="loaded")return;f=true;clearTimeout(t);try{Typekit.load(config)}catch(e){}};s.parentNode.insertBefore(tk,s)
})(document);

var url = window.location.pathname;
console.log(url);

let todo_btn = document.querySelector(".todo_btn");
let setting_btn = document.querySelector(".setting_btn");

if(url == '/todo/'){
  todo_btn.style.background = "#F1EDE9";
  setting_btn.style.background = "#ff9d00";
} else if (url == '/setting/') {
  todo_btn.style.background = "#ff9d00";
  setting_btn.style.background = "#F1EDE9";
}

// let close = document.querySelector("#cross");
// close.addEventListener("click", function(){
//   const popup2 = document.getElementById("donewrap").style.display = "none";
// })

//조단희가 수정한 부분 
$(document).ready(function () {
  $(".modal .btn_close").click(function () {
      setCookieMobile( "todayCookie", "done" , 1);
      $("#donewrap").css("visibility", "hidden");
  });
});

function setCookieMobile ( name, value, expiredays ) {
  var todayDate = new Date();
  todayDate.setDate( todayDate.getDate() + expiredays );
  document.cookie = name + "=" + escape( value ) + "; path=/; expires=" + todayDate.toGMTString() + ";"
}


function getCookieMobile () {
  var cookiedata = document.cookie;
  if ( cookiedata.indexOf("todayCookie") < 0 ){
    $("#donewrap").css("visibility", "visible");
  }
  else {
    $("#donewrap").css("visibility", "hidden");
  }
}

getCookieMobile();
//수정 끝


window.onload = function(){
  todo_btn.addEventListener("click", function(){
    todo_btn.style.background = "#F1EDE9";
    setting_btn.style.background = "#ff9d00";
    console.log(url);
  });

  setting_btn.addEventListener("click", function(){
    todo_btn.style.background = "#ff9d00";
    setting_btn.style.background = "#F1EDE9";
    console.log(url);
  });
}

