
if (window.location.protocol == "https:") {
    var ws_scheme = "wss://";
} else {
    var ws_scheme = "ws://"
};

var ws = new ReconnectingWebSocket(ws_scheme + location.host + "/register");

ws.onopen = function() {
    ws.send('1234');
}

var contentsWrapper = document.querySelector('.contents-wrapper');

ws.onmessage = function(msg) {
    let txt = msg.data;
    // dirty cache buster start
    const re = /([^\/]+\.gif)/g
    txt = txt.replace(re, `$1?dummy=${Math.random()}`)
    // dirty cache buster end
    contentsWrapper.innerHTML = txt;
    let svg = contentsWrapper.firstChild;
    let snap = Snap(svg)
    snap.attr({width: '100%', height: '100%', preserveAspectRatio: 'none', style: 'background-color:black'});
}
ws.onclose = function() {
    console.log('closed');
    ws = new WebSocket(ws.url);
}
