import streamlit as st
import streamlit.components.v1 as components
import json
import random
import datetime
import requests
import time as time_module


def send_ntfy(topic: str, title: str, message: str, tags: list = None, priority: str = "default") -> bool:
    """Send a push notification via ntfy.sh — completely free, no auth needed."""
    try:
        headers = {
            "Title": title,
            "Priority": priority,
            "Tags": ",".join(tags) if tags else "bell",
        }
        response = requests.post(
            f"https://ntfy.sh/{topic}",
            data=message.encode("utf-8"),
            headers=headers,
            timeout=10
        )
        return response.status_code == 200
    except Exception:
        return False

st.set_page_config(
    page_title="ML Engineer Roadmap — 6 Months to Tier-1",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@keyframes aurora1 {
    0%,100% { transform: translate(0,0) scale(1); opacity: 0.5; }
    50%      { transform: translate(80px,-60px) scale(1.1); opacity: 0.7; }
}
@keyframes aurora2 {
    0%,100% { transform: translate(0,0) scale(1); opacity: 0.4; }
    50%      { transform: translate(-60px,80px) scale(1.08); opacity: 0.6; }
}
@keyframes aurora3 {
    0%,100% { transform: translate(0,0) scale(1); opacity: 0.35; }
    50%      { transform: translate(50px,50px) scale(1.05); opacity: 0.55; }
}

.bg-blob {
    position: fixed;
    border-radius: 50%;
    filter: blur(80px);
    pointer-events: none !important;
    z-index: 0;
}
#b1 { width:600px; height:500px; top:-100px; left:-100px;
      background:radial-gradient(ellipse, rgba(93,202,165,0.12), transparent 70%);
      animation: aurora1 20s ease-in-out infinite;
      pointer-events: none !important; }
#b2 { width:700px; height:600px; top:30vh; right:-150px;
      background:radial-gradient(ellipse, rgba(55,138,221,0.1), transparent 70%);
      animation: aurora2 25s ease-in-out infinite;
      pointer-events: none !important; }
#b3 { width:650px; height:500px; bottom:-100px; left:30vw;
      background:radial-gradient(ellipse, rgba(127,119,221,0.09), transparent 70%);
      animation: aurora3 22s ease-in-out infinite;
      pointer-events: none !important; }

.stApp { background: #020810 !important; }
section[data-testid="stSidebar"] {
    background: rgba(2,8,16,0.95) !important;
    backdrop-filter: blur(12px) !important;
    border-right: 1px solid rgba(93,202,165,0.1) !important;
}
header[data-testid="stHeader"] {
    background: rgba(2,8,16,0.8) !important;
    backdrop-filter: blur(8px) !important;
}
.main .block-container {
    position: relative !important;
    z-index: 2 !important;
    background: transparent !important;
}
</style>
<div class="bg-blob" id="b1"></div>
<div class="bg-blob" id="b2"></div>
<div class="bg-blob" id="b3"></div>
""", unsafe_allow_html=True)

def render_animated_background():
    st.markdown("""
    <style>
    .stApp { background: #020810 !important; }
    section[data-testid="stSidebar"] { background: #020810 !important; border-right: 1px solid #0d2137 !important; }
    .main .block-container { position: relative; z-index: 1; }
    header[data-testid="stHeader"] { background: transparent !important; }
    </style>
    """, unsafe_allow_html=True)

    components.html("""
<!DOCTYPE html>
<html>
<head>
<style>
* { margin:0; padding:0; }
html, body { width:100%; height:100%; background:transparent; overflow:hidden; }
canvas { position:fixed; top:0; left:0; width:100vw; height:100vh; }
</style>
</head>
<body>
<canvas id="c"></canvas>
<script>
const canvas = document.getElementById('c');
const ctx = canvas.getContext('2d');
let W, H;

function resize() {
    W = canvas.width = window.innerWidth;
    H = canvas.height = window.innerHeight;
}
resize();
window.addEventListener('resize', resize);

const COLORS = {
    bg: '#020810',
    nodeCore: '#5DCAA5',
    nodeGlow: 'rgba(93,202,165,',
    edgePrimary: 'rgba(55,138,221,',
    edgeSecondary: 'rgba(93,202,165,',
    particle: 'rgba(127,119,221,',
    pulse: 'rgba(93,202,165,',
    hub: '#378ADD',
    hubGlow: 'rgba(55,138,221,'
};

const NODE_COUNT = 55;
const HUB_COUNT = 6;

class Node {
    constructor(isHub = false) {
        this.x = Math.random() * W;
        this.y = Math.random() * H;
        this.vx = (Math.random() - 0.5) * (isHub ? 0.2 : 0.38);
        this.vy = (Math.random() - 0.5) * (isHub ? 0.2 : 0.38);
        this.isHub = isHub;
        this.r = isHub ? Math.random() * 4 + 5 : Math.random() * 2 + 1.5;
        this.baseR = this.r;
        this.phase = Math.random() * Math.PI * 2;
        this.speed = Math.random() * 0.02 + 0.008;
        this.pulseAmp = isHub ? 3 : 1.2;
        this.alpha = Math.random() * 0.4 + 0.6;
    }
    update(t) {
        this.x += this.vx;
        this.y += this.vy;
        if (this.x < -50) this.x = W + 50;
        if (this.x > W + 50) this.x = -50;
        if (this.y < -50) this.y = H + 50;
        if (this.y > H + 50) this.y = -50;
        this.r = this.baseR + Math.sin(t * this.speed + this.phase) * this.pulseAmp;
    }
    draw(ctx) {
        const glowSize = this.r * (this.isHub ? 5 : 3.5);
        const grad = ctx.createRadialGradient(this.x, this.y, 0, this.x, this.y, glowSize);
        const col = this.isHub ? COLORS.hubGlow : COLORS.nodeGlow;
        grad.addColorStop(0, col + (this.isHub ? '0.35)' : '0.25)'));
        grad.addColorStop(0.4, col + '0.08)');
        grad.addColorStop(1, col + '0)');
        ctx.fillStyle = grad;
        ctx.beginPath();
        ctx.arc(this.x, this.y, glowSize, 0, Math.PI * 2);
        ctx.fill();

        ctx.beginPath();
        ctx.arc(this.x, this.y, this.r, 0, Math.PI * 2);
        ctx.fillStyle = this.isHub ? COLORS.hub : COLORS.nodeCore;
        ctx.globalAlpha = this.alpha;
        ctx.fill();
        ctx.globalAlpha = 1;

        if (this.isHub) {
            ctx.beginPath();
            ctx.arc(this.x - this.r * 0.3, this.y - this.r * 0.3, this.r * 0.35, 0, Math.PI * 2);
            ctx.fillStyle = 'rgba(200,240,255,0.6)';
            ctx.fill();
        }
    }
}

class Particle {
    constructor(from, to) {
        this.from = from;
        this.to = to;
        this.t = Math.random();
        this.speed = Math.random() * 0.004 + 0.002;
        this.size = Math.random() * 2 + 1;
        this.alpha = Math.random() * 0.7 + 0.3;
        this.color = Math.random() > 0.5 ? COLORS.particle : COLORS.edgePrimary;
    }
    update() { this.t += this.speed; if (this.t > 1) this.t = 0; }
    draw(ctx) {
        const x = this.from.x + (this.to.x - this.from.x) * this.t;
        const y = this.from.y + (this.to.y - this.from.y) * this.t;
        ctx.beginPath();
        ctx.arc(x, y, this.size, 0, Math.PI * 2);
        ctx.fillStyle = this.color + this.alpha + ')';
        ctx.fill();
    }
}

class PulseRing {
    constructor(x, y) {
        this.x = x; this.y = y;
        this.r = 0;
        this.maxR = Math.random() * 80 + 60;
        this.speed = Math.random() * 0.8 + 0.4;
        this.alpha = 0.5;
        this.done = false;
    }
    update() {
        this.r += this.speed;
        this.alpha = 0.5 * (1 - this.r / this.maxR);
        if (this.r >= this.maxR) this.done = true;
    }
    draw(ctx) {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.r, 0, Math.PI * 2);
        ctx.strokeStyle = COLORS.pulse + this.alpha + ')';
        ctx.lineWidth = 1.5;
        ctx.stroke();
    }
}

const nodes = [];
for (let i = 0; i < HUB_COUNT; i++) nodes.push(new Node(true));
for (let i = 0; i < NODE_COUNT - HUB_COUNT; i++) nodes.push(new Node(false));

const MAX_DIST = 180;
const MAX_HUB_DIST = 280;
const particles = [];
const pulseRings = [];

function refreshParticles() {
    particles.length = 0;
    for (let i = 0; i < nodes.length; i++) {
        for (let j = i + 1; j < nodes.length; j++) {
            const ni = nodes[i], nj = nodes[j];
            const dx = ni.x - nj.x, dy = ni.y - nj.y;
            const d = Math.sqrt(dx*dx + dy*dy);
            const maxD = (ni.isHub || nj.isHub) ? MAX_HUB_DIST : MAX_DIST;
            if (d < maxD && (ni.isHub || nj.isHub)) {
                if (Math.random() > 0.4) particles.push(new Particle(ni, nj));
            }
        }
    }
}
refreshParticles();
setInterval(refreshParticles, 4000);

setInterval(() => {
    const hub = nodes[Math.floor(Math.random() * HUB_COUNT)];
    pulseRings.push(new PulseRing(hub.x, hub.y));
}, 1200);

let frame = 0;
function draw() {
    frame++;
    ctx.fillStyle = 'rgba(2,8,16,0.18)';
    ctx.fillRect(0, 0, W, H);

    for (let i = pulseRings.length - 1; i >= 0; i--) {
        pulseRings[i].update();
        pulseRings[i].draw(ctx);
        if (pulseRings[i].done) pulseRings.splice(i, 1);
    }

    for (let i = 0; i < nodes.length; i++) {
        for (let j = i + 1; j < nodes.length; j++) {
            const ni = nodes[i], nj = nodes[j];
            const dx = ni.x - nj.x, dy = ni.y - nj.y;
            const d = Math.sqrt(dx*dx + dy*dy);
            const maxD = (ni.isHub || nj.isHub) ? MAX_HUB_DIST : MAX_DIST;
            if (d < maxD) {
                const alpha = (1 - d / maxD) * (ni.isHub || nj.isHub ? 0.55 : 0.22);
                const isHubEdge = ni.isHub || nj.isHub;
                ctx.strokeStyle = (isHubEdge ? COLORS.edgePrimary : COLORS.edgeSecondary) + alpha + ')';
                ctx.lineWidth = isHubEdge ? 1.2 : 0.6;
                ctx.beginPath();
                ctx.moveTo(ni.x, ni.y);
                ctx.lineTo(nj.x, nj.y);
                ctx.stroke();
            }
        }
    }

    particles.forEach(p => { p.update(); p.draw(ctx); });

    nodes.sort((a,b) => a.isHub - b.isHub);
    nodes.forEach(n => { n.update(frame); n.draw(ctx); });

    requestAnimationFrame(draw);
}
draw();
</script>
</body>
</html>
    """, height=1, scrolling=False)

    st.markdown("""
<style>
iframe {
    border: none !important;
}

div[data-testid="stIFrame"]:first-of-type iframe,
div.stHtml iframe:first-of-type,
[data-testid="stMain"] iframe:first-of-type {
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    width: 100vw !important;
    height: 100vh !important;
    z-index: 0 !important;
    pointer-events: none !important;
    margin: 0 !important;
    padding: 0 !important;
    border: none !important;
    max-width: none !important;
    max-height: none !important;
}

div[data-testid="stIFrame"]:first-of-type,
div.stHtml:first-of-type {
    height: 0 !important;
    min-height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
    overflow: visible !important;
}

.main .block-container {
    position: relative !important;
    z-index: 2 !important;
    background: transparent !important;
}

section[data-testid="stSidebar"] {
    z-index: 10 !important;
    background: rgba(2, 8, 16, 0.85) !important;
    backdrop-filter: blur(10px) !important;
}

header[data-testid="stHeader"] {
    z-index: 10 !important;
    background: rgba(2, 8, 16, 0.7) !important;
    backdrop-filter: blur(8px) !important;
}

.stApp {
    background: #020810 !important;
}
</style>
""", unsafe_allow_html=True)

def render_floating_chatbot():
    groq_key = ""
    try:
        groq_key = st.secrets.get("GROQ_API_KEY", "")
    except:
        pass

    st.markdown('<div id="chatbot-wrapper"></div>', unsafe_allow_html=True)
    components.html(f"""
    <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ background: transparent; overflow: hidden; pointer-events: all; font-family: -apple-system, sans-serif; }}

    #bubble {{
        position: fixed;
        bottom: 24px; right: 24px;
        width: 52px; height: 52px;
        border-radius: 50%;
        background: linear-gradient(135deg, #5DCAA5 0%, #378ADD 100%);
        display: flex; align-items: center; justify-content: center;
        cursor: pointer;
        box-shadow: 0 4px 24px rgba(93,202,165,0.45);
        transition: transform .2s, box-shadow .2s;
        z-index: 999;
    }}
    #bubble:hover {{ transform: scale(1.1); box-shadow: 0 6px 32px rgba(93,202,165,0.65); }}
    #bubble svg {{ width: 24px; height: 24px; fill: white; }}

    #win {{
        position: fixed;
        bottom: 86px; right: 24px;
        width: 340px; height: 480px;
        background: #161B22;
        border: 1px solid #30363D;
        border-radius: 14px;
        display: none; flex-direction: column;
        box-shadow: 0 8px 40px rgba(0,0,0,0.6);
        z-index: 998;
        overflow: hidden;
    }}
    #win.open {{ display: flex; }}

    #hdr {{
        padding: 12px 14px;
        background: #0D1117;
        border-bottom: 1px solid #21262D;
        display: flex; align-items: center; justify-content: space-between;
        flex-shrink: 0;
    }}
    .hdr-l {{ display: flex; align-items: center; gap: 9px; }}
    .av {{
        width: 30px; height: 30px; border-radius: 50%;
        background: linear-gradient(135deg, #5DCAA5, #378ADD);
        display: flex; align-items: center; justify-content: center;
        font-size: 14px;
    }}
    .ttl {{ color: #E6EDF3; font-size: 13px; font-weight: 600; }}
    .sub {{ color: #7D8590; font-size: 10px; }}
    .cls {{ color: #7D8590; cursor: pointer; font-size: 18px; padding: 2px 6px; border-radius: 4px; }}
    .cls:hover {{ color: #E6EDF3; background: #21262D; }}

    #msgs {{
        flex: 1; overflow-y: auto; padding: 12px;
        display: flex; flex-direction: column; gap: 8px;
        scrollbar-width: thin; scrollbar-color: #30363D transparent;
    }}
    .m {{
        max-width: 86%; padding: 8px 12px; border-radius: 10px;
        font-size: 12.5px; line-height: 1.5; word-wrap: break-word;
    }}
    .m.u {{
        background: #1F6FEB22; border: 1px solid #1F6FEB44;
        color: #E6EDF3; align-self: flex-end; border-bottom-right-radius: 3px;
    }}
    .m.b {{
        background: #21262D; border: 1px solid #30363D;
        color: #C9D1D9; align-self: flex-start; border-bottom-left-radius: 3px;
    }}
    .m.t {{ color: #7D8590; font-style: italic; }}

    .qw {{ display: flex; flex-wrap: wrap; gap: 5px; padding: 0 12px 8px; flex-shrink: 0; }}
    .qb {{
        font-size: 10.5px; padding: 3px 9px;
        background: #21262D; border: 1px solid #30363D;
        border-radius: 99px; color: #8B949E; cursor: pointer;
        transition: all .15s; white-space: nowrap;
    }}
    .qb:hover {{ background: #2D333B; color: #E6EDF3; border-color: #5DCAA5; }}

    #inp-area {{
        padding: 10px 12px; border-top: 1px solid #21262D;
        display: flex; gap: 7px; flex-shrink: 0; background: #0D1117;
    }}
    #inp {{
        flex: 1; background: #21262D; border: 1px solid #30363D;
        border-radius: 7px; color: #E6EDF3; padding: 7px 11px;
        font-size: 12px; outline: none; resize: none; height: 36px;
    }}
    #inp:focus {{ border-color: #5DCAA5; }}
    #inp::placeholder {{ color: #7D8590; }}
    #snd {{
        width: 36px; height: 36px; border-radius: 7px;
        background: linear-gradient(135deg, #5DCAA5, #378ADD);
        border: none; cursor: pointer;
        display: flex; align-items: center; justify-content: center; flex-shrink: 0;
    }}
    #snd:hover {{ opacity: 0.85; }}
    #snd svg {{ width: 15px; height: 15px; fill: white; }}
    </style>

    <div id="bubble" onclick="toggle()">
        <svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.03 2 11c0 2.7 1.26 5.12 3.28 6.79L4 22l4.5-1.96C9.6 20.65 10.77 21 12 21c5.52 0 10-4.03 10-9S17.52 2 12 2z"/></svg>
    </div>

    <div id="win">
        <div id="hdr">
            <div class="hdr-l">
                <div class="av">🧠</div>
                <div><div class="ttl">ML Mentor</div><div class="sub">Roadmap-scoped · llama-3.3-70b</div></div>
            </div>
            <div class="cls" onclick="toggle()">×</div>
        </div>
        <div id="msgs">
            <div class="m b">Hey! Ask me about any concept, project, or resource in the roadmap 👋</div>
        </div>
        <div class="qw" id="qw">
            <span class="qb" onclick="sq('Explain LoRA mathematically')">LoRA math</span>
            <span class="qb" onclick="sq('What to do in week 1?')">Week 1</span>
            <span class="qb" onclick="sq('Walk me through tabular-baseline')">tabular-baseline</span>
            <span class="qb" onclick="sq('Explain KV cache')">KV cache</span>
            <span class="qb" onclick="sq('Quiz me on attention')">Quiz me</span>
        </div>
        <div id="inp-area">
            <textarea id="inp" placeholder="Ask your ML mentor..."></textarea>
            <button id="snd" onclick="send()">
                <svg viewBox="0 0 24 24"><path d="M2 21l21-9L2 3v7l15 2-15 2v7z"/></svg>
            </button>
        </div>
    </div>

    <script>
    const KEY = "{groq_key}";
    const SYS = `You are an ML roadmap mentor. ONLY answer questions about this 6-month ML Engineer Roadmap. Refuse anything outside it with: "I'm your roadmap mentor — ask me about the ML roadmap topics only!"

Roadmap: Math (linear algebra, calculus, probability), Python ML toolchain (numpy, pandas, sklearn, mlflow, wandb), Classical ML (regression, trees, XGBoost, LightGBM, clustering, PCA), Neural nets + PyTorch (backprop, optimizers, training loop, DataLoader, checkpoints), Deep Learning (CNNs ResNet EfficientNet, LSTMs, Transformers self-attention multi-head RoPE ALiBi, ViT, Diffusion DDPM), Training at scale (mixed precision bf16 fp16, DDP FSDP DeepSpeed ZeRO, Accelerate), NLP + HuggingFace (BPE tokenization, AutoModel AutoTokenizer, peft LoRA QLoRA, trl SFT DPO GRPO), RAG (chunking, qdrant vector DB, hybrid BM25+dense, reranking, ragas eval), LLM internals (Flash Attention, KV cache, quantization GPTQ AWQ GGUF, speculative decoding), vllm serving, MLOps (DVC mlflow drift Evidently Langfuse), Agents (LangGraph MCP tool-calling guardrails). Projects: tabular-baseline, mnist-from-scratch-then-torch, rag-on-your-docs, qlora-domain-tune, prod-llm-platform, agent-with-evals. Be concise (under 250 words), practical, use short code examples.`;

    let msgs = [];
    let open = false;

    function toggle() {{
        open = !open;
        document.getElementById('win').classList.toggle('open', open);
        if (open) document.getElementById('inp').focus();
    }}

    function sq(t) {{ document.getElementById('inp').value = t; send(); }}

    function send() {{
        const inp = document.getElementById('inp');
        const txt = inp.value.trim();
        if (!txt) return;
        inp.value = '';
        add(txt, 'u');
        msgs.push({{role:'user', content:txt}});
        document.getElementById('qw').style.display = 'none';
        const th = add('Thinking...', 'b t');
        if (!KEY) {{ th.remove(); add('⚠️ No GROQ_API_KEY in Streamlit secrets.', 'b'); return; }}
        fetch('https://api.groq.com/openai/v1/chat/completions', {{
            method:'POST',
            headers:{{'Content-Type':'application/json','Authorization':'Bearer '+KEY}},
            body:JSON.stringify({{model:'llama-3.3-70b-versatile', max_tokens:500,
                messages:[{{role:'system',content:SYS}},...msgs]}})
        }})
        .then(r=>r.json())
        .then(d=>{{
            th.remove();
            const rep = d.choices?.[0]?.message?.content || 'Sorry, something went wrong.';
            add(rep,'b');
            msgs.push({{role:'assistant',content:rep}});
        }})
        .catch(()=>{{ th.remove(); add('Network error.','b'); }});
    }}

    function add(txt, cls) {{
        const el = document.createElement('div');
        el.className = 'm '+cls;
        el.textContent = txt;
        const c = document.getElementById('msgs');
        c.appendChild(el);
        c.scrollTop = c.scrollHeight;
        return el;
    }}

    document.getElementById('inp').addEventListener('keydown', e=>{{
        if (e.key==='Enter' && !e.shiftKey) {{ e.preventDefault(); send(); }}
    }});
    // Make sure this iframe marks itself as interactive
    document.documentElement.style.pointerEvents = 'all';
    document.body.style.pointerEvents = 'all';
    </script>
    """, height=1, scrolling=False)

    st.markdown("""
<style>
/* Target by position — the very last iframe on the page */
iframe[title="st.iframe"] {
    position: fixed !important;
    bottom: 0 !important;
    right: 0 !important;
    top: auto !important;
    left: auto !important;
    width: 420px !important;
    height: 570px !important;
    z-index: 99999 !important;
    border: none !important;
    pointer-events: all !important;
    background: transparent !important;
    display: block !important;
    visibility: visible !important;
    opacity: 1 !important;
}

/* The container holding the chatbot iframe */
#chatbot-wrapper + div,
#chatbot-wrapper ~ div {
    height: 0 !important;
    overflow: visible !important;
    margin: 0 !important;
    padding: 0 !important;
}

/* CRITICAL — make sure NOTHING has pointer-events that covers bottom-right */
.bg-blob, #b1, #b2, #b3,
.stApp::before, .stApp::after {
    pointer-events: none !important;
}

/* Everything else normal z-index */
.main .block-container { z-index: 2 !important; }
section[data-testid="stSidebar"] { z-index: 50 !important; }
header[data-testid="stHeader"] { z-index: 50 !important; }
</style>
""", unsafe_allow_html=True)

render_animated_background()
render_floating_chatbot()

# Collapse containers holding both iframes so they take zero layout space
st.markdown("""
<style>
section[data-testid="stMain"] .block-container > div > div:nth-child(1),
section[data-testid="stMain"] .block-container > div > div:nth-child(2) {
    height: 0 !important;
    min-height: 0 !important;
    overflow: visible !important;
    margin: 0 !important;
    padding: 0 !important;
}
section[data-testid="stMain"] .block-container > div > div:nth-child(1) iframe,
section[data-testid="stMain"] .block-container > div > div:nth-child(2) iframe {
    margin: 0 !important;
    padding: 0 !important;
}
</style>
""", unsafe_allow_html=True)

# ── First-load toast ──────────────────────────────────────────────────────────
if "welcomed" not in st.session_state:
    st.session_state.welcomed = True
    st.toast("Welcome back! Keep pushing — consistency beats intensity. 🚀")

# ── Persist checkboxes across rerenders ──────────────────────────────────────
if "checked" not in st.session_state:
    st.session_state.checked = {}

if "messages" not in st.session_state:
    st.session_state.messages = []

def toggle(key):
    st.session_state.checked[key] = not st.session_state.checked.get(key, False)

def is_checked(key):
    return st.session_state.checked.get(key, False)

# ── Data ─────────────────────────────────────────────────────────────────────
ROADMAP = {
    "beginner": {
        "label": "Beginner",
        "months": "Months 1–2",
        "hours": "~176 hrs (22h/week)",
        "color": "#0F6E56",
        "bg": "#E1F5EE",
        "sections": [
            {
                "name": "Math Foundations",
                "topics": [
                    {
                        "name": "Linear algebra, analytic geometry — vectors, matrices, decompositions",
                        "sub": "Chapters 2, 3 of MML book",
                        "res_type": "BOOK",
                        "res_name": "Mathematics for Machine Learning (Deisenroth et al.)",
                        "res_desc": "Free PDF, canonical reference",
                        "res_url": "https://mml-book.github.io",
                    },
                    {
                        "name": "Probability, distributions, Bayes theorem",
                        "sub": "Chapter 6 of MML book",
                        "res_type": "BOOK",
                        "res_name": "Mathematics for Machine Learning — Ch.6",
                        "res_desc": "Free PDF, do every 3rd exercise",
                        "res_url": "https://mml-book.github.io",
                    },
                    {
                        "name": "Vector calculus — gradients, chain rule, Jacobians",
                        "sub": "Chapter 5 of MML book",
                        "res_type": "BOOK",
                        "res_name": "Mathematics for Machine Learning — Ch.5",
                        "res_desc": "Foundation for backprop",
                        "res_url": "https://mml-book.github.io",
                    },
                    {
                        "name": "Matrix decompositions — SVD, eigendecomposition",
                        "sub": "Chapter 4 of MML book",
                        "res_type": "BOOK",
                        "res_name": "Mathematics for Machine Learning — Ch.4",
                        "res_desc": "Core of PCA and many ML algorithms",
                        "res_url": "https://mml-book.github.io",
                    },
                ],
            },
            {
                "name": "Production Python",
                "topics": [
                    {
                        "name": "Python production patterns — type hints, async, data model",
                        "sub": "Chapters 1, 7, 8, 17",
                        "res_type": "BOOK",
                        "res_name": "Fluent Python 2nd ed. (Luciano Ramalho)",
                        "res_desc": "Best Python internals book",
                        "res_url": "https://www.oreilly.com/library/view/fluent-python-2nd/9781492056348/",
                    },
                    {
                        "name": "uv, Ruff, pre-commit, pytest, pyproject.toml",
                        "sub": "Replace conda+pip+requirements.txt entirely",
                        "res_type": "DOCS",
                        "res_name": "uv official docs",
                        "res_desc": "Fastest Python package manager 2025",
                        "res_url": "https://docs.astral.sh/uv/",
                    },
                    {
                        "name": "SQL — window functions, CTEs, joins on real schemas",
                        "sub": "50 problems on StrataScratch",
                        "res_type": "WEB",
                        "res_name": "StrataScratch SQL problems",
                        "res_desc": "Real company interview SQL questions",
                        "res_url": "https://www.stratascratch.com",
                    },
                    {
                        "name": "Git at depth — forked-branch workflow, atomic PRs",
                        "sub": "Write 3 PRs against your own repos",
                        "res_type": "WEB",
                        "res_name": "Atlassian Advanced Git Tutorial",
                        "res_desc": "Rebasing, merging, branching strategies",
                        "res_url": "https://www.atlassian.com/git/tutorials/advanced-overview",
                    },
                    {
                        "name": "GitHub Actions CI — hello world pipeline",
                        "sub": "Push everything to yourname-ai org",
                        "res_type": "DOCS",
                        "res_name": "GitHub Actions quickstart",
                        "res_desc": "Official, fastest way to learn CI",
                        "res_url": "https://docs.github.com/en/actions/quickstart",
                    },
                ],
            },
            {
                "name": "ML Fundamentals",
                "topics": [
                    {
                        "name": "Linear regression → neural networks, reproduce every notebook",
                        "sub": "Sections 1–2, no copy-paste",
                        "res_type": "COURSE",
                        "res_name": "Made With ML — Foundations (Goku Mohandas)",
                        "res_desc": "Production-first ML education, free",
                        "res_url": "https://madewithml.com/courses/foundations/",
                    },
                    {
                        "name": "End-to-end ML project — California housing, production style",
                        "sub": "Chapters 1, 2, 4 — rebuild with production patterns",
                        "res_type": "BOOK",
                        "res_name": "Hands-On ML 3rd ed. (Aurélien Géron)",
                        "res_desc": "Most practical ML book available",
                        "res_url": "https://www.oreilly.com/library/view/hands-on-machine-learning/9781098125967/",
                    },
                    {
                        "name": "ML system design thinking — Chapters 1–2",
                        "sub": "Take written notes, not highlights",
                        "res_type": "BOOK",
                        "res_name": "Designing ML Systems (Chip Huyen)",
                        "res_desc": "Must-read for tier-1 system design rounds",
                        "res_url": "https://www.oreilly.com/library/view/designing-machine-learning/9781098107963/",
                    },
                ],
            },
            {
                "name": "Deep Learning + Transformers",
                "topics": [
                    {
                        "name": "Deep learning top-down — lessons 1–7, do every homework",
                        "sub": "Push a notebook per lesson to GitHub",
                        "res_type": "COURSE",
                        "res_name": "fast.ai — Practical Deep Learning for Coders",
                        "res_desc": "Best top-down DL course, free",
                        "res_url": "https://course.fast.ai",
                    },
                    {
                        "name": "Deep feedforward networks, regularization, optimization",
                        "sub": "Chapters 6, 7, 8 — read for intuition not derivations",
                        "res_type": "BOOK",
                        "res_name": "Deep Learning (Goodfellow, Bengio, Courville)",
                        "res_desc": "Free online, theoretical foundation",
                        "res_url": "https://www.deeplearningbook.org",
                    },
                    {
                        "name": "PyTorch — nn.Module, torch.compile, save/load",
                        "sub": "Build one custom nn.Module from scratch",
                        "res_type": "DOCS",
                        "res_name": "PyTorch official tutorials",
                        "res_desc": "Learn the Basics + Quickstart + torch.compile",
                        "res_url": "https://pytorch.org/tutorials/",
                    },
                    {
                        "name": "Transformer models — fine-tuning HuggingFace, Chapters 1–4",
                        "sub": "Self-attention, KV-cache, decoder-only dominance",
                        "res_type": "COURSE",
                        "res_name": "HuggingFace LLM Course",
                        "res_desc": "Official, free, covers full HF stack",
                        "res_url": "https://huggingface.co/learn/llm-course",
                    },
                ],
            },
            {
                "name": "AWS Cloud Foundations",
                "topics": [
                    {
                        "name": "S3, Glue, Athena, SageMaker Feature Store, Data Wrangler",
                        "sub": "Domain 1 — 28% of MLA-C01 exam",
                        "res_type": "COURSE",
                        "res_name": "AWS Skill Builder — MLA-C01 Exam Prep",
                        "res_desc": "Free with AWS account, official",
                        "res_url": "https://explore.skillbuilder.aws/learn/course/external/view/elearning/19688/aws-certified-machine-learning-engineer-associate-official-practice-question-set-mla-c01-english",
                    },
                    {
                        "name": "SageMaker — modeling and deployment domains",
                        "sub": "Domains 2+3 of MLA-C01",
                        "res_type": "COURSE",
                        "res_name": "Stéphane Maarek — Ultimate AWS MLA-C01 (Udemy)",
                        "res_desc": "Highest-rated AWS ML cert course",
                        "res_url": "https://www.udemy.com/course/aws-machine-learning/",
                    },
                ],
            },
        ],
        "projects": [
            {
                "name": "proj-00-tabular-baseline",
                "month": "Month 1",
                "desc": "Production-shaped tabular classifier. Not Titanic/MNIST — use UCI Adult, Kaggle Home Credit Default, or scrape your own. With pyproject.toml, tests, Ruff CI, typed predict() API, Dockerfile, and a README written like a tech blog post.",
                "tags": ["uv", "ruff", "pytest", "docker", "FastAPI"],
            },
            {
                "name": "proj-01-text-classifier",
                "month": "Month 2",
                "desc": "Fine-tune DistilBERT on a non-trivial dataset (AG News, IMDB with stratified-by-length analysis, or dental product reviews). Serve via FastAPI in Docker, deploy to HuggingFace Spaces (free).",
                "tags": ["transformers", "FastAPI", "docker", "HF Spaces"],
            },
        ],
        "milestones": [
            "Write a clean Python class with type hints, dataclasses, and async I/O without Googling",
            "Explain bias-variance, regularisation, cross-validation, ROC-AUC vs PR-AUC in 60 seconds each",
            "Write a SQL query joining 3 tables with a window function and CTE without help",
            "CI-green public repo at github.com/yourname-ai/proj-00-tabular-baseline",
            "Implement a 2-layer MLP from scratch in PyTorch (forward + backward + train loop) in <30 minutes",
            "Explain self-attention, KV-cache, positional encodings, and why decoder-only transformers dominate",
            "Working AWS CLI, S3 bucket with versioning, Glue crawler over a dataset",
        ],
    },
    "intermediate": {
        "label": "Intermediate",
        "months": "Months 3–4",
        "hours": "~176 hrs (22h/week)",
        "color": "#185FA5",
        "bg": "#E6F1FB",
        "sections": [
            {
                "name": "MLOps Stack",
                "topics": [
                    {
                        "name": "MLflow tracking, model registry, experiment management",
                        "sub": "Module 2 of MLOps Zoomcamp",
                        "res_type": "COURSE",
                        "res_name": "MLOps Zoomcamp — DataTalks.Club",
                        "res_desc": "Free, self-paced on YouTube + GitHub",
                        "res_url": "https://github.com/DataTalksClub/mlops-zoomcamp",
                    },
                    {
                        "name": "Orchestration — Prefect or Airflow DAGs",
                        "sub": "Module 3 of MLOps Zoomcamp",
                        "res_type": "DOCS",
                        "res_name": "Prefect docs — getting started",
                        "res_desc": "Modern workflow orchestration",
                        "res_url": "https://docs.prefect.io/latest/getting-started/quickstart/",
                    },
                    {
                        "name": "Docker multi-stage builds, deployment to AWS Lambda + Kinesis",
                        "sub": "Module 4 of MLOps Zoomcamp",
                        "res_type": "DOCS",
                        "res_name": "Docker multi-stage build docs",
                        "res_desc": "Official, production Docker patterns",
                        "res_url": "https://docs.docker.com/build/building/multi-stage/",
                    },
                    {
                        "name": "Monitoring with Evidently + Grafana, CI/CD for ML",
                        "sub": "Modules 5–6 of MLOps Zoomcamp",
                        "res_type": "DOCS",
                        "res_name": "Evidently AI tutorial",
                        "res_desc": "Data, concept, prediction drift",
                        "res_url": "https://docs.evidentlyai.com/get-started/tutorial",
                    },
                    {
                        "name": "Designing ML Systems — deployment, data distribution shifts",
                        "sub": "Chapters 7–8",
                        "res_type": "BOOK",
                        "res_name": "Designing ML Systems (Chip Huyen) — Ch.7–8",
                        "res_desc": "Training-serving skew, drift, retraining",
                        "res_url": "https://www.oreilly.com/library/view/designing-machine-learning/9781098107963/",
                    },
                ],
            },
            {
                "name": "RAG & Agent Architecture",
                "topics": [
                    {
                        "name": "LangGraph — stateful multi-tool agents, tracing with Langfuse",
                        "sub": "Build a 3-tool agent and trace it end-to-end",
                        "res_type": "DOCS",
                        "res_name": "LangGraph introduction tutorial",
                        "res_desc": "Official, builds agent step-by-step",
                        "res_url": "https://langchain-ai.github.io/langgraph/tutorials/introduction/",
                    },
                    {
                        "name": "Hybrid retrieval — BM25 + dense, Reciprocal Rank Fusion, rerankers",
                        "sub": "Cohere Rerank-v3 or Jina-Reranker-v2",
                        "res_type": "BLOG",
                        "res_name": "Pinecone — RAG with rerankers",
                        "res_desc": "Best practical guide for hybrid RAG",
                        "res_url": "https://www.pinecone.io/learn/series/rag/rerankers/",
                    },
                    {
                        "name": "Qdrant vector store — metadata filtering, hybrid search",
                        "sub": "Self-hosted, better filtering than Pinecone",
                        "res_type": "DOCS",
                        "res_name": "Qdrant getting started guide",
                        "res_desc": "Best production-ready vector DB docs",
                        "res_url": "https://docs.qdrant.tech/guides/getting-started/",
                    },
                    {
                        "name": "RAG evaluation — Ragas faithfulness, context precision/recall",
                        "sub": "200-pair hand-labelled domain eval set",
                        "res_type": "DOCS",
                        "res_name": "ragas docs — getting started",
                        "res_desc": "Canonical RAG eval framework",
                        "res_url": "https://docs.ragas.io/en/latest/getstarted/",
                    },
                    {
                        "name": "Langfuse observability — trace every query, cost + latency",
                        "sub": "Self-hostable via Docker",
                        "res_type": "DOCS",
                        "res_name": "Langfuse quickstart",
                        "res_desc": "Open-source LLM tracing + evals",
                        "res_url": "https://docs.langfuse.com/docs/get-started",
                    },
                    {
                        "name": "LLM Engineer's Handbook — RAG, evaluation, deployment",
                        "sub": "Chapters 4–7",
                        "res_type": "BOOK",
                        "res_name": "LLM Engineer's Handbook (Iusztin & Labonne)",
                        "res_desc": "Packt 2024, most current LLM engineering book",
                        "res_url": "https://www.packtpub.com/en-us/product/llm-engineers-handbook-9781836200079",
                    },
                ],
            },
            {
                "name": "Fine-tuning LLMs",
                "topics": [
                    {
                        "name": "QLoRA — rank 16, NF4 4-bit, q/k/v/o projections with Unsloth",
                        "sub": "2× faster, less VRAM than standard PEFT",
                        "res_type": "DOCS",
                        "res_name": "Unsloth documentation",
                        "res_desc": "Fastest QLoRA fine-tuning library",
                        "res_url": "https://docs.unsloth.ai",
                    },
                    {
                        "name": "SFT dataset curation — chat templates, HF dataset card",
                        "sub": "5K–10K examples, document construction process",
                        "res_type": "DOCS",
                        "res_name": "HuggingFace trl — SFTTrainer",
                        "res_desc": "Official SFT recipe with chat templates",
                        "res_url": "https://huggingface.co/docs/trl/sft_trainer",
                    },
                    {
                        "name": "Eval — lm-evaluation-harness, LLM-as-judge, win-rate vs base",
                        "sub": "Prove no catastrophic forgetting on MMLU",
                        "res_type": "GH",
                        "res_name": "EleutherAI lm-evaluation-harness",
                        "res_desc": "Standard benchmark harness, open source",
                        "res_url": "https://github.com/EleutherAI/lm-evaluation-harness",
                    },
                    {
                        "name": "HuggingFace LLM Course — datasets, tokenizers, fine-tuning",
                        "sub": "Chapters 5–12",
                        "res_type": "COURSE",
                        "res_name": "HuggingFace LLM Course — Ch.5–12",
                        "res_desc": "Free, official, dataset curation + RLHF",
                        "res_url": "https://huggingface.co/learn/llm-course",
                    },
                ],
            },
            {
                "name": "AWS MLA-C01 Certification",
                "topics": [
                    {
                        "name": "Tutorials Dojo practice exams — aim 75%+ on 3 full mocks",
                        "sub": "~$15, highest-quality practice questions",
                        "res_type": "WEB",
                        "res_name": "Tutorials Dojo — AWS MLA-C01 practice",
                        "res_desc": "Most accurate mock exams available",
                        "res_url": "https://tutorialsdojo.com/courses/aws-certified-machine-learning-engineer-associate-practice-exams/",
                    },
                ],
            },
        ],
        "projects": [
            {
                "name": "DentalRAG",
                "month": "Month 3–4",
                "desc": "Production-grade RAG over 50K dental clinical documents and product manuals. Hybrid search (BM25+dense), Cohere reranker, Ragas eval harness, Langfuse observability, FastAPI on AWS Fargate. v2 adds your fine-tuned model as generator — story of cost reduction.",
                "tags": ["qdrant", "ragas", "langfuse", "FastAPI", "terraform", "AWS Fargate"],
            },
        ],
        "milestones": [
            "AWS MLA-C01 in hand — add to LinkedIn the same day",
            "DentalRAG v1 live with one vector DB and basic Ragas eval",
            "Comfortable with MLflow tracking + model registry, Docker multi-stage builds",
            "Working Airflow/Prefect DAG for a training pipeline",
            "GitHub Actions ML CI — linting, tests, model eval on every PR",
            "Explain PagedAttention, continuous batching, prefix caching, LoRA vs QLoRA, DPO",
            "Working LangGraph multi-tool agent with full Langfuse traces in portfolio",
        ],
    },
    "advanced": {
        "label": "Advanced",
        "months": "Months 5–6",
        "hours": "~220 hrs (22h/week)",
        "color": "#3C3489",
        "bg": "#EEEDFE",
        "sections": [
            {
                "name": "Distributed Systems & Inference",
                "topics": [
                    {
                        "name": "Reliability, scalability, storage engines, partitioning, stream processing",
                        "sub": "Chapters 1, 3, 6, 11 — most-cited in FAANG ML system design",
                        "res_type": "BOOK",
                        "res_name": "Designing Data-Intensive Applications (Kleppmann)",
                        "res_desc": "The DDIA book — single most important read",
                        "res_url": "https://dataintensive.net",
                    },
                    {
                        "name": "vLLM — OpenAI-compatible serving, continuous batching, benchmark throughput",
                        "sub": "req/s and TTFT vs TGI vs vanilla Transformers",
                        "res_type": "DOCS",
                        "res_name": "vLLM quickstart",
                        "res_desc": "Get serving in <10 min",
                        "res_url": "https://docs.vllm.ai/en/latest/getting_started/quickstart.html",
                    },
                    {
                        "name": "Quantization — AWQ-4bit, GGUF Q4_K_M, cost-per-million-tokens benchmark",
                        "sub": "Serve same model in 3 formats, produce comparison table",
                        "res_type": "BLOG",
                        "res_name": "HuggingFace — quantization overview",
                        "res_desc": "Compares GPTQ, AWQ, GGUF with code",
                        "res_url": "https://huggingface.co/blog/overview-quantization-transformers",
                    },
                    {
                        "name": "NVIDIA Triton + vLLM backend — enterprise inference platform",
                        "sub": "nvcr.io/nvidia/tritonserver vLLM container",
                        "res_type": "DOCS",
                        "res_name": "NVIDIA Triton vLLM backend docs",
                        "res_desc": "Signals enterprise inference knowledge",
                        "res_url": "https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/index.html",
                    },
                    {
                        "name": "LLM internals — Stanford CS336 lectures 1,2,3,6,10",
                        "sub": "Tokenization, architectures, Triton kernels, inference",
                        "res_type": "YT",
                        "res_name": "Stanford CS336 — Language Modeling from Scratch",
                        "res_desc": "Spring 2025, watch for intuition",
                        "res_url": "https://www.youtube.com/playlist?list=PLoROMvodv4rOY23Y27xPcqFjI03l-tR4G",
                    },
                ],
            },
            {
                "name": "Streaming & Feature Stores",
                "topics": [
                    {
                        "name": "Kafka/Redpanda + Flink SQL — windowed aggregations, streaming features",
                        "sub": "100–1000 events/sec synthetic transaction stream",
                        "res_type": "WEB",
                        "res_name": "Confluent — Kafka for ML whitepaper",
                        "res_desc": "Production Kafka for ML pipelines",
                        "res_url": "https://www.confluent.io/resources/white-paper/kafka-the-definitive-guide/",
                    },
                    {
                        "name": "Feast feature store — point-in-time correctness, Redis online store",
                        "sub": "Most-asked question by senior MLE interviewers 2025–26",
                        "res_type": "DOCS",
                        "res_name": "Feast documentation",
                        "res_desc": "End-to-end feature store docs",
                        "res_url": "https://docs.feast.dev",
                    },
                    {
                        "name": "Drift detection — Evidently PSI, KS-statistics, Slack alerts",
                        "sub": "Hourly drift computation with automated retraining trigger",
                        "res_type": "DOCS",
                        "res_name": "Evidently AI tutorial",
                        "res_desc": "Data, concept, prediction drift in code",
                        "res_url": "https://docs.evidentlyai.com/get-started/tutorial",
                    },
                ],
            },
            {
                "name": "Infrastructure & Kubernetes",
                "topics": [
                    {
                        "name": "Kubernetes — kubectl, Helm, HPA, deploy RAG app to GKE/EKS",
                        "sub": "Chapters 1–7 + official tutorial",
                        "res_type": "BOOK",
                        "res_name": "Kubernetes Up & Running (Burns/Beda/Hightower)",
                        "res_desc": "Canonical K8s book, free on O'Reilly",
                        "res_url": "https://www.oreilly.com/library/view/kubernetes-up-and/9781098110192/",
                    },
                    {
                        "name": "Terraform — provision S3, ECR, SageMaker endpoint as code",
                        "sub": "Tear down nightly to save money",
                        "res_type": "DOCS",
                        "res_name": "HashiCorp Learn — Terraform on AWS",
                        "res_desc": "Official tutorial, fastest path to IaC",
                        "res_url": "https://developer.hashicorp.com/terraform/tutorials/aws-get-started",
                    },
                ],
            },
            {
                "name": "ML System Design + Interview Grind",
                "topics": [
                    {
                        "name": "7-step framework — visual search, fraud detection, video recommendation",
                        "sub": "Chapters 1–11, draw architecture diagrams by hand",
                        "res_type": "BOOK",
                        "res_name": "ML System Design Interview (Alex Xu & Ali Aminian)",
                        "res_desc": "Highest-ROI interview prep book",
                        "res_url": "https://www.amazon.com/Machine-Learning-System-Design-Interview/dp/1736049127",
                    },
                    {
                        "name": "LeetCode — 150 problems, NeetCode patterns, ML coding from scratch",
                        "sub": "80% Medium, solve new Medium in 25–30 min",
                        "res_type": "WEB",
                        "res_name": "NeetCode 150",
                        "res_desc": "Canonical pattern-based LeetCode list",
                        "res_url": "https://neetcode.io/practice",
                    },
                    {
                        "name": "ML fundamentals depth — alirezadir repo, Chip Huyen interview book",
                        "sub": "ml-fundamental.md + ml-coding.md + MLSD case studies",
                        "res_type": "GH",
                        "res_name": "alirezadir/Machine-Learning-Interviews",
                        "res_desc": "Most comprehensive ML interview repo",
                        "res_url": "https://github.com/alirezadir/Machine-Learning-Interviews",
                    },
                    {
                        "name": "Databricks Certified ML Associate — 48 questions, 90 min",
                        "sub": "Databricks Academy + Community Edition (free hands-on)",
                        "res_type": "DOCS",
                        "res_name": "Databricks ML Associate exam guide",
                        "res_desc": "$200 USD, strong EU enterprise signal",
                        "res_url": "https://www.databricks.com/learn/certification/machine-learning-associate",
                    },
                    {
                        "name": "EU AI Act — Article 27 FRIA, Annex III high-risk, audit logging",
                        "sub": "High-risk provisions enforceable August 2026",
                        "res_type": "WEB",
                        "res_name": "EU AI Act official text",
                        "res_desc": "Build compliance into portfolio projects",
                        "res_url": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689",
                    },
                ],
            },
        ],
        "projects": [
            {
                "name": "DentaCoder-7B",
                "month": "Month 4–5",
                "desc": "QLoRA fine-tune of Qwen2.5-7B-Instruct on 5K–10K SFT examples for dental procedure notes → ICD-10/CDT codes. Unsloth 2× faster training, eval with lm-evaluation-harness, vLLM serving with throughput benchmark, AWQ + GGUF quantization comparison table.",
                "tags": ["QLoRA", "Unsloth", "vLLM", "lm-eval-harness", "Modal/RunPod"],
            },
            {
                "name": "FraudStream",
                "month": "Month 5–6",
                "desc": "Streaming ML pipeline: Redpanda → Flink SQL windowed features → Feast (Redis online + S3 offline) → XGBoost served via FastAPI on K8s with HPA. Evidently drift detection hourly, Airflow retraining DAG with canary deploy. Public Grafana dashboard.",
                "tags": ["Kafka/Redpanda", "Feast", "Evidently", "Airflow", "Kubernetes", "MLflow"],
            },
        ],
        "milestones": [
            "Databricks ML Associate in hand — both AWS + Databricks certs on LinkedIn",
            "Three enterprise-grade projects live with public monitoring dashboards",
            "Draw end-to-end recommendation system from ingestion to serving in 25 minutes",
            "Working Terraform that provisions S3 + ECR + SageMaker endpoint",
            "80+ applications submitted, 5+ first-round interviews booked",
            "12 STAR stories drafted from R&D work — each under 2 minutes",
            "3 long-form blog posts published (RAG, QLoRA economics, EU AI Act FRIA)",
        ],
    },
}

INTERVIEW_QS = [
    "Design a production RAG system for a knowledge base with 1M documents — architecture, eval, and monitoring",
    "Explain point-in-time correctness in feature stores — why does it matter and how does Feast implement it?",
    "Walk me through PagedAttention and continuous batching in vLLM — why does it improve throughput?",
    "What is training-serving skew? How do you detect and prevent it in a production ML system?",
    "Design a fraud detection system: data ingestion to real-time inference in <50ms p99",
    "LoRA vs QLoRA — when would you choose each? What is rank and how does it affect capacity vs compute?",
    "Explain the EU AI Act Article 27 FRIA — what does it require and how would you build a compliant system?",
    "ROC-AUC vs PR-AUC — when is PR-AUC the only honest metric? Give a concrete example",
    "Design a retraining pipeline: when to retrain, how to trigger, how to validate before canary deploy",
    "Implement scaled dot-product attention from scratch in PyTorch — then explain KV-cache",
    "L1 vs L2 regularisation — why does L1 produce sparsity? Derive it or explain geometrically",
    "Your embedding model drifts in production — how do you detect it and what do you do?",
]

MENTAL_MODELS = [
    ("Applied AI > Classical ML", "Foundation-model commoditisation has eaten the bottom 40% of classical ML work. The durable skills are system design, retrieval, evaluation, and observability — not tuning XGBoost in notebooks. Pick the right branch of the bifurcating 'ML Engineer' title."),
    ("Point-in-time correctness", "The most-asked senior MLE interview question. When training, features must reflect what was known at prediction time — no future leakage. Feast implements this via entity_df with timestamps. Get this wrong and your model is trained on the future."),
    ("Training-serving skew", "The model trains on one feature distribution and serves on another. Causes: different preprocessing code paths, real-time vs batch features, data drift. Fix: shared feature store, parity tests, shadow mode evaluation."),
    ("Continuous batching (vLLM)", "Naive batching waits for all requests to finish before starting new ones — GPU idles. Continuous batching adds new requests as soon as slots free up. PagedAttention manages KV-cache like virtual memory pages. Result: 2-24× throughput improvement."),
    ("RAG vs fine-tune decision", "RAG: when knowledge changes frequently, when you need citations, when domain data is <10K examples. Fine-tune: when you need style/format change, when latency budget is tight, when inference cost must drop. Use both in DentalRAG v2 — RAG retrieval + fine-tuned generator."),
    ("EU AI Act as hiring tailwind", "Annex III high-risk provisions enforceable August 2026. Every EU employer needs engineers who can build Article 27-compliant systems. 90% of candidates ignore this. Committing a FRIA document to your RAG project is a hiring superpower."),
    ("Cost-per-token economics", "The table that wins interviews: same model as (1) full-precision BF16, (2) AWQ-4bit, (3) GGUF Q4_K_M. Quantification shows you think in production economics, not research benchmarks. Know your numbers: what does 1M tokens cost on H100 vs A10G?"),
    ("PR-AUC over ROC-AUC for imbalanced data", "ROC-AUC looks good even on bad classifiers when classes are imbalanced — it averages over thresholds including useless ones. PR-AUC measures precision-recall tradeoff where it matters. Fraud detection at 0.1% base rate: always use PR-AUC as the primary metric."),
    ("Canary deployment pattern", "Never push a new model version to 100% traffic immediately. Route 5% → measure online metrics vs control → if no regression after N requests, promote to 100%. Implement with weighted routing in FastAPI or a service mesh. Automated rollback on metric degradation."),
    ("Certifications as signal", "AWS MLA-C01 ($150) signals MLOps + SageMaker + Bedrock competence to European recruiters. Databricks ML Associate ($200) signals competence on the de-facto enterprise platform (SAP, Allianz, ING, Adyen). Two certs, ~100h prep total, €330 cost, outsized hiring signal."),
]

QUOTES = [
    ("The expert in anything was once a beginner.", "Helen Hayes"),
    ("An investment in knowledge pays the best interest.", "Benjamin Franklin"),
    ("The beautiful thing about learning is that no one can take it away from you.", "B.B. King"),
    ("Do not wait to strike till the iron is hot; but make it hot by striking.", "W.B. Yeats"),
    ("It does not matter how slowly you go as long as you do not stop.", "Confucius"),
    ("Success is the sum of small efforts repeated day in and day out.", "Robert Collier"),
    ("The secret of getting ahead is getting started.", "Mark Twain"),
    ("Push yourself, because no one else is going to do it for you.", "Unknown"),
    ("Great things never come from comfort zones.", "Unknown"),
    ("Dream it. Wish it. Do it.", "Unknown"),
    ("Don't watch the clock; do what it does. Keep going.", "Sam Levenson"),
    ("The harder you work for something, the greater you'll feel when you achieve it.", "Unknown"),
]

PROJECTS_DETAIL = {
    "proj-00-tabular-baseline": {
        "emoji": "📊",
        "month": "Month 1",
        "phase": "Beginner",
        "overview": "Production-shaped tabular classifier — not Titanic/MNIST.",
        "goal": "A typed, tested, Dockerised ML service with CI. Not a notebook. Demonstrates software engineering rigour, not just ML knowledge.",
        "dataset_suggestion": "UCI Adult Income, Kaggle Home Credit Default Risk, or scrape your own. Titanic and MNIST are explicitly forbidden in the portfolio.",
        "steps": [
            "Pick a real dataset — not Titanic, not MNIST. UCI Adult or Home Credit Default are good choices",
            "Set up project with uv, pyproject.toml, Ruff, pre-commit hooks — no conda, no requirements.txt",
            "Write EDA as a Marimo reactive notebook (not Jupyter) — commit to repo",
            "Build typed Python classes for data loading, feature engineering, training (dataclasses + type hints throughout)",
            "Train XGBoost or LightGBM with optuna HPO — track every run in MLflow",
            "Write pytest test suite — test data pipeline, feature transforms, predict() API. Aim ≥70% coverage",
            "Build FastAPI app with typed predict() endpoint and /health check",
            "Multi-stage Dockerfile — builder stage + slim runtime stage",
            "GitHub Actions CI — Ruff lint + pytest + docker build on every push",
            "README written like a tech blog post: problem, architecture diagram (Mermaid), results, what next",
        ],
        "must_haves": [
            "pyproject.toml with uv — no conda, no requirements.txt",
            "Type annotations on every function and class",
            "pytest with ≥70% coverage",
            "Multi-stage Dockerfile",
            "GitHub Actions CI green",
            "MLflow run logged",
            "README with Mermaid architecture diagram",
        ],
        "skills_demonstrated": ["Production Python", "MLflow tracking", "Docker", "FastAPI", "CI/CD", "Testing discipline"],
        "interview_talking_point": "Walk through why you chose uv over poetry and Ruff over flake8+black — shows you're current on the 2025 Python ecosystem.",
        "tags": ["uv", "ruff", "pytest", "mlflow", "fastapi", "docker", "github-actions"],
        "time_estimate": "~30–40 hours",
        "difficulty": "⭐⭐☆☆☆",
    },
    "proj-01-text-classifier": {
        "emoji": "📝",
        "month": "Month 2",
        "phase": "Beginner",
        "overview": "Fine-tune DistilBERT on a non-trivial dataset, serve via FastAPI, deploy to HuggingFace Spaces.",
        "goal": "A live, publicly accessible NLP service. Domain specificity is a superpower — dental product reviews would tie to your R&D background.",
        "dataset_suggestion": "AG News (topic classification), IMDB with stratified-by-length analysis, or dental product reviews scraped from Amazon/Trustpilot — the latter is a compelling portfolio story no generic candidate has.",
        "steps": [
            "Choose domain — dental product reviews is recommended given your Redent Nova background",
            "Scrape or download dataset — document data collection process in a dataset card",
            "Tokenise with AutoTokenizer, fine-tune DistilBERT with HuggingFace Trainer",
            "Stratified train/val/test split — no data leakage",
            "Evaluate: accuracy, F1, PR-AUC, confusion matrix",
            "Wrap in FastAPI with typed /predict endpoint",
            "Dockerise with multi-stage build",
            "Deploy to HuggingFace Spaces (free, Gradio or FastAPI mode)",
            "Add Langfuse tracing for every prediction — token count, latency, prediction",
            "README: dataset card, model card, architecture diagram",
        ],
        "must_haves": [
            "Non-trivial dataset — not MNIST, not toy data",
            "Domain specificity — dental if possible",
            "FastAPI with typed endpoints",
            "Live deployment on HF Spaces",
            "Langfuse tracing integrated",
            "Model card committed to repo",
        ],
        "skills_demonstrated": ["HuggingFace fine-tuning", "FastAPI", "Docker", "HF Spaces deployment", "Model cards"],
        "interview_talking_point": "Why DistilBERT over BERT? Why not a full GPT-based model? Know the latency/accuracy tradeoff cold.",
        "tags": ["transformers", "distilbert", "fastapi", "docker", "hf-spaces", "langfuse"],
        "time_estimate": "~25–35 hours",
        "difficulty": "⭐⭐⭐☆☆",
    },
    "DentalRAG": {
        "emoji": "🦷",
        "month": "Month 3–4",
        "phase": "Intermediate",
        "overview": "Production-grade RAG over 50K dental clinical documents, papers, and product manuals.",
        "goal": "Hybrid search with Ragas faithfulness ≥0.85, Langfuse tracing, Terraform-provisioned on AWS Fargate. v2 uses your fine-tuned DentaCoder-7B as generator — measurable cost reduction story.",
        "dataset_suggestion": "Dental clinical guidelines (ADA, FDI), PubMed dental abstracts, product manuals from your Redent Nova experience. Target 50K+ chunks. This domain story is unique — no generic candidate has it.",
        "steps": [
            "Ingest PDFs with Unstructured.io → semantic chunking with LlamaIndex SentenceWindowParser",
            "Extract metadata → S3 raw lake + DuckDB metadata catalog",
            "Embed with BGE-M3 or Voyage-3-lite, batched via vLLM-style server",
            "Store in Qdrant self-hosted — write comparison doc vs Weaviate",
            "Build BM25 index (Tantivy or Elasticsearch) for keyword search",
            "Implement Reciprocal Rank Fusion to combine BM25 + dense scores",
            "Add Cohere Rerank-v3 or Jina-Reranker-v2 as final reranking step",
            "Build LangGraph agent with multi-hop RAG for complex queries",
            "Integrate Langfuse — trace every query with cost, latency, retrieval scores",
            "Deploy FastAPI behind nginx to AWS Fargate with Terraform IaC",
            "Build 200-pair hand-labelled eval set, run Ragas (faithfulness, answer relevancy, context precision/recall)",
            "Commit Article 27 FRIA document to repo — EU AI Act compliance signal",
        ],
        "must_haves": [
            "≥50K chunks in Qdrant",
            "Hybrid BM25 + dense with RRF fusion",
            "Cohere or Jina reranker",
            "Ragas faithfulness ≥0.85 on 200-pair eval",
            "Langfuse traces with cost + latency per query",
            "Terraform-provisioned infrastructure",
            "Article 27 FRIA document in repo",
            "Public monitoring dashboard",
        ],
        "skills_demonstrated": ["RAG architecture", "Hybrid retrieval", "Reranking", "LangGraph agents", "Observability", "IaC", "EU AI Act compliance"],
        "interview_talking_point": "Why Qdrant not Pinecone? What was your p95 latency? What happens if the embedding model drifts? These are the exact bar-raiser questions.",
        "tags": ["qdrant", "ragas", "langfuse", "langgraph", "terraform", "aws-fargate", "unstructured"],
        "time_estimate": "~80 hours (v1+v2)",
        "difficulty": "⭐⭐⭐⭐☆",
    },
    "DentaCoder-7B": {
        "emoji": "🤖",
        "month": "Month 4–5",
        "phase": "Intermediate",
        "overview": "QLoRA fine-tune of Qwen2.5-7B-Instruct for dental procedure notes → ICD-10/CDT code conversion.",
        "goal": "≥win-rate vs base model judged by GPT-4o-as-judge. vLLM serving with documented throughput. Quantization comparison table. Stretch: NVIDIA Triton backend.",
        "dataset_suggestion": "5K–10K SFT examples: input = dental procedure note, output = structured ICD-10/CDT codes. Generate with GPT-4o + manual curation. Document construction in a HuggingFace dataset card.",
        "steps": [
            "Design task: dental procedure note → structured ICD-10/CDT code JSON",
            "Generate 5K–10K SFT examples with GPT-4o, manually curate 500 for quality control",
            "Format as chat template (ShareGPT format), commit HF dataset card",
            "Configure QLoRA: rank=16, NF4 4-bit, target q,k,v,o projections, use Unsloth",
            "Train on single H100 via Modal or RunPod (~$15–30 total)",
            "Log training: loss curve, gradient norm, learning rate to wandb",
            "Evaluate: lm-evaluation-harness on MMLU + HellaSwag (no catastrophic forgetting)",
            "Win-rate eval: GPT-4o-as-judge comparing base vs fine-tuned on 100 test cases",
            "Serve via vLLM — benchmark req/s and TTFT vs HF TGI and vanilla Transformers",
            "Serve also as AWQ-4bit and GGUF Q4_K_M — produce cost-per-million-tokens table",
            "Stretch: deploy under NVIDIA Triton Inference Server with vLLM backend",
        ],
        "must_haves": [
            "Unsloth QLoRA — rank=16, NF4 4-bit",
            "HuggingFace dataset card committed",
            "lm-eval-harness results (no forgetting proof)",
            "GPT-4o-as-judge win-rate evaluation",
            "vLLM throughput benchmark vs TGI",
            "AWQ + GGUF quantization comparison table",
            "wandb training run logged",
        ],
        "skills_demonstrated": ["Efficient fine-tuning", "Distributed inference economics", "Evaluation rigour", "GPU cost awareness", "Enterprise inference (Triton)"],
        "interview_talking_point": "The cost-per-million-tokens table is the conversation starter. Know exactly how much cheaper your fine-tuned quantized model is vs GPT-4o for this narrow task.",
        "tags": ["QLoRA", "Unsloth", "vLLM", "lm-eval-harness", "nvidia-triton", "Modal", "wandb"],
        "time_estimate": "~70 hours",
        "difficulty": "⭐⭐⭐⭐☆",
    },
    "FraudStream": {
        "emoji": "🌊",
        "month": "Month 5–6",
        "phase": "Advanced",
        "overview": "Streaming ML pipeline with feature store and real-time fraud inference — de-risks you against hiring managers worried you're 'just an LLM kid'.",
        "goal": "End-to-end: Redpanda → Flink → Feast → XGBoost → FastAPI on K8s. <50ms p99 inference. Evidently drift alerts. Automated Airflow retraining with canary deploy. Public Grafana dashboard.",
        "dataset_suggestion": "Synthetic transaction stream using Sparkov fraud generator at 100–1000 events/sec. Document the synthetic data generation process — shows you understand data engineering, not just model training.",
        "steps": [
            "Set up Redpanda (Kafka-compatible, lighter) with docker-compose for local dev",
            "Generate synthetic fraud stream with Sparkov at 100 events/sec",
            "Write Flink SQL windowed aggregations: last-1h-tx-count, last-24h-amount-sum, velocity features",
            "Set up Feast: Redis as online store, Parquet on S3 as offline store",
            "Demonstrate point-in-time correctness in Feast — document this explicitly, it's the most-asked senior MLE question",
            "Train XGBoost on offline features from Feast, track in MLflow",
            "Build FastAPI serving: pull online features from Feast/Redis, predict in <50ms p99",
            "Deploy to Kubernetes with HPA (Horizontal Pod Autoscaler)",
            "Evidently computing PSI + KS-statistics hourly, alert via Slack webhook when drift exceeds threshold",
            "Airflow DAG: drift trigger → full retrain → MLflow registry → canary deploy 5%→100%",
            "Grafana dashboard: requests/sec, p99 latency, drift scores, model version — make it public",
            "Stretch: add River online learning model; Great Expectations data quality checks; SHAP explanations in Streamlit",
        ],
        "must_haves": [
            "Redpanda streaming at ≥100 events/sec",
            "Feast with point-in-time correctness demonstrated",
            "FastAPI <50ms p99 inference",
            "K8s deployment with HPA",
            "Evidently drift detection with automated alerts",
            "Airflow retraining DAG with canary deploy",
            "Public Grafana monitoring dashboard",
        ],
        "skills_demonstrated": ["Streaming", "Feature stores", "Online/offline consistency", "Drift detection", "Automated retraining", "Classical ML at scale", "K8s"],
        "interview_talking_point": "Point-in-time correctness in Feast — explain exactly what it is, why it matters, and how you implemented it. This trips up 80% of candidates.",
        "tags": ["Redpanda", "Flink", "Feast", "Evidently", "Airflow", "Kubernetes", "MLflow", "Grafana"],
        "time_estimate": "~70 hours",
        "difficulty": "⭐⭐⭐⭐⭐",
    },
}

RES_COLORS = {
    "YT":     ("#2A1A1A", "#FF6B6B", "▶"),
    "DOCS":   ("#0D1F33", "#5BA4D4", "📄"),
    "BLOG":   ("#0F2A22", "#5DCAA5", "✍"),
    "COURSE": ("#1A1535", "#9D96E8", "🎓"),
    "GH":     ("#1A1A1A", "#C9D1D9", "⌥"),
    "PAPER":  ("#2A1E0D", "#D4A44A", "📑"),
    "BOOK":   ("#2A0E1A", "#D48BA5", "📚"),
    "WEB":    ("#0D1F33", "#5BA4D4", "🌐"),
}

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

section[data-testid="stAppViewContainer"] {
    background: transparent !important;
}
section[data-testid="stAppViewContainer"] > div:first-child {
    background: transparent !important;
}
.stApp {
    background: #0D1117 !important;
}

.main .block-container {
    padding-top: 1.5rem;
    padding-bottom: 3rem;
    max-width: 1100px;
}

/* Cards */
.card {
    background: #161B22;
    border: 1px solid #21262D;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin-bottom: .75rem;
}

.phase-header {
    display: flex; align-items: center; gap: 12px;
    margin: 1.5rem 0 1rem;
}
.phase-pill {
    font-size: 11px; font-weight: 600; padding: 3px 12px;
    border-radius: 99px; letter-spacing: .04em;
}
.section-divider {
    font-size: 11px; font-weight: 600; color: #8B949E;
    letter-spacing: .07em; text-transform: uppercase;
    margin: 1.2rem 0 .4rem; padding-bottom: 4px;
    border-bottom: 1px solid #21262D;
}
.topic-row {
    display: grid; grid-template-columns: 1.6fr 1fr;
    border-bottom: 1px solid #21262D; padding: 8px 0;
    align-items: center; gap: 12px;
}
.topic-name { font-size: 13.5px; font-weight: 500; color: #E6EDF3; }
.topic-sub  { font-size: 11px; color: #8B949E; margin-top: 2px; }
.res-badge  {
    display: inline-flex; align-items: center; gap: 6px;
    font-size: 12px; padding: 4px 10px; border-radius: 6px;
    text-decoration: none; font-weight: 500; width: fit-content;
}
.proj-card {
    border: 1px solid #21262D; border-radius: 12px;
    padding: 1rem 1.2rem; margin-bottom: .75rem;
    background: #161B22;
}
.proj-title { font-size: 15px; font-weight: 600; margin-bottom: 4px; color: #E6EDF3; }
.proj-desc  { font-size: 13px; color: #8B949E; line-height: 1.5; margin-bottom: 8px; }
.tag {
    display: inline-block; font-size: 11px; padding: 2px 8px;
    border-radius: 6px; background: #21262D; color: #8B949E;
    margin-right: 4px; margin-bottom: 2px;
}
.milestone-item {
    font-size: 13px; color: #C9D1D9; padding: 5px 0;
    border-bottom: 1px solid #21262D; display: flex; gap: 8px; align-items: flex-start;
}
.q-card {
    background: #161B22; border: 1px solid #21262D; border-radius: 8px;
    padding: 10px 14px; font-size: 13px; color: #C9D1D9;
    margin-bottom: 6px;
}
.mental-card {
    border: 1px solid #21262D; border-radius: 10px;
    padding: .85rem 1rem; margin-bottom: .6rem;
    background: #161B22;
}
.mental-title { font-size: 14px; font-weight: 600; color: #E6EDF3; margin-bottom: 3px; }
.mental-body  { font-size: 13px; color: #8B949E; line-height: 1.5; }
.stat-box {
    background: #161B22; border: 1px solid #21262D; border-radius: 10px;
    padding: 1rem; text-align: center;
}
.stat-val   { font-size: 26px; font-weight: 600; color: #E6EDF3; }
.stat-label { font-size: 12px; color: #8B949E; margin-top: 2px; }

/* Big progress ring card */
.progress-ring-card {
    background: #161B22;
    border: 1px solid #21262D;
    border-radius: 12px;
    padding: 2rem 1.2rem;
    text-align: center;
    margin-bottom: 1rem;
}
.progress-pct {
    font-size: 64px;
    font-weight: 700;
    color: #5DCAA5;
    line-height: 1;
}
.progress-sub {
    font-size: 14px;
    color: #8B949E;
    margin-top: 6px;
}

/* Quote card */
.quote-card {
    background: #161B22;
    border: 1px solid #21262D;
    border-left: 3px solid #5DCAA5;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin-bottom: 1.2rem;
}
.quote-label {
    font-size: 11px;
    font-weight: 600;
    color: #5DCAA5;
    letter-spacing: .05em;
    text-transform: uppercase;
    margin-bottom: 8px;
}
.quote-text {
    font-size: 16px;
    font-style: italic;
    color: #E6EDF3;
    line-height: 1.5;
}
.quote-author {
    font-size: 13px;
    color: #8B949E;
    margin-top: 6px;
}

/* Phase tip box */
.tip-box {
    background: #161B22;
    border: 1px solid #21262D;
    border-radius: 10px;
    padding: .75rem 1rem;
    margin-bottom: 1rem;
    font-size: 13px;
    color: #C9D1D9;
    line-height: 1.5;
}

/* Month cards on overview */
.month-card {
    border-radius: 0 8px 8px 0;
    background: #161B22;
    margin-bottom: .75rem;
    padding: .75rem 1rem;
}

stButton > button { border-radius: 8px !important; }
</style>
""", unsafe_allow_html=True)

# ── Build all_keys once (used in sidebar + overview) ─────────────────────────
all_keys = []
for phase in ROADMAP.values():
    for sec in phase["sections"]:
        for i, t in enumerate(sec["topics"]):
            all_keys.append(f"{phase['label']}_{sec['name']}_{i}")
    for j, m in enumerate(phase["milestones"]):
        all_keys.append(f"{phase['label']}_mile_{j}")

done_total = sum(1 for k in all_keys if is_checked(k))
total_items = len(all_keys)
pct_total = int(done_total / total_items * 100) if total_items else 0


def _phase_progress(phase_key):
    phase = ROADMAP[phase_key]
    keys = []
    for sec in phase["sections"]:
        for i in range(len(sec["topics"])):
            keys.append(f"{phase['label']}_{sec['name']}_{i}")
    for j in range(len(phase["milestones"])):
        keys.append(f"{phase['label']}_mile_{j}")
    p_done = sum(1 for k in keys if is_checked(k))
    return p_done, len(keys)


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🧠 ML Roadmap")
    st.markdown("**6 months to tier-1**")
    st.markdown("---")

    page = st.radio(
        "Navigate",
        ["Overview", "Beginner", "Intermediate", "Advanced", "Projects", "Interview Prep", "Notifications"],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown(f"**Overall progress**")
    st.progress(pct_total / 100, text=f"{pct_total}% · {done_total}/{total_items} done")
    st.markdown("---")
    st.markdown("**Daily target:** 2h weekdays + 3–4h Saturday")
    st.markdown("**Weekly target:** ~15 hours")
    st.caption("Tick topics as you finish them →")

# ── Helper renderers ──────────────────────────────────────────────────────────

def render_resource(t):
    rt = t["res_type"]
    bg, fg, icon = RES_COLORS.get(rt, ("#21262D", "#C9D1D9", "🔗"))
    st.markdown(
        f'<a class="res-badge" href="{t["res_url"]}" target="_blank" '
        f'style="background:{bg}; color:{fg};">'
        f'{icon} {t["res_name"]}'
        f'<span style="font-weight:400;font-size:11px;color:{fg};opacity:.75"> — {t["res_desc"]}</span>'
        f'</a>',
        unsafe_allow_html=True,
    )


def render_phase(phase_key, tip_html=None):
    phase = ROADMAP[phase_key]
    pill_style = f"background:{phase['bg']};color:{phase['color']};"

    if tip_html:
        st.markdown(f'<div class="tip-box">{tip_html}</div>', unsafe_allow_html=True)

    st.markdown(
        f'<div class="phase-header">'
        f'<span class="phase-pill" style="{pill_style}">{phase["label"]}</span>'
        f'<span style="font-size:18px;font-weight:500;color:#E6EDF3">{phase["months"]} &nbsp;·&nbsp; {phase["hours"]}</span>'
        f'</div>',
        unsafe_allow_html=True,
    )

    p_done, p_total = _phase_progress(phase_key)
    p_pct = int(p_done / p_total * 100) if p_total else 0
    st.progress(p_pct / 100, text=f"{p_pct}% of this phase complete")

    for sec in phase["sections"]:
        st.markdown(f'<div class="section-divider">{sec["name"]}</div>', unsafe_allow_html=True)

        for i, t in enumerate(sec["topics"]):
            key = f"{phase['label']}_{sec['name']}_{i}"
            col1, col2 = st.columns([1.6, 1.4])
            with col1:
                checked = st.checkbox(
                    t["name"],
                    value=is_checked(key),
                    key=f"cb_{key}",
                )
                st.session_state.checked[key] = checked
                if t["sub"]:
                    st.caption(t["sub"])
            with col2:
                render_resource(t)

    st.markdown("---")
    st.markdown("#### Projects")
    for proj in phase["projects"]:
        tags_html = " ".join(f'<span class="tag">{tg}</span>' for tg in proj["tags"])
        st.markdown(
            f'<div class="proj-card">'
            f'<div class="proj-title">📦 {proj["name"]} <span style="font-size:11px;font-weight:400;color:#8B949E;margin-left:8px">{proj["month"]}</span></div>'
            f'<div class="proj-desc">{proj["desc"]}</div>'
            f'{tags_html}'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown("#### ✅ Done when you can...")
    for j, m in enumerate(phase["milestones"]):
        key = f"{phase['label']}_mile_{j}"
        checked = st.checkbox(m, value=is_checked(key), key=f"mile_{key}")
        st.session_state.checked[key] = checked


SYSTEM_PROMPT = """You are an AI mentor embedded inside a 6-month ML Engineer Roadmap dashboard. Your ONLY job is to help the user understand and complete this specific roadmap.

YOU MUST REFUSE any question not related to this roadmap. If asked something outside the roadmap scope, reply: "I'm your roadmap mentor — I can only help with topics in this 6-month ML roadmap. Ask me about any concept, project, or resource from the dashboard!"

WHAT YOU CAN HELP WITH:
1. Explaining any concept in the roadmap (math, ML algorithms, PyTorch, transformers, RAG, fine-tuning, MLOps, agents)
2. Guiding through the 6 projects — step by step help, debugging advice, architecture decisions
3. Resources — explaining what to focus on in each linked resource
4. Interview prep — practicing the listed questions, explaining mental models
5. Motivation and study planning — how to stay on track, prioritize topics

THE ROADMAP COVERS:
BEGINNER (months 1-3): Linear algebra, calculus, probability, numpy, pandas, polars, scikit-learn, classical ML (linear/logistic regression, decision trees, random forests, XGBoost, LightGBM, k-means, PCA), model evaluation metrics, feature engineering, neural networks (MLP, backprop, activations, optimizers), PyTorch (tensors, autograd, nn.Module, Dataset, DataLoader, training loop, checkpoints), reproducibility.

INTERMEDIATE (months 4-5): CNNs (ResNet, EfficientNet), RNNs/LSTMs, Transformers (self-attention, multi-head, positional encodings, RoPE, ALiBi), ViT, diffusion models, mixed precision training (bf16/fp16), DDP/FSDP, DeepSpeed ZeRO, Accelerate, hyperparameter tuning (Optuna, ASHA), NLP tokenization (BPE, WordPiece), HuggingFace ecosystem (transformers, datasets, peft, trl), LoRA, QLoRA, SFT, DPO, GRPO, RAG (chunking, vector DBs, hybrid search, reranking), prompt engineering (CoT, ReAct, structured output), ragas evaluation.

ADVANCED (month 6): LLM internals (Flash Attention, KV cache, paged attention, speculative decoding, quantization GPTQ/AWQ/GGUF), vllm serving, continuous batching, CI/CD for ML (DVC, MLflow, GitHub Actions), drift detection (Evidently), observability (Langfuse, LangSmith, OpenTelemetry), LangGraph agents, MCP, prompt injection defense, guardrails.

PROJECTS: tabular-baseline, mnist-from-scratch-then-torch, rag-on-your-docs, qlora-domain-tune, prod-llm-platform, agent-with-evals.

Be concise, practical, and encouraging. Use code examples when explaining concepts. Keep responses under 300 words unless the user asks for more detail."""

# ── Pages ─────────────────────────────────────────────────────────────────────

if page == "Overview":
    st.markdown("# ML Engineer Roadmap — 6 Months to Tier-1")
    st.caption("320–460 hrs total · Prereqs: Python intermediate, linear algebra basics, git fluency")

    # Daily motivation quote (seeded to today — stable all day)
    random.seed(datetime.date.today().toordinal())
    quote_text, quote_author = random.choice(QUOTES)
    st.markdown(
        f'<div class="quote-card">'
        f'<div class="quote-label">📅 Today\'s focus</div>'
        f'<div class="quote-text">"{quote_text}"</div>'
        f'<div class="quote-author">— {quote_author}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # Big overall progress card
    st.markdown(
        f'<div class="progress-ring-card">'
        f'<div class="progress-pct">{pct_total}%</div>'
        f'<div class="progress-sub">of roadmap complete &nbsp;·&nbsp; {done_total} / {total_items} items</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # Per-phase progress bars
    phase_cfg = [
        ("beginner",     "Beginner",     "#5DCAA5"),
        ("intermediate", "Intermediate", "#378ADD"),
        ("advanced",     "Advanced",     "#7F77DD"),
    ]
    for pk, label, color in phase_cfg:
        pd, pt = _phase_progress(pk)
        pp = int(pd / pt * 100) if pt else 0
        st.markdown(
            f'<div style="display:flex;align-items:center;gap:12px;margin-bottom:6px;">'
            f'<span style="font-size:13px;font-weight:500;color:{color};min-width:90px">{label}</span>'
            f'<div style="flex:1;background:#21262D;border-radius:99px;height:8px;">'
            f'<div style="width:{pp}%;background:{color};height:8px;border-radius:99px;"></div>'
            f'</div>'
            f'<span style="font-size:12px;color:#8B949E;min-width:90px;text-align:right">{pd} / {pt} done</span>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")

    c1, c2, c3, c4 = st.columns(4)
    for col, val, label in zip(
        [c1, c2, c3, c4],
        ["572h", "22h", "3", "2"],
        ["Total hours", "Weekly target", "Projects", "Certifications"],
    ):
        col.markdown(
            f'<div class="stat-box"><div class="stat-val">{val}</div><div class="stat-label">{label}</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown("### Month-by-month plan")

    months = [
        ("Month 1", "Math + Production Python + ML Fundamentals", "~88h", "beginner"),
        ("Month 2", "Deep Learning + Transformers + AWS Foundations", "~88h", "beginner"),
        ("Month 3", "MLOps Stack + AWS MLA-C01 Cert + DentalRAG v1", "~88h", "intermediate"),
        ("Month 4", "RAG v2 + Agents + Fine-tuning LLMs (DentaCoder)", "~88h", "intermediate"),
        ("Month 5", "Distributed Systems + FraudStream + K8s + Terraform", "~88h", "advanced"),
        ("Month 6", "FraudStream finish + Databricks Cert + Interview Grind + Job Hunt", "~132h", "advanced"),
    ]
    phase_colors = {"beginner": "#5DCAA5", "intermediate": "#378ADD", "advanced": "#7F77DD"}

    cols = st.columns(3)
    for idx, (month, topic, hrs, ph) in enumerate(months):
        color = phase_colors[ph]
        cols[idx % 3].markdown(
            f'<div style="border-left:3px solid {color};padding:.75rem 1rem;'
            f'border-radius:0 8px 8px 0;background:#161B22;border:1px solid #21262D;border-left:3px solid {color};margin-bottom:.75rem;">'
            f'<div style="font-size:11px;font-weight:600;color:{color};margin-bottom:2px">{month}</div>'
            f'<div style="font-size:13px;font-weight:500;color:#E6EDF3">{topic}</div>'
            f'<div style="font-size:11px;color:#8B949E;margin-top:2px">{hrs}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown("### Daily habit — the only schedule that works")
    for habit in [
        "Weekdays: 2h focused study (1h theory + 1h coding)",
        "Saturday: 3–4h project work",
        "Sunday: review + Anki flashcards + read 1 paper abstract",
        "Log every session in a public GitHub README — accountability is real",
    ]:
        st.markdown(f"✅ &nbsp; {habit}")

elif page == "Beginner":
    render_phase(
        "beginner",
        tip_html="💡 <strong>Tip:</strong> Don't skip the math. Every concept here will appear in interviews. Go slow, go deep.",
    )

elif page == "Intermediate":
    render_phase(
        "intermediate",
        tip_html="💡 <strong>Tip:</strong> At this stage, run every concept in code within 24 hours of learning it. Theory without practice evaporates.",
    )

elif page == "Advanced":
    render_phase(
        "advanced",
        tip_html="💡 <strong>Tip:</strong> Start applying for jobs now. Interviews take 4–6 weeks. Don't wait until you feel 'ready'.",
    )

elif page == "Projects":
    st.markdown("# All 6 Projects")
    st.caption("Build them publicly on GitHub. Each one is a direct interview talking point.")

    for phase_key in ["beginner", "intermediate", "advanced"]:
        phase = ROADMAP[phase_key]
        pill_style = f"background:{phase['bg']};color:{phase['color']};"
        st.markdown(
            f'<span class="phase-pill" style="{pill_style}">{phase["label"]} — {phase["months"]}</span>',
            unsafe_allow_html=True,
        )
        st.markdown("")
        for proj in phase["projects"]:
            name = proj["name"]
            p = PROJECTS_DETAIL.get(name)
            if p:
                expander_label = f"{p['emoji']} {name} — {p['time_estimate']} · {p['difficulty']}"
                with st.expander(expander_label):
                    st.markdown(f"**Overview:** {p['overview']}")
                    st.markdown(f"**Goal:** {p['goal']}")
                    st.markdown(f"**Dataset suggestion:** {p['dataset_suggestion']}")
                    st.markdown("---")
                    st.markdown("**Step-by-step:**")
                    for i, step in enumerate(p["steps"], 1):
                        st.markdown(f"{i}. {step}")
                    st.markdown("---")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**Must-haves (checklist):**")
                        for must in p["must_haves"]:
                            key = f"proj_must_{name}_{must[:20]}"
                            val = st.checkbox(must, key=key, value=st.session_state.checked.get(key, False))
                            st.session_state.checked[key] = val
                    with col2:
                        st.markdown("**Skills demonstrated:**")
                        for skill in p["skills_demonstrated"]:
                            st.markdown(f"• {skill}")
                    st.info(f"🎯 **Interview talking point:** {p['interview_talking_point']}")
                    tags_html = " ".join(f'<span class="tag">{tg}</span>' for tg in p["tags"])
                    st.markdown(tags_html, unsafe_allow_html=True)
            else:
                tags_html = " ".join(f'<span class="tag">{tg}</span>' for tg in proj["tags"])
                st.markdown(
                    f'<div class="proj-card">'
                    f'<div class="proj-title">📦 {name} <span style="font-size:11px;font-weight:400;color:#8B949E;margin-left:8px">{proj["month"]}</span></div>'
                    f'<div class="proj-desc">{proj["desc"]}</div>'
                    f'{tags_html}'
                    f'</div>',
                    unsafe_allow_html=True,
                )
        st.markdown("---")

elif page == "Interview Prep":
    st.markdown("# Interview Prep")

    st.markdown("### Mental models — know these cold")
    for title, body in MENTAL_MODELS:
        st.markdown(
            f'<div class="mental-card">'
            f'<div class="mental-title">{title}</div>'
            f'<div class="mental-body">{body}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown("### Top interview questions")
    st.caption("These are the exact patterns tier-1 companies test.")
    for q in INTERVIEW_QS:
        st.markdown(f'<div class="q-card">❓ {q}</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Behavioral — 3 STAR stories to prepare")
    for story in [
        "A shipped ML system that failed in production and how you debugged it",
        "A time you chose a simpler model over a fancier one — and why",
        "A cross-functional data/model/infra decision you drove",
    ]:
        st.markdown(f"⭐ &nbsp; {story}")

elif page == "Notifications":
    st.markdown("# Notifications")
    st.caption("Free push notifications via ntfy.sh — no account needed.")

    st.markdown("### Step 1 — Install the app on your phone")
    col1, col2 = st.columns(2)
    col1.markdown("""
**Android:** [Play Store — ntfy](https://play.google.com/store/apps/details?id=io.heckel.ntfy)
**iOS:** [App Store — ntfy](https://apps.apple.com/us/app/ntfy/id1625396347)
    """)
    col2.info("Free, open source, no account needed.")

    st.markdown("### Step 2 — Choose your unique topic name")
    st.caption("Make it long and personal so nobody else guesses it. This is your private notification channel.")

    topic = st.text_input(
        "Your topic name",
        value=st.session_state.get("ntfy_topic", ""),
        placeholder="e.g. likith-ml-roadmap-x7k2-2026",
        help="Only use letters, numbers, and hyphens. No spaces."
    )
    if topic:
        st.session_state["ntfy_topic"] = topic
        st.markdown(f"**Your ntfy channel:** `ntfy.sh/{topic}`")
        st.caption(f"In the ntfy app, subscribe to topic: `{topic}`")

    st.markdown("### Step 3 — Set your daily reminder time")
    notif_time = st.time_input(
        "Send daily reminder at",
        value=datetime.time(9, 0),
        help="Pick a time you are usually free — morning works best."
    )
    if topic:
        st.session_state["ntfy_time"] = notif_time.strftime("%H:%M")

    st.markdown("### Step 4 — Test it right now")
    if st.button("Send test notification to my phone"):
        if not topic:
            st.error("Enter your topic name first.")
        else:
            success = send_ntfy(
                topic=topic,
                title="ML Roadmap — test notification",
                message="Your notifications are working! Time to study. Keep going.",
                tags=["brain", "rocket"],
                priority="default"
            )
            if success:
                st.success("Notification sent! Check your phone.")
            else:
                st.error("Failed. Check your topic name and internet connection.")

    if topic:
        st.markdown("---")
        st.markdown("### What your daily notification looks like")

        done = sum(1 for k in all_keys if is_checked(k))
        total = len(all_keys)
        pct = int(done / total * 100) if total else 0

        st.markdown(f"""
        <div style="background:#161B22; border:1px solid #30363D; border-left: 4px solid #5DCAA5;
                    border-radius:10px; padding:1rem 1.2rem; font-family:sans-serif;">
            <div style="font-size:13px; color:#7D8590; margin-bottom:4px">📱 Preview</div>
            <div style="font-size:15px; font-weight:600; color:#E6EDF3; margin-bottom:4px">
                🧠 ML Roadmap — Daily Check-in
            </div>
            <div style="font-size:13px; color:#C9D1D9; line-height:1.6">
                Progress: {pct}% complete · {done}/{total} topics done<br>
                Today's target: 2h study (1h theory + 1h coding)<br>
                Open your roadmap and tick at least ONE topic today.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Step 5 — Enable auto daily notifications on Streamlit Cloud")
    st.info("""
**ntfy.sh can't auto-send from Streamlit directly** (no background threads in cloud).
Use one of these FREE options to schedule daily sends:

**Option A — GitHub Actions (easiest, already have the repo):**
Add a workflow file — it runs every day at your chosen time and calls ntfy.sh.
Copy the workflow code below into `.github/workflows/daily_reminder.yml` in your repo.
    """)

    if topic:
        hour, minute = notif_time.hour, notif_time.minute
        utc_hour = (hour - 5) % 24
        utc_minute = (minute - 30) % 60

        workflow_yaml = f"""name: Daily ML Roadmap Reminder

on:
  schedule:
    # Runs at {notif_time.strftime('%H:%M')} IST = {utc_hour:02d}:{utc_minute:02d} UTC
    - cron: '{utc_minute} {utc_hour} * * *'
  workflow_dispatch:  # allows manual trigger

jobs:
  remind:
    runs-on: ubuntu-latest
    steps:
      - name: Send ntfy notification
        run: |
          curl -X POST https://ntfy.sh/{topic} \\
            -H "Title: ML Roadmap - Daily Study Time!" \\
            -H "Priority: high" \\
            -H "Tags: brain,fire,rocket" \\
            -d "Time to grind. Open your roadmap and tick at least ONE topic today. Tier-1 is waiting. You got this."
"""
        st.code(workflow_yaml, language="yaml")
        st.caption("Copy this file exactly into .github/workflows/daily_reminder.yml and push. GitHub runs it free every day.")

    st.markdown("""
**Option B — cron-job.org (zero setup, free):**
1. Go to [cron-job.org](https://cron-job.org) — free account
2. New cronjob → URL: `https://ntfy.sh/YOUR_TOPIC_NAME`
3. Method: POST, Body: `Study time. Open your ML roadmap now.`
4. Schedule: daily at your time
Done.
    """)