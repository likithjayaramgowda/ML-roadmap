import streamlit as st
import json
import random
import datetime

st.set_page_config(
    page_title="ML Engineer Roadmap — 6 Months to Tier-1",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

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

.stApp {
    background-color: #0D1117;
    background-image: radial-gradient(circle, #1a2332 1px, transparent 1px);
    background-size: 28px 28px;
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
        ["Overview", "Beginner", "Intermediate", "Advanced", "Projects", "Interview Prep", "AI Mentor"],
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
    st.markdown("# AI Mentor — ask me anything")
    st.caption("Powered by Claude. Ask about any topic in the roadmap.")

    col_clear, _ = st.columns([1, 5])
    with col_clear:
        if st.button("Clear chat"):
            st.session_state.messages = []
            st.rerun()

    # Display existing messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    if prompt := st.chat_input("Ask your ML mentor anything..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Check for API key
        api_key = None
        try:
            api_key = st.secrets.get("ANTHROPIC_API_KEY", None)
        except Exception:
            pass

        if not api_key or api_key == "your-key-here":
            st.warning(
                "No API key found. Add `ANTHROPIC_API_KEY = 'sk-...'` to `.streamlit/secrets.toml` to enable the AI Mentor.",
                icon="⚠️",
            )
        else:
            try:
                import anthropic

                client = anthropic.Anthropic(api_key=api_key)

                system_prompt = """You are an expert ML engineering mentor helping a student follow a 6-month roadmap to become a job-ready ML engineer at a tier-1 company.

The roadmap covers:
- Beginner (months 1-3): Math foundations, Python ML toolchain, Classical ML, Neural nets, PyTorch
- Intermediate (months 4-5): Deep learning architectures, Training at scale, NLP, HuggingFace, RAG, Fine-tuning LLMs
- Advanced (month 6): LLM internals, Inference serving, MLOps, Agent frameworks, Interview prep

Be concise, practical, and encouraging. When explaining concepts, use code examples where helpful. Always relate answers back to what they need to know for tier-1 ML engineering interviews."""

                with st.chat_message("assistant"):
                    with st.spinner("Thinking..."):
                        response = client.messages.create(
                            model="claude-haiku-4-5-20251001",
                            max_tokens=1024,
                            system=system_prompt,
                            messages=[
                                {"role": m["role"], "content": m["content"]}
                                for m in st.session_state.messages
                            ],
                        )
                        reply = response.content[0].text
                        st.markdown(reply)

                st.session_state.messages.append({"role": "assistant", "content": reply})

            except ImportError:
                st.error("The `anthropic` package is not installed. Run `pip install anthropic`.")
            except Exception as e:
                st.error(f"API error: {e}")

    st.markdown("---")
    st.caption("Add your API key to `.streamlit/secrets.toml` as `ANTHROPIC_API_KEY = 'sk-...'`")
