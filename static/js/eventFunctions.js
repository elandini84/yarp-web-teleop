let positionX = -1
let positionY = -1
let drag = false;
let pressed = false;
let ws = new WebSocket("wss://"+window.location.host+"/ws");
const LEFT_BTN = 0;
const RIGHT_BTN = 2;
const ROBOT = "camera_img";
const MAP = "map_img";
console.log(window.location.host);

function convertMousePos(x,y,elem){
    var conversionX = elem.prop("naturalWidth")/elem.width();
    var conversionY = elem.prop("naturalHeight")/elem.height();
    return {"x": Math.round(x*conversionX),
            "y": Math.round(y*conversionY)};
}

function updateMousePos(isRobot,btnPressed) {
    pressed = false;
    drag = false;
    $("#clickXTxt").html(positionX);
    $("#clickYTxt").html(positionY);
    var msg = {"x":positionX,
               "y":positionY,
               "button":btnPressed,
               "is_robot":isRobot};
    ws.send(JSON.stringify(msg));
    console.log("UpdateMousePos; pressed: "+pressed+" drag: "+drag);
}

function manageDrag(e,elem) {
    pressed = false;
    drag = false;
    var posX = elem.offset().left
    var posY = elem.offset().top;
    var cursorX = e.pageX - posX;
    var cursorY = e.pageY - posY;
    var cursors = convertMousePos(cursorX,cursorY,elem);
    var diffX = Math.abs(positionX - cursors.x);
    var diffY = Math.abs(positionY - cursors.y);
    if (diffX < 5 && diffY < 5) 
    {
        updateMousePos(elem.prop("id")===ROBOT,e.button);
    } else 
    {
        $("#clickXTxt").html(positionX+" to "+cursors.x);
        $("#clickYTxt").html(positionY+" to "+cursors.y);

        var msg = {"x-start":positionX,
                   "y-start":positionY,
                   "x-end":cursors.x,
                   "y-end":cursors.y,
                   "is_robot":elem.prop("id")===ROBOT,
                   "button": e.button};
        ws.send(JSON.stringify(msg));
    }
}

function simpleDown(e,elem) {
    drag = false;
    pressed = true;
    console.log("simpleDown "+e.button+" called from: "+elem.prop("id"));
    var posX = elem.offset().left
    var posY = elem.offset().top;
    var fakeX = e.pageX - posX;
    var fakeY = e.pageY - posY;
    var position = convertMousePos(fakeX,fakeY,elem);
    positionX = position.x;
    positionY = position.y;
}

function init() {
    var camera = $("#camera_img");
    var map = $("#map_img");
    camera.on("dragstart",function() { return false; });
    camera.on("contextmenu",function() { return false; });
    map.on("dragstart",function() { return false; });
    map.on("contextmenu",function() { return false; });

    camera.mousedown((e) => simpleDown(e,camera));
    camera.mousemove(function(){if(pressed) drag = true;});
    camera.mouseup((e) => drag ? manageDrag(e,camera) : updateMousePos(true,e.button));

    map.mousedown((e) => simpleDown(e,map));
    map.mousemove(function(){if(pressed) drag = true;});
    map.mouseup((e) => drag ? manageDrag(e,map) : updateMousePos(false,e.button));
}

function showNatSize() {
    var camera = $("#camera_img");
    var map = $("#map_img");
    $("#clickXTxt").html(camera.prop("naturalWidth")+"x"+camera.prop("naturalHeight"));
    $("#clickYTxt").html(map.prop("naturalWidth")+"x"+map.prop("naturalHeight"));
    console.log(document.body.clientHeight);
    console.log($("#mainGrid").height());
}
