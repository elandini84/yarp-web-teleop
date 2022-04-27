let positionX = -1
let positionY = -1
let drag = false;
let pressed = false;
let resized = false;
let righty = false;
let ws = new WebSocket(wsType+window.location.host+"/ws");
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
    $(".stream-img").css("cursor","auto");

    if (!isRobot && btnPressed===2){
        //resizeMap();
        return;
    }

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
    $(".stream-img").css("cursor","auto");
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
    }
    else
    {
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
    if (e.button===2) {
        if (elem.prop("id")==="camera_img") {
            elem.css("cursor", "url(static/images/eye_pointer_36_green.png) 18 18,auto");
            righty = true;
        }
    }
    else{
        $(".stream-img").css("cursor","url(static/images/click_pointer_36_green.png) 18 0,auto");
        righty = false;
    }
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
    resizeMap(false);
    var camera = $("#camera_img");
    var map = $("#map_img");
    camera.on("dragstart",function() { return false; });
    camera.on("contextmenu",function() { return false; });
    map.on("dragstart",function() { return false; });
    map.on("contextmenu",function() { return false; });

    camera.mousedown((e) => simpleDown(e,camera));
    camera.mousemove((e) => manageDragging(e, true));
    camera.mouseup((e) => drag ? manageDrag(e,camera) : updateMousePos(true,e.button));

    map.mousedown((e) => simpleDown(e,map));
    map.mousemove((e) => manageDragging(e, false));
    map.mouseup((e) => drag ? manageDrag(e,map) : updateMousePos(false,e.button));
}

function shout_out(){
    var shout_list = document.getElementById("shout-select");
    window.alert(shout_list[shout_list.selectedIndex].textContent+"\n"+shout_list.value);
}

function manageDragging(e,isRobot){
    if(pressed) {
        drag = true;
        if (righty) {
            if (isRobot)
                $(".stream-img").css("cursor", "url(static/images/eye_pointer_36_red.png) 18 18,auto");
        } else {
            if (isRobot) {
                $(".stream-img").css("cursor", "url(static/images/rotat_pointer_36_red.png) 18 18,auto");
            }
            else{
                $(".stream-img").css("cursor", "url(static/images/place_red_36dp.png) 18 18,auto");
            }
        }
    }
}

function resizeMap(onResize){
    var height = (window.innerHeight > 0) ? window.innerHeight : screen.height;
    var map = $("#map_img");
    var tall = map.prop("naturalWidth") < map.prop("naturalHeight");
    console.log("Madonna troia on resize " + onResize);
    if ((map.height() < height && !onResize) || !tall){
        return;
    }
    console.log("Madonna puttana");
    var width = (window.innerWidth > 0) ? window.innerWidth : screen.width;
    var card = $("#map_card");
    var grid = $("#map-gridI");
    var spacer = $("#main-spacer");
    var main_grid = $("#mainGrid");
    var camera = $("#camera_img");
    var camera_card = $("#camera_card");
    var shout_card = $(".info-card");
    if (width > 1000) {
        map.height(height - 150);
        card.height(map.height());
        map.width(map.height() * (map.prop("naturalWidth") / map.prop("naturalHeight")));
        card.width(map.width());
        spacer.width(600);
    }
    else{
        card.width('auto');
        map.width('auto');
        map.height('auto');
    }
    console.log("Canedio height card: " + camera_card.height());
    console.log("Canedio height img: " + camera.height());
    camera.width(camera.height() * (camera.prop("naturalWidth") / camera.prop("naturalHeight")));
    camera_card.width(camera.width());
    shout_card.width(camera.width()-20);
}

function windowResized(){
    resizeMap(true);
}
