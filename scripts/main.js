function loadChat() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        document.getElementById("group-chat").innerHTML = this.responseText;
    }
    };
    xhttp.open("POST", "chat-history/chat-log.log", true);
    xhttp.send();
}

loadChat()
setInterval(loadChat, 3000);

function makeAddPostVisible() {
    var modal = document.getElementById("my-modal-post");
    var addPostButton = document.getElementById("add-post-button");
    modal.style.display = "block";
}

function makeModalPostInvisible() {
    var modal = document.getElementById("my-modal-post");
    var addPostButton = document.getElementById("add-post-button");
    modal.style.display = "none";
}

var menu = null, squeezeInterval = null;

var menu_x_scale = 10;
function squeezeMenu() {
    menu_x_scale -= 1;
    menu.style.width = menu_x_scale*10 + '%';
    if (menu_x_scale == 0.0) {
        menu.style.display = "none";
        clearInterval(squeezeInterval);
    }
}
function toggleMenu() {
    menu = document.getElementById("left-pane");
    if (menu.style.display == "none" || menu.style.display == "") {
        menu.style.width='96.5%';
        menu.style.display = "block";
        menu_x_scale = 10;
    } else {
        squeezeInterval = setInterval(squeezeMenu, 10);
    }
}