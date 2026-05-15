import streamlit as st
import streamlit.components.v1 as components
import json
import random
import datetime
import requests
import time as time_module


import re as _re

_TOPIC_RE = _re.compile(r'^[A-Za-z0-9_-]{3,64}$')

def _validate_topic(topic: str) -> str:
    """Return sanitized topic or raise ValueError."""
    topic = topic.strip()
    if not _TOPIC_RE.match(topic):
        raise ValueError("Topic must be 3–64 characters: letters, numbers, hyphens, underscores only.")
    return topic

def send_ntfy(topic: str, title: str, message: str, tags: list = None, priority: str = "default") -> bool:
    """Send a push notification via ntfy.sh — completely free, no auth needed."""
    try:
        topic = _validate_topic(topic)
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
    except ValueError:
        return False
    except Exception:
        return False

st.set_page_config(
    page_title="ML Engineer Roadmap — 6 Months to Tier-1",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

def render_animated_background():
    st.markdown("""
    <style>
    @keyframes drift1 {
        0%   { transform: translate(0px, 0px) scale(1); }
        33%  { transform: translate(60px, -40px) scale(1.08); }
        66%  { transform: translate(-30px, 50px) scale(0.95); }
        100% { transform: translate(0px, 0px) scale(1); }
    }
    @keyframes drift2 {
        0%   { transform: translate(0px, 0px) scale(1); }
        33%  { transform: translate(-70px, 50px) scale(1.05); }
        66%  { transform: translate(40px, -60px) scale(1.1); }
        100% { transform: translate(0px, 0px) scale(1); }
    }
    @keyframes drift3 {
        0%   { transform: translate(0px, 0px) scale(1); }
        50%  { transform: translate(50px, 60px) scale(1.06); }
        100% { transform: translate(0px, 0px) scale(1); }
    }
    @keyframes twinkle {
        0%, 100% { opacity: 0.15; }
        50%       { opacity: 0.55; }
    }
    @keyframes moveDots {
        0%   { background-position: 0px 0px, 40px 40px; }
        100% { background-position: 80px 80px, 120px 120px; }
    }

    /* Full screen fixed background layer */
    .stApp::before {
        content: '';
        position: fixed;
        inset: 0;
        z-index: 0;
        background: #020810;
        pointer-events: none;
    }

    /* Animated star dots */
    .stApp::after {
        content: '';
        position: fixed;
        inset: 0;
        z-index: 0;
        pointer-events: none;
        background-image:
            radial-gradient(1px 1px at 15% 20%, rgba(200,230,255,0.35) 0%, transparent 100%),
            radial-gradient(1px 1px at 72% 8%,  rgba(200,230,255,0.25) 0%, transparent 100%),
            radial-gradient(1px 1px at 45% 55%, rgba(200,230,255,0.3)  0%, transparent 100%),
            radial-gradient(1px 1px at 88% 35%, rgba(200,230,255,0.2)  0%, transparent 100%),
            radial-gradient(1px 1px at 30% 78%, rgba(200,230,255,0.3)  0%, transparent 100%),
            radial-gradient(1px 1px at 60% 90%, rgba(200,230,255,0.2)  0%, transparent 100%),
            radial-gradient(1px 1px at 5%  60%, rgba(200,230,255,0.25) 0%, transparent 100%),
            radial-gradient(1px 1px at 93% 72%, rgba(200,230,255,0.2)  0%, transparent 100%),
            radial-gradient(1px 1px at 50% 30%, rgba(200,230,255,0.3)  0%, transparent 100%),
            radial-gradient(1px 1px at 22% 45%, rgba(200,230,255,0.2)  0%, transparent 100%),
            radial-gradient(1px 1px at 78% 60%, rgba(200,230,255,0.25) 0%, transparent 100%),
            radial-gradient(1.5px 1.5px at 35% 15%, rgba(93,202,165,0.4) 0%, transparent 100%),
            radial-gradient(1.5px 1.5px at 65% 80%, rgba(55,138,221,0.35) 0%, transparent 100%),
            radial-gradient(2px 2px at 10% 90%,  rgba(93,202,165,0.3) 0%, transparent 100%),
            radial-gradient(2px 2px at 90% 15%,  rgba(55,138,221,0.3) 0%, transparent 100%);
        animation: twinkle 4s ease-in-out infinite alternate;
    }

    /* Aurora blob 1 — teal, top left */
    #aurora1 {
        position: fixed;
        top: -10vh; left: -10vw;
        width: 65vw; height: 60vh;
        border-radius: 50%;
        background: radial-gradient(ellipse at center,
            rgba(93,202,165,0.055) 0%,
            rgba(93,202,165,0.02) 45%,
            transparent 70%);
        pointer-events: none;
        z-index: 0;
        animation: drift1 18s ease-in-out infinite;
        filter: blur(40px);
    }

    /* Aurora blob 2 — blue, right side */
    #aurora2 {
        position: fixed;
        top: 20vh; right: -15vw;
        width: 60vw; height: 70vh;
        border-radius: 50%;
        background: radial-gradient(ellipse at center,
            rgba(55,138,221,0.05) 0%,
            rgba(55,138,221,0.018) 45%,
            transparent 70%);
        pointer-events: none;
        z-index: 0;
        animation: drift2 22s ease-in-out infinite;
        filter: blur(50px);
    }

    /* Aurora blob 3 — purple, bottom */
    #aurora3 {
        position: fixed;
        bottom: -20vh; left: 20vw;
        width: 70vw; height: 55vh;
        border-radius: 50%;
        background: radial-gradient(ellipse at center,
            rgba(127,119,221,0.045) 0%,
            rgba(127,119,221,0.015) 45%,
            transparent 70%);
        pointer-events: none;
        z-index: 0;
        animation: drift3 25s ease-in-out infinite;
        filter: blur(45px);
    }

    /* Neural dot grid — subtle moving pattern */
    #neural-grid {
        position: fixed;
        inset: 0;
        z-index: 0;
        pointer-events: none;
        background-image:
            radial-gradient(circle, rgba(93,202,165,0.08) 1px, transparent 1px),
            radial-gradient(circle, rgba(55,138,221,0.05) 1px, transparent 1px);
        background-size: 80px 80px, 130px 130px;
        animation: moveDots 12s linear infinite;
        opacity: 0.6;
    }

    /* Make sure ALL content sits above background */
    .stApp {
        background: #020810 !important;
    }
    section[data-testid="stMain"],
    .main .block-container {
        position: relative !important;
        z-index: 2 !important;
        background: transparent !important;
    }
    section[data-testid="stSidebar"] {
        position: relative !important;
        z-index: 100 !important;
        background: rgba(2,8,16,0.92) !important;
        backdrop-filter: blur(14px) !important;
        border-right: 1px solid rgba(93,202,165,0.08) !important;
    }
    header[data-testid="stHeader"] {
        position: relative !important;
        z-index: 100 !important;
        background: rgba(2,8,16,0.7) !important;
        backdrop-filter: blur(10px) !important;
    }
    </style>

    <!-- Aurora blobs injected as real DOM elements — no iframe -->
    <div id="aurora1"></div>
    <div id="aurora2"></div>
    <div id="aurora3"></div>
    <div id="neural-grid"></div>
    """, unsafe_allow_html=True)

def render_floating_chatbot():
    groq_key = ""
    try:
        groq_key = st.secrets.get("GROQ_API_KEY", "")
    except:
        pass

    components.html(f"""
<!DOCTYPE html>
<html>
<head>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{background:transparent;overflow:hidden;font-family:-apple-system,BlinkMacSystemFont,sans-serif}}
#bbl{{
  position:fixed;bottom:24px;right:24px;width:54px;height:54px;
  border-radius:50%;background:linear-gradient(135deg,#5DCAA5,#378ADD);
  display:flex;align-items:center;justify-content:center;cursor:pointer;
  box-shadow:0 0 0 0 rgba(93,202,165,0.5);
  animation:pulse 2.5s ease-in-out infinite;z-index:999;transition:transform .2s;
}}
@keyframes pulse{{
  0%{{box-shadow:0 0 0 0 rgba(93,202,165,0.5)}}
  70%{{box-shadow:0 0 0 14px rgba(93,202,165,0)}}
  100%{{box-shadow:0 0 0 0 rgba(93,202,165,0)}}
}}
#bbl:hover{{transform:scale(1.1)}}
#bbl svg{{width:25px;height:25px;fill:white}}
#win{{
  position:fixed;bottom:88px;right:24px;width:345px;height:490px;
  background:#0D1117;border:1px solid #30363D;border-radius:16px;
  display:none;flex-direction:column;
  box-shadow:0 25px 80px rgba(0,0,0,0.85),0 0 50px rgba(93,202,165,0.08);
  z-index:998;overflow:hidden;
}}
#win.open{{display:flex;animation:slideUp .25s ease}}
@keyframes slideUp{{from{{opacity:0;transform:translateY(16px)}}to{{opacity:1;transform:translateY(0)}}}}
#hdr{{
  padding:13px 15px;flex-shrink:0;
  background:linear-gradient(135deg,#0d2137 0%,#0D1117 100%);
  border-bottom:1px solid #21262D;
  display:flex;align-items:center;justify-content:space-between;
}}
.hl{{display:flex;align-items:center;gap:9px}}
.av{{width:32px;height:32px;border-radius:50%;background:linear-gradient(135deg,#5DCAA5,#378ADD);display:flex;align-items:center;justify-content:center;font-size:15px}}
.tt{{color:#E6EDF3;font-size:13px;font-weight:600}}
.sb{{color:#5DCAA5;font-size:10px;margin-top:1px}}
.cl{{color:#7D8590;cursor:pointer;font-size:22px;line-height:1;padding:2px 6px;border-radius:4px}}
.cl:hover{{color:#E6EDF3;background:#21262D}}
#msgs{{flex:1;overflow-y:auto;padding:12px;display:flex;flex-direction:column;gap:8px;scrollbar-width:thin;scrollbar-color:#30363D transparent}}
.m{{max-width:87%;padding:8px 12px;border-radius:11px;font-size:12.5px;line-height:1.55;word-wrap:break-word}}
.u{{background:#1F6FEB22;border:1px solid #1F6FEB55;color:#E6EDF3;align-self:flex-end;border-bottom-right-radius:3px}}
.b{{background:#161B22;border:1px solid #30363D;color:#C9D1D9;align-self:flex-start;border-bottom-left-radius:3px}}
.t{{color:#7D8590;font-style:italic}}
.qw{{display:flex;flex-wrap:wrap;gap:5px;padding:0 12px 10px;flex-shrink:0}}
.qb{{font-size:10.5px;padding:3px 10px;background:#21262D;border:1px solid #30363D;border-radius:99px;color:#8B949E;cursor:pointer;transition:all .15s;white-space:nowrap}}
.qb:hover{{background:#2D333B;color:#E6EDF3;border-color:#5DCAA5}}
#ia{{padding:10px 12px;border-top:1px solid #21262D;display:flex;gap:7px;flex-shrink:0;background:#0a0f14}}
#inp{{flex:1;background:#21262D;border:1px solid #30363D;border-radius:8px;color:#E6EDF3;padding:7px 11px;font-size:12px;outline:none;resize:none;height:36px;font-family:inherit}}
#inp:focus{{border-color:#5DCAA5;box-shadow:0 0 0 2px rgba(93,202,165,0.1)}}
#inp::placeholder{{color:#7D8590}}
#snd{{width:36px;height:36px;border-radius:8px;background:linear-gradient(135deg,#5DCAA5,#378ADD);border:none;cursor:pointer;display:flex;align-items:center;justify-content:center;flex-shrink:0;transition:opacity .2s}}
#snd:hover{{opacity:0.85}}
#snd svg{{width:15px;height:15px;fill:white}}
</style>
</head>
<body>
<div id="bbl" onclick="tog()">
  <svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.03 2 11c0 2.7 1.26 5.12 3.28 6.79L4 22l4.5-1.96C9.6 20.65 10.77 21 12 21c5.52 0 10-4.03 10-9S17.52 2 12 2z"/></svg>
</div>
<div id="win">
  <div id="hdr">
    <div class="hl">
      <div class="av">🧠</div>
      <div><div class="tt">ML Mentor</div><div class="sb">● online · roadmap-scoped</div></div>
    </div>
    <div class="cl" onclick="tog()">×</div>
  </div>
  <div id="msgs">
    <div class="m b">Hey Likith! 👋 Ask me anything about the roadmap — concepts, projects, interview prep, or study planning.</div>
  </div>
  <div class="qw" id="qw">
    <span class="qb" onclick="sq('Explain LoRA mathematically')">LoRA math</span>
    <span class="qb" onclick="sq('What to do in week 1?')">Week 1 plan</span>
    <span class="qb" onclick="sq('Walk me through tabular-baseline project')">tabular-baseline</span>
    <span class="qb" onclick="sq('Explain KV cache and why it matters')">KV cache</span>
    <span class="qb" onclick="sq('Quiz me on transformer attention')">Quiz me ⚡</span>
  </div>
  <div id="ia">
    <textarea id="inp" placeholder="Ask your ML mentor..."></textarea>
    <button id="snd" onclick="send()">
      <svg viewBox="0 0 24 24"><path d="M2 21l21-9L2 3v7l15 2-15 2v7z"/></svg>
    </button>
  </div>
</div>
<script>
const KEY="{groq_key}";
const SYS=`You are an ML roadmap mentor for Likith. ONLY answer questions about this 6-month ML Engineer Roadmap. Refuse anything outside it with: "I can only help with the ML roadmap topics!" Roadmap: Math (linear algebra, calculus, probability), Python toolchain (numpy, pandas, sklearn, mlflow, wandb), Classical ML (regression, trees, XGBoost, LightGBM, clustering, PCA), Neural nets+PyTorch (backprop, optimizers, training loop, DataLoader), Deep Learning (CNNs ResNet, LSTMs, Transformers self-attention RoPE, ViT, Diffusion), Training at scale (mixed precision, DDP, FSDP, DeepSpeed, Accelerate), HuggingFace (tokenization, AutoModel, peft LoRA QLoRA, trl SFT DPO GRPO), RAG (chunking, qdrant, hybrid BM25+dense, reranking, ragas), LLM internals (Flash Attention, KV cache, quantization GPTQ AWQ, speculative decoding), vllm serving, MLOps (DVC, mlflow, drift Evidently, Langfuse), Agents (LangGraph, MCP, guardrails). Projects: tabular-baseline, mnist-from-scratch-then-torch, rag-on-your-docs, qlora-domain-tune, prod-llm-platform, agent-with-evals. Be concise under 250 words, practical, use short code examples.`;
let msgs=[],isOpen=false;
function tog(){{isOpen=!isOpen;document.getElementById('win').classList.toggle('open',isOpen);if(isOpen)document.getElementById('inp').focus();}}
function sq(t){{document.getElementById('inp').value=t;send();}}
function send(){{
  const el=document.getElementById('inp');
  const txt=el.value.trim();if(!txt)return;
  el.value='';add(txt,'u');msgs.push({{role:'user',content:txt}});
  document.getElementById('qw').style.display='none';
  const th=add('Thinking...','b t');
  if(!KEY){{th.remove();add('⚠️ Add GROQ_API_KEY to Streamlit secrets.','b');return;}}
  fetch('https://api.groq.com/openai/v1/chat/completions',{{
    method:'POST',
    headers:{{'Content-Type':'application/json','Authorization':'Bearer '+KEY}},
    body:JSON.stringify({{model:'llama-3.3-70b-versatile',max_tokens:500,
      messages:[{{role:'system',content:SYS}},...msgs]}})
  }}).then(r=>r.json()).then(d=>{{
    th.remove();
    const rep=d.choices?.[0]?.message?.content||'Something went wrong, try again.';
    add(rep,'b');msgs.push({{role:'assistant',content:rep}});
  }}).catch(()=>{{th.remove();add('Network error. Check connection.','b');}});
}}
function add(txt,cls){{
  const el=document.createElement('div');el.className='m '+cls;el.textContent=txt;
  const c=document.getElementById('msgs');c.appendChild(el);c.scrollTop=c.scrollHeight;return el;
}}
document.getElementById('inp').addEventListener('keydown',e=>{{
  if(e.key==='Enter'&&!e.shiftKey){{e.preventDefault();send();}};
}});
</script>
</body>
</html>
    """, height=560, scrolling=False)

render_animated_background()
render_floating_chatbot()

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

# ── CSS ─────────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg-deep:   #020810;
    --bg-card:   #161B22;
    --bg-raised: #1C2128;
    --border:    #21262D;
    --border-hi: #30363D;
    --text-hi:   #E6EDF3;
    --text-mid:  #C9D1D9;
    --text-lo:   #8B949E;
    --teal:      #5DCAA5;
    --blue:      #378ADD;
    --purple:    #7F77DD;
    --r:         12px;
    --r-sm:      8px;
}

html, body, [class*="css"] { font-family: 'Outfit', sans-serif; }

section[data-testid="stAppViewContainer"] { background: transparent !important; }
section[data-testid="stAppViewContainer"] > div:first-child { background: transparent !important; }
.stApp { background: var(--bg-deep) !important; }

.main .block-container {
    padding-top: 1.5rem;
    padding-bottom: 3rem;
    max-width: 1100px;
}

/* ─── Cards ──────────────────────────────────── */
.card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--r);
    padding: 1rem 1.2rem;
    margin-bottom: .75rem;
    transition: border-color .2s, box-shadow .2s;
}
.card:hover { border-color: var(--border-hi); box-shadow: 0 4px 20px rgba(0,0,0,.35); }

/* ─── Phase pills ─────────────────────────── */
.phase-header { display: flex; align-items: center; gap: 12px; margin: 1.5rem 0 1rem; }
.phase-pill {
    font-size: 10px; font-weight: 700;
    padding: 5px 16px; border-radius: 99px;
    letter-spacing: .12em; text-transform: uppercase;
    background: transparent; border: 1.5px solid;
    display: inline-block;
    font-family: 'Outfit', sans-serif;
}

/* ─── Section divider ─────────────────────── */
.section-divider {
    font-size: 10px; font-weight: 700; color: var(--text-lo);
    letter-spacing: .1em; text-transform: uppercase;
    margin: 1.4rem 0 .6rem;
    padding: 0 0 6px 10px;
    border-bottom: 1px solid var(--border);
    position: relative;
}
.section-divider::before {
    content: ''; position: absolute; left: 0; top: 0;
    width: 3px; height: 14px;
    background: var(--teal); border-radius: 2px;
}

/* ─── Topics ────────────────────────────────── */
.topic-row {
    display: grid; grid-template-columns: 1.6fr 1fr;
    border-bottom: 1px solid var(--border); padding: 8px 0;
    align-items: center; gap: 12px;
}
.topic-name { font-size: 13.5px; font-weight: 500; color: var(--text-hi); }
.topic-sub  { font-size: 11px; color: var(--text-lo); margin-top: 2px; }

/* ─── Resource badge ──────────────────────── */
.res-badge {
    display: inline-flex; align-items: center; gap: 6px;
    font-size: 12px; padding: 4px 10px; border-radius: 6px;
    text-decoration: none; font-weight: 500; width: fit-content;
    transition: filter .15s, transform .1s;
}
.res-badge:hover { filter: brightness(1.18); transform: translateY(-1px); }

/* ─── Project cards ───────────────────────── */
.proj-card {
    border: 1px solid var(--border); border-radius: var(--r);
    padding: 1rem 1.2rem; margin-bottom: .75rem;
    background: var(--bg-card);
    transition: border-color .2s, box-shadow .2s, transform .15s;
}
.proj-card:hover {
    border-color: var(--teal);
    box-shadow: 0 4px 24px rgba(93,202,165,.12);
    transform: translateY(-1px);
}
.proj-title { font-size: 15px; font-weight: 600; margin-bottom: 4px; color: var(--text-hi); }
.proj-desc  { font-size: 13px; color: var(--text-lo); line-height: 1.55; margin-bottom: 8px; }

/* ─── Tags ──────────────────────────────────────── */
.tag {
    display: inline-block; font-size: 11px; padding: 2px 8px;
    border-radius: 4px; background: var(--bg-raised); color: var(--text-lo);
    margin-right: 4px; margin-bottom: 2px;
    font-family: 'JetBrains Mono', monospace;
    border: 1px solid var(--border);
}

/* ─── Milestones ─────────────────────────────── */
.milestone-item {
    font-size: 13px; color: var(--text-mid); padding: 5px 0;
    border-bottom: 1px solid var(--border); display: flex; gap: 8px; align-items: flex-start;
}

/* ─── Interview Q-cards ───────────────────── */
.q-card {
    background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--r);
    padding: 10px 14px; font-size: 13px; color: var(--text-mid);
    margin-bottom: 6px;
    transition: border-color .2s, box-shadow .2s;
}
.q-card:hover { border-color: var(--blue); box-shadow: 0 2px 12px rgba(55,138,221,.1); }

/* ─── Mental model cards ──────────────────── */
.mental-card {
    border: 1px solid var(--border); border-radius: var(--r);
    padding: .85rem 1rem; margin-bottom: .6rem;
    background: var(--bg-card);
    transition: border-color .2s, box-shadow .2s;
}
.mental-card:hover { border-color: var(--purple); box-shadow: 0 2px 16px rgba(127,119,221,.1); }
.mental-title { font-size: 14px; font-weight: 600; color: var(--text-hi); margin-bottom: 3px; }
.mental-body  { font-size: 13px; color: var(--text-lo); line-height: 1.5; }

/* ─── Stat boxes ─────────────────────────────── */
.stat-box {
    background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--r);
    padding: 1rem; text-align: center;
    transition: border-color .2s, box-shadow .2s, transform .15s;
}
.stat-box:hover {
    border-color: var(--teal);
    box-shadow: 0 4px 20px rgba(93,202,165,.1);
    transform: translateY(-2px);
}
.stat-val   { font-size: 28px; font-weight: 700; color: var(--text-hi); }
.stat-label { font-size: 12px; color: var(--text-lo); margin-top: 2px; letter-spacing: .03em; }

/* ─── Progress ring (big %) ─────────────────── */
.progress-ring-card {
    background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--r);
    padding: 2rem 1.2rem; text-align: center; margin-bottom: 1rem;
    position: relative; overflow: hidden;
}
.progress-ring-card::before {
    content: ''; position: absolute; inset: 0;
    background: radial-gradient(circle at 50% 0%, rgba(93,202,165,.06) 0%, transparent 65%);
    pointer-events: none;
}
.progress-pct {
    font-size: 72px; font-weight: 700; color: var(--teal); line-height: 1;
    text-shadow: 0 0 40px rgba(93,202,165,.35);
    position: relative; z-index: 1;
}
.progress-sub { font-size: 14px; color: var(--text-lo); margin-top: 8px; position: relative; z-index: 1; }

/* ─── Quote card ──────────────────────────────── */
.quote-card {
    background: var(--bg-card); border: 1px solid var(--border);
    border-left: 3px solid var(--teal); border-radius: var(--r);
    padding: 1rem 1.2rem; margin-bottom: 1.2rem;
}
.quote-label { font-size: 10px; font-weight: 700; color: var(--teal); letter-spacing: .08em; text-transform: uppercase; margin-bottom: 8px; }
.quote-text  { font-size: 16px; font-style: italic; color: var(--text-hi); line-height: 1.6; }
.quote-author { font-size: 13px; color: var(--text-lo); margin-top: 6px; }

/* ─── Tip box ───────────────────────────────────── */
.tip-box {
    background: var(--bg-card); border: 1px solid var(--border);
    border-left: 3px solid var(--blue); border-radius: var(--r);
    padding: .75rem 1rem; margin-bottom: 1rem;
    font-size: 13px; color: var(--text-mid); line-height: 1.5;
}

/* ─── Phase progress bars (custom HTML) ─────────── */
@keyframes shimmer {
    0%   { background-position: -200% center; }
    100% { background-position:  200% center; }
}
.phase-bar-wrap  { display: flex; align-items: center; gap: 12px; margin-bottom: 10px; }
.phase-bar-label { font-size: 13px; font-weight: 600; min-width: 100px; }
.phase-bar-track { flex: 1; background: var(--border); border-radius: 99px; height: 10px; overflow: hidden; }
.phase-bar-fill  { height: 10px; border-radius: 99px; background-size: 200% auto; animation: shimmer 2.5s linear infinite; }
.phase-bar-count { font-size: 12px; color: var(--text-lo); min-width: 90px; text-align: right; }

/* ─── Native st.progress styling ──────────────── */
div[data-testid="stProgress"] { padding: 0 !important; }
div[data-testid="stProgress"] > div {
    background: var(--border) !important; border-radius: 99px !important;
    height: 6px !important; overflow: hidden !important;
}
div[data-testid="stProgress"] > div > div {
    background: linear-gradient(90deg, var(--teal) 0%, var(--blue) 100%) !important;
    border-radius: 99px !important;
    box-shadow: 0 0 6px rgba(93,202,165,.4) !important;
}

/* ─── Month cards ─────────────────────────────── */
.month-card {
    border-radius: 0 var(--r) var(--r) 0;
    background: var(--bg-card); margin-bottom: .75rem;
    padding: .75rem 1rem; border: 1px solid var(--border);
    transition: transform .15s;
}
.month-card:hover { transform: translateX(2px); }

/* ─── Sidebar nav ─────────────────────────────── */
section[data-testid="stSidebar"] .stRadio > div {
    display: flex; flex-direction: column; gap: 2px;
}
section[data-testid="stSidebar"] .stRadio label {
    display: flex !important; align-items: center !important;
    padding: 8px 12px !important; border-radius: 8px !important;
    font-size: 13px !important; font-weight: 500 !important;
    color: var(--text-lo) !important; cursor: pointer !important;
    transition: background .15s, color .15s, border-color .15s !important;
    border: 1px solid transparent !important;
    margin: 0 !important;
}
section[data-testid="stSidebar"] .stRadio label:hover {
    background: var(--bg-card) !important; color: var(--text-hi) !important;
}
section[data-testid="stSidebar"] .stRadio label:has(input:checked) {
    background: rgba(93,202,165,.08) !important;
    color: var(--teal) !important;
    border-color: rgba(93,202,165,.2) !important;
}
section[data-testid="stSidebar"] [data-baseweb="radio"] > div:first-child,
section[data-testid="stSidebar"] .stRadio label > span:first-child { display: none !important; }

/* ─── Buttons ───────────────────────────────────── */
.stButton > button {
    border-radius: var(--r-sm) !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 500 !important;
}

/* ─── Mobile ──────────────────────────────────────── */
@media (max-width: 768px) {
    .topic-row { grid-template-columns: 1fr; gap: 6px; }
    .main .block-container { padding-left: 1rem; padding-right: 1rem; }
    .phase-bar-count { display: none; }
    .stat-val { font-size: 20px; }
    .progress-pct { font-size: 52px; }
    div[data-testid="stIFrame"]:nth-of-type(2) iframe { width: 100vw !important; max-width: 380px !important; }
}
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
    st.markdown("""
    <div style="padding:.25rem 0 1rem;border-bottom:1px solid #21262D;margin-bottom:.5rem;">
        <div style="font-size:17px;font-weight:700;color:#E6EDF3;display:flex;align-items:center;gap:8px;font-family:'Outfit',sans-serif;">
            🧠 ML Roadmap
        </div>
        <div style="font-size:11px;color:#8B949E;margin-top:3px;letter-spacing:.03em;">
            6 months · Tier-1 Engineer
        </div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Navigate",
        ["Overview", "Beginner", "Intermediate", "Advanced", "Projects", "Interview Prep", "Notifications"],
        label_visibility="collapsed",
    )

    b_done, b_total = _phase_progress("beginner")
    i_done, i_total = _phase_progress("intermediate")
    a_done, a_total = _phase_progress("advanced")
    b_pct = int(b_done / b_total * 100) if b_total else 0
    i_pct = int(i_done / i_total * 100) if i_total else 0
    a_pct = int(a_done / a_total * 100) if a_total else 0

    st.markdown(f"""
    <div style="border-top:1px solid #21262D;padding-top:.75rem;margin-top:.25rem;">
        <div style="font-size:9px;font-weight:700;color:#8B949E;letter-spacing:.1em;margin-bottom:8px;">PROGRESS</div>
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:10px;">
            <div style="flex:1;background:#21262D;border-radius:99px;height:5px;overflow:hidden;">
                <div style="width:{pct_total}%;background:linear-gradient(90deg,#5DCAA5,#378ADD);height:5px;border-radius:99px;box-shadow:0 0 6px rgba(93,202,165,.5);"></div>
            </div>
            <span style="font-size:11px;color:#5DCAA5;font-weight:700;min-width:30px;text-align:right;">{pct_total}%</span>
        </div>
        <div style="display:flex;flex-direction:column;gap:5px;margin-bottom:12px;">
            <div style="display:flex;align-items:center;gap:6px;">
                <span style="font-size:9px;color:#5DCAA5;min-width:64px;font-weight:700;letter-spacing:.05em;">BEGINNER</span>
                <div style="flex:1;background:#21262D;border-radius:99px;height:3px;overflow:hidden;">
                    <div style="width:{b_pct}%;background:#5DCAA5;height:3px;border-radius:99px;"></div>
                </div>
                <span style="font-size:9px;color:#8B949E;min-width:22px;text-align:right;">{b_pct}%</span>
            </div>
            <div style="display:flex;align-items:center;gap:6px;">
                <span style="font-size:9px;color:#378ADD;min-width:64px;font-weight:700;letter-spacing:.05em;">INTER</span>
                <div style="flex:1;background:#21262D;border-radius:99px;height:3px;overflow:hidden;">
                    <div style="width:{i_pct}%;background:#378ADD;height:3px;border-radius:99px;"></div>
                </div>
                <span style="font-size:9px;color:#8B949E;min-width:22px;text-align:right;">{i_pct}%</span>
            </div>
            <div style="display:flex;align-items:center;gap:6px;">
                <span style="font-size:9px;color:#7F77DD;min-width:64px;font-weight:700;letter-spacing:.05em;">ADVANCED</span>
                <div style="flex:1;background:#21262D;border-radius:99px;height:3px;overflow:hidden;">
                    <div style="width:{a_pct}%;background:#7F77DD;height:3px;border-radius:99px;"></div>
                </div>
                <span style="font-size:9px;color:#8B949E;min-width:22px;text-align:right;">{a_pct}%</span>
            </div>
        </div>
        <div style="font-size:11px;color:#8B949E;line-height:1.9;border-top:1px solid #21262D;padding-top:.6rem;">
            <div>⏱&nbsp; 2h/day weekdays</div>
            <div>📅&nbsp; 3–4h Saturday</div>
            <div style="color:#5DCAA5;margin-top:4px;font-size:10px;">↓ Tick topics as you finish</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

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
    pill_style = f"color:{phase['color']};border-color:{phase['color']};box-shadow:0 0 14px {phase['color']}44;"

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
    st.markdown(
        f'<div style="margin:.25rem 0 1.2rem;">'
        f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">'
        f'<span style="font-size:10px;font-weight:700;color:#8B949E;letter-spacing:.08em;">PHASE PROGRESS</span>'
        f'<span style="font-size:11px;font-weight:700;color:{phase["color"]}">{p_pct}%</span>'
        f'</div>'
        f'<div style="background:#21262D;border-radius:99px;height:8px;overflow:hidden;">'
        f'<div style="width:{p_pct}%;height:8px;border-radius:99px;'
        f'background:linear-gradient(90deg,{phase["color"]}88,{phase["color"]});'
        f'box-shadow:0 0 8px {phase["color"]}66;"></div>'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

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
            f'<div class="phase-bar-wrap">'
            f'<span class="phase-bar-label" style="color:{color}">{label}</span>'
            f'<div class="phase-bar-track">'
            f'<div class="phase-bar-fill" style="width:{pp}%;'
            f'background:linear-gradient(90deg,{color}77 0%,{color} 50%,{color}77 100%);'
            f'box-shadow:0 0 8px {color}66;"></div>'
            f'</div>'
            f'<span class="phase-bar-count">{pd} / {pt} done</span>'
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
        pill_style = f"color:{phase['color']};border-color:{phase['color']};box-shadow:0 0 14px {phase['color']}44;"
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

elif page == "AI Mentor":
    st.markdown("# AI Mentor")
    st.caption("Powered by Groq (llama-3.3-70b) — roadmap-scoped. API call stays on the server; your key is never sent to the browser.")

    col_clear, _ = st.columns([1, 5])
    with col_clear:
        if st.button("Clear chat"):
            st.session_state.messages = []
            st.rerun()

    if not st.session_state.messages:
        st.markdown("**Try asking:**")
        starter_qs = [
            "Explain how LoRA works mathematically",
            "Help me debug my PyTorch training loop — loss isn't decreasing",
            "What should I focus on in week 1?",
            "Walk me through the tabular-baseline project step by step",
            "What's the difference between DDP and FSDP?",
            "How do I know if my RAG pipeline has data leakage?",
            "Quiz me on transformer attention",
        ]
        cols = st.columns(2)
        for i, q in enumerate(starter_qs):
            if cols[i % 2].button(q, key=f"starter_{i}"):
                st.session_state.messages.append({"role": "user", "content": q})
                st.rerun()

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ask your ML mentor anything..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        api_key = None
        try:
            api_key = st.secrets.get("GROQ_API_KEY", None)
        except Exception:
            pass

        if not api_key:
            st.warning("No API key found. Add `GROQ_API_KEY = 'gsk_...'` to `.streamlit/secrets.toml`.", icon="⚠️")
        else:
            try:
                from groq import Groq
                client = Groq(api_key=api_key)
                with st.chat_message("assistant"):
                    with st.spinner("Thinking..."):
                        response = client.chat.completions.create(
                            model="llama-3.3-70b-versatile",
                            max_tokens=1024,
                            messages=[{"role": "system", "content": SYSTEM_PROMPT}] +
                                     [{"role": m["role"], "content": m["content"]}
                                      for m in st.session_state.messages],
                        )
                        reply = response.choices[0].message.content
                        st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except ImportError:
                st.error("The `groq` package is not installed. Run `pip install groq`.")
            except Exception as e:
                st.error(f"API error: {e}")

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
        if not _TOPIC_RE.match(topic.strip()):
            st.error("Topic must be 3–64 characters: letters, numbers, hyphens, and underscores only. No spaces or special characters.")
            topic = ""
        else:
            topic = topic.strip()
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
        <div style="background:#161B22; border:1px solid #21262D; border-left: 4px solid #5DCAA5;
                    border-radius:12px; padding:1rem 1.2rem; font-family:'Outfit',sans-serif;">
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

