
var host = "10.114.69.121:8090";

if (window.location.protocol == "https:") {
    var ws_scheme = "wss://";
} else {
    var ws_scheme = "ws://"
};

//var screen = new ReconnectingWebSocket(ws_scheme + host + "/screen");
var screen = new WebSocket(ws_scheme + host + "/screen");
screen.onmessage = function(msg) {
    console.log(msg)
}
screen.onclose = function() {
    console.log('closed');
}

document.querySelector('.btn').addEventListener('click', function (ev) {
    const txt = document.querySelector('.txt').value;
    screen.send(txt)
    console.time(txt);
});
