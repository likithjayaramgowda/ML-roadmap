import streamlit as st
import streamlit.components.v1 as components
import json
import random
import datetime

st.set_page_config(
    page_title="ML Engineer Roadmap — 6 Months to Tier-1",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

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

    components.html(f"""
    <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ background: transparent; overflow: hidden; font-family: -apple-system, sans-serif; }}

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
    </script>
    """, height=1, scrolling=False)

    st.markdown("""
<style>
div[data-testid="stIFrame"]:nth-of-type(2) iframe,
div.stHtml:nth-of-type(2) iframe,
[data-testid="stMain"] iframe:nth-of-type(2) {
    position: fixed !important;
    bottom: 0 !important;
    right: 0 !important;
    top: auto !important;
    left: auto !important;
    width: 420px !important;
    height: 600px !important;
    z-index: 9999 !important;
    pointer-events: all !important;
    border: none !important;
    background: transparent !important;
    margin: 0 !important;
    max-width: none !important;
}

div[data-testid="stIFrame"]:nth-of-type(2),
div.stHtml:nth-of-type(2) {
    height: 0 !important;
    min-height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
    overflow: visible !important;
}
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
        "months": "Months 1–3",
        "hours": "~90–130 hrs",
        "color": "#5DCAA5",
        "bg": "#0F2A22",
        "sections": [
            {
                "name": "Math Foundations",
                "topics": [
                    {
                        "name": "Linear algebra — vectors, matrices, dot product, SVD",
                        "sub": "Core of everything in ML",
                        "res_type": "YT",
                        "res_name": "3Blue1Brown — Essence of Linear Algebra",
                        "res_desc": "16 short videos, best visual intuition",
                        "res_url": "https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab",
                    },
                    {
                        "name": "Calculus — derivatives, chain rule, partial derivatives",
                        "sub": "Foundation for backprop",
                        "res_type": "YT",
                        "res_name": "3Blue1Brown — Essence of Calculus",
                        "res_desc": "12 videos, chain rule in ch.4",
                        "res_url": "https://www.youtube.com/playlist?list=PLZHQObOWTQDMsr9K-rj53DwVRMYO3t5Yr",
                    },
                    {
                        "name": "Probability, distributions, Bayes' theorem",
                        "sub": "Gaussian, Bernoulli, KL divergence",
                        "res_type": "WEB",
                        "res_name": "Seeing Theory — Brown University",
                        "res_desc": "Interactive visual probability — free",
                        "res_url": "https://seeing-theory.brown.edu",
                    },
                    {
                        "name": "Information theory — entropy, cross-entropy, KL divergence",
                        "sub": "",
                        "res_type": "BLOG",
                        "res_name": "Colah's blog — Visual Information Theory",
                        "res_desc": "Single best article on this topic",
                        "res_url": "https://colah.github.io/posts/2015-09-Visual-Information/",
                    },
                ],
            },
            {
                "name": "Python ML Toolchain",
                "topics": [
                    {
                        "name": "numpy — arrays, broadcasting, vectorization",
                        "sub": "",
                        "res_type": "DOCS",
                        "res_name": "NumPy official quickstart",
                        "res_desc": "Canonical, covers broadcasting fully",
                        "res_url": "https://numpy.org/doc/stable/user/quickstart.html",
                    },
                    {
                        "name": "polars + pandas for tabular data",
                        "sub": "",
                        "res_type": "DOCS",
                        "res_name": "Polars getting started guide",
                        "res_desc": "Prefer polars; pandas for legacy code",
                        "res_url": "https://pola.rs/posts/getting-started/",
                    },
                    {
                        "name": "mlflow + wandb for experiment tracking",
                        "sub": "",
                        "res_type": "DOCS",
                        "res_name": "Weights & Biases quickstart",
                        "res_desc": "Start with wandb; mlflow for self-hosted",
                        "res_url": "https://docs.wandb.ai/quickstart",
                    },
                    {
                        "name": "scikit-learn Pipeline + ColumnTransformer",
                        "sub": "",
                        "res_type": "DOCS",
                        "res_name": "sklearn — Pipeline user guide",
                        "res_desc": "Official, most thorough explanation",
                        "res_url": "https://scikit-learn.org/stable/modules/compose.html",
                    },
                ],
            },
            {
                "name": "Data Handling & EDA",
                "topics": [
                    {
                        "name": "Train/val/test splits, data leakage, class imbalance",
                        "sub": "",
                        "res_type": "BLOG",
                        "res_name": "ML Mastery — data leakage guide",
                        "res_desc": "Most practical guide on this pitfall",
                        "res_url": "https://machinelearningmastery.com/data-leakage-machine-learning/",
                    },
                    {
                        "name": "Feature scaling, encoding, missing values, outliers",
                        "sub": "",
                        "res_type": "COURSE",
                        "res_name": "Kaggle Learn — Data Cleaning",
                        "res_desc": "Free, hands-on, 5 notebooks",
                        "res_url": "https://www.kaggle.com/learn/data-cleaning",
                    },
                ],
            },
            {
                "name": "Classical ML",
                "topics": [
                    {
                        "name": "Linear regression, logistic regression, sigmoid",
                        "sub": "",
                        "res_type": "YT",
                        "res_name": "StatQuest with Josh Starmer",
                        "res_desc": 'Search "StatQuest logistic regression"',
                        "res_url": "https://www.youtube.com/@statquest",
                    },
                    {
                        "name": "Decision trees, random forests, gradient boosting",
                        "sub": "",
                        "res_type": "YT",
                        "res_name": "StatQuest — Random Forests & XGBoost series",
                        "res_desc": "Clearest visual explanation online",
                        "res_url": "https://www.youtube.com/watch?v=J4Wdy0Wc_xQ",
                    },
                    {
                        "name": "k-means, DBSCAN, PCA, t-SNE, UMAP",
                        "sub": "",
                        "res_type": "DOCS",
                        "res_name": "sklearn — unsupervised learning guide",
                        "res_desc": "With runnable examples for every method",
                        "res_url": "https://scikit-learn.org/stable/unsupervised_learning.html",
                    },
                    {
                        "name": "Model evaluation — precision, recall, F1, ROC-AUC, CV",
                        "sub": "",
                        "res_type": "COURSE",
                        "res_name": "Google ML Crash Course — Classification",
                        "res_desc": "Free, interactive, covers all metrics",
                        "res_url": "https://developers.google.com/machine-learning/crash-course/classification",
                    },
                    {
                        "name": "Feature engineering — transforms, encoding, selection",
                        "sub": "",
                        "res_type": "COURSE",
                        "res_name": "Kaggle Learn — Feature Engineering",
                        "res_desc": "Free, practical, 6 notebooks with code",
                        "res_url": "https://www.kaggle.com/learn/feature-engineering",
                    },
                ],
            },
            {
                "name": "Intro Neural Nets + PyTorch",
                "topics": [
                    {
                        "name": "Perceptron, MLP, forward pass, backprop intuition",
                        "sub": "",
                        "res_type": "YT",
                        "res_name": "Karpathy — micrograd (backprop from scratch)",
                        "res_desc": "2.5h video, builds autograd engine live",
                        "res_url": "https://www.youtube.com/watch?v=VMj-3S1tku0",
                    },
                    {
                        "name": "Optimizers — SGD, Adam, AdamW, LR schedulers",
                        "sub": "",
                        "res_type": "BLOG",
                        "res_name": "Sebastian Ruder — Optimizers overview",
                        "res_desc": "The definitive survey post",
                        "res_url": "https://www.ruder.io/optimizing-gradient-descent/",
                    },
                    {
                        "name": "PyTorch — tensors, autograd, nn.Module, training loop",
                        "sub": "",
                        "res_type": "DOCS",
                        "res_name": "PyTorch — 60 min blitz tutorial",
                        "res_desc": "Official, covers full training loop",
                        "res_url": "https://pytorch.org/tutorials/beginner/deep_learning_60min_blitz.html",
                    },
                    {
                        "name": "Dataset, DataLoader, torch.compile, checkpoints",
                        "sub": "",
                        "res_type": "DOCS",
                        "res_name": "PyTorch — Datasets & DataLoaders tutorial",
                        "res_desc": "Official docs, includes custom datasets",
                        "res_url": "https://pytorch.org/tutorials/beginner/basics/data_tutorial.html",
                    },
                    {
                        "name": "Reproducibility — seeds, config tracking, artifact logging",
                        "sub": "",
                        "res_type": "DOCS",
                        "res_name": "PyTorch — reproducibility notes",
                        "res_desc": "Covers all seed + determinism flags",
                        "res_url": "https://pytorch.org/docs/stable/notes/randomness.html",
                    },
                ],
            },
        ],
        "projects": [
            {
                "name": "tabular-baseline",
                "month": "Month 2–3",
                "desc": "End-to-end classifier on a real Kaggle-style tabular dataset. sklearn.Pipeline with ColumnTransformer, stratified CV, LightGBM baseline beating logistic regression by ≥3% F1. MLflow run logged with params + metrics + artifacts.",
                "tags": ["scikit-learn", "lightgbm", "mlflow", "pandas"],
            },
            {
                "name": "mnist-from-scratch-then-torch",
                "month": "Month 3",
                "desc": "Digit classifier twice: first a numpy-only MLP with manual backprop hitting ≥95% accuracy, then a PyTorch CNN hitting ≥99%. Both seeded, with a comparison plot.",
                "tags": ["numpy", "pytorch", "CNN", "reproducibility"],
            },
        ],
        "milestones": [
            "Spot data leakage in someone else's notebook within 5 minutes",
            "Choose between accuracy, F1, and ROC-AUC for a given problem without googling",
            "Write a PyTorch training loop from scratch without copy-pasting",
            "Explain bias vs variance using a learning curve you generated",
            "Reproduce a teammate's experiment from their MLflow run",
        ],
    },
    "intermediate": {
        "label": "Intermediate",
        "months": "Months 4–5",
        "hours": "~110–160 hrs",
        "color": "#378ADD",
        "bg": "#0D1F33",
        "sections": [
            {
                "name": "Deep Learning Architectures",
                "topics": [
                    {
                        "name": "CNN — conv, pool, batchnorm, residual, ResNet",
                        "sub": "",
                        "res_type": "COURSE",
                        "res_name": "Stanford CS231n lecture slides",
                        "res_desc": "Gold standard for CNN theory + vision",
                        "res_url": "https://cs231n.stanford.edu/slides/",
                    },
                    {
                        "name": "RNN, LSTM, GRU and why they were replaced",
                        "sub": "",
                        "res_type": "BLOG",
                        "res_name": "Colah's blog — Understanding LSTMs",
                        "res_desc": "Most-cited LSTM explainer ever written",
                        "res_url": "https://colah.github.io/posts/2015-08-Understanding-LSTMs/",
                    },
                    {
                        "name": "Transformer — self-attention, multi-head, encoder/decoder",
                        "sub": "",
                        "res_type": "BLOG",
                        "res_name": "Jay Alammar — The Illustrated Transformer",
                        "res_desc": "Best visual walkthrough, read before code",
                        "res_url": "https://jalammar.github.io/illustrated-transformer/",
                    },
                    {
                        "name": "Positional encodings — sinusoidal, RoPE, ALiBi",
                        "sub": "KV cache shape and size",
                        "res_type": "BLOG",
                        "res_name": "HuggingFace blog — positional encodings",
                        "res_desc": "Covers all modern variants",
                        "res_url": "https://huggingface.co/blog/alibi",
                    },
                    {
                        "name": "ViT, Swin, diffusion basics (DDPM, DDIM)",
                        "sub": "",
                        "res_type": "BLOG",
                        "res_name": "HuggingFace — Annotated Diffusion Model",
                        "res_desc": "Code-first walkthrough of DDPM",
                        "res_url": "https://huggingface.co/blog/annotated-diffusion",
                    },
                ],
            },
            {
                "name": "Training at Scale",
                "topics": [
                    {
                        "name": "Mixed precision — bf16, fp16, autocast, GradScaler",
                        "sub": "",
                        "res_type": "DOCS",
                        "res_name": "PyTorch AMP docs",
                        "res_desc": "Official, covers autocast + GradScaler",
                        "res_url": "https://pytorch.org/docs/stable/amp.html",
                    },
                    {
                        "name": "DDP, FSDP, DeepSpeed ZeRO stages",
                        "sub": "",
                        "res_type": "DOCS",
                        "res_name": "HuggingFace Accelerate docs",
                        "res_desc": "Abstracts DDP/FSDP/DeepSpeed cleanly",
                        "res_url": "https://huggingface.co/docs/accelerate",
                    },
                    {
                        "name": "Hyperparameter tuning — Bayesian, ASHA, Hyperband",
                        "sub": "",
                        "res_type": "DOCS",
                        "res_name": "Optuna tutorial",
                        "res_desc": "De-facto standard HPO library",
                        "res_url": "https://optuna.readthedocs.io/en/stable/tutorial/index.html",
                    },
                ],
            },
            {
                "name": "NLP + HuggingFace Ecosystem",
                "topics": [
                    {
                        "name": "Tokenization — BPE, WordPiece, SentencePiece, tiktoken",
                        "sub": "",
                        "res_type": "YT",
                        "res_name": "Karpathy — Let's build the GPT Tokenizer",
                        "res_desc": "2h, builds BPE from scratch",
                        "res_url": "https://www.youtube.com/watch?v=zduSFxRajkE",
                    },
                    {
                        "name": "AutoModel, AutoTokenizer, pipeline, datasets library",
                        "sub": "",
                        "res_type": "COURSE",
                        "res_name": "HuggingFace NLP Course — Ch 1–4",
                        "res_desc": "Free, official, covers full HF stack",
                        "res_url": "https://huggingface.co/learn/nlp-course/chapter1/1",
                    },
                    {
                        "name": "PEFT — LoRA, QLoRA, rank, alpha, target modules",
                        "sub": "",
                        "res_type": "DOCS",
                        "res_name": "HuggingFace peft docs",
                        "res_desc": "Canonical LoRA / QLoRA config reference",
                        "res_url": "https://huggingface.co/docs/peft",
                    },
                    {
                        "name": "SFT, DPO, ORPO, GRPO fine-tuning with trl",
                        "sub": "",
                        "res_type": "DOCS",
                        "res_name": "HuggingFace trl docs",
                        "res_desc": "SFTTrainer, DPOTrainer recipes",
                        "res_url": "https://huggingface.co/docs/trl",
                    },
                    {
                        "name": "When fine-tuning beats prompting (and when it doesn't)",
                        "sub": "",
                        "res_type": "BLOG",
                        "res_name": "Anyscale — Fine-tuning is for form, not facts",
                        "res_desc": "Best single framing for this decision",
                        "res_url": "https://www.anyscale.com/blog/fine-tuning-is-for-form-not-facts",
                    },
                ],
            },
            {
                "name": "RAG + Prompt Engineering",
                "topics": [
                    {
                        "name": "Chunking, embedding models, vector DBs (qdrant, pgvector)",
                        "sub": "",
                        "res_type": "DOCS",
                        "res_name": "Qdrant getting started guide",
                        "res_desc": "Best production-ready vector DB docs",
                        "res_url": "https://docs.qdrant.tech/guides/getting-started/",
                    },
                    {
                        "name": "Hybrid search — BM25 + dense + cross-encoder reranking",
                        "sub": "",
                        "res_type": "BLOG",
                        "res_name": "Pinecone — RAG with rerankers",
                        "res_desc": "Best practical guide for hybrid RAG",
                        "res_url": "https://www.pinecone.io/learn/series/rag/rerankers/",
                    },
                    {
                        "name": "Chain-of-thought, ReAct, structured output (instructor)",
                        "sub": "",
                        "res_type": "WEB",
                        "res_name": "Prompt Engineering Guide — DAIR.AI",
                        "res_desc": "Free, covers all major techniques",
                        "res_url": "https://www.promptingguide.ai",
                    },
                    {
                        "name": "RAG evaluation with ragas (faithfulness, context recall)",
                        "sub": "",
                        "res_type": "DOCS",
                        "res_name": "ragas docs — getting started",
                        "res_desc": "Canonical RAG eval framework",
                        "res_url": "https://docs.ragas.io/en/latest/getstarted/",
                    },
                ],
            },
            {
                "name": "LLM Evaluation",
                "topics": [
                    {
                        "name": "LLM-as-judge, golden datasets, regression suites",
                        "sub": "",
                        "res_type": "GH",
                        "res_name": "EleutherAI lm-evaluation-harness",
                        "res_desc": "Standard benchmark harness, open source",
                        "res_url": "https://github.com/EleutherAI/lm-evaluation-harness",
                    },
                ],
            },
        ],
        "projects": [
            {
                "name": "rag-on-your-docs",
                "month": "Month 4–5",
                "desc": "Production-leaning RAG over a real corpus (≥10k chunks). Hybrid search (BM25 + dense) with reranker, structured JSON answers with citations, ragas faithfulness ≥0.85, FastAPI endpoint with streaming.",
                "tags": ["qdrant", "ragas", "FastAPI", "bge-reranker"],
            },
            {
                "name": "qlora-domain-tune",
                "month": "Month 5",
                "desc": "QLoRA fine-tune of a 7–13B open model on a domain dataset. trl.SFTTrainer + bitsandbytes 4-bit, before/after eval on held-out set with ≥5% lift, model card on HF Hub.",
                "tags": ["QLoRA", "trl", "bitsandbytes", "HF Hub"],
            },
        ],
        "milestones": [
            "Read a transformer paper and map every block to PyTorch code",
            "Decide between fine-tuning, RAG, and prompting for a real ask, with reasons",
            "Train a model with FSDP across 2+ GPUs without copy-pasting",
            "Run a QLoRA fine-tune end-to-end and ship the adapter to HF Hub",
            "Write a structured-output generator that never returns invalid JSON",
        ],
    },
    "advanced": {
        "label": "Advanced",
        "months": "Month 6",
        "hours": "~120–170 hrs",
        "color": "#7F77DD",
        "bg": "#16123A",
        "sections": [
            {
                "name": "LLM Internals",
                "topics": [
                    {
                        "name": "Transformer math — attention, FFN, residual, parameter count",
                        "sub": "",
                        "res_type": "YT",
                        "res_name": "Karpathy — Let's build GPT from scratch",
                        "res_desc": "2h, builds full GPT-2 live in PyTorch",
                        "res_url": "https://www.youtube.com/watch?v=kCc8FmEb1nY",
                    },
                    {
                        "name": "KV cache, paged attention, Flash Attention 2/3",
                        "sub": "",
                        "res_type": "DOCS",
                        "res_name": "vllm — architecture overview",
                        "res_desc": "Explains PagedAttention + continuous batching",
                        "res_url": "https://docs.vllm.ai/en/latest/design/arch_overview.html",
                    },
                    {
                        "name": "Quantization — GPTQ, AWQ, GGUF, FP8, INT4",
                        "sub": "",
                        "res_type": "BLOG",
                        "res_name": "HuggingFace — quantization overview",
                        "res_desc": "Compares all methods with code",
                        "res_url": "https://huggingface.co/blog/overview-quantization-transformers",
                    },
                    {
                        "name": "Speculative decoding, draft models, MoE routing",
                        "sub": "",
                        "res_type": "PAPER",
                        "res_name": "Speculative Decoding paper (Chen et al.)",
                        "res_desc": "Original paper — read abstract + §3",
                        "res_url": "https://arxiv.org/abs/2302.01318",
                    },
                ],
            },
            {
                "name": "Inference Serving + MLOps",
                "topics": [
                    {
                        "name": "vllm — continuous batching, OpenAI-compat endpoint",
                        "sub": "",
                        "res_type": "DOCS",
                        "res_name": "vllm quickstart",
                        "res_desc": "Get serving in <10 min",
                        "res_url": "https://docs.vllm.ai/en/latest/getting_started/quickstart.html",
                    },
                    {
                        "name": "CI/CD for models — DVC + mlflow + GitHub Actions",
                        "sub": "",
                        "res_type": "DOCS",
                        "res_name": "DVC getting started",
                        "res_desc": "Data + model versioning, CI integration",
                        "res_url": "https://dvc.org/doc/start",
                    },
                    {
                        "name": "Drift detection — evidently, nannyml",
                        "sub": "",
                        "res_type": "DOCS",
                        "res_name": "Evidently AI tutorial",
                        "res_desc": "Data, concept, prediction drift in code",
                        "res_url": "https://docs.evidentlyai.com/get-started/tutorial",
                    },
                    {
                        "name": "Observability — LangSmith, Langfuse, OpenTelemetry",
                        "sub": "",
                        "res_type": "DOCS",
                        "res_name": "Langfuse quickstart",
                        "res_desc": "Open-source LLM tracing + evals",
                        "res_url": "https://docs.langfuse.com/docs/get-started",
                    },
                ],
            },
            {
                "name": "Agent Frameworks + Safety",
                "topics": [
                    {
                        "name": "LangGraph — stateful agent graphs, planner-executor",
                        "sub": "",
                        "res_type": "DOCS",
                        "res_name": "LangGraph introduction tutorial",
                        "res_desc": "Official, builds agent step-by-step",
                        "res_url": "https://langchain-ai.github.io/langgraph/tutorials/introduction/",
                    },
                    {
                        "name": "MCP servers and clients, tool/function calling protocols",
                        "sub": "",
                        "res_type": "DOCS",
                        "res_name": "MCP official introduction",
                        "res_desc": "Spec + examples for MCP integration",
                        "res_url": "https://modelcontextprotocol.io/introduction",
                    },
                    {
                        "name": "Prompt injection — direct + indirect, guardrails, Pydantic",
                        "sub": "",
                        "res_type": "GH",
                        "res_name": "guardrails-ai GitHub + docs",
                        "res_desc": "Read README + output validation guide",
                        "res_url": "https://github.com/guardrails-ai/guardrails",
                    },
                ],
            },
            {
                "name": "Production Systems Design",
                "topics": [
                    {
                        "name": "Full ML system design — feature store, training, serving, monitoring",
                        "sub": "",
                        "res_type": "BOOK",
                        "res_name": "Designing ML Systems — Chip Huyen",
                        "res_desc": "Must-read for tier-1 system design rounds",
                        "res_url": "https://www.oreilly.com/library/view/designing-machine-learning/9781098107963/",
                    },
                    {
                        "name": "Research literacy — reading papers, ablations, reproducing",
                        "sub": "",
                        "res_type": "WEB",
                        "res_name": "Papers With Code",
                        "res_desc": "SOTA + code; daily reading habit",
                        "res_url": "https://paperswithcode.com",
                    },
                ],
            },
        ],
        "projects": [
            {
                "name": "prod-llm-platform",
                "month": "Month 6",
                "desc": "Multi-tenant LLM API with vllm backend, continuous batching, OpenAI-compatible endpoint, per-tenant rate limits + budgets, OpenTelemetry traces, prompt-injection guardrails. ≥99% uptime over a 7-day soak test.",
                "tags": ["vllm", "FastAPI", "OpenTelemetry", "guardrails"],
            },
            {
                "name": "agent-with-evals",
                "month": "Month 6",
                "desc": "Tool-using agent with regression eval suite. LangGraph, ≥5 tools with Pydantic-validated args, golden eval set with ≥50 cases, CI fails on quality regression, traces in Langfuse.",
                "tags": ["LangGraph", "Langfuse", "Pydantic", "CI/CD"],
            },
        ],
        "milestones": [
            "Choose between LoRA, full FT, continued pretraining, and RAG with cost math",
            "Stand up vllm with continuous batching and hit a documented tokens/sec target",
            "Profile a training run, identify the bottleneck (data, compute, comm), and fix it",
            "Red-team your own agent and patch at least one indirect prompt-injection path",
            "Reproduce a recent paper's main result within 10% on a small budget",
        ],
    },
}

INTERVIEW_QS = [
    "Gradient descent variants and why Adam usually wins — and when it doesn't",
    "Transformer math: attention complexity, KV cache size, parameter count",
    "RAG vs fine-tune vs long-context: when to use which, with cost math",
    "ML system design: feature store → training pipeline → serving → monitoring",
    "Recommender system design: candidate gen → ranking → reranking",
    "Tokenization edge cases: BPE merges, unicode, code tokens, emoji",
    "Coding: implement scaled dot-product attention in PyTorch",
    "Cross-validation pitfalls: data leakage, time series CV, grouped data",
    "How do you debug a loss spike in training? Systematic approach",
    "LLM eval design: golden sets, LLM-as-judge bias, statistical significance",
]

MENTAL_MODELS = [
    ("Bias / variance", "Underfitting trades off with overfitting. Regularization, more data, and better features shift the curve. Diagnose with learning curves."),
    ("Backprop is just chain rule", "Every layer caches what it needs for its local gradient. The framework handles bookkeeping. Understand it, don't memorize the math."),
    ("Attention is soft lookup", "Queries match keys to weight values. Complexity is O(n²) in sequence length without tricks like Flash Attention."),
    ("KV cache", "At inference, keys and values from past tokens are cached so each new token costs O(n) not O(n²). Critical for latency."),
    ("RAG vs fine-tune", "RAG injects fresh knowledge at query time. FT changes behavior/style. Use both, not either/or. Long context is a third option."),
    ("MFU / HFU", "Model FLOPs utilization tells you how close training is to hardware peak. <30% means you're leaving money on the table — profile and fix."),
    ("Prompt injection is the new SQLi", "Never trust tool args or retrieved text. Validate with Pydantic, sandbox, and allowlist. Top-labs interviewers ask this."),
    ("PEFT", "Train a tiny number of new params (LoRA adapters) and freeze the base. Cheap, composable, near-FT quality."),
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
    "tabular-baseline": {
        "emoji": "📊",
        "month": "Month 2–3",
        "phase": "Beginner",
        "overview": "End-to-end classifier on a real Kaggle-style tabular dataset.",
        "goal": "Beat logistic regression by ≥3% F1 using LightGBM inside a sklearn Pipeline. Log everything to MLflow.",
        "dataset_suggestion": "Use the Titanic, House Prices, or Telco Churn dataset from Kaggle.",
        "steps": [
            "Download dataset and do EDA — plot distributions, null counts, class balance",
            "Build sklearn Pipeline with ColumnTransformer (StandardScaler for numerics, OneHotEncoder for categoricals)",
            "Train baseline logistic regression — record F1 score",
            "Train LightGBM inside the same Pipeline — tune with optuna (20 trials)",
            "Run stratified 5-fold CV — report mean ± std F1",
            "Log params, metrics, and the model artifact to MLflow",
            "Write a clean README with results table and learning notes",
        ],
        "must_haves": [
            "sklearn.Pipeline with ColumnTransformer (no leakage)",
            "Stratified CV — not a single train/test split",
            "LightGBM beating logistic regression by ≥3% F1",
            "MLflow run with params + metrics + artifact logged",
            "Seeded for reproducibility (random_state=42 everywhere)",
        ],
        "skills_demonstrated": ["Data preprocessing", "Pipeline design", "Gradient boosting", "Experiment tracking", "Avoiding data leakage"],
        "interview_talking_point": "Walk an interviewer through your feature engineering choices and why you picked F1 over accuracy for this dataset.",
        "tags": ["scikit-learn", "lightgbm", "mlflow", "pandas", "optuna"],
        "time_estimate": "~15–20 hours",
        "difficulty": "⭐⭐☆☆☆",
    },
    "mnist-from-scratch-then-torch": {
        "emoji": "🔢",
        "month": "Month 3",
        "phase": "Beginner",
        "overview": "Build a digit classifier twice — first with raw numpy, then with PyTorch CNN.",
        "goal": "numpy MLP ≥95% test accuracy. PyTorch CNN ≥99%. Both fully seeded with a side-by-side comparison plot.",
        "dataset_suggestion": "MNIST — load via torchvision.datasets.MNIST or keras.datasets.mnist.",
        "steps": [
            "Part 1 — numpy only: implement forward pass (matmul + ReLU + softmax), cross-entropy loss, and backprop manually",
            "Train numpy MLP for 50 epochs with mini-batch SGD — hit ≥95% test accuracy",
            "Part 2 — PyTorch: build CNN with 2 conv layers + batchnorm + dropout + FC head",
            "Use DataLoader with augmentation (RandomRotation, RandomAffine)",
            "Train with AdamW + cosine LR scheduler — hit ≥99% test accuracy",
            "Plot: training curves side-by-side, confusion matrices for both models",
            "Seed everything: random, numpy, torch, cudnn.deterministic=True",
        ],
        "must_haves": [
            "numpy backprop from scratch — no autograd",
            "PyTorch CNN hitting ≥99% test accuracy",
            "Both models seeded identically for reproducibility",
            "Comparison plot: accuracy curves + confusion matrices",
            "torch.compile used for PyTorch model (free speedup)",
        ],
        "skills_demonstrated": ["Manual backprop", "PyTorch CNN", "Reproducibility", "Data augmentation", "Result visualization"],
        "interview_talking_point": "Explain exactly how gradients flow through your numpy MLP — this is a classic whiteboard question.",
        "tags": ["numpy", "pytorch", "CNN", "backprop", "reproducibility"],
        "time_estimate": "~20–25 hours",
        "difficulty": "⭐⭐⭐☆☆",
    },
    "rag-on-your-docs": {
        "emoji": "🔍",
        "month": "Month 4–5",
        "phase": "Intermediate",
        "overview": "Production-grade RAG pipeline over a real document corpus (≥10k chunks).",
        "goal": "Hybrid search (BM25 + dense) with reranking, FastAPI endpoint, ragas faithfulness ≥0.85.",
        "dataset_suggestion": "Use ArXiv ML papers, Wikipedia ML articles, or your own domain documents. Target ≥50 PDFs.",
        "steps": [
            "Collect corpus: ≥50 PDFs or documents in your domain",
            "Chunk documents: try fixed (512 tokens), semantic, and recursive — compare retrieval quality",
            "Embed with bge-small-en-v1.5 (free, local) — store in Qdrant",
            "Build BM25 index with rank_bm25 for keyword search",
            "Implement hybrid retrieval: combine BM25 + dense scores with RRF (Reciprocal Rank Fusion)",
            "Add cross-encoder reranker (bge-reranker-base) to rerank top-20 → top-5",
            "Build FastAPI endpoint: POST /query → returns JSON with answer + source citations",
            "Add streaming response with SSE",
            "Evaluate with ragas: faithfulness, context_recall, answer_relevancy — target ≥0.85 faithfulness",
            "Document latency budget: P50 and P95 response times",
        ],
        "must_haves": [
            "≥10k chunks in Qdrant",
            "Hybrid BM25 + dense search with RRF fusion",
            "Cross-encoder reranker (bge-reranker-base)",
            "Structured JSON output with cited sources",
            "ragas faithfulness ≥0.85 on 20-question eval set",
            "FastAPI endpoint with streaming",
            "Latency documented (P50/P95)",
        ],
        "skills_demonstrated": ["RAG pipeline design", "Vector search", "Hybrid retrieval", "Reranking", "API design", "LLM evaluation"],
        "interview_talking_point": "Explain why naive RAG fails and how hybrid search + reranking fixes it. Show your ragas eval numbers.",
        "tags": ["qdrant", "ragas", "FastAPI", "bge-reranker", "BM25", "sentence-transformers"],
        "time_estimate": "~25–35 hours",
        "difficulty": "⭐⭐⭐⭐☆",
    },
    "qlora-domain-tune": {
        "emoji": "🤖",
        "month": "Month 5",
        "phase": "Intermediate",
        "overview": "QLoRA fine-tune a 7–13B open model on a domain-specific dataset.",
        "goal": "≥5% lift on held-out eval vs base model. Model card published on HF Hub. Full training run logged in wandb.",
        "dataset_suggestion": "Use a domain you care about: medical QA (MedQA), legal text (legal_contracts on HF), code (the-stack), or finance (financial_phrasebank). Min 5k examples.",
        "steps": [
            "Pick a 7–13B base model: Llama-3.1-8B, Mistral-7B, or Qwen2.5-7B",
            "Download and format dataset into chat template (ShareGPT or Alpaca format)",
            "Configure QLoRA: rank=16, alpha=32, target_modules=['q_proj','v_proj'], load_in_4bit=True",
            "Set up trl.SFTTrainer with bitsandbytes 4-bit quantization",
            "Run training — log loss curve, gradient norm, and learning rate to wandb",
            "Evaluate base model vs fine-tuned on held-out 200-example set — measure your metric (accuracy / ROUGE / exact match)",
            "Confirm ≥5% lift over base model",
            "Merge LoRA adapter into base weights using peft merge_and_unload()",
            "Push adapter (not merged weights) to HF Hub with full model card",
            "Model card must include: dataset description, training config, eval results table, limitations",
        ],
        "must_haves": [
            "QLoRA config: rank=16, alpha=32, 4-bit quantization",
            "trl.SFTTrainer with proper chat template",
            "Before/after eval on held-out set showing ≥5% lift",
            "wandb training run logged with loss + metrics",
            "Adapter published to HF Hub",
            "Model card with eval results table",
        ],
        "skills_demonstrated": ["QLoRA fine-tuning", "PEFT", "Dataset formatting", "LLM evaluation", "HF Hub publishing", "Experiment tracking"],
        "interview_talking_point": "Explain the math of LoRA — why low-rank decomposition works, how rank affects capacity vs compute tradeoff.",
        "tags": ["QLoRA", "trl", "bitsandbytes", "peft", "HF Hub", "wandb"],
        "time_estimate": "~20–30 hours",
        "difficulty": "⭐⭐⭐⭐☆",
    },
    "prod-llm-platform": {
        "emoji": "🚀",
        "month": "Month 6",
        "phase": "Advanced",
        "overview": "Multi-tenant LLM inference API with rate limiting, observability, and guardrails.",
        "goal": "OpenAI-compatible endpoint backed by vllm. ≥99% uptime over 7-day soak test. Full observability stack.",
        "dataset_suggestion": "No dataset needed — this is an infra project. Use any open 7B model (Llama-3.1-8B-Instruct).",
        "steps": [
            "Set up vllm server with Llama-3.1-8B-Instruct: docker run vllm/vllm-openai",
            "Build FastAPI wrapper with OpenAI-compatible /v1/chat/completions endpoint",
            "Add per-tenant API key auth (store in Redis or simple dict for demo)",
            "Implement per-tenant rate limiting: X requests/min, Y tokens/day",
            "Add per-tenant token budget tracking",
            "Integrate OpenTelemetry: trace every request with latency, token counts, model ID",
            "Add prompt injection detection: block common injection patterns with a classifier or regex allowlist",
            "Add guardrails-ai output validator for PII detection",
            "Write a 7-day soak test script: 1000 requests/hour, log error rate + p95 latency",
            "Document: tokens/sec throughput, GPU memory usage, cost per 1M tokens estimate",
        ],
        "must_haves": [
            "vllm backend with continuous batching",
            "OpenAI-compatible API (works with openai Python client)",
            "Per-tenant rate limits + token budgets",
            "OpenTelemetry traces with token usage",
            "Prompt injection detection",
            "7-day soak test showing ≥99% uptime",
            "Cost per 1M tokens documented",
        ],
        "skills_demonstrated": ["LLM serving", "API design", "Multi-tenancy", "Observability", "Security", "Performance testing"],
        "interview_talking_point": "Walk through your architecture diagram. Explain how vllm's PagedAttention enables continuous batching and why it matters for throughput.",
        "tags": ["vllm", "FastAPI", "OpenTelemetry", "guardrails", "Redis", "Docker"],
        "time_estimate": "~30–40 hours",
        "difficulty": "⭐⭐⭐⭐⭐",
    },
    "agent-with-evals": {
        "emoji": "🧠",
        "month": "Month 6",
        "phase": "Advanced",
        "overview": "Tool-using LLM agent with a full regression eval suite and CI integration.",
        "goal": "≥5 tools, ≥50 golden eval cases, CI fails on quality regression, deployed with traces in Langfuse.",
        "dataset_suggestion": "Build your own golden eval set — 50 question/expected-output pairs that test each tool. This IS the hard part.",
        "steps": [
            "Design agent purpose: choose a domain (e.g. ML paper researcher, code reviewer, data analyst)",
            "Implement ≥5 tools with Pydantic-validated args: e.g. web_search, read_file, run_python, query_db, send_summary",
            "Build agent graph in LangGraph with: planner node, tool executor node, reflection node",
            "Add Langfuse tracing — every tool call and LLM call gets a span",
            "Write ≥50 golden eval cases: (user_query, expected_tool_calls, expected_output_contains)",
            "Build eval harness: run all 50 cases, compute pass rate",
            "Add GitHub Actions workflow: runs eval on every PR, fails if pass rate drops >5% from baseline",
            "Deploy on Cloud Run or Railway with autoscaling",
            "Write runbook: how to debug a failing eval case",
        ],
        "must_haves": [
            "≥5 tools with Pydantic-validated input schemas",
            "LangGraph stateful agent (not simple chain)",
            "≥50 golden eval cases in a JSON/YAML file",
            "CI that fails on quality regression (GitHub Actions)",
            "Langfuse traces for every run",
            "Deployed and publicly accessible",
            "Runbook for debugging eval failures",
        ],
        "skills_demonstrated": ["Agent architecture", "Tool design", "Eval engineering", "CI/CD for AI", "Observability", "Deployment"],
        "interview_talking_point": "Explain your eval design — how do you catch regressions without flaky tests? What makes a good golden dataset?",
        "tags": ["LangGraph", "Langfuse", "Pydantic", "CI/CD", "Cloud Run", "evals"],
        "time_estimate": "~35–45 hours",
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
        ["Overview", "Beginner", "Intermediate", "Advanced", "Projects", "Interview Prep"],
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
        ["390", "15h", "6", "3"],
        ["Total hours", "Weekly target", "Projects", "Phases"],
    ):
        col.markdown(
            f'<div class="stat-box"><div class="stat-val">{val}</div><div class="stat-label">{label}</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown("### Month-by-month plan")

    months = [
        ("Month 1", "Math + Python toolchain", "~60h", "beginner"),
        ("Month 2", "Classical ML + EDA + Eval", "~65h", "beginner"),
        ("Month 3", "Neural nets + PyTorch", "~60h", "beginner"),
        ("Month 4", "DL arches + NLP + CV", "~70h", "intermediate"),
        ("Month 5", "Fine-tuning + RAG + LLMs", "~65h", "intermediate"),
        ("Month 6", "MLOps + Agents + Serving", "~70h", "advanced"),
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

