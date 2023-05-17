let positionY = -1
let positionX = -1
let drag = false;
let pressed = false;
let resized = false;
let righty = false;
let velMsgTimeRes = 100;
let ws = new WebSocket(wsType+window.location.host+"/ws");
let wsb = new WebSocket(wsType+window.location.host+"/wsb");
let fastLeftOn = false;
let leftOn = false;
let forwardOn = false;
let rightOn = false;
let fastRightOn = false;
const LEFT_BTN = 0;
const RIGHT_BTN = 2;
const ROBOT = "camera_img";
const MAP = "map_img";
const LIGHTCOL = "#b7d5e1";
const DARKCOL = "#3b7991";
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
    document.getElementById("mainBody").addEventListener("keydown",(e)=>keyNavigation(e));
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
    //window.alert(shout_list[shout_list.selectedIndex].textContent+"\n"+shout_list.value);
    if (shout_list.value !== "EMPTY") {
        var msg = {"audio": shout_list.value};
        wsb.send(JSON.stringify(msg));
    }
}

function sendVelocityData(velLeft,velRight,velForward=0.0){
    var msg = {"vel-right":velRight,
        "vel-left":velLeft,
        "vel-forward":velForward};
    wsb.send(JSON.stringify(msg));
}

function keyNavigation(e) {
    var charCode = (typeof e.which == "number") ? e.which : e.keyCode;
    if (charCode > 0) {
        console.log("Typed character: " + String.fromCharCode(charCode));
        if (String.fromCharCode(charCode) === "A"){
            sendVelocityData(100,0);
        }
        else if (String.fromCharCode(charCode) === "D"){
            sendVelocityData(0,100);
        }
        else if (String.fromCharCode(charCode) === "Q"){
            sendVelocityData(50,0);
        }
        else if (String.fromCharCode(charCode) === "E"){
            sendVelocityData(0,50);
        }
        else if (String.fromCharCode(charCode) === "W"){
            sendVelocityData(0,0, 50);
        }
    }
}

function pressedFastLeft(){
    //window.alert("Sent fast left");
    fastLeftOn = true;
    fastLeftLoop();
}

function fastLeftLoop(){
    setTimeout(function() {
        console.log('fast left');
        sendVelocityData(100,0);
        if (fastLeftOn) {
            fastLeftLoop();
        }
    }, velMsgTimeRes);
}

function releasedAll(){
    fastLeftOn = false;
    leftOn = false;
    rightOn = false;
    fastRightOn = false;
    forwardOn = false;
}

function pressedForward(){
    //window.alert("Sent fast left");
    forwardOn = true;
    forwardLoop();
}

function forwardLoop(){
    setTimeout(function() {
        console.log('forward');
        sendVelocityData(0,0, 100);
        if (forwardOn) {
            forwardLoop();
        }
    }, velMsgTimeRes);
}

function releasedForward(){
    forwardOn = false;
}

function pressedLeft(){
    //window.alert("Sent fast left");
    leftOn = true;
    leftLoop();
}

function leftLoop(){
    setTimeout(function() {
        console.log('left');
        sendVelocityData(50,0);
        if (leftOn) {
            leftLoop();
        }
    }, velMsgTimeRes);
}

function releasedLeft(){
    leftOn = false;
}

function pressedRight(){
    //window.alert("Sent fast left");
    rightOn = true;
    rightLoop();
}

function rightLoop(){
    setTimeout(function() {
        console.log('right');
        sendVelocityData(0,50);
        if (rightOn) {
            rightLoop();
        }
    }, velMsgTimeRes);
}

function releasedRight(){
    rightOn = false;
}

function pressedFastRight(){
    //window.alert("Sent fast left");
    fastRightOn = true;
    fastRightLoop()
}

function fastRightLoop(){
    setTimeout(function() {
        console.log('fast right');
        sendVelocityData(0,100);
        if (fastRightOn) {
            fastRightLoop();
        }
    }, velMsgTimeRes)
}

function releasedFastRight(){
    fastRightOn = false;
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
    var wider = map.prop("naturalHeight") < map.prop("naturalWidth");
    var widerer = (map.prop("naturalWidth")/map.prop("naturalHeight")) > 1.3;
    console.log("On resize " + onResize + " wider: " + wider + " widerer: " + widerer);

    var width = (window.innerWidth > 0) ? window.innerWidth : screen.width;
    var map_card = $("#map_card");
    var spacer = $("#main-spacer");
    var camera = $("#camera_img");
    var camera_card = $("#camera_card");
    var shout_card = $("#alarms-controls-gridLO");
    var padding = $("#mainGrid").css("padding");
    if (width > 1000 && !(wider && widerer)) {
        /* MANAGING MAP SIZE */
        map_card.css("height",(height - $("#main_header").height()*3));
        map.height(map_card.height() - $("#map_card_title").height());
        map_card.width(map.height() * (map.prop("naturalWidth") / map.prop("naturalHeight")));
        map.width(map_card.width());

        /*console.log("Checking screen height: " + screen.width);
        console.log("Checking height: " + height);
        console.log("Checking width: " + width);
        console.log("Checking header: " + $("#main_header").height());
        console.log("Checking height map_card: " + map_card.height());
        console.log("Checking height map: " + map.height());*/

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
        /*console.log("Checking max width camera: " + camera.css("max-width"));
        console.log("Checking height camera_card: " + camera_card.height());
        console.log("Checking height camera: " + camera.height());
        console.log("Checking width camera_card: " + camera_card.width());
        console.log("Checking width camera: " + camera.width());
        console.log("Checking height shout_card: " + shout_card.height());*/
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

function clickedAlarm(){
    var instructionBtn = $("#instructionBtn");
    var alarmBtn = $("#alarmBtn");
    var rotateBtn = $("#rotateBtn");

    instructionBtn.css("color",DARKCOL);
    alarmBtn.css("color",LIGHTCOL);
    rotateBtn.css("color",DARKCOL);
    instructionBtn.css("background-color",LIGHTCOL);
    alarmBtn.css("background-color",DARKCOL);
    rotateBtn.css("background-color",LIGHTCOL);

    $("#shout_card").css("visibility","visible");
    $("#instructionCard").css("visibility","hidden");
    $("#rotate_card").css("visibility","hidden");

    openMicrophone();
}

function clickedRotate(){
    var instructionBtn = $("#instructionBtn");
    var alarmBtn = $("#alarmBtn");
    var rotateBtn = $("#rotateBtn");

    instructionBtn.css("color",DARKCOL);
    alarmBtn.css("color",DARKCOL);
    rotateBtn.css("color",LIGHTCOL);
    instructionBtn.css("background-color",LIGHTCOL);
    alarmBtn.css("background-color",LIGHTCOL);
    rotateBtn.css("background-color",DARKCOL);

    $("#shout_card").css("visibility","hidden");
    $("#instructionCard").css("visibility","hidden");
    $("#rotate_card").css("visibility","visible");
}

function clickedInstruction(){
    var instructionBtn = $("#instructionBtn");
    var alarmBtn = $("#alarmBtn");
    var rotateBtn = $("#rotateBtn");

    instructionBtn.css("color",LIGHTCOL);
    alarmBtn.css("color",DARKCOL);
    rotateBtn.css("color",DARKCOL);
    instructionBtn.css("background-color",DARKCOL);
    alarmBtn.css("background-color",LIGHTCOL);
    rotateBtn.css("background-color",LIGHTCOL);

    $("#shout_card").css("visibility","hidden");
    $("#instructionCard").css("visibility","visible");
    $("#rotate_card").css("visibility","hidden");
}

function windowResized(){
    location.reload();
    resizeMap(true);
}
