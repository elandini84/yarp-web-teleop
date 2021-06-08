let positionX = -1
let positionY = -1

function printMousePos(e) {
    $("#clickXTxt").html(positionX);
    $("#clickYTxt").html(positionY);
    //document.getElementById("example").innerHTML = "click x: " + positionX + ", y: " + positionY +  " button " + e.button;
    publish_msg(positionX, positionY, -1, -1)
    // click relative to image, for the siza we can get document.getElementById("image_raw").offsetHeight and document.getElementById("image_raw").offsetWidth
    // HERE I CAN SEND ROS OR YARP MESSAGES
}
function printDragMousePos(e) {
    var posX = $(this).offset().left
    var posY = $(this).offset().top;
    cursorX = e.pageX - posX;
    cursorY = e.pageY - posY;
    diffX = Math.abs(positionX - cursorX);
    diffY = Math.abs(positionY - cursorY);
    if (diffX < 5 && diffY < 5) 
    {
        printMousePos();
    } else 
    {
        $("#clickXTxt").html(positionX+" to "+cursorX);
        $("#clickYTxt").html(positionY+" to "+cursorY);
        //document.getElementById("example").innerHTML = "drag initial x: " + positionX + " initial y: " + positionY + " end x " + cursorX + " end y: " + cursorY + " button " + e.button;
        publish_msg(positionX, positionY, cursorX, cursorY)
        // click relative to image, for the siza we can get document.getElementById("image_raw").offsetHeight and document.getElementById("image_raw").offsetWidth
        // HERE I CAN SEND ROS OR YARP MESSAGES
    }
}
function simpleDown(event) {
    var posX = $(this).offset().left
    var posY = $(this).offset().top;
    positionX = e.pageX - posX;
    positionY = e.pageY - posY;
    drag = false;
}
function init() {
    //document.getElementById("image_raw").addEventListener("click", printMousePos);
    //document.getElementById("image_raw").addEventListener("drag", printMousePos);
    $("#camera_img").on("dragstart",function() { return false; });
    $("#camera_img").on("contextmenu",function() { return false; });
    //document.getElementById('camera_img').ondragstart = function() { return false; };
    //document.getElementById('camera_img').oncontextmenu = function() { return false; };

    let drag = false;

    $("#camera_img").mousedown(simpleDown(e));
    $("#camera_img").mousemove(function(){drag = true;});
    $("#camera_img").mousemove((e) => drag ? printDragMousePos(e) : printMousePos(e));
    //document.getElementById("camera_img").addEventListener('mousedown', (e) => {positionX = e.offsetX; positionY = e.offsetY, drag=false});
    //document.getElementById("camera_img").addEventListener('mousemove', (e) => drag = true);
    //document.getElementById("camera_img").addEventListener('mouseup', (e) => drag ? printDragMousePos(e) : printMousePos(e));
}