var Nolida = window.nolida.default

if (window.location.protocol == "https:") {
    var ws_scheme = "wss://";
} else {
    var ws_scheme = "ws://"
};

var ws = new ReconnectingWebSocket(ws_scheme + location.host + "/register");

ws.onopen = function () {
    ws.send('1234');
}

var contentsWrapper = document.querySelector('.contents-wrapper');
var canvas = document.querySelector('.physics-canvas')

let engine = Matter.Engine.create()
let render = Matter.Render.create({
    canvas: canvas,
    engine: engine,
    options: {
        background: 'transparent',
        wireframeBackground: 'rgba(0, 0, 0, 0.2)',
        wireframes: false
    }
})

Matter.Render.run(render)
let runner = Matter.Runner.create()
Matter.Runner.run(runner, engine)
Matter.Events.on(render, 'afterRender', Nolida.OnContents)

var globalObjIds = []

ws.onmessage = function (msg) {
    let json = JSON.parse(msg.data)
    var svgTxt = json.svg
    // dirty cache buster start
    const re = /([^\/]+\.gif)/g
    svgTxt = svgTxt.replace(re, `$1?dummy=${Math.random()}`)
    // dirty cache buster end
    contentsWrapper.innerHTML = svgTxt;
    let svg = contentsWrapper.firstChild;
    let snap = Snap(svg)
    snap.attr({ width: '100%', height: '100%', preserveAspectRatio: 'none', style: 'background-color:black' });

    const styles = json.css
    for (let name in styles) {
        const css = styles[name]
        if (!document.head.querySelector(`style[data-name="${name}"]`)) {
            const style = document.createElement('style')
            style.setAttribute('type', 'text/css')
            style.dataset.name = name
            style.innerHTML = css
            document.head.appendChild(style)
        }
    }

    let box = svg.viewBox.baseVal
    canvas.width = box.width
    canvas.height = box.height
    render.options.width = box.width
    render.options.height = box.height

    // clean previous objects
    globalObjIds.forEach(id => Nolida.removePhysicsGlobalContents(id))
    Matter.Composite.clear(engine.world, false)

    const cd = json.nolida
    for (let i = 0; i < cd.lands.length; i++) {
        const land = cd.lands[i]
        const obj = Nolida.createComposite(land.x, land.y, land.vertices, {
            isStatic: true,
            render: {
                opacity: 0
            }
        })
        Matter.Composite.add(engine.world, obj)
    }

    for (let i = 0; i < cd.worldObjects.length; i++) {
        const objId = Nolida.makePhysicsGlobalContents(engine, box.width, box.height, cd.worldObjects[i])
        globalObjIds.push(objId)
    }
}
ws.onclose = function () {
    console.log('closed');

    ws = new WebSocket(ws.url);
}
