let positionX = -1
let positionY = -1
var ws = new WebSocket("ws://"+window.location.host+"/ws");

function updateMousePos() {
    console.log("mi hanno clickato!");
    $("#clickXTxt").html(positionX);
    $("#clickYTxt").html(positionY);
    var msg = {"x":positionX,
               "y":positionY};
    ws.send(JSON.stringify(msg));
}
function manageDrag(e) {
    var posX = $("#camera_img").offset().left
    var posY = $("#camera_img").offset().top;
    cursorX = e.pageX - posX;
    cursorY = e.pageY - posY;
    diffX = Math.abs(positionX - cursorX);
    diffY = Math.abs(positionY - cursorY);
    if (diffX < 5 && diffY < 5) 
    {
        updateMousePos();
    } else 
    {
        $("#clickXTxt").html(positionX+" to "+cursorX);
        $("#clickYTxt").html(positionY+" to "+cursorY);

        var msg = {"x-start":positionX,
                   "y-start":positionY,
                   "x-end":cursorX,
                   "y-end":cursorY};
        ws.send(JSON.stringify(msg));
    }
}
function simpleDown(e) {
    console.log("down on me");
    var posX = $("#camera_img").offset().left
    var posY = $("#camera_img").offset().top;
    positionX = e.pageX - posX;
    positionY = e.pageY - posY;
    drag = false;
}
function init() {
    console.log("merda");
    //document.getElementById("image_raw").addEventListener("click", printMousePos);
    //document.getElementById("image_raw").addEventListener("drag", printMousePos);
    $("#camera_img").on("dragstart",function() { return false; });
    $("#camera_img").on("contextmenu",function() { return false; });
    //document.getElementById('camera_img').ondragstart = function() { return false; };
    //document.getElementById('camera_img').oncontextmenu = function() { return false; };

    let drag = false;

    $("#camera_img").mousedown((e) => simpleDown(e));
    $("#camera_img").mousemove(function(){drag = true;});
    $("#camera_img").mouseup((e) => drag ? manageDrag(e) : updateMousePos());
    //document.getElementById("camera_img").addEventListener('mousedown', (e) => {positionX = e.offsetX; positionY = e.offsetY, drag=false});
    //document.getElementById("camera_img").addEventListener('mousemove', (e) => drag = true);
    //document.getElementById("camera_img").addEventListener('mouseup', (e) => drag ? printDragMousePos(e) : updateMousePos());
}
