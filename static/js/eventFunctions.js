let positionX = -1
let positionY = -1
let drag = false;
let ws = new WebSocket("ws://"+window.location.host+"/ws");
console.log(window.location.host);

function convertMousePos(x,y){
    var camera = $("#camera_img");
    var conversionX = camera.prop("naturalWidth")/camera.width();
    var conversionY = camera.prop("naturalHeight")/camera.height();
    return {"x": Math.round(x*conversionX),
            "y": Math.round(y*conversionY)};
}

function updateMousePos() {
    $("#clickXTxt").html(positionX);
    $("#clickYTxt").html(positionY);
    var msg = {"x":positionX,
               "y":positionY};
    ws.send(JSON.stringify(msg));
}

function manageDrag(e) {
    var camera = $("#camera_img");
    var posX = camera.offset().left
    var posY = camera.offset().top;
    var cursorX = e.pageX - posX;
    var cursorY = e.pageY - posY;
    var cursors = convertMousePos(cursorX,cursorY);
    var diffX = Math.abs(positionX - cursors.x);
    var diffY = Math.abs(positionY - cursors.y);
    if (diffX < 5 && diffY < 5) 
    {
        updateMousePos();
    } else 
    {
        $("#clickXTxt").html(positionX+" to "+cursors.x);
        $("#clickYTxt").html(positionY+" to "+cursors.y);

        var msg = {"x-start":positionX,
                   "y-start":positionY,
                   "x-end":cursors.x,
                   "y-end":cursors.y};
        ws.send(JSON.stringify(msg));
    }
}

function simpleDown(e) {
    var camera = $("#camera_img");
    var posX = camera.offset().left
    var posY = camera.offset().top;
    var fakeX = e.pageX - posX;
    var fakeY = e.pageY - posY;
    var position = convertMousePos(fakeX,fakeY);
    positionX = position.x;
    positionY = position.y;
    drag = false;
}

function init() {
    var camera = $("#camera_img");
    //document.getElementById("image_raw").addEventListener("click", printMousePos);
    //document.getElementById("image_raw").addEventListener("drag", printMousePos);
    camera.on("dragstart",function() { return false; });
    camera.on("contextmenu",function() { return false; });
    //document.getElementById('camera_img').ondragstart = function() { return false; };
    //document.getElementById('camera_img').oncontextmenu = function() { return false; };

    camera.mousedown((e) => simpleDown(e));
    camera.mousemove(function(){drag = true;});
    camera.mouseup((e) => drag ? manageDrag(e) : updateMousePos());
    //document.getElementById("camera_img").addEventListener('mousedown', (e) => {positionX = e.offsetX; positionY = e.offsetY, drag=false});
    //document.getElementById("camera_img").addEventListener('mousemove', (e) => drag = true);
    //document.getElementById("camera_img").addEventListener('mouseup', (e) => drag ? printDragMousePos(e) : updateMousePos());
}

function showNatSize() {
    var camera = $("#camera_img");
    var map = $("#map_img");
    $("#clickXTxt").html(camera.prop("naturalWidth")+"x"+camera.prop("naturalHeight"));
    $("#clickYTxt").html(map.prop("naturalWidth")+"x"+map.prop("naturalHeight"));
    console.log(document.body.clientHeight);
    console.log($("#mainGrid").height());
}
