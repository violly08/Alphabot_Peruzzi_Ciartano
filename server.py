from flask import Flask, jsonify, render_template_string
from libreria import AlphaBot

app = Flask(__name__)
Ab = AlphaBot(speed=50)

HTML = """
<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>AlphaBot</title>
  <style>
    body {
      font-family: sans-serif;
      background: #f0f0f0;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      min-height: 100vh;
      margin: 0;
    }
    h1 { margin-bottom: 20px; font-size: 1.4rem; color: #333; }
    .speed-box {
      margin-bottom: 20px;
      text-align: center;
      font-size: 1rem;
      color: #333;
    }
    .speed-box span { font-size: 1.4rem; font-weight: bold; }
    .dpad {
      display: grid;
      grid-template-columns: repeat(3, 70px);
      grid-template-rows: repeat(3, 70px);
      gap: 8px;
      margin-bottom: 20px;
    }
    .btn {
      width: 70px; height: 70px;
      font-size: 1.5rem;
      border: none; border-radius: 10px;
      background: #fff;
      box-shadow: 0 2px 6px rgba(0,0,0,0.15);
      cursor: pointer;
      display: flex; align-items: center; justify-content: center;
    }
    .btn:active, .btn.active { background: #ddd; box-shadow: inset 0 2px 4px rgba(0,0,0,0.15); }
    .btn-stop { background: #ffdddd; }
    .btn-stop:active, .btn-stop.active { background: #ffbbbb; }
    .empty { visibility: hidden; }
    .hint { font-size: 0.75rem; color: #888; text-align: center; }
    .speed-btns { display: inline-flex; gap: 6px; margin-left: 8px; }
    .sbtn {
      width: 36px; height: 36px; font-size: 1.1rem;
      border: none; border-radius: 8px;
      background: #fff; box-shadow: 0 2px 4px rgba(0,0,0,0.12);
      cursor: pointer; display: flex; align-items: center; justify-content: center;
    }
    .sbtn:active { background: #ddd; }
  </style>
</head>
<body>

  <h1>AlphaBot</h1>

  <div class="speed-box">
    Velocità: <span id="spd">50</span>%
    <div class="speed-btns">
      <button class="sbtn" onclick="sendSpeed('up')">+</button>
      <button class="sbtn" onclick="sendSpeed('down')">−</button>
    </div>
  </div>

  <div class="dpad">
    <div class="empty"></div>
    <button class="btn" id="btn-w" data-cmd="w">▲</button>
    <div class="empty"></div>

    <button class="btn" id="btn-a" data-cmd="a">◀</button>
    <button class="btn btn-stop" id="btn-stop" data-cmd="stop">■</button>
    <button class="btn" id="btn-d" data-cmd="d">▶</button>

    <div class="empty"></div>
    <button class="btn" id="btn-s" data-cmd="s">▼</button>
    <div class="empty"></div>
  </div>

  <p class="hint">WASD per muoversi &nbsp;|&nbsp; E / R per la velocità &nbsp;|&nbsp; Spazio per stop</p>

<script>
  function send(cmd) {
    fetch('/move/' + cmd).catch(() => {});
    document.querySelectorAll('.btn').forEach(b => b.classList.remove('active'));
    const btn = document.querySelector('[data-cmd="' + cmd + '"]');
    if (btn) btn.classList.add('active');
  }

  function sendSpeed(action) {
    fetch('/speed/' + action)
      .then(r => r.json())
      .then(d => { document.getElementById('spd').textContent = d.speed; })
      .catch(() => {});
  }

  const pressed = new Set();

  document.addEventListener('keydown', e => {
    const k = e.key.toLowerCase();
    if (pressed.has(k)) return;
    pressed.add(k);
    if (k === 'w') send('w');
    else if (k === 's') send('s');
    else if (k === 'a') send('a');
    else if (k === 'd') send('d');
    else if (k === ' ') { e.preventDefault(); send('stop'); }
    else if (k === 'e') sendSpeed('up');
    else if (k === 'r') sendSpeed('down');
  });

  document.addEventListener('keyup', e => {
    const k = e.key.toLowerCase();
    pressed.delete(k);
    if (['w', 'a', 's', 'd'].includes(k)) {
      send('stop');
      document.querySelectorAll('.btn').forEach(b => b.classList.remove('active'));
    }
  });

  document.querySelectorAll('.btn').forEach(btn => {
    const cmd = btn.dataset.cmd;
    btn.addEventListener('mousedown', () => send(cmd));
    btn.addEventListener('mouseup', () => {
      if (cmd !== 'stop') {
        send('stop');
        document.querySelectorAll('.btn').forEach(b => b.classList.remove('active'));
      }
    });
    btn.addEventListener('mouseleave', () => {
      if (cmd !== 'stop' && btn.classList.contains('active')) {
        send('stop');
        btn.classList.remove('active');
      }
    });
    btn.addEventListener('touchstart', e => { e.preventDefault(); send(cmd); });
    btn.addEventListener('touchend', e => {
      e.preventDefault();
      if (cmd !== 'stop') {
        send('stop');
        document.querySelectorAll('.btn').forEach(b => b.classList.remove('active'));
      }
    });
  });
</script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/move/<direction>")
def move(direction):
    actions = {
        "w": Ab.forward,
        "s": Ab.backward,
        "a": Ab.left,
        "d": Ab.right,
        "stop": Ab.stop,
    }
    fn = actions.get(direction)
    if fn:
        fn()
    return "OK"

@app.route("/speed/<action>")
def speed(action):
    if action == "up":
        Ab.increase_speed(10)
    elif action == "down":
        Ab.decrease_speed(10)
    return jsonify(speed=Ab.speed)

if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)
    finally:
        Ab.cleanup()
