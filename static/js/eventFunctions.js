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
    console.log("On resize " + onResize);
    if ((map.height() < height && !onResize) || !tall){
        return;
    }
    var width = (window.innerWidth > 0) ? window.innerWidth : screen.width;
    var map_card = $("#map_card");
    var spacer = $("#main-spacer");
    var camera = $("#camera_img");
    var camera_card = $("#camera_card");
    var shout_card = $("#shout_card");
    var padding = $("#mainGrid").css("padding");
    if (width > 1000) {
        /* MANAGING MAP SIZE */
        map_card.css("height",(height - $("#main_header").height()*3));
        map.height(map_card.height() - $("#map_card_title").height());
        map_card.width(map.height() * (map.prop("naturalWidth") / map.prop("naturalHeight")));
        map.width(map_card.width());

        console.log("Checking screen height: " + screen.width);
        console.log("Checking height: " + height);
        console.log("Checking width: " + width);
        console.log("Checking header: " + $("#main_header").height());
        console.log("Checking height map_card: " + map_card.height());
        console.log("Checking height map: " + map.height());

        /* ADAPTING CAMERA COLUMN TO MAP SIZE */
        shout_card.css("height",100);
        shout_card.css("max-height",100);
        camera_card.height(map_card.height() - shout_card.height() - padding);
        camera.height(camera.width() * (camera.prop("naturalHeight") / camera.prop("naturalWidth")));
        if (camera.height() !== (camera_card.height()-$("#camera_card_title").height())){
            camera.height(camera_card.height()-$("#camera_card_title").height()-20);
        }
        camera_card.width(camera.height() * (camera.prop("naturalWidth") / camera.prop("naturalHeight")));
        camera.width(camera_card.width());
        console.log("Checking max width camera: " + camera.css("max-width"));
        console.log("Checking height camera_card: " + camera_card.height());
        console.log("Checking height camera: " + camera.height());
        console.log("Checking width camera_card: " + camera_card.width());
        console.log("Checking width camera: " + camera.width());
        console.log("Checking height shout_card: " + shout_card.height());
        shout_card.width(camera.width()-20);

        spacer.width(width - camera_card.width() - map_card.width() - padding*2);
    }
    else{
        map_card.width('auto');
        map_card.height('auto')
        map.width('auto');
        map.height('auto');
        camera_card.css("width",'auto');
        camera_card.height('auto')
        camera.css("width",'auto');
        camera.height('auto');
        shout_card.width('auto');
        shout_card.height('auto');
    }
}

function windowResized(){
    location.reload();
    resizeMap(true);
}
