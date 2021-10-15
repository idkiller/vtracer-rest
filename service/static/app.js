
if (window.location.protocol == "https:") {
    var ws_scheme = "wss://";
} else {
    var ws_scheme = "ws://"
};

var screen = new ReconnectingWebSocket(ws_scheme + location.host + "/register");

screen.onopen = function() {
    screen.send('1234');
}

var contentsWrapper = document.querySelector('.contents-wrapper');

screen.onmessage = function(msg) {
    contentsWrapper.innerHTML = msg.data;
    let svg = contentsWrapper.firstChild;
    let snap = Snap(svg)
    snap.attr({width: '100%', height: '100%', preserveAspectRatio: 'none'});
    document.body.style.backgroundColor = 'black';
}
screen.onclose = function() {
    console.log('closed');
    screen = new WebSocket(screen.url);
}
