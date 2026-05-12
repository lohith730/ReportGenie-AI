"""
╔══════════════════════════════════════════════════════════════╗
║          ReportGenie AI  —  Full-Stack AI Analytics          ║
║  Powered by Google Gemini API (FREE - no credit card needed) ║
║  Get FREE key: https://aistudio.google.com/app/apikey        ║
╚══════════════════════════════════════════════════════════════╝

INSTALL:
    pip install streamlit pandas numpy plotly google-generativeai scikit-learn

RUN:
    streamlit run reportgenie_ai.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import json, re, warnings, io, base64, time
from datetime import datetime, timedelta
from collections import defaultdict
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

warnings.filterwarnings("ignore")

# ─── HARDCODED FREE API KEY ────────────────────────────────────────────────────
DEFAULT_API_KEY = "AIzaSyCAgFIsFWPgK6HqJiVq2qwBdb-u73CxDO8"

# ─── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ReportGenie AI",
    page_icon="🧞",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ══════════════════════════════════════════════════════════════════════════════
# GLOBAL CSS — Dark premium theme
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@300;400;500&family=Outfit:wght@300;400;500;600&display=swap');

:root {
  --bg0:#02040a; --bg1:#060d18; --bg2:#0a1525; --bg3:#0e1c30; --bg4:#121f32;
  --bd:#1a2d45; --bd2:#1f3555; --bd3:#263f65;
  --blue:#3b82f6; --cyan:#06b6d4; --violet:#8b5cf6; --emerald:#10b981;
  --amber:#f59e0b; --rose:#f43f5e; --purple:#a855f7; --pink:#ec4899; --sky:#38bdf8;
  --t0:#e8f4ff; --t1:#7eb0d4; --t2:#3a5a78; --t3:#1e3347;
  --glow-blue:rgba(59,130,246,0.18); --glow-cyan:rgba(6,182,212,0.15);
}

*, *::before, *::after { box-sizing: border-box; }
html, body, .stApp { background-color:var(--bg0) !important; font-family:'Outfit',sans-serif; color:var(--t0); }
section[data-testid="stSidebar"] {
  background:linear-gradient(180deg,var(--bg1) 0%,var(--bg0) 100%) !important;
  border-right:1px solid var(--bd) !important;
}
section[data-testid="stSidebar"] * { color:var(--t0) !important; }
#MainMenu, footer, header { visibility:hidden; }
.block-container { padding:1.2rem 1.8rem !important; max-width:100% !important; }

/* ── HEADER ── */
.rg-header {
  background:linear-gradient(135deg,var(--bg1) 0%,var(--bg2) 60%,var(--bg1) 100%);
  border:1px solid var(--bd); border-radius:18px;
  padding:22px 28px; margin-bottom:22px;
  display:flex; align-items:center; gap:18px;
  position:relative; overflow:hidden;
}
.rg-header::before {
  content:''; position:absolute; top:0; left:0; right:0; height:3px;
  background:linear-gradient(90deg,var(--blue),var(--cyan),var(--violet),var(--emerald));
}
.rg-header::after {
  content:''; position:absolute; top:-80px; right:-80px;
  width:200px; height:200px; border-radius:50%;
  background:radial-gradient(circle,rgba(59,130,246,0.08) 0%,transparent 70%);
}
.rg-logo {
  width:52px; height:52px;
  background:linear-gradient(135deg,var(--blue),var(--violet));
  border-radius:14px; display:flex; align-items:center; justify-content:center;
  font-size:26px; box-shadow:0 0 30px rgba(59,130,246,0.4); flex-shrink:0;
}
.rg-title {
  font-family:'Syne',sans-serif; font-size:28px; font-weight:800;
  background:linear-gradient(135deg,var(--t0),var(--cyan));
  -webkit-background-clip:text; -webkit-text-fill-color:transparent;
  letter-spacing:-0.5px; line-height:1;
}
.rg-sub {
  font-family:'JetBrains Mono',monospace; font-size:10px; color:var(--t2);
  letter-spacing:1.5px; text-transform:uppercase; margin-top:4px;
}
.rg-badge {
  margin-left:auto; text-align:right;
  background:rgba(16,185,129,0.08); border:1px solid rgba(16,185,129,0.25);
  border-radius:10px; padding:8px 14px;
}
.rg-badge-top { font-family:'JetBrains Mono',monospace; font-size:9px; color:var(--t2); letter-spacing:1px; }
.rg-badge-val { font-family:'Syne',sans-serif; font-size:13px; font-weight:700; color:var(--emerald); margin-top:2px; }

/* ── CARDS ── */
.glass-card {
  background:var(--bg3); border:1px solid var(--bd);
  border-radius:16px; padding:20px;
  position:relative; overflow:hidden;
}
.glass-card::before {
  content:''; position:absolute; top:0; left:0; right:0; height:2px;
  border-radius:16px 16px 0 0;
}
.glass-card.blue::before  { background:linear-gradient(90deg,var(--blue),var(--cyan)); }
.glass-card.violet::before { background:linear-gradient(90deg,var(--violet),var(--blue)); }
.glass-card.green::before  { background:linear-gradient(90deg,var(--emerald),var(--cyan)); }
.glass-card.amber::before  { background:linear-gradient(90deg,var(--amber),var(--rose)); }
.glass-card.rose::before   { background:linear-gradient(90deg,var(--rose),var(--pink)); }
.glass-card.purple::before { background:linear-gradient(90deg,var(--purple),var(--violet)); }

/* ── KPI CARDS ── */
.kpi-row { display:grid; grid-template-columns:repeat(auto-fill,minmax(185px,1fr)); gap:12px; margin-bottom:22px; }
.kpi-c {
  background:var(--bg4); border:1px solid var(--bd);
  border-radius:14px; padding:16px 18px;
  position:relative; overflow:hidden; cursor:default;
  transition:border-color 0.2s,transform 0.15s;
}
.kpi-c:hover { border-color:var(--bd2); transform:translateY(-1px); }
.kpi-c::after { content:''; position:absolute; bottom:0; left:0; right:0; height:2px; }
.c-blue::after   { background:linear-gradient(90deg,var(--blue),transparent); }
.c-cyan::after   { background:linear-gradient(90deg,var(--cyan),transparent); }
.c-violet::after { background:linear-gradient(90deg,var(--violet),transparent); }
.c-green::after  { background:linear-gradient(90deg,var(--emerald),transparent); }
.c-amber::after  { background:linear-gradient(90deg,var(--amber),transparent); }
.c-rose::after   { background:linear-gradient(90deg,var(--rose),transparent); }
.kpi-icon { position:absolute; top:13px; right:13px; font-size:20px; opacity:0.18; }
.kpi-lbl { font-family:'JetBrains Mono',monospace; font-size:9px; color:var(--t2); text-transform:uppercase; letter-spacing:1px; margin-bottom:6px; }
.kpi-val { font-family:'Syne',sans-serif; font-size:24px; font-weight:800; line-height:1; margin-bottom:3px; }
.kpi-sub { font-size:10px; color:var(--t2); margin-top:4px; }
.kpi-delta { font-size:10px; margin-top:5px; font-family:'JetBrains Mono',monospace; }
.kpi-delta.up { color:var(--emerald); } .kpi-delta.down { color:var(--rose); }

/* ── AGENT PIPELINE ── */
.pipe-wrap { display:flex; align-items:stretch; gap:0; margin:16px 0; }
.pipe-node {
  flex:1; background:var(--bg4); border:1px solid var(--bd);
  padding:14px 10px; text-align:center;
  transition:all 0.3s;
}
.pipe-node:first-child { border-radius:14px 0 0 14px; }
.pipe-node:last-child  { border-radius:0 14px 14px 0; }
.pipe-node.run { border-color:var(--blue); background:rgba(59,130,246,0.06); animation:pulse-border 1s infinite; }
.pipe-node.done { border-color:var(--emerald); background:rgba(16,185,129,0.05); }
.pipe-node.err  { border-color:var(--rose); background:rgba(244,63,94,0.05); }
.pipe-icon { font-size:22px; margin-bottom:5px; }
.pipe-name { font-family:'Syne',sans-serif; font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:0.5px; }
.pipe-desc { font-size:9px; color:var(--t2); margin-top:2px; }
.pipe-status { font-size:9px; margin-top:5px; font-family:'JetBrains Mono',monospace; }
.pipe-arr { width:22px; display:flex; align-items:center; justify-content:center; color:var(--t2); font-size:14px; flex-shrink:0; }

/* ── ANOMALY ── */
.anom { background:var(--bg4); border:1px solid var(--bd); border-left:3px solid;
  border-radius:12px; padding:14px 18px; margin-bottom:10px;
  display:flex; gap:12px; align-items:flex-start; }
.anom.high   { border-left-color:var(--rose); }
.anom.medium { border-left-color:var(--amber); }
.anom.low    { border-left-color:var(--blue); }

/* ── ALERT RULES ── */
.alert-rule {
  background:var(--bg4); border:1px solid var(--bd); border-radius:12px;
  padding:14px 18px; margin-bottom:8px;
  display:flex; align-items:center; justify-content:space-between; gap:12px;
}
.alert-triggered { border-color:var(--rose); background:rgba(244,63,94,0.05); }

/* ── CHAT ── */
.chat-wrap { max-height:420px; overflow-y:auto; padding:10px 0; }
.chat-msg { display:flex; gap:10px; margin-bottom:14px; }
.chat-msg.user { flex-direction:row-reverse; }
.chat-bubble {
  max-width:75%; padding:12px 16px;
  border-radius:14px; font-size:13px; line-height:1.6;
}
.chat-msg.user .chat-bubble {
  background:linear-gradient(135deg,var(--blue),var(--violet));
  color:#fff; border-radius:14px 14px 4px 14px;
}
.chat-msg.ai .chat-bubble {
  background:var(--bg4); border:1px solid var(--bd);
  color:var(--t0); border-radius:14px 14px 14px 4px;
}
.chat-avatar {
  width:32px; height:32px; border-radius:50%; flex-shrink:0;
  display:flex; align-items:center; justify-content:center; font-size:16px;
}
.chat-msg.user .chat-avatar { background:linear-gradient(135deg,var(--blue),var(--violet)); }
.chat-msg.ai  .chat-avatar { background:linear-gradient(135deg,var(--emerald),var(--cyan)); }

/* ── STORY CARDS ── */
.story-card {
  background:var(--bg4); border:1px solid var(--bd); border-radius:14px;
  padding:18px 20px; margin-bottom:12px;
  display:flex; gap:14px; align-items:flex-start;
  position:relative; overflow:hidden;
}
.story-card::before { content:''; position:absolute; left:0; top:0; bottom:0; width:3px; }
.story-card.pos::before { background:var(--emerald); }
.story-card.neg::before { background:var(--rose); }
.story-card.neu::before { background:var(--blue); }
.story-number {
  width:36px; height:36px; border-radius:50%; flex-shrink:0;
  display:flex; align-items:center; justify-content:center;
  font-family:'Syne',sans-serif; font-weight:800; font-size:14px;
}
.story-card.pos .story-number { background:rgba(16,185,129,0.15); color:var(--emerald); }
.story-card.neg .story-number { background:rgba(244,63,94,0.15); color:var(--rose); }
.story-card.neu .story-number { background:rgba(59,130,246,0.15); color:var(--blue); }

/* ── DQ SCORE ── */
.dq-ring { position:relative; display:inline-flex; align-items:center; justify-content:center; }
.dq-label { position:absolute; text-align:center; }
.dq-score { font-family:'Syne',sans-serif; font-size:28px; font-weight:800; }
.dq-sub { font-size:10px; color:var(--t2); font-family:'JetBrains Mono',monospace; }

/* ── FORECAST ── */
.forecast-badge {
  display:inline-flex; align-items:center; gap:6px;
  background:rgba(139,92,246,0.1); border:1px solid rgba(139,92,246,0.3);
  border-radius:99px; padding:4px 12px; font-size:11px; color:var(--violet);
  font-family:'JetBrains Mono',monospace; margin-bottom:10px;
}

/* ── SECTION HEAD ── */
.sec-head { display:flex; align-items:center; gap:10px; margin:18px 0 14px; }
.sec-dot { width:8px; height:8px; border-radius:50%; flex-shrink:0; }
.sec-title { font-family:'Syne',sans-serif; font-size:12px; font-weight:700; letter-spacing:1.5px; text-transform:uppercase; color:var(--t1); }
.sec-line { flex:1; height:1px; background:var(--bd); }

/* ── QUERY BOX ── */
.q-box {
  background:var(--bg2); border:1px solid var(--bd2); border-radius:16px;
  padding:20px 22px; margin-bottom:22px; position:relative;
}
.q-box::before {
  content:'QUERY ENGINE'; position:absolute; top:-1px; left:20px;
  background:var(--blue); color:#fff;
  font-family:'JetBrains Mono',monospace; font-size:8px; font-weight:700; letter-spacing:1.5px;
  padding:3px 10px; border-radius:0 0 6px 6px;
}

/* ── FREE BADGE ── */
.free-badge {
  background:linear-gradient(135deg,rgba(16,185,129,0.08),rgba(6,182,212,0.06));
  border:1px solid rgba(16,185,129,0.3); border-radius:12px;
  padding:14px 16px; margin-bottom:16px;
}

/* ── ANIMATIONS ── */
@keyframes pulse-border { 0%,100%{opacity:1;} 50%{opacity:0.5;} }
@keyframes fadeSlideIn { from{opacity:0;transform:translateY(10px);} to{opacity:1;transform:translateY(0);} }
@keyframes shimmer { 0%{background-position:-200% 0;} 100%{background-position:200% 0;} }
.fade-in { animation:fadeSlideIn 0.4s ease forwards; }

/* ── BADGE ── */
.badge { display:inline-block; padding:2px 9px; border-radius:99px; font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:0.5px; }
.badge-high   { background:rgba(244,63,94,0.15);  color:var(--rose);    border:1px solid rgba(244,63,94,0.3); }
.badge-med    { background:rgba(245,158,11,0.15); color:var(--amber);   border:1px solid rgba(245,158,11,0.3); }
.badge-low    { background:rgba(16,185,129,0.15); color:var(--emerald); border:1px solid rgba(16,185,129,0.3); }
.badge-blue   { background:rgba(59,130,246,0.15); color:var(--blue);    border:1px solid rgba(59,130,246,0.3); }

/* ── STREAMLIT OVERRIDES ── */
.stTextInput>div>div>input {
  background:var(--bg2) !important; border:1px solid var(--bd2) !important;
  border-radius:10px !important; color:var(--t0) !important;
  font-family:'Outfit',sans-serif !important; font-size:14px !important;
}
.stTextInput>div>div>input:focus { border-color:var(--blue) !important; box-shadow:0 0 0 2px rgba(59,130,246,0.2) !important; }
.stTextArea>div>div>textarea {
  background:var(--bg2) !important; border:1px solid var(--bd2) !important;
  border-radius:10px !important; color:var(--t0) !important;
  font-family:'Outfit',sans-serif !important;
}
.stButton>button {
  background:linear-gradient(135deg,var(--blue),var(--violet)) !important;
  color:#fff !important; border:none !important; border-radius:10px !important;
  font-family:'Syne',sans-serif !important; font-weight:700 !important;
  font-size:14px !important; padding:10px 22px !important; letter-spacing:0.3px !important;
  transition:all 0.2s !important;
}
.stButton>button:hover { transform:translateY(-2px) !important; box-shadow:0 8px 24px rgba(59,130,246,0.35) !important; }
.stTabs [data-baseweb="tab-list"] {
  background:var(--bg1) !important; border:1px solid var(--bd) !important;
  border-radius:12px !important; padding:4px !important; gap:3px !important;
}
.stTabs [data-baseweb="tab"] {
  background:transparent !important; color:var(--t2) !important;
  border-radius:8px !important; font-family:'Outfit',sans-serif !important;
  font-size:12px !important; font-weight:500 !important; padding:7px 14px !important;
}
.stTabs [aria-selected="true"] { background:var(--blue) !important; color:#fff !important; }
.stSelectbox>div>div { background:var(--bg2) !important; border-color:var(--bd) !important; color:var(--t0) !important; }
.stMultiSelect>div>div { background:var(--bg2) !important; border-color:var(--bd) !important; }
.stSlider>div { color:var(--t0) !important; }
.stSlider [data-baseweb="slider"] div { background:var(--blue) !important; }
.stFileUploader { background:var(--bg2) !important; border:1px dashed var(--bd2) !important; border-radius:12px !important; }
.stDataFrame { border:1px solid var(--bd) !important; border-radius:12px !important; overflow:hidden !important; }
.stDataFrame * { color:var(--t0) !important; }
div[data-testid="stExpander"] { background:var(--bg4) !important; border:1px solid var(--bd) !important; border-radius:12px !important; }
div[data-testid="stExpander"] * { color:var(--t0) !important; }
.stAlert { border-radius:12px !important; }
.stCheckbox label { color:var(--t0) !important; }
.stRadio label { color:var(--t0) !important; }
.stSuccess { background:rgba(16,185,129,0.1) !important; border:1px solid rgba(16,185,129,0.3) !important; border-radius:10px !important; }
.stError { background:rgba(244,63,94,0.1) !important; border:1px solid rgba(244,63,94,0.3) !important; border-radius:10px !important; }
.stInfo { background:rgba(59,130,246,0.08) !important; border:1px solid rgba(59,130,246,0.25) !important; border-radius:10px !important; }
.stWarning { background:rgba(245,158,11,0.08) !important; border:1px solid rgba(245,158,11,0.25) !important; border-radius:10px !important; }
hr { border-color:var(--bd) !important; }
p, li { color:var(--t1) !important; }
h1,h2,h3,h4 { color:var(--t0) !important; font-family:'Syne',sans-serif !important; }
::-webkit-scrollbar { width:5px; height:5px; }
::-webkit-scrollbar-track { background:var(--bg1); }
::-webkit-scrollbar-thumb { background:var(--bd2); border-radius:5px; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════════════════════════
DEFAULTS = {
    "df": None, "df2": None, "schema": None, "kpis": None, "anomalies": None,
    "results": None, "history": [], "filename": None, "filename2": None,
    "chat_history": [], "alert_rules": [], "alert_triggers": [],
    "theme": "dark", "cleaned_cols": [], "dq_score": None,
    "chart_specs": [], "forecast_data": {},
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ══════════════════════════════════════════════════════════════════════════════
# PLOTLY THEME
# ══════════════════════════════════════════════════════════════════════════════
PLY_COLORS = ["#3b82f6","#06b6d4","#8b5cf6","#10b981","#f59e0b","#f43f5e","#a855f7","#ec4899","#38bdf8","#34d399"]
PLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(6,13,24,0.7)",
    font=dict(family="Outfit,sans-serif", color="#7eb0d4", size=12),
    margin=dict(l=48,r=20,t=44,b=40),
    xaxis=dict(gridcolor="#1a2d45", linecolor="#1a2d45", tickfont=dict(size=11), zeroline=False),
    yaxis=dict(gridcolor="#1a2d45", linecolor="#1a2d45", tickfont=dict(size=11), zeroline=False),
    colorway=PLY_COLORS,
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#7eb0d4", size=11)),
    hoverlabel=dict(bgcolor="#0a1525", font=dict(family="Outfit", color="#e8f4ff", size=12), bordercolor="#3b82f6")
)
def ply(fig, title="", h=None):
    fig.update_layout(**PLY_LAYOUT, title=dict(text=title, font=dict(family="Syne",size=14,color="#e8f4ff"), x=0))
    if h: fig.update_layout(height=h)
    return fig

# ══════════════════════════════════════════════════════════════════════════════
# FORMAT HELPER
# ══════════════════════════════════════════════════════════════════════════════
def fv(val, fmt="plain", short=False):
    try:
        n = float(val)
        if fmt == "currency":
            if short:
                if abs(n)>=1e9: return f"${n/1e9:.2f}B"
                if abs(n)>=1e6: return f"${n/1e6:.1f}M"
                if abs(n)>=1e3: return f"${n/1e3:.1f}k"
                return f"${n:,.0f}"
            return f"${n:,.2f}"
        if fmt=="percent": return f"{n:.2f}%"
        if fmt=="count":
            if short and abs(n)>=1e6: return f"{n/1e6:.1f}M"
            if short and abs(n)>=1e3: return f"{n/1e3:.1f}k"
            return f"{int(n):,}"
        if short and abs(n)>=1e6: return f"{n/1e6:.1f}M"
        if short and abs(n)>=1e3: return f"{n/1e3:.1f}k"
        return f"{n:,.2f}"
    except: return str(val)

def sec(title, color="var(--blue)"):
    st.markdown(f'<div class="sec-head"><div class="sec-dot" style="background:{color};"></div><div class="sec-title">{title}</div><div class="sec-line"></div></div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# AUTO COLUMN CLASSIFIER
# ══════════════════════════════════════════════════════════════════════════════
def classify_columns(df):
    schema = {}
    date_kw = ["date","time","month","week","year","day","period","quarter","dt","ts","timestamp","created","updated","at"]
    curr_kw = ["revenue","sales","price","cost","spend","income","profit","amount","total","value","fee","wage","salary","budget","gmv","arr","mrr","ltv","cac","gross","net","earn","charge","invoice","payment","balance"]
    pct_kw  = ["rate","ratio","pct","percent","share","margin","growth","churn","conversion","ctr","roas","roi","yield","score","perc","percentage"]
    cnt_kw  = ["count","qty","quantity","units","sold","orders","clicks","views","visits","sessions","impressions","customers","users","transactions","leads","items","tickets","num","number","#","cnt","total_records"]

    for col in df.columns:
        cl = col.lower().replace(" ","_")
        s  = df[col].dropna()
        if len(s) == 0:
            schema[col] = {"type":"empty","format":"plain"}; continue

        # Date detection
        if any(k in cl for k in date_kw):
            try:
                pd.to_datetime(s.head(30))
                schema[col] = {"type":"date","format":"date"}; continue
            except: pass

        # Numeric
        if pd.api.types.is_numeric_dtype(s):
            ur = s.nunique() / max(len(s),1)
            if s.nunique() <= 20 and ur < 0.15 and s.max() < 10000:
                schema[col] = {"type":"categorical_numeric","format":"plain","categories":sorted(s.unique().tolist())}; continue
            fmt = "plain"
            if any(k in cl for k in curr_kw): fmt = "currency"
            elif any(k in cl for k in pct_kw): fmt = "percent"
            elif any(k in cl for k in cnt_kw): fmt = "count"
            elif s.mean() > 500 and "id" not in cl: fmt = "currency"
            schema[col] = {"type":"numeric","format":fmt,
                           "min":float(s.min()),"max":float(s.max()),
                           "mean":float(s.mean()),"std":float(s.std() or 0),
                           "missing":int(df[col].isna().sum())}
            continue

        # Boolean
        uv = {str(v).strip().lower() for v in s.unique()}
        if uv <= {"true","false"} or uv <= {"yes","no"} or uv <= {"0","1"} or uv <= {"y","n"}:
            schema[col] = {"type":"boolean","format":"plain"}; continue

        # Categorical
        ur = s.nunique() / max(len(s),1)
        if s.nunique() <= 60 or ur < 0.4:
            schema[col] = {"type":"categorical","format":"plain",
                           "categories":s.unique()[:30].tolist(),"nunique":int(s.nunique()),
                           "missing":int(df[col].isna().sum())}; continue

        schema[col] = {"type":"text","format":"plain","missing":int(df[col].isna().sum())}
    return schema

# ══════════════════════════════════════════════════════════════════════════════
# AUTO DATA CLEANER
# ══════════════════════════════════════════════════════════════════════════════
def auto_clean(df, schema):
    df2 = df.copy(); cleaned = []
    for col, info in schema.items():
        miss = df2[col].isna().sum()
        if miss == 0: continue
        if info["type"] == "numeric":
            df2[col].fillna(df2[col].median(), inplace=True)
            cleaned.append(f"'{col}': {miss} missing → filled with median ({fv(df[col].median(), info['format'])})")
        elif info["type"] == "categorical":
            mode = df2[col].mode()
            if len(mode) > 0:
                df2[col].fillna(mode[0], inplace=True)
                cleaned.append(f"'{col}': {miss} missing → filled with mode ('{mode[0]}')")
        elif info["type"] == "date":
            df2[col].fillna(method="ffill", inplace=True)
            cleaned.append(f"'{col}': {miss} missing → forward-filled")
    # Fix numeric cols stored as strings
    for col, info in schema.items():
        if info["type"] == "numeric" and df2[col].dtype == object:
            df2[col] = pd.to_numeric(df2[col].astype(str).str.replace(",","").str.replace("$",""), errors="coerce")
            cleaned.append(f"'{col}': converted string→numeric")
    return df2, cleaned

# ══════════════════════════════════════════════════════════════════════════════
# DATA QUALITY SCORE
# ══════════════════════════════════════════════════════════════════════════════
def compute_dq_score(df, schema):
    scores = {}
    total = len(df)
    # Completeness
    missing_pct = df.isnull().sum().sum() / (total * len(df.columns))
    scores["Completeness"] = round((1 - missing_pct) * 100, 1)
    # Consistency (no duplicate rows)
    dup_pct = df.duplicated().sum() / total
    scores["Consistency"] = round((1 - dup_pct) * 100, 1)
    # Validity (numeric cols in range)
    num_cols = [c for c,s in schema.items() if s["type"]=="numeric"]
    if num_cols:
        valid_scores = []
        for col in num_cols:
            q1, q3 = df[col].quantile(0.01), df[col].quantile(0.99)
            outlier_pct = ((df[col] < q1) | (df[col] > q3)).sum() / total
            valid_scores.append(1 - min(outlier_pct, 0.5))
        scores["Validity"] = round(np.mean(valid_scores) * 100, 1)
    else:
        scores["Validity"] = 100.0
    # Reliability (enough rows)
    scores["Reliability"] = min(100.0, round(total / 10, 1))
    overall = round(np.mean(list(scores.values())), 1)
    return {"overall": overall, "breakdown": scores}

# ══════════════════════════════════════════════════════════════════════════════
# KPI CALCULATOR
# ══════════════════════════════════════════════════════════════════════════════
def compute_kpis(df, schema):
    kpis = {}
    num_cols  = [c for c,s in schema.items() if s["type"]=="numeric"]
    cat_cols  = [c for c,s in schema.items() if s["type"] in ("categorical","categorical_numeric")]
    date_cols = [c for c,s in schema.items() if s["type"]=="date"]

    kpis["summary"] = {}
    for col in num_cols:
        s = df[col].dropna()
        if len(s) == 0: continue
        # Compute period-over-period if we have enough data
        half = len(s)//2
        prev_mean = float(s.iloc[:half].mean()) if half > 0 else float(s.mean())
        curr_mean = float(s.iloc[half:].mean()) if half > 0 else float(s.mean())
        pct_change = ((curr_mean - prev_mean)/prev_mean*100) if prev_mean != 0 else 0
        kpis["summary"][col] = {
            "sum":float(s.sum()),"mean":float(s.mean()),"median":float(s.median()),
            "std":float(s.std() or 0),"min":float(s.min()),"max":float(s.max()),
            "count":int(s.count()),"format":schema[col]["format"],
            "pct_change":round(pct_change,1)
        }

    kpis["breakdowns"] = {}
    if cat_cols:
        cat = cat_cols[0]; kpis["primary_cat"] = cat
        for num in num_cols[:6]:
            try:
                g = df.groupby(cat)[num].agg(["sum","mean","count"]).reset_index()
                g.columns = [cat,"sum","mean","count"]
                kpis["breakdowns"][f"{cat}_{num}"] = {"by":cat,"metric":num,"data":g.to_dict("records"),"format":schema[num]["format"]}
            except: pass

    kpis["time_series"] = {}
    if date_cols:
        dc = date_cols[0]; kpis["primary_date"] = dc
        try:
            dfc = df.copy()
            dfc["_dp"] = pd.to_datetime(dfc[dc], errors="coerce")
            dfc = dfc.dropna(subset=["_dp"]).sort_values("_dp")
            for num in num_cols[:5]:
                g = dfc.groupby("_dp")[num].sum().reset_index()
                g.columns = ["date","value"]; g["date"] = g["date"].astype(str)
                kpis["time_series"][num] = g.to_dict("records")
        except: pass

    kpis["derived"] = {}
    for i,c1 in enumerate(num_cols):
        for c2 in num_cols[i+1:]:
            s2 = df[c2].sum()
            if s2 == 0: continue
            r = df[c1].sum()/s2
            if 0.001 < abs(r) < 1000:
                kpis["derived"][f"{c1}_per_{c2}"] = {"numerator":c1,"denominator":c2,"value":round(r,4)}
    return kpis

# ══════════════════════════════════════════════════════════════════════════════
# ANOMALY DETECTION
# ══════════════════════════════════════════════════════════════════════════════
def detect_anomalies(df, schema):
    anomalies = []
    num_cols = [c for c,s in schema.items() if s["type"]=="numeric"]
    cat_cols = [c for c,s in schema.items() if s["type"] in ("categorical","categorical_numeric")]
    grp_col  = cat_cols[0] if cat_cols else None

    for col in num_cols:
        try:
            if grp_col:
                groups = [(k,g) for k,g in df.groupby(grp_col)[col]]
            else:
                groups = [("ALL", df[col])]
            for gk, gdata in groups:
                vals = gdata.dropna().values
                if len(vals) < 3: continue
                mn, sd = float(np.mean(vals)), float(np.std(vals))
                if sd == 0: continue
                sub = df[df[grp_col]==gk] if grp_col else df
                for _, row in sub.iterrows():
                    v = row.get(col)
                    if pd.isna(v): continue
                    z = abs((float(v)-mn)/sd)
                    if z < 2.0: continue
                    ctx = " | ".join(f"{c}={row[c]}" for c in schema if schema[c]["type"] in ("categorical","date") and c in row.index)[:120]
                    anomalies.append({
                        "column":col,"group":str(gk),"value":float(v),
                        "mean":round(mn,2),"z_score":round(z,2),
                        "direction":"spike ↑" if v>mn else "drop ↓",
                        "severity":"high" if z>=3 else "medium" if z>=2.5 else "low",
                        "context":ctx,"format":schema[col]["format"]
                    })
        except: pass

    anomalies.sort(key=lambda x:-x["z_score"])
    seen=defaultdict(int); out=[]
    for a in anomalies:
        k=(a["column"],a["group"])
        if seen[k]<2: out.append(a); seen[k]+=1
    return out[:15]

# ══════════════════════════════════════════════════════════════════════════════
# SMART ALERTS ENGINE
# ══════════════════════════════════════════════════════════════════════════════
def check_alerts(df, schema, kpis, rules):
    triggered = []
    for rule in rules:
        try:
            col   = rule["column"]
            op    = rule["operator"]
            thresh= float(rule["threshold"])
            metric= rule.get("metric","mean")
            if col not in kpis.get("summary",{}): continue
            val = kpis["summary"][col].get(metric, kpis["summary"][col]["mean"])
            hit = False
            if op == ">" and val > thresh: hit=True
            elif op == "<" and val < thresh: hit=True
            elif op == ">=" and val >= thresh: hit=True
            elif op == "<=" and val <= thresh: hit=True
            elif op == "drop%" and kpis["summary"][col]["pct_change"] < -abs(thresh): hit=True
            elif op == "rise%" and kpis["summary"][col]["pct_change"] > abs(thresh): hit=True
            if hit:
                triggered.append({**rule, "actual":val, "message":f"'{col}' {metric}={fv(val,schema.get(col,{}).get('format','plain'))} {op} {thresh}"})
        except: pass
    return triggered

# ══════════════════════════════════════════════════════════════════════════════
# FORECASTING (Moving Average + Trend)
# ══════════════════════════════════════════════════════════════════════════════
def forecast_series(ts_data, periods=10):
    """Simple moving average + linear trend forecast."""
    if len(ts_data) < 4:
        return []
    vals = np.array([d["value"] for d in ts_data])
    n    = len(vals)
    x    = np.arange(n)
    # Linear regression for trend
    m, b = np.polyfit(x, vals, 1)
    # Moving average for smoothing
    w = min(5, n//2)
    ma = np.convolve(vals, np.ones(w)/w, mode="valid")
    last_ma = ma[-1] if len(ma)>0 else vals[-1]
    # Residual std for confidence
    trend = m*x + b
    residuals = vals - trend
    std = float(np.std(residuals))
    # Generate forecast dates
    last_date_str = ts_data[-1]["date"]
    try:
        last_date = pd.to_datetime(last_date_str)
        step = (last_date - pd.to_datetime(ts_data[-2]["date"])) if len(ts_data)>1 else timedelta(days=7)
    except:
        last_date = datetime.now(); step = timedelta(days=7)
    forecasts = []
    for i in range(1, periods+1):
        pred = float(m*(n+i) + b)
        forecasts.append({
            "date": str((last_date + step*i).date()),
            "value": max(0, pred),
            "lower": max(0, pred - 1.64*std),
            "upper": pred + 1.64*std
        })
    return forecasts

# ══════════════════════════════════════════════════════════════════════════════
# GEMINI API (FREE)
# ══════════════════════════════════════════════════════════════════════════════
def call_gemini(api_key, prompt, max_tokens=2000):
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(
            "gemini-flash-latest",
            generation_config={"temperature":0.25,"max_output_tokens":max_tokens}
        )
        full = "You are ReportGenie AI, an expert business analytics system. Respond ONLY with valid JSON — no markdown, no code fences, no explanation text.\n\n" + prompt
        resp = model.generate_content(full)
        raw  = resp.text.strip()
        raw  = re.sub(r"```json|```","",raw).strip()
        m    = re.search(r"\{.*\}",raw,re.DOTALL)
        if m: raw = m.group(0)
        return json.loads(raw)
    except Exception as e:
        raise Exception(f"Gemini error: {e}")

def call_gemini_text(api_key, prompt, max_tokens=1000):
    """Returns plain text (for chat, story etc)."""
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(
            "gemini-flash-latest",
            generation_config={"temperature":0.4,"max_output_tokens":max_tokens}
        )
        resp = model.generate_content(prompt)
        return resp.text.strip()
    except Exception as e:
        return f"Error: {e}"

# ══════════════════════════════════════════════════════════════════════════════
# CHART SPEC → PLOTLY (Natural Language → Chart)
# ══════════════════════════════════════════════════════════════════════════════
def nl_to_chart_spec(api_key, query, schema, kpis, df):
    """Ask Gemini to interpret NL query and return a chart specification."""
    col_info = {c:{"type":s["type"],"format":s.get("format","plain")} for c,s in schema.items()}
    numeric_cols = [c for c,s in schema.items() if s["type"]=="numeric"]
    cat_cols = [c for c,s in schema.items() if s["type"]=="categorical"]
    date_cols = [c for c,s in schema.items() if s["type"]=="date"]
    prompt = f"""User asked: "{query}"
Available columns: {json.dumps(col_info)}
Numeric columns: {numeric_cols}
Categorical columns: {cat_cols}
Date columns: {date_cols}

Determine what chart to create. Return JSON:
{{
  "chart_type": "bar|line|scatter|histogram|box|heatmap|pie|area",
  "x_col": "column_name or null",
  "y_col": "column_name or null",
  "color_col": "column_name or null",
  "aggregation": "sum|mean|count|none",
  "title": "Chart title",
  "interpretation": "one sentence explaining what this chart shows"
}}"""
    try:
        return call_gemini(api_key, prompt, max_tokens=500)
    except:
        return None

def render_chart_from_spec(df, spec, schema):
    """Render a Plotly chart from a Gemini-generated spec."""
    if not spec: return None
    ct = spec.get("chart_type","bar")
    x  = spec.get("x_col")
    y  = spec.get("y_col")
    c  = spec.get("color_col")
    agg= spec.get("aggregation","none")
    title = spec.get("title","Chart")

    # Validate columns exist
    if x and x not in df.columns: x = None
    if y and y not in df.columns: y = None
    if c and c not in df.columns: c = None

    try:
        df_plot = df.copy()
        # Apply aggregation
        if agg in ("sum","mean","count") and x and y:
            if agg == "sum":   df_plot = df.groupby(x)[y].sum().reset_index()
            elif agg == "mean": df_plot = df.groupby(x)[y].mean().reset_index()
            elif agg == "count": df_plot = df.groupby(x)[y].count().reset_index()
            c = None  # after aggregation no color col

        fmt = schema.get(y,{}).get("format","plain") if y else "plain"

        if ct == "bar":
            fig = px.bar(df_plot,x=x,y=y,color=c,barmode="group",
                         color_discrete_sequence=PLY_COLORS, title=title)
        elif ct == "line" or ct == "area":
            fig = px.line(df_plot,x=x,y=y,color=c,
                          color_discrete_sequence=PLY_COLORS, title=title)
            if ct == "area": fig.update_traces(fill="tozeroy",fillcolor="rgba(59,130,246,0.1)")
        elif ct == "scatter":
            fig = px.scatter(df_plot,x=x,y=y,color=c,
                             color_discrete_sequence=PLY_COLORS, title=title)
            fig.update_traces(marker=dict(size=8,line=dict(width=0.5,color="#0a1525")))
        elif ct == "histogram":
            col = y or x
            fig = px.histogram(df_plot,x=col,color=c,nbins=30,
                               color_discrete_sequence=PLY_COLORS, title=title)
        elif ct == "box":
            fig = px.box(df_plot,x=c,y=y,color=c,
                         color_discrete_sequence=PLY_COLORS, title=title)
        elif ct == "pie":
            if x and y:
                fig = px.pie(df_plot,names=x,values=y,
                             color_discrete_sequence=PLY_COLORS, title=title)
            else:
                return None
        elif ct == "heatmap":
            num_cols = [col for col in df_plot.columns if pd.api.types.is_numeric_dtype(df_plot[col])]
            if len(num_cols)>=2:
                corr = df_plot[num_cols].corr()
                fig = go.Figure(go.Heatmap(z=corr.values,x=corr.columns.tolist(),y=corr.columns.tolist(),
                    colorscale=[[0,"#f43f5e"],[0.5,"#0a1525"],[1,"#3b82f6"]],
                    text=[[f"{v:.2f}" for v in row] for row in corr.values],texttemplate="%{text}",zmin=-1,zmax=1))
                fig.update_layout(title=title)
            else: return None
        else:
            fig = px.bar(df_plot,x=x,y=y,color=c,color_discrete_sequence=PLY_COLORS,title=title)

        ply(fig, title, h=340)
        return fig, spec.get("interpretation","")
    except Exception as e:
        return None

# ══════════════════════════════════════════════════════════════════════════════
# STORY GENERATOR
# ══════════════════════════════════════════════════════════════════════════════
def generate_story(api_key, kpis, schema, anomalies, domain=""):
    """Generate auto narrative story cards."""
    kpi_snap = {c:{"sum":s["sum"],"mean":s["mean"],"pct_change":s.get("pct_change",0),"format":s["format"]} for c,s in kpis.get("summary",{}).items()}
    an_snap  = [{"column":a["column"],"direction":a["direction"],"severity":a["severity"],"z_score":a["z_score"]} for a in anomalies[:5]]
    prompt   = f"""Domain: {domain}
KPIs: {json.dumps(kpi_snap)}
Anomalies: {json.dumps(an_snap)}

Generate 5 auto-narrative story cards for a business dashboard. Each card should be a key insight.
Return JSON:
{{
  "stories": [
    {{
      "headline": "Short headline (e.g. Revenue dropped 12% due to Region X)",
      "detail": "2-sentence explanation",
      "sentiment": "positive|negative|neutral",
      "metric": "column_name or empty",
      "icon": "emoji"
    }}
  ]
}}"""
    try:
        return call_gemini(api_key, prompt, max_tokens=800)
    except:
        return {"stories":[]}

# ══════════════════════════════════════════════════════════════════════════════
# 5-AGENT PIPELINE
# ══════════════════════════════════════════════════════════════════════════════
AGENT_DEFS = [
    ("schema","🗂","Schema Agent","Domain & column intelligence"),
    ("kpi","📊","KPI Agent","Adaptive metric ranking"),
    ("insight","🧠","Insight Agent","Causal root-cause AI"),
    ("critic","🔬","Critic Agent","Confidence validation"),
    ("report","📋","Report Agent","Executive synthesis"),
]

def render_pipeline(status_map):
    html = '<div class="pipe-wrap">'
    for i,(key,icon,name,desc) in enumerate(AGENT_DEFS):
        s = status_map.get(key,"idle")
        css = "run" if s=="running" else "done" if s=="done" else "err" if s=="error" else ""
        sc  = "#3b82f6" if s=="running" else "#10b981" if s=="done" else "#f43f5e" if s=="error" else "#3a5a78"
        si  = "⟳" if s=="running" else "✓" if s=="done" else "✕" if s=="error" else "·"
        html += f'<div class="pipe-node {css}"><div class="pipe-icon">{icon}</div><div class="pipe-name">{name}</div><div class="pipe-desc">{desc}</div><div class="pipe-status" style="color:{sc};">{si} {s.upper()}</div></div>'
        if i < len(AGENT_DEFS)-1: html += '<div class="pipe-arr">→</div>'
    html += '</div>'
    return html

def run_pipeline(api_key, query, df, schema, kpis, anomalies, cb):
    res = {}
    kpi_snap  = {c:{"sum":s["sum"],"mean":s["mean"],"format":s["format"],"pct_change":s.get("pct_change",0)} for c,s in kpis.get("summary",{}).items()}
    anom_snap = [{"column":a["column"],"group":a["group"],"direction":a["direction"],"z_score":a["z_score"],"severity":a["severity"]} for a in anomalies[:6]]
    scm_snap  = {k:{x:v for x,v in s.items() if x!="categories"} for k,s in schema.items()}

    # Agent 1
    cb("schema","running")
    res["schema"] = call_gemini(api_key, f"""Dataset schema: {json.dumps(scm_snap)}
Sample rows: {df.head(5).to_dict(orient='records')}
User query: "{query}"
Return JSON: {{"domain":"E-Commerce|Finance|HR|Healthcare|Marketing|Logistics|etc","description":"2 sentences","column_roles":{{"col":"role desc"}},"primary_metrics":["col"],"suggested_analyses":["idea1","idea2","idea3"]}}""")
    cb("schema","done")

    # Agent 2
    cb("kpi","running")
    res["kpi"] = call_gemini(api_key, f"""Domain: {res['schema'].get('domain','')}
Query: "{query}"
KPIs: {json.dumps(kpi_snap)}
Column roles: {json.dumps(res['schema'].get('column_roles',{}))}
Return JSON: {{"top_kpis":[{{"name":"col","display_label":"label","value":"formatted str","importance":"High|Medium|Low","trend":"positive|negative|neutral","insight":"one line"}}],"kpi_summary":"2 sentence overview","watchlist":["metric"]}}""")
    cb("kpi","done")

    # Agent 3
    cb("insight","running")
    res["insight"] = call_gemini(api_key, f"""Domain: {res['schema'].get('domain','')}
Query: "{query}"
KPI analysis: {json.dumps(res['kpi'])}
Anomalies: {json.dumps(anom_snap)}
Return JSON: {{"executive_summary":"3 sentences for executives","insights":[{{"title":"title","explanation":"what","cause":"why","impact":"business impact","confidence":0.85,"urgency":"High|Medium|Low"}}]}}""", max_tokens=2000)
    cb("insight","done")

    # Agent 4
    cb("critic","running")
    res["critic"] = call_gemini(api_key, f"""Validate these insights against data.
KPIs: {json.dumps(kpi_snap)}
Insights: {json.dumps(res['insight'])}
Return JSON: {{"overall_confidence":0.85,"report_quality":"Excellent|Good|Fair","validated_insights":[{{"title":"t","confidence":0.85,"data_support":"support","caveat":"caveat","verdict":"Confirmed|Plausible|Speculative"}}],"data_gaps":["gap"],"critic_summary":"2 sentences"}}""")
    cb("critic","done")

    # Agent 5
    cb("report","running")
    res["report"] = call_gemini(api_key, f"""Write executive report.
Domain: {res['schema'].get('domain','')}
Query: "{query}"
KPIs: {json.dumps(res['kpi'])}
Insights: {json.dumps(res['insight'].get('insights',[]))}
Validation: {json.dumps(res['critic'].get('validated_insights',[]))}
Anomalies: {json.dumps(anom_snap)}
Return JSON: {{"title":"title","executive_summary":"4-5 sentences","key_findings":["f1","f2","f3","f4","f5"],"anomaly_narratives":[{{"event":"event","explanation":"why","urgency":"High|Medium|Low"}}],"recommendations":[{{"action":"action","priority":"High|Medium|Low","impact":"impact","timeline":"Immediate|Short-term|Long-term"}}],"next_kpis_to_watch":["k1","k2","k3"],"risk_flags":["r1","r2"],"root_causes":[{{"finding":"finding","cause":"root cause","evidence":"data evidence"}}]}}""", max_tokens=2500)
    cb("report","done")
    return res

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style='padding:10px 0 14px;'>
        <div style='font-family:Syne,sans-serif;font-size:22px;font-weight:800;
            background:linear-gradient(135deg,#e8f4ff,#06b6d4);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent;'>🧞 ReportGenie AI</div>
        <div style='font-family:JetBrains Mono,monospace;font-size:9px;color:#3a5a78;letter-spacing:1.5px;text-transform:uppercase;margin-top:2px;'>AI Analytics Engine v2.0</div>
    </div>
    """, unsafe_allow_html=True)

    # API Key
    st.markdown("""
    <div class='free-badge'>
        <div style='font-family:Syne,sans-serif;font-weight:700;font-size:13px;color:#10b981;margin-bottom:6px;'>🆓 Google Gemini — 100% Free</div>
        <div style='font-size:11px;color:#7eb0d4;line-height:1.9;'>
            <b>Get FREE key (no card):</b><br>
            1. <b>aistudio.google.com/app/apikey</b><br>
            2. Sign in with Google<br>
            3. Click <b>"Create API Key"</b><br>
            4. Paste below (or use default 👇)<br><br>
            <span style='color:#f59e0b;'>✦ 1500 free requests/day</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    key_input = st.text_input("API Key", value=DEFAULT_API_KEY, type="password", placeholder="AIza...", label_visibility="collapsed")
    API_KEY = key_input if key_input else DEFAULT_API_KEY
    if API_KEY:
        st.markdown('<div style="color:#10b981;font-size:11px;margin-top:3px;font-family:JetBrains Mono,monospace;">✓ Key ready</div>', unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # File Upload — Primary
    st.markdown('<div style="font-family:Syne,sans-serif;font-size:11px;font-weight:700;color:#7eb0d4;letter-spacing:1px;text-transform:uppercase;margin-bottom:6px;">📂 Primary Dataset</div>', unsafe_allow_html=True)
    up1 = st.file_uploader("Primary CSV", type=["csv"], label_visibility="collapsed")
    if up1:
        try:
            raw = pd.read_csv(up1); raw.columns=[c.strip() for c in raw.columns]
            st.session_state.df       = raw
            st.session_state.filename = up1.name
            st.session_state.schema   = classify_columns(raw)
            raw2, cleaned = auto_clean(raw.copy(), st.session_state.schema)
            if cleaned:
                st.session_state.df = raw2
                st.session_state.cleaned_cols = cleaned
            st.session_state.kpis      = compute_kpis(st.session_state.df, st.session_state.schema)
            st.session_state.anomalies = detect_anomalies(st.session_state.df, st.session_state.schema)
            st.session_state.dq_score  = compute_dq_score(raw, st.session_state.schema)
            st.session_state.results   = None
            st.session_state.chart_specs = []
            st.session_state.forecast_data = {}
            st.success(f"✓ {up1.name}")
            st.markdown(f'<div style="font-size:11px;color:#3a5a78;font-family:JetBrains Mono,monospace;">{raw.shape[0]:,} rows · {raw.shape[1]} cols</div>', unsafe_allow_html=True)
            if cleaned:
                st.info(f"🧹 Auto-cleaned {len(cleaned)} issues")
        except Exception as e:
            st.error(f"Error: {e}")

    # File Upload — Secondary (Data Blending)
    st.markdown('<div style="font-family:Syne,sans-serif;font-size:11px;font-weight:700;color:#7eb0d4;letter-spacing:1px;text-transform:uppercase;margin-bottom:6px;margin-top:12px;">📂 Blend Dataset (optional)</div>', unsafe_allow_html=True)
    up2 = st.file_uploader("Secondary CSV", type=["csv"], label_visibility="collapsed", key="up2")
    if up2:
        try:
            raw2 = pd.read_csv(up2); raw2.columns=[c.strip() for c in raw2.columns]
            st.session_state.df2       = raw2
            st.session_state.filename2 = up2.name
            st.success(f"✓ {up2.name} ready to blend")
        except Exception as e:
            st.error(f"Error: {e}")

    # Schema display
    if st.session_state.schema:
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('<div style="font-family:Syne,sans-serif;font-size:11px;font-weight:700;color:#7eb0d4;letter-spacing:1px;text-transform:uppercase;margin-bottom:8px;">🗂 Auto Schema</div>', unsafe_allow_html=True)
        tc = {"numeric":"#3b82f6","categorical":"#8b5cf6","date":"#06b6d4","boolean":"#10b981","text":"#f59e0b","categorical_numeric":"#a855f7","empty":"#3a5a78"}
        for col,info in st.session_state.schema.items():
            c = tc.get(info["type"],"#7eb0d4")
            miss = info.get("missing",0)
            miss_str = f' ⚠{miss}' if miss else ''
            st.markdown(f'<div style="display:flex;align-items:center;gap:7px;margin-bottom:5px;font-size:10px;"><span style="width:6px;height:6px;background:{c};border-radius:50%;flex-shrink:0;"></span><span style="color:#e8f4ff;flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;" title="{col}">{col}</span><span style="color:{c};font-family:JetBrains Mono,monospace;font-size:8px;">{info["type"][:4]}{miss_str}</span></div>', unsafe_allow_html=True)

    # Alert count
    if st.session_state.alert_triggers:
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown(f'<div style="background:rgba(244,63,94,0.1);border:1px solid rgba(244,63,94,0.3);border-radius:8px;padding:8px 12px;font-size:12px;color:#f43f5e;font-family:Syne,sans-serif;font-weight:700;">🚨 {len(st.session_state.alert_triggers)} Alert(s) Triggered!</div>', unsafe_allow_html=True)

    if st.session_state.history:
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown(f'<div style="font-size:10px;color:#3a5a78;font-family:JetBrains Mono,monospace;">📼 {len(st.session_state.history)} analyses saved</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════════════════════
dq = st.session_state.dq_score
dq_val = dq["overall"] if dq else "—"
dq_col = "#10b981" if dq and dq["overall"]>=80 else "#f59e0b" if dq and dq["overall"]>=60 else "#f43f5e"

st.markdown(f"""
<div class='rg-header'>
    <div class='rg-logo'>🧞</div>
    <div>
        <div class='rg-title'>ReportGenie AI</div>
        <div class='rg-sub'>Autonomous · Multi-Agent · Decision Engine · Any Dataset</div>
    </div>
    <div style='margin-left:auto;display:flex;gap:12px;align-items:center;'>
        <div class='rg-badge'>
            <div class='rg-badge-top'>DATA QUALITY</div>
            <div class='rg-badge-val' style='color:{dq_col};'>{dq_val}{'%' if dq else ''}</div>
        </div>
        <div class='rg-badge'>
            <div class='rg-badge-top'>POWERED BY</div>
            <div class='rg-badge-val'>Gemini · 5 Agents · FREE</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── NO DATA ────────────────────────────────────────────────────────────────────
if st.session_state.df is None:
    st.markdown("""
    <div style='text-align:center;padding:60px 30px;'>
        <div style='font-size:64px;margin-bottom:18px;'>🧞</div>
        <div style='font-family:Syne,sans-serif;font-size:28px;font-weight:800;color:#e8f4ff;margin-bottom:12px;'>ReportGenie AI</div>
        <div style='color:#3a5a78;font-size:15px;max-width:540px;margin:0 auto;line-height:1.9;'>
            Upload any CSV in the sidebar. ReportGenie AI auto-detects your data, cleans it, scores quality,
            computes KPIs, finds anomalies, forecasts trends, and runs 5 AI agents — all free.
        </div>
    </div>""", unsafe_allow_html=True)
    feats=[("🆓","Free Gemini AI","1500 requests/day, no card needed"),
           ("🔍","Auto Schema Detect","Classifies every column automatically"),
           ("📈","Dynamic KPIs","Computes metrics adaptive to your data"),
           ("🚨","Anomaly + Alerts","Z-score detection + custom alert rules"),
           ("🤖","5 AI Agents","Schema→KPI→Insight→Critic→Report"),
           ("💬","Chat Mode","Follow-up questions in conversation"),
           ("📖","Auto Storytelling","Narrative insight cards"),
           ("📉","Forecasting","30-day trend projections"),
           ("🧾","Export Reports","Download PDF/CSV summaries"),
           ("🔗","Data Blending","Merge two CSVs for joint analysis"),
           ("🧹","Auto Cleaning","Handles missing values automatically"),
           ("🎯","NL→Charts","Type 'show revenue by region' → chart"),
           ]
    cols=st.columns(4)
    for i,(ic,ti,de) in enumerate(feats):
        with cols[i%4]:
            st.markdown(f'<div style="background:#0a1525;border:1px solid #1a2d45;border-radius:13px;padding:16px;margin-bottom:10px;"><div style="font-size:24px;margin-bottom:7px;">{ic}</div><div style="font-family:Syne,sans-serif;font-weight:700;font-size:13px;color:#e8f4ff;margin-bottom:4px;">{ti}</div><div style="font-size:11px;color:#3a5a78;line-height:1.6;">{de}</div></div>',unsafe_allow_html=True)
    st.stop()

# ══════════════════════════════════════════════════════════════════════════════
# MAIN DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
df     = st.session_state.df
schema = st.session_state.schema
kpis   = st.session_state.kpis
anoms  = st.session_state.anomalies
num_cols_list = [c for c,s in schema.items() if s["type"]=="numeric"]
cat_cols_list = [c for c,s in schema.items() if s["type"]=="categorical"]
date_cols_list= [c for c,s in schema.items() if s["type"]=="date"]

# ── CHECK ALERTS ON LOAD ───────────────────────────────────────────────────────
if st.session_state.alert_rules:
    st.session_state.alert_triggers = check_alerts(df, schema, kpis, st.session_state.alert_rules)

# ── QUERY BOX ──────────────────────────────────────────────────────────────────
st.markdown('<div class="q-box">', unsafe_allow_html=True)
qc1,qc2 = st.columns([5,1])
with qc1:
    query = st.text_input("q",label_visibility="collapsed",
        placeholder='Try: "Show revenue by region as bar chart" · "Why did sales drop?" · "Forecast next 30 days" · "What are top risks?"',
        key="main_query")
with qc2:
    run_btn = st.button("🧞 Analyze",use_container_width=True)

chips=[]
if num_cols_list: chips.append(f"Summarize {num_cols_list[0]} trends")
if cat_cols_list: chips.append(f"Show {num_cols_list[0] if num_cols_list else 'data'} by {cat_cols_list[0]} as bar chart")
if len(num_cols_list)>=2: chips.append(f"Plot {num_cols_list[0]} vs {num_cols_list[1]}")
chips.append("What are the top 3 risks in this dataset?")
chips.append("Generate storytelling dashboard")
chips.append("Forecast trends for next 30 days")

st.markdown('<div style="display:flex;gap:7px;flex-wrap:wrap;margin-top:10px;">'+"".join(
    f'<span style="background:#0a1525;border:1px solid #1a2d45;border-radius:99px;padding:3px 12px;font-size:10px;color:#7eb0d4;cursor:pointer;">{p}</span>' for p in chips)+'</div>',
    unsafe_allow_html=True)
st.markdown('</div>',unsafe_allow_html=True)

# ── ALERT BANNER ──────────────────────────────────────────────────────────────
if st.session_state.alert_triggers:
    for trig in st.session_state.alert_triggers:
        st.error(f"🚨 Alert Triggered: {trig['message']} (Rule: {trig.get('name','Unnamed')})")

# ── CLEANED BANNER ─────────────────────────────────────────────────────────────
if st.session_state.cleaned_cols:
    with st.expander(f"🧹 Auto-cleaned {len(st.session_state.cleaned_cols)} issues before analysis"):
        for c in st.session_state.cleaned_cols:
            st.markdown(f'<div style="font-size:12px;color:#10b981;padding:3px 0;">✓ {c}</div>',unsafe_allow_html=True)

# ── RUN PIPELINE ───────────────────────────────────────────────────────────────
if run_btn and query:
    if not API_KEY:
        st.error("⚠ API key required. Get one free at aistudio.google.com/app/apikey")
    else:
        # Detect if this is a chart request
        chart_kws = ["chart","plot","graph","show","visualize","bar","line","scatter","histogram","pie","heatmap","area","draw","display"]
        is_chart  = any(kw in query.lower() for kw in chart_kws)
        # Detect forecast request
        fc_kws    = ["forecast","predict","next","future","project","trend"]
        is_fc     = any(kw in query.lower() for kw in fc_kws)
        # Detect story request
        story_kws = ["story","narrative","storytelling","dashboard story"]
        is_story  = any(kw in query.lower() for kw in story_kws)

        if is_chart:
            with st.spinner("🎨 Generating chart from your query..."):
                spec = nl_to_chart_spec(API_KEY, query, schema, kpis, df)
                if spec:
                    result = render_chart_from_spec(df, spec, schema)
                    if result:
                        fig, interp = result
                        st.session_state.chart_specs.append({"query":query,"spec":spec,"interp":interp})
                        st.success(f"✓ Chart ready — {spec.get('title','')}")
                        st.plotly_chart(fig, use_container_width=True)
                        st.markdown(f'<div style="background:rgba(59,130,246,0.06);border:1px solid rgba(59,130,246,0.2);border-radius:10px;padding:10px 14px;font-size:13px;color:#7eb0d4;margin-top:-10px;">💡 {interp}</div>', unsafe_allow_html=True)
                    else:
                        st.warning("Couldn't render chart — try rephrasing")
                else:
                    st.error("Chart spec failed — check API key")
        elif is_fc:
            with st.spinner("📉 Computing forecasts..."):
                fcols = num_cols_list[:3]
                for fc_col in fcols:
                    ts = kpis.get("time_series",{}).get(fc_col,[])
                    if not ts and date_cols_list:
                        # Build ts from df
                        try:
                            tmp = df.copy()
                            tmp["_d"] = pd.to_datetime(tmp[date_cols_list[0]],errors="coerce")
                            tmp = tmp.dropna(subset=["_d"]).sort_values("_d")
                            grp = tmp.groupby("_d")[fc_col].sum().reset_index()
                            ts  = [{"date":str(r["_d"].date()),"value":float(r[fc_col])} for _,r in grp.iterrows()]
                        except: pass
                    if ts:
                        fc_data = forecast_series(ts, periods=10)
                        st.session_state.forecast_data[fc_col] = {"historical":ts,"forecast":fc_data}
                if st.session_state.forecast_data:
                    st.success(f"✓ Forecasts generated for {list(st.session_state.forecast_data.keys())}")
                else:
                    st.warning("No date column found for time-series forecasting. Please ensure your dataset has a date column.")
        elif is_story:
            with st.spinner("📖 Generating narrative dashboard..."):
                domain = st.session_state.results.get("schema",{}).get("domain","") if st.session_state.results else ""
                story_data = generate_story(API_KEY, kpis, schema, anoms, domain)
                st.session_state.results = st.session_state.results or {}
                st.session_state.results["story"] = story_data
                st.success("✓ Story dashboard ready — check Story tab")
        else:
            # Full 5-agent pipeline
            status_map = {k:"waiting" for k,*_ in AGENT_DEFS}
            ph = st.empty()
            ph.markdown(render_pipeline(status_map),unsafe_allow_html=True)
            def scb(agent,status):
                status_map[agent]=status
                ph.markdown(render_pipeline(status_map),unsafe_allow_html=True)
            try:
                with st.spinner("Running ReportGenie 5-Agent AI Pipeline..."):
                    res = run_pipeline(API_KEY,query,df,schema,kpis,anoms,scb)
                st.session_state.results = res
                st.session_state.history.insert(0,{"query":query,"timestamp":datetime.now().strftime("%H:%M · %b %d"),"results":res})
                st.session_state.history = st.session_state.history[:8]
                # Also add to chat
                st.session_state.chat_history.append({"role":"user","content":query})
                summary = res.get("report",{}).get("executive_summary","Analysis complete.")
                st.session_state.chat_history.append({"role":"ai","content":summary})
                ph.markdown(render_pipeline({k:"done" for k,*_ in AGENT_DEFS}),unsafe_allow_html=True)
                st.success("✓ Analysis complete — see Report tab for full results")
            except Exception as e:
                ph.markdown(render_pipeline({**status_map}),unsafe_allow_html=True)
                st.error(f"Pipeline error: {e}")
                st.info("💡 Get a free Gemini key at aistudio.google.com/app/apikey")

# ── KPI CARDS ─────────────────────────────────────────────────────────────────
if kpis and kpis.get("summary"):
    items  = list(kpis["summary"].items())
    ccls   = ["c-blue","c-cyan","c-violet","c-green","c-amber","c-rose"]
    accs   = {"c-blue":"#3b82f6","c-cyan":"#06b6d4","c-violet":"#8b5cf6","c-green":"#10b981","c-amber":"#f59e0b","c-rose":"#f43f5e"}
    icons  = {"currency":"💰","percent":"📉","count":"🔢","plain":"📌"}
    kcols  = st.columns(min(len(items),6))
    for i,(col,stats) in enumerate(items[:6]):
        fmt=stats["format"]; cc=ccls[i%len(ccls)]; ac=accs[cc]
        pc=stats.get("pct_change",0)
        delta_html=f'<div class="kpi-delta {"up" if pc>=0 else "down"}">{"▲" if pc>=0 else "▼"} {abs(pc):.1f}% period</div>' if pc!=0 else ""
        with kcols[i]:
            st.markdown(f"""
            <div class="kpi-c {cc}">
                <div class="kpi-icon">{icons.get(fmt,'📌')}</div>
                <div class="kpi-lbl">{col}</div>
                <div class="kpi-val" style="color:{ac};">{fv(stats['sum'],fmt,short=True)}</div>
                <div class="kpi-sub">avg {fv(stats['mean'],fmt,short=True)} · n={stats['count']:,}</div>
                {delta_html}
            </div>""",unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════════════════════════════
TABS = ["📊 Overview","🤖 Agents","💬 Chat","🚨 Anomalies","📈 Charts",
        "📖 Story","📋 Report","📉 Forecast","🔔 Alerts","🔗 Blend","🗃 Data","🧠 Memory"]
tabs = st.tabs(TABS)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 1 — OVERVIEW
# ─────────────────────────────────────────────────────────────────────────────
with tabs[0]:
    ar = st.session_state.results or {}
    dom = ar.get("schema",{})

    c1,c2,c3 = st.columns([3,2,2])
    with c1:
        st.markdown(f"""
        <div class='glass-card blue'>
            <div style='font-family:JetBrains Mono,monospace;font-size:10px;color:#3b82f6;letter-spacing:1px;text-transform:uppercase;margin-bottom:8px;'>📡 Dataset Domain</div>
            <div style='font-family:Syne,sans-serif;font-size:20px;font-weight:800;color:#e8f4ff;margin-bottom:8px;'>{dom.get("domain","Run analysis to detect domain")}</div>
            <div style='font-size:13px;color:#7eb0d4;line-height:1.7;'>{dom.get("description","Upload a CSV and run an analysis query to activate domain intelligence.")}</div>
        </div>""",unsafe_allow_html=True)

    with c2:
        dq = st.session_state.dq_score
        if dq:
            dq_col2 = "#10b981" if dq["overall"]>=80 else "#f59e0b" if dq["overall"]>=60 else "#f43f5e"
            st.markdown(f"""
            <div class='glass-card green'>
                <div style='font-family:JetBrains Mono,monospace;font-size:10px;color:#10b981;letter-spacing:1px;text-transform:uppercase;margin-bottom:10px;'>📐 Data Quality Score</div>
                <div style='font-family:Syne,sans-serif;font-size:40px;font-weight:800;color:{dq_col2};text-align:center;margin:8px 0;'>{dq["overall"]}%</div>
                {"".join(f'<div style="display:flex;justify-content:space-between;padding:5px 0;border-bottom:1px solid #1a2d45;font-size:11px;"><span style="color:#3a5a78;">{k}</span><span style="color:#e8f4ff;font-family:JetBrains Mono,monospace;">{v}%</span></div>' for k,v in dq["breakdown"].items())}
            </div>""",unsafe_allow_html=True)
        else:
            st.markdown('<div class="glass-card"><div style="font-size:30px;text-align:center;padding:20px;color:#3a5a78;">📐<br><span style="font-size:14px;font-family:Syne,sans-serif;">Upload a dataset to see Data Quality Score</span></div></div>',unsafe_allow_html=True)

    with c3:
        num_t = sum(1 for s in schema.values() if s["type"]=="numeric")
        cat_t = sum(1 for s in schema.values() if s["type"]=="categorical")
        dat_t = sum(1 for s in schema.values() if s["type"]=="date")
        miss  = sum(s.get("missing",0) for s in schema.values())
        st.markdown(f"""
        <div class='glass-card violet'>
            <div style='font-family:JetBrains Mono,monospace;font-size:10px;color:#8b5cf6;letter-spacing:1px;text-transform:uppercase;margin-bottom:10px;'>🗂 Dataset Stats</div>
            {"".join(f'<div style="display:flex;justify-content:space-between;padding:7px 0;border-bottom:1px solid #1a2d45;font-size:12px;"><span style="color:#3a5a78;">{l}</span><span style="color:#e8f4ff;font-family:JetBrains Mono,monospace;font-size:11px;">{v}</span></div>' for l,v in [
                ("Rows",f"{df.shape[0]:,}"),("Columns",df.shape[1]),
                ("Numeric cols",num_t),("Categorical cols",cat_t),
                ("Date cols",dat_t),("Missing values",miss),
                ("Anomalies detected",len(anoms)),("File",st.session_state.filename)])}
        </div>""",unsafe_allow_html=True)

    # Column roles
    if dom.get("column_roles"):
        sec("Column Intelligence (AI-detected)", "#06b6d4")
        tc2={"numeric":"#3b82f6","categorical":"#8b5cf6","date":"#06b6d4","boolean":"#10b981","text":"#f59e0b"}
        rcols=st.columns(3)
        for i,(col,role) in enumerate(dom["column_roles"].items()):
            cl=tc2.get(schema.get(col,{}).get("type",""),"#7eb0d4")
            with rcols[i%3]:
                st.markdown(f'<div style="background:#0a1525;border:1px solid #1a2d45;border-radius:10px;padding:10px 13px;margin-bottom:8px;"><div style="display:flex;align-items:center;gap:6px;margin-bottom:4px;"><span style="width:5px;height:5px;background:{cl};border-radius:50%;"></span><span style="font-family:JetBrains Mono,monospace;font-size:10px;color:{cl};">{col}</span></div><div style="font-size:11px;color:#7eb0d4;line-height:1.5;">{role}</div></div>',unsafe_allow_html=True)

    if dom.get("suggested_analyses"):
        sec("Suggested Analyses", "#10b981")
        for s in dom["suggested_analyses"]:
            st.markdown(f'<div style="background:#0a1525;border:1px solid #1a2d45;border-radius:9px;padding:10px 14px;margin-bottom:7px;font-size:13px;color:#7eb0d4;"><span style="color:#3b82f6;margin-right:7px;">→</span>{s}</div>',unsafe_allow_html=True)

    if kpis.get("summary"):
        sec("Full Numeric Summary (Auto-computed)", "#f59e0b")
        rows=[{"Column":c,"Format":s["format"],"Total":fv(s["sum"],s["format"]),"Mean":fv(s["mean"],s["format"]),"Median":fv(s["median"],s["format"]),"Std":fv(s["std"],s["format"]),"Min":fv(s["min"],s["format"]),"Max":fv(s["max"],s["format"]),"Count":f"{s['count']:,}","Trend":f"{'▲' if s.get('pct_change',0)>=0 else '▼'} {abs(s.get('pct_change',0)):.1f}%"} for c,s in kpis["summary"].items()]
        st.dataframe(pd.DataFrame(rows),use_container_width=True,hide_index=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 2 — AGENTS
# ─────────────────────────────────────────────────────────────────────────────
with tabs[1]:
    ar = st.session_state.results
    if not ar:
        st.markdown('<div style="text-align:center;padding:60px 20px;"><div style="font-size:48px;margin-bottom:14px;">🤖</div><div style="font-family:Syne,sans-serif;font-size:18px;font-weight:700;color:#e8f4ff;margin-bottom:7px;">5-Agent Pipeline Ready</div><div style="color:#3a5a78;font-size:13px;">Enter a query above and click Analyze to activate all 5 agents</div></div>',unsafe_allow_html=True)
    else:
        st.markdown(render_pipeline({k:"done" for k,*_ in AGENT_DEFS}),unsafe_allow_html=True)
        a1,a2=st.columns(2)
        with a1:
            if ar.get("kpi"):
                st.markdown('<div class="glass-card blue"><div style="font-family:JetBrains Mono,monospace;font-size:10px;color:#3b82f6;letter-spacing:1px;text-transform:uppercase;margin-bottom:10px;">📊 KPI Agent Output</div>',unsafe_allow_html=True)
                st.markdown(f'<div style="font-size:12px;color:#7eb0d4;line-height:1.7;margin-bottom:12px;">{ar["kpi"].get("kpi_summary","")}</div>',unsafe_allow_html=True)
                for k in ar["kpi"].get("top_kpis",[]):
                    ic={"High":"#f43f5e","Medium":"#f59e0b","Low":"#10b981"}.get(k.get("importance",""),"#3b82f6")
                    st.markdown(f'<div style="padding:9px 0;border-bottom:1px solid #1a2d45;display:flex;justify-content:space-between;align-items:center;"><div><div style="font-size:12px;color:#e8f4ff;font-weight:500;">{k.get("display_label",k.get("name",""))}</div><div style="font-size:10px;color:#3a5a78;margin-top:1px;">{k.get("insight","")}</div></div><div style="text-align:right;"><div style="font-family:Syne,sans-serif;font-size:15px;font-weight:700;color:{ic};">{k.get("value","")}</div><div style="font-size:8px;color:{ic};font-family:JetBrains Mono,monospace;">{k.get("importance","")}</div></div></div>',unsafe_allow_html=True)
                st.markdown('</div>',unsafe_allow_html=True)
        with a2:
            if ar.get("critic"):
                conf=ar["critic"].get("overall_confidence",0.8)
                cc="#10b981" if conf>=0.8 else "#f59e0b" if conf>=0.6 else "#f43f5e"
                st.markdown(f'<div class="glass-card amber"><div style="font-family:JetBrains Mono,monospace;font-size:10px;color:#f59e0b;letter-spacing:1px;text-transform:uppercase;margin-bottom:10px;">🔬 Critic Agent</div><div style="display:flex;align-items:center;gap:10px;margin-bottom:12px;"><div style="font-family:Syne,sans-serif;font-size:32px;font-weight:800;color:{cc};">{int(conf*100)}%</div><div><div style="font-size:11px;color:#7eb0d4;">Overall Confidence</div><div style="font-size:11px;color:{cc};font-weight:600;">{ar["critic"].get("report_quality","")}</div></div></div><div style="font-size:12px;color:#7eb0d4;line-height:1.7;margin-bottom:12px;">{ar["critic"].get("critic_summary","")}</div>',unsafe_allow_html=True)
                for vi in ar["critic"].get("validated_insights",[])[:3]:
                    vc=vi.get("confidence",0.75); vd=vi.get("verdict","")
                    vc2={"Confirmed":"#10b981","Plausible":"#f59e0b","Speculative":"#f43f5e"}.get(vd,"#3b82f6")
                    st.markdown(f'<div style="padding:8px 0;border-bottom:1px solid #1a2d45;"><div style="display:flex;justify-content:space-between;margin-bottom:3px;"><span style="font-size:12px;color:#e8f4ff;">{vi.get("title","")}</span><span style="font-size:8px;color:{vc2};font-family:JetBrains Mono,monospace;font-weight:700;">{vd}</span></div><div style="background:#1a2d45;border-radius:3px;height:3px;margin:4px 0;"><div style="width:{int(vc*100)}%;height:100%;background:linear-gradient(90deg,#3b82f6,#06b6d4);border-radius:3px;"></div></div><div style="font-size:10px;color:#3a5a78;font-style:italic;">{vi.get("caveat","")}</div></div>',unsafe_allow_html=True)
                st.markdown('</div>',unsafe_allow_html=True)

        if ar.get("insight"):
            sec("Insight Agent — Causal Analysis","#10b981")
            st.markdown(f'<div style="background:rgba(16,185,129,0.05);border:1px solid rgba(16,185,129,0.2);border-left:3px solid #10b981;border-radius:12px;padding:14px 18px;margin-bottom:14px;font-size:13px;color:#7eb0d4;line-height:1.8;">{ar["insight"].get("executive_summary","")}</div>',unsafe_allow_html=True)
            ic2=st.columns(2)
            for i,ins in enumerate(ar["insight"].get("insights",[])):
                conf=ins.get("confidence",0.75); urg=ins.get("urgency","Medium")
                uc={"High":"#f43f5e","Medium":"#f59e0b","Low":"#10b981"}.get(urg,"#3b82f6")
                with ic2[i%2]:
                   st.markdown(
    f"""
    <div style="background:rgba(255,255,255,0.02);border:1px solid #1a2d45;border-radius:12px;padding:14px;margin-bottom:10px;">
        <div style="font-family:Syne,sans-serif;font-weight:700;font-size:14px;color:#e8f4ff;margin-bottom:6px;">
            {ins.get("title","")}
        </div>
        <div style="font-size:12px;color:#7eb0d4;line-height:1.6;">
            {ins.get("explanation","")}
        </div>

        {f'<div style="font-size:11px;color:#f59e0b;margin-top:6px;">↳ Cause: {ins["cause"]}</div>' if ins.get("cause") else ""}

        {f'<div style="font-size:11px;color:#f43f5e;margin-top:3px;">↳ Impact: {ins["impact"]}</div>' if ins.get("impact") else ""}

        <div style="margin-top:10px;display:flex;align-items:center;gap:8px;">
            <div style="flex:1;background:#1a2d45;border-radius:3px;height:3px;">
                <div style="width:{int(conf*100)}%;height:100%;background:linear-gradient(90deg,#3b82f6,#06b6d4);border-radius:3px;"></div>
            </div>
            <span style="font-size:9px;color:#3b82f6;font-family:JetBrains Mono,monospace;">
                {int(conf*100)}% conf
            </span>
            <span style="font-size:9px;color:{uc};font-weight:700;font-family:JetBrains Mono,monospace;">
                {urg}
            </span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
        # Root cause analysis
        if ar.get("report",{}).get("root_causes"):
            sec("Root Cause Analysis (Deep AI)","#a855f7")
            for rc in ar["report"]["root_causes"]:
                st.markdown(f'<div style="background:#0a1525;border:1px solid #1a2d45;border-left:3px solid #a855f7;border-radius:10px;padding:12px 16px;margin-bottom:9px;"><div style="font-weight:600;font-size:13px;color:#e8f4ff;margin-bottom:4px;">{rc.get("finding","")}</div><div style="font-size:12px;color:#a855f7;margin-bottom:4px;">Root Cause: {rc.get("cause","")}</div><div style="font-size:11px;color:#3a5a78;">Evidence: {rc.get("evidence","")}</div></div>',unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 3 — CHAT
# ─────────────────────────────────────────────────────────────────────────────
with tabs[2]:
    st.markdown('<div style="font-family:Syne,sans-serif;font-size:16px;font-weight:700;color:#e8f4ff;margin-bottom:14px;">💬 Conversational Analytics Chat</div>',unsafe_allow_html=True)
    st.markdown('<div style="font-size:12px;color:#3a5a78;margin-bottom:16px;">Ask follow-up questions. ReportGenie AI remembers your previous analysis context.</div>',unsafe_allow_html=True)

    # Chat history
    if st.session_state.chat_history:
        st.markdown('<div class="chat-wrap">',unsafe_allow_html=True)
        for msg in st.session_state.chat_history:
            role = msg["role"]
            av = "👤" if role=="user" else "🧞"
            st.markdown(f'<div class="chat-msg {role}"><div class="chat-avatar">{av}</div><div class="chat-bubble">{msg["content"]}</div></div>',unsafe_allow_html=True)
        st.markdown('</div>',unsafe_allow_html=True)
    else:
        st.markdown('<div style="text-align:center;padding:40px;color:#3a5a78;"><div style="font-size:36px;margin-bottom:10px;">💬</div><div style="font-size:13px;">Start a conversation! Run an analysis above then ask follow-up questions here.</div></div>',unsafe_allow_html=True)

    # Chat input
    cc1,cc2=st.columns([5,1])
    with cc1:
        chat_q=st.text_input("chat",label_visibility="collapsed",placeholder="Ask a follow-up: 'Why did this spike happen?' · 'Drill into Region A' · 'Compare Q1 vs Q2'",key="chat_input")
    with cc2:
        chat_btn=st.button("Send 💬",use_container_width=True,key="chat_send")

    if chat_btn and chat_q and API_KEY:
        st.session_state.chat_history.append({"role":"user","content":chat_q})
        # Build context
        context = ""
        if st.session_state.results:
            context = f"""Previous analysis context:
- Domain: {st.session_state.results.get('schema',{}).get('domain','')}
- Executive Summary: {st.session_state.results.get('report',{}).get('executive_summary','')}
- Key KPIs: {json.dumps({c:{"sum":s["sum"],"format":s["format"]} for c,s in kpis.get("summary",{}).items()}, default=str)}
- Key findings: {', '.join(st.session_state.results.get('report',{}).get('key_findings',[])[:3])}
"""
        data_context = f"Dataset has {df.shape[0]} rows, columns: {', '.join(df.columns.tolist()[:10])}"
        full_prompt  = f"""{context}
{data_context}

Chat history:
{chr(10).join(f"{m['role'].upper()}: {m['content']}" for m in st.session_state.chat_history[-4:])}

User follow-up: "{chat_q}"

Answer concisely and helpfully as ReportGenie AI. Reference specific data/numbers where possible. Keep it under 150 words."""

        with st.spinner("Thinking..."):
            reply = call_gemini_text(API_KEY, full_prompt, max_tokens=500)
        st.session_state.chat_history.append({"role":"ai","content":reply})
        st.rerun()

    if st.button("Clear Chat 🗑",key="clear_chat"):
        st.session_state.chat_history=[]
        st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# TAB 4 — ANOMALIES
# ─────────────────────────────────────────────────────────────────────────────
with tabs[3]:
    if not anoms:
        st.markdown('<div style="text-align:center;padding:60px;color:#3a5a78;font-size:15px;">✓ No significant anomalies detected (threshold: Z ≥ 2.0σ)</div>',unsafe_allow_html=True)
    else:
        sc_counts={"high":sum(1 for a in anoms if a["severity"]=="high"),"medium":sum(1 for a in anoms if a["severity"]=="medium"),"low":sum(1 for a in anoms if a["severity"]=="low")}
        mc=st.columns(4)
        for i,(lbl,val,cl) in enumerate([("High Severity",sc_counts["high"],"#f43f5e"),("Medium Severity",sc_counts["medium"],"#f59e0b"),("Low Severity",sc_counts["low"],"#3b82f6"),("Total Detected",len(anoms),"#06b6d4")]):
            with mc[i]:
                st.markdown(f'<div class="kpi-c"><div class="kpi-lbl">{lbl}</div><div class="kpi-val" style="color:{cl};">{val}</div><div style="position:absolute;bottom:0;left:0;right:0;height:2px;background:linear-gradient(90deg,{cl},transparent);"></div></div>',unsafe_allow_html=True)
        st.markdown("<br>",unsafe_allow_html=True)
        for a in anoms:
            sc2={"high":"#f43f5e","medium":"#f59e0b","low":"#3b82f6"}.get(a["severity"],"#7eb0d4")
            icon="📈" if "↑" in a["direction"] else "📉"
            st.markdown(f"""<div class="anom {a['severity']}">
                <div style="font-size:24px;flex-shrink:0;">{icon}</div>
                <div style="flex:1;">
                    <div style="font-weight:600;font-size:13px;color:#e8f4ff;margin-bottom:3px;">{a["column"]} — {a["direction"]} <span style="display:inline-block;padding:1px 7px;border-radius:99px;font-size:9px;font-family:JetBrains Mono,monospace;font-weight:700;background:{sc2}20;color:{sc2};border:1px solid {sc2}40;margin-left:6px;">{a["z_score"]}σ</span></div>
                    <div style="font-size:13px;color:#e8f4ff;margin:3px 0;">Value: <b style="color:{sc2};">{fv(a["value"],a["format"])}</b> vs avg: {fv(a["mean"],a["format"])}</div>
                    <div style="font-size:10px;color:#3a5a78;font-family:JetBrains Mono,monospace;">{a["context"]}</div>
                </div>
                <div style="text-align:right;flex-shrink:0;"><div style="font-size:9px;color:{sc2};font-family:JetBrains Mono,monospace;font-weight:700;background:{sc2}10;border:1px solid {sc2}30;border-radius:6px;padding:3px 8px;">{a["severity"].upper()}</div>
                <div style="font-size:9px;color:#3a5a78;margin-top:4px;font-family:JetBrains Mono,monospace;">Group: {a["group"]}</div></div>
            </div>""",unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 5 — CHARTS (NL → Charts + static charts)
# ─────────────────────────────────────────────────────────────────────────────
with tabs[4]:
    sec("Natural Language → Charts","#3b82f6")
    st.markdown('<div style="font-size:12px;color:#3a5a78;margin-bottom:12px;">Type chart requests in the main query box above (e.g. "Show revenue by region as bar chart"). Generated charts appear here.</div>',unsafe_allow_html=True)

    if st.session_state.chart_specs:
        for cs in st.session_state.chart_specs:
            st.markdown(f'<div style="background:#0a1525;border:1px solid #1a2d45;border-radius:10px;padding:10px 14px;margin-bottom:4px;font-size:12px;color:#7eb0d4;"><span style="color:#3b82f6;margin-right:6px;">Query:</span>{cs["query"]}</div>',unsafe_allow_html=True)
            result = render_chart_from_spec(df, cs["spec"], schema)
            if result:
                fig, interp = result
                st.plotly_chart(fig, use_container_width=True)
                st.markdown(f'<div style="font-size:12px;color:#3a5a78;margin-bottom:16px;">💡 {interp}</div>',unsafe_allow_html=True)
        if st.button("Clear All Charts"):
            st.session_state.chart_specs=[]
            st.rerun()
    else:
        st.markdown('<div style="background:#060d18;border:1px dashed #1a2d45;border-radius:12px;padding:24px;text-align:center;margin-bottom:20px;color:#3a5a78;font-size:13px;">Type a chart request in the main query box<br><span style="font-family:JetBrains Mono,monospace;font-size:11px;">e.g. "Show revenue by region as bar chart"</span></div>',unsafe_allow_html=True)

    sec("Auto-Generated Charts (Static)","#8b5cf6")

    if kpis.get("time_series"):
        sec("Time Series","#3b82f6")
        ts_keys=list(kpis["time_series"].keys())
        for i in range(0,min(len(ts_keys),4),2):
            gc=st.columns(2)
            for j,cn in enumerate(ts_keys[i:i+2]):
                dts=pd.DataFrame(kpis["time_series"][cn])
                fig=go.Figure()
                fig.add_trace(go.Scatter(x=dts["date"],y=dts["value"],mode="lines+markers",
                    line=dict(color="#3b82f6",width=2.5),marker=dict(size=5,color="#06b6d4"),
                    fill="tozeroy",fillcolor="rgba(59,130,246,0.07)",name=cn))
                ply(fig,cn,h=240); fig.update_layout(showlegend=False)
                with gc[j]: st.plotly_chart(fig,use_container_width=True)

    if kpis.get("breakdowns"):
        sec("Category Breakdowns","#8b5cf6")
        bkeys=list(kpis["breakdowns"].items())[:6]
        for i in range(0,len(bkeys),2):
            bc=st.columns(2)
            for j,(key,bd) in enumerate(bkeys[i:i+2]):
                dfb=pd.DataFrame(bd["data"]).sort_values("sum",ascending=False)
                fig=go.Figure(go.Bar(x=dfb[bd["by"]],y=dfb["sum"],
                    marker_color=PLY_COLORS[:len(dfb)],
                    text=[fv(v,bd["format"],short=True) for v in dfb["sum"]],
                    textposition="outside",textfont=dict(color="#e8f4ff",size=10)))
                ply(fig,f'{bd["metric"]} by {bd["by"]}',h=260); fig.update_layout(showlegend=False)
                with bc[j]: st.plotly_chart(fig,use_container_width=True)

    if num_cols_list:
        sec("Distributions","#10b981")
        for i in range(0,min(len(num_cols_list),4),2):
            dc=st.columns(2)
            for j,cn in enumerate(num_cols_list[i:i+2]):
                fig=px.histogram(df,x=cn,nbins=30,color_discrete_sequence=["#3b82f6"])
                ply(fig,f"Distribution: {cn}",h=230); fig.update_layout(showlegend=False)
                fig.update_traces(marker_line_color="#1a2d45",marker_line_width=0.5)
                with dc[j]: st.plotly_chart(fig,use_container_width=True)

    if len(num_cols_list)>=3:
        sec("Correlation Heatmap","#f59e0b")
        corr=df[num_cols_list].corr()
        fig=go.Figure(go.Heatmap(z=corr.values,x=corr.columns.tolist(),y=corr.columns.tolist(),
            colorscale=[[0,"#f43f5e"],[0.5,"#0a1525"],[1,"#3b82f6"]],
            text=[[f"{v:.2f}" for v in row] for row in corr.values],texttemplate="%{text}",
            zmin=-1,zmax=1,colorbar=dict(tickfont=dict(color="#7eb0d4"))))
        ply(fig,"Correlation Heatmap",h=400)
        st.plotly_chart(fig,use_container_width=True)

    if len(num_cols_list)>=2 and cat_cols_list:
        sec("Scatter","#f43f5e")
        fig=px.scatter(df,x=num_cols_list[0],y=num_cols_list[1],color=cat_cols_list[0],
            color_discrete_sequence=PLY_COLORS)
        ply(fig,f"{num_cols_list[0]} vs {num_cols_list[1]}",h=360)
        fig.update_traces(marker=dict(size=8,line=dict(width=0.5,color="#0a1525")))
        st.plotly_chart(fig,use_container_width=True)

    if num_cols_list and cat_cols_list:
        sec("Box Plots","#a855f7")
        fig=px.box(df,x=cat_cols_list[0],y=num_cols_list[0],color=cat_cols_list[0],
            color_discrete_sequence=PLY_COLORS)
        ply(fig,f"{num_cols_list[0]} by {cat_cols_list[0]}",h=320)
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig,use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 6 — STORY
# ─────────────────────────────────────────────────────────────────────────────
with tabs[5]:
    ar = st.session_state.results or {}
    stories_data = ar.get("story",{})

    if not stories_data or not stories_data.get("stories"):
        st.markdown('<div style="text-align:center;padding:40px 20px;"><div style="font-size:48px;margin-bottom:14px;">📖</div><div style="font-family:Syne,sans-serif;font-size:18px;font-weight:700;color:#e8f4ff;margin-bottom:7px;">Auto-Narrative Dashboard</div><div style="color:#3a5a78;font-size:13px;margin-bottom:20px;">Type "Generate storytelling dashboard" in the query box above</div></div>',unsafe_allow_html=True)
        if st.button("✨ Generate Story Dashboard Now"):
            domain = ar.get("schema",{}).get("domain","") if ar else ""
            with st.spinner("📖 Generating narrative story cards..."):
                story_data = generate_story(API_KEY,kpis,schema,anoms,domain)
            st.session_state.results = ar or {}
            st.session_state.results["story"] = story_data
            st.rerun()
    else:
        sec("Auto-Narrative Story Dashboard","#3b82f6")
        domain = ar.get("schema",{}).get("domain","Your Dataset")
        st.markdown(f'<div style="font-family:Syne,sans-serif;font-size:18px;font-weight:700;color:#e8f4ff;margin-bottom:16px;">📖 {domain} — Business Story</div>',unsafe_allow_html=True)
        for i,story in enumerate(stories_data.get("stories",[])):
            sent=story.get("sentiment","neutral")
            sc2={"positive":"pos","negative":"neg","neutral":"neu"}.get(sent,"neu")
            cc={"positive":"#10b981","negative":"#f43f5e","neutral":"#3b82f6"}.get(sent,"#3b82f6")
            ic=story.get("icon","📌")
            st.markdown(f"""
            <div class="story-card {sc2}">
                <div class="story-number">{i+1}</div>
                <div style="flex:1;">
                    <div style="font-family:Syne,sans-serif;font-weight:700;font-size:16px;color:#e8f4ff;margin-bottom:6px;">{ic} {story.get("headline","")}</div>
                    <div style="font-size:13px;color:#7eb0d4;line-height:1.7;">{story.get("detail","")}</div>
                    {f'<div style="font-size:10px;color:{cc};font-family:JetBrains Mono,monospace;margin-top:8px;text-transform:uppercase;letter-spacing:0.5px;">{sent.upper()} · {story.get("metric","")}</div>' if story.get("metric") else ""}
                </div>
                <div style="font-size:28px;flex-shrink:0;opacity:0.5;">{ic}</div>
            </div>""",unsafe_allow_html=True)

        # Regenerate
        if st.button("🔄 Regenerate Story"):
            domain = ar.get("schema",{}).get("domain","") if ar else ""
            with st.spinner("Regenerating..."):
                sd=generate_story(API_KEY,kpis,schema,anoms,domain)
            st.session_state.results["story"]=sd
            st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# TAB 7 — REPORT
# ─────────────────────────────────────────────────────────────────────────────
with tabs[6]:
    ar = st.session_state.results
    if not ar or not ar.get("report"):
        st.markdown('<div style="text-align:center;padding:60px 20px;"><div style="font-size:48px;margin-bottom:14px;">📋</div><div style="font-family:Syne,sans-serif;font-size:18px;font-weight:700;color:#e8f4ff;margin-bottom:7px;">No Report Yet</div><div style="color:#3a5a78;font-size:13px;">Run an analysis query to generate your AI executive report</div></div>',unsafe_allow_html=True)
    else:
        rep=ar["report"]
        st.markdown(f"""
        <div class='glass-card blue' style='margin-bottom:18px;'>
            <div style='font-family:Syne,sans-serif;font-size:24px;font-weight:800;color:#e8f4ff;margin-bottom:12px;letter-spacing:-0.3px;'>{rep.get("title","Executive Report")}</div>
            <div style='font-size:14px;color:#7eb0d4;line-height:1.9;border-top:1px solid #1a2d45;padding-top:12px;'>{rep.get("executive_summary","")}</div>
        </div>""",unsafe_allow_html=True)

        rc1,rc2=st.columns(2)
        with rc1:
            st.markdown('<div class="glass-card violet"><div style="font-family:JetBrains Mono,monospace;font-size:10px;color:#8b5cf6;letter-spacing:1px;text-transform:uppercase;margin-bottom:12px;">🔍 Key Findings</div>',unsafe_allow_html=True)
            for f in rep.get("key_findings",[]):
                st.markdown(f'<div style="display:flex;gap:8px;margin-bottom:9px;font-size:13px;color:#7eb0d4;line-height:1.6;"><span style="color:#3b82f6;font-weight:700;flex-shrink:0;">→</span><span>{f}</span></div>',unsafe_allow_html=True)
            st.markdown('</div>',unsafe_allow_html=True)
        with rc2:
            st.markdown('<div class="glass-card green"><div style="font-family:JetBrains Mono,monospace;font-size:10px;color:#10b981;letter-spacing:1px;text-transform:uppercase;margin-bottom:12px;">⚡ Recommendations</div>',unsafe_allow_html=True)
            for rec in rep.get("recommendations",[]):
                pri=rec.get("priority","Medium")
                pc={"High":"#f43f5e","Medium":"#f59e0b","Low":"#10b981"}.get(pri,"#3b82f6")
                st.markdown(f'<div style="background:rgba(255,255,255,0.02);border:1px solid #1a2d45;border-radius:10px;padding:12px;margin-bottom:8px;"><div style="margin-bottom:5px;"><span style="background:{pc}18;border:1px solid {pc}30;border-radius:99px;padding:2px 8px;font-size:9px;color:{pc};font-weight:700;margin-right:6px;">{pri}</span><span style="font-size:10px;color:#3a5a78;font-family:JetBrains Mono,monospace;">{rec.get("timeline","")}</span></div><div style="font-size:13px;color:#e8f4ff;font-weight:500;margin-bottom:3px;">{rec.get("action","")}</div><div style="font-size:11px;color:#3a5a78;">{rec.get("impact","")}</div></div>',unsafe_allow_html=True)
            st.markdown('</div>',unsafe_allow_html=True)

        if rep.get("anomaly_narratives"):
            st.markdown('<div class="glass-card rose"><div style="font-family:JetBrains Mono,monospace;font-size:10px;color:#f43f5e;letter-spacing:1px;text-transform:uppercase;margin-bottom:12px;">🚨 Anomaly Narratives</div>',unsafe_allow_html=True)
            for an in rep["anomaly_narratives"]:
                urg=an.get("urgency","Medium")
                uc={"High":"#f43f5e","Medium":"#f59e0b","Low":"#10b981"}.get(urg,"#3b82f6")
                st.markdown(f'<div style="padding:10px 0;border-bottom:1px solid #1a2d45;"><div style="display:flex;align-items:center;gap:8px;margin-bottom:5px;"><span style="font-size:9px;color:{uc};font-family:JetBrains Mono,monospace;font-weight:700;background:{uc}10;border:1px solid {uc}30;border-radius:6px;padding:2px 7px;">{urg}</span><span style="font-size:13px;color:#e8f4ff;font-weight:600;">{an.get("event","")}</span></div><div style="font-size:12px;color:#7eb0d4;line-height:1.6;">{an.get("explanation","")}</div></div>',unsafe_allow_html=True)
            st.markdown('</div>',unsafe_allow_html=True)

        nc1,nc2=st.columns(2)
        with nc1:
            st.markdown('<div class="glass-card purple"><div style="font-family:JetBrains Mono,monospace;font-size:10px;color:#a855f7;letter-spacing:1px;text-transform:uppercase;margin-bottom:10px;">👁 KPIs to Watch</div>',unsafe_allow_html=True)
            for k in rep.get("next_kpis_to_watch",[]):
                st.markdown(f'<span style="display:inline-block;background:rgba(168,85,247,0.1);border:1px solid rgba(168,85,247,0.3);border-radius:99px;padding:4px 13px;font-size:12px;color:#a855f7;margin:3px 3px 3px 0;">{k}</span>',unsafe_allow_html=True)
            st.markdown('</div>',unsafe_allow_html=True)
        with nc2:
            st.markdown('<div class="glass-card rose"><div style="font-family:JetBrains Mono,monospace;font-size:10px;color:#f43f5e;letter-spacing:1px;text-transform:uppercase;margin-bottom:10px;">⚠ Risk Flags</div>',unsafe_allow_html=True)
            for r in rep.get("risk_flags",[]):
                st.markdown(f'<div style="display:flex;gap:7px;margin-bottom:7px;font-size:12px;color:#7eb0d4;"><span style="color:#f43f5e;">⚠</span>{r}</div>',unsafe_allow_html=True)
            st.markdown('</div>',unsafe_allow_html=True)

        # Export
        sec("Export Options","#06b6d4")
        exp1,exp2=st.columns(2)
        with exp1:
            # CSV report
            report_rows=[{"Section":"Executive Summary","Content":rep.get("executive_summary","")},
                         *[{"Section":"Key Finding","Content":f} for f in rep.get("key_findings",[])],
                         *[{"Section":"Recommendation","Content":r.get("action","")} for r in rep.get("recommendations",[])],
                         *[{"Section":"Risk Flag","Content":r} for r in rep.get("risk_flags",[])]]
            csv_bytes=pd.DataFrame(report_rows).to_csv(index=False).encode()
            st.download_button("⬇ Download Report CSV",csv_bytes,file_name="reportgenie_report.csv",mime="text/csv",use_container_width=True)
        with exp2:
            # JSON export
            json_bytes=json.dumps(ar,indent=2,default=str).encode()
            st.download_button("⬇ Download Full JSON",json_bytes,file_name="reportgenie_full.json",mime="application/json",use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 8 — FORECAST
# ─────────────────────────────────────────────────────────────────────────────
with tabs[7]:
    sec("30-Day Trend Forecasting","#8b5cf6")
    st.markdown('<div style="font-size:12px;color:#3a5a78;margin-bottom:14px;">Type "Forecast trends" in the main query box above to generate forecasts. Below shows results.</div>',unsafe_allow_html=True)

    if not st.session_state.forecast_data:
        st.markdown('<div style="text-align:center;padding:50px;color:#3a5a78;"><div style="font-size:36px;margin-bottom:12px;">📉</div><div style="font-size:14px;">Type "Forecast trends for next 30 days" in the query box to generate forecasts</div></div>',unsafe_allow_html=True)

        # Offer quick forecast if date col exists
        if date_cols_list and num_cols_list:
            st.markdown("<br>",unsafe_allow_html=True)
            if st.button("📉 Quick Forecast (no AI needed)",use_container_width=False):
                for fc_col in num_cols_list[:3]:
                    ts=kpis.get("time_series",{}).get(fc_col,[])
                    if not ts:
                        try:
                            tmp=df.copy()
                            tmp["_d"]=pd.to_datetime(tmp[date_cols_list[0]],errors="coerce")
                            tmp=tmp.dropna(subset=["_d"]).sort_values("_d")
                            grp=tmp.groupby("_d")[fc_col].sum().reset_index()
                            ts=[{"date":str(r["_d"].date()),"value":float(r[fc_col])} for _,r in grp.iterrows()]
                        except: pass
                    if ts:
                        fc_data=forecast_series(ts,10)
                        st.session_state.forecast_data[fc_col]={"historical":ts,"forecast":fc_data}
                st.rerun()
    else:
        for fc_col,fc_info in st.session_state.forecast_data.items():
            fmt=schema.get(fc_col,{}).get("format","plain")
            hist=fc_info["historical"]; fcast=fc_info["forecast"]
            if not fcast: continue

            st.markdown(f'<div class="forecast-badge">📉 Forecast: {fc_col} · {len(fcast)}-period projection</div>',unsafe_allow_html=True)

            fig=go.Figure()
            # Historical
            fig.add_trace(go.Scatter(x=[d["date"] for d in hist],y=[d["value"] for d in hist],
                mode="lines+markers",name="Historical",
                line=dict(color="#3b82f6",width=2.5),marker=dict(size=5,color="#3b82f6")))
            # Forecast
            fig.add_trace(go.Scatter(x=[d["date"] for d in fcast],y=[d["value"] for d in fcast],
                mode="lines+markers",name="Forecast",
                line=dict(color="#8b5cf6",width=2.5,dash="dash"),marker=dict(size=6,color="#8b5cf6",symbol="diamond")))
            # Confidence band
            fig.add_trace(go.Scatter(
                x=[d["date"] for d in fcast]+[d["date"] for d in reversed(fcast)],
                y=[d["upper"] for d in fcast]+[d["lower"] for d in reversed(fcast)],
                fill="toself",fillcolor="rgba(139,92,246,0.1)",line=dict(color="rgba(0,0,0,0)"),
                name="90% Confidence",showlegend=True))
            # Divider
            if hist and fcast:
                fig.add_vline(x=hist[-1]["date"],line_dash="dot",line_color="#3a5a78",
                    annotation_text="Forecast →",annotation_font_color="#7eb0d4",annotation_font_size=11)
            ply(fig,f"{fc_col} — Historical + Forecast",h=360)
            st.plotly_chart(fig,use_container_width=True)

            # Summary
            last_hist=hist[-1]["value"] if hist else 0
            last_fc  =fcast[-1]["value"] if fcast else 0
            change   =((last_fc-last_hist)/last_hist*100) if last_hist!=0 else 0
            chg_col  ="#10b981" if change>=0 else "#f43f5e"
            st.markdown(f'<div style="display:flex;gap:20px;margin-bottom:20px;padding:12px 16px;background:#060d18;border:1px solid #1a2d45;border-radius:10px;"><div><div style="font-size:10px;color:#3a5a78;font-family:JetBrains Mono,monospace;">LAST ACTUAL</div><div style="font-family:Syne,sans-serif;font-size:18px;font-weight:700;color:#e8f4ff;">{fv(last_hist,fmt,short=True)}</div></div><div><div style="font-size:10px;color:#3a5a78;font-family:JetBrains Mono,monospace;">FORECAST END</div><div style="font-family:Syne,sans-serif;font-size:18px;font-weight:700;color:#8b5cf6;">{fv(last_fc,fmt,short=True)}</div></div><div><div style="font-size:10px;color:#3a5a78;font-family:JetBrains Mono,monospace;">PROJECTED CHANGE</div><div style="font-family:Syne,sans-serif;font-size:18px;font-weight:700;color:{chg_col};">{"▲" if change>=0 else "▼"} {abs(change):.1f}%</div></div></div>',unsafe_allow_html=True)

        if st.button("🔄 Clear Forecasts"):
            st.session_state.forecast_data={}
            st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# TAB 9 — ALERTS
# ─────────────────────────────────────────────────────────────────────────────
with tabs[8]:
    sec("Smart Alert Rules","#f43f5e")
    st.markdown('<div style="font-size:12px;color:#3a5a78;margin-bottom:16px;">Define alert rules. Alerts are checked automatically every time you upload a dataset.</div>',unsafe_allow_html=True)

    # Add rule
    st.markdown('<div class="glass-card blue" style="margin-bottom:16px;"><div style="font-family:Syne,sans-serif;font-size:13px;font-weight:700;color:#3b82f6;margin-bottom:12px;">➕ Add New Alert Rule</div>',unsafe_allow_html=True)
    ar1,ar2,ar3,ar4,ar5=st.columns([2,1.5,1,1,1])
    with ar1:
        rule_col=st.selectbox("Column",num_cols_list if num_cols_list else ["no numeric columns"],key="alert_col")
    with ar2:
        rule_metric=st.selectbox("Metric",["mean","sum","max","min"],key="alert_metric")
    with ar3:
        rule_op=st.selectbox("Operator",[">","<",">=","<=","drop%","rise%"],key="alert_op")
    with ar4:
        rule_thresh=st.number_input("Threshold",value=0.0,key="alert_thresh")
    with ar5:
        rule_name=st.text_input("Rule Name","My Alert",key="alert_name")

    if st.button("➕ Add Alert Rule",key="add_alert"):
        if num_cols_list:
            new_rule={"name":rule_name,"column":rule_col,"metric":rule_metric,"operator":rule_op,"threshold":rule_thresh}
            st.session_state.alert_rules.append(new_rule)
            st.session_state.alert_triggers=check_alerts(df,schema,kpis,st.session_state.alert_rules)
            st.success(f"✓ Alert '{rule_name}' added")
            st.rerun()
    st.markdown('</div>',unsafe_allow_html=True)

    # Show existing rules
    if st.session_state.alert_rules:
        sec("Active Rules","#f59e0b")
        for i,rule in enumerate(st.session_state.alert_rules):
            triggered=any(t.get("name")==rule.get("name") for t in st.session_state.alert_triggers)
            cls="alert-triggered" if triggered else ""
            status_icon="🚨" if triggered else "✅"
            status_col="#f43f5e" if triggered else "#10b981"
            actual_val=""
            if triggered:
                for t in st.session_state.alert_triggers:
                    if t.get("name")==rule.get("name"):
                        actual_val=f" — TRIGGERED: actual={fv(t.get('actual',0),schema.get(rule['column'],{}).get('format','plain'))}"; break
            c1,c2=st.columns([5,1])
            with c1:
                st.markdown(f'<div class="alert-rule {cls}"><div style="display:flex;align-items:center;gap:10px;"><span style="font-size:18px;">{status_icon}</span><div><div style="font-family:Syne,sans-serif;font-weight:700;font-size:13px;color:#e8f4ff;">{rule.get("name","")}</div><div style="font-size:11px;color:#3a5a78;font-family:JetBrains Mono,monospace;">{rule["column"]} {rule["metric"]} {rule["operator"]} {rule["threshold"]}{actual_val}</div></div></div></div>',unsafe_allow_html=True)
            with c2:
                if st.button("🗑",key=f"del_alert_{i}"):
                    st.session_state.alert_rules.pop(i)
                    st.session_state.alert_triggers=check_alerts(df,schema,kpis,st.session_state.alert_rules)
                    st.rerun()
    else:
        st.markdown('<div style="text-align:center;padding:40px;color:#3a5a78;font-size:13px;">No alert rules yet. Add one above.</div>',unsafe_allow_html=True)

    # Triggered alerts
    if st.session_state.alert_triggers:
        sec("🚨 Triggered Alerts","#f43f5e")
        for t in st.session_state.alert_triggers:
            st.error(f"🚨 **{t.get('name','')}**: {t['message']}")

# ─────────────────────────────────────────────────────────────────────────────
# TAB 10 — DATA BLENDING
# ─────────────────────────────────────────────────────────────────────────────
with tabs[9]:
    sec("Multi-File Data Blending","#06b6d4")
    st.markdown('<div style="font-size:12px;color:#3a5a78;margin-bottom:16px;">Upload a second CSV in the sidebar, then blend it with your primary dataset below.</div>',unsafe_allow_html=True)

    if st.session_state.df2 is None:
        st.markdown('<div style="background:#060d18;border:1px dashed #1a2d45;border-radius:12px;padding:30px;text-align:center;color:#3a5a78;font-size:13px;">Upload a second CSV in the sidebar to enable data blending</div>',unsafe_allow_html=True)
    else:
        df2=st.session_state.df2
        st.markdown(f'<div style="background:rgba(6,182,212,0.06);border:1px solid rgba(6,182,212,0.25);border-radius:10px;padding:12px 16px;margin-bottom:16px;font-size:12px;color:#7eb0d4;">📊 Dataset 1: <b>{st.session_state.filename}</b> ({df.shape[0]:,} rows × {df.shape[1]} cols) &nbsp;&nbsp; | &nbsp;&nbsp; 📊 Dataset 2: <b>{st.session_state.filename2}</b> ({df2.shape[0]:,} rows × {df2.shape[1]} cols)</div>',unsafe_allow_html=True)

        # Common columns
        common_cols=list(set(df.columns)&set(df2.columns))
        bc1,bc2,bc3=st.columns(3)
        with bc1:
            join_key=st.selectbox("Join on column:",common_cols if common_cols else df.columns.tolist(),key="blend_key")
        with bc2:
            join_how=st.selectbox("Join type:",["inner","left","right","outer"],key="blend_how")
        with bc3:
            st.markdown("<br>",unsafe_allow_html=True)
            blend_btn=st.button("🔗 Blend Datasets",use_container_width=True,key="do_blend")

        if blend_btn and join_key:
            try:
                blended=pd.merge(df,df2,on=join_key,how=join_how,suffixes=("_primary","_secondary"))
                st.success(f"✓ Blended! Result: {blended.shape[0]:,} rows × {blended.shape[1]} cols")
                st.dataframe(blended.head(50),use_container_width=True,height=350)
                # Option to use blended as main df
                if st.button("✅ Use Blended as Main Dataset"):
                    st.session_state.df      = blended
                    st.session_state.schema  = classify_columns(blended)
                    st.session_state.kpis    = compute_kpis(blended,st.session_state.schema)
                    st.session_state.anomalies=detect_anomalies(blended,st.session_state.schema)
                    st.session_state.filename=f"blended_{st.session_state.filename}"
                    st.success("✓ Blended dataset set as main!")
                    st.rerun()
                # Download
                st.download_button("⬇ Download Blended CSV",blended.to_csv(index=False).encode(),file_name="blended.csv",mime="text/csv")
            except Exception as e:
                st.error(f"Blend error: {e}")

        # Side-by-side comparison
        sec("Side-by-Side Comparison","#8b5cf6")
        c1c,c2c=st.columns(2)
        with c1c:
            st.markdown(f'<div style="font-family:Syne,sans-serif;font-size:13px;font-weight:700;color:#3b82f6;margin-bottom:8px;">{st.session_state.filename}</div>',unsafe_allow_html=True)
            st.dataframe(df.describe(),use_container_width=True)
        with c2c:
            st.markdown(f'<div style="font-family:Syne,sans-serif;font-size:13px;font-weight:700;color:#8b5cf6;margin-bottom:8px;">{st.session_state.filename2}</div>',unsafe_allow_html=True)
            st.dataframe(df2.describe(),use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 11 — DATA PREVIEW
# ─────────────────────────────────────────────────────────────────────────────
with tabs[10]:
    st.markdown(f'<div style="display:flex;align-items:center;gap:10px;margin-bottom:14px;"><div style="font-family:Syne,sans-serif;font-size:15px;font-weight:700;color:#e8f4ff;">Raw Data</div><div style="font-family:JetBrains Mono,monospace;font-size:10px;color:#3a5a78;background:#060d18;border:1px solid #1a2d45;border-radius:6px;padding:2px 8px;">{df.shape[0]:,} × {df.shape[1]}</div><div style="font-family:JetBrains Mono,monospace;font-size:10px;color:#10b981;background:rgba(16,185,129,0.08);border:1px solid rgba(16,185,129,0.2);border-radius:6px;padding:2px 8px;">{st.session_state.filename}</div></div>',unsafe_allow_html=True)

    df_show=df
    if cat_cols_list:
        fc=st.selectbox("Filter by:",[" (none)"]+cat_cols_list,key="data_filter")
        if fc!=" (none)":
            sel=st.multiselect("Values:",df[fc].unique().tolist(),default=df[fc].unique().tolist()[:8],key="data_filter_vals")
            if sel: df_show=df[df[fc].isin(sel)]

    st.dataframe(df_show,use_container_width=True,height=480)

    dd1,dd2=st.columns(2)
    with dd1:
        st.download_button("⬇ Download Dataset",df.to_csv(index=False).encode(),file_name=st.session_state.filename or "data.csv",mime="text/csv",use_container_width=True)
    with dd2:
        st.download_button("⬇ Download KPI Summary",pd.DataFrame([{"Column":c,"Sum":fv(s["sum"],s["format"]),"Mean":fv(s["mean"],s["format"]),"Format":s["format"]} for c,s in kpis.get("summary",{}).items()]).to_csv(index=False).encode(),file_name="kpi_summary.csv",mime="text/csv",use_container_width=True)

    if kpis.get("derived"):
        sec("Auto-Derived Ratios","#f59e0b")
        st.dataframe(pd.DataFrame([{"Ratio":k,"Numerator":v["numerator"],"Denominator":v["denominator"],"Value":round(v["value"],4)} for k,v in kpis["derived"].items()]),use_container_width=True,hide_index=True)

    if st.session_state.cleaned_cols:
        sec("Auto-Cleaned Issues","#10b981")
        for c in st.session_state.cleaned_cols:
            st.markdown(f'<div style="font-size:12px;color:#10b981;padding:4px 0;font-family:JetBrains Mono,monospace;">✓ {c}</div>',unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 12 — MEMORY
# ─────────────────────────────────────────────────────────────────────────────
with tabs[11]:
    if not st.session_state.history:
        st.markdown('<div style="text-align:center;padding:60px 20px;"><div style="font-size:48px;margin-bottom:14px;">🧠</div><div style="font-family:Syne,sans-serif;font-size:18px;font-weight:700;color:#e8f4ff;margin-bottom:7px;">No History Yet</div><div style="color:#3a5a78;font-size:13px;">Your analysis sessions will be saved here automatically</div></div>',unsafe_allow_html=True)
    else:
        st.markdown(f'<div style="background:rgba(59,130,246,0.05);border:1px solid rgba(59,130,246,0.2);border-radius:12px;padding:12px 18px;margin-bottom:18px;font-size:12px;color:#7eb0d4;line-height:1.7;">🧠 <b style="color:#3b82f6;">{len(st.session_state.history)} analyses</b> saved this session. Click any to restore.</div>',unsafe_allow_html=True)
        for i,h in enumerate(st.session_state.history):
            rep=h.get("results",{}).get("report",{})
            domain=h.get("results",{}).get("schema",{}).get("domain","Unknown")
            snippet=(rep.get("executive_summary","")[:180]+"…") if rep.get("executive_summary") else "No summary."
            n_ins=len(h.get("results",{}).get("insight",{}).get("insights",[]))
            n_rec=len(rep.get("recommendations",[]))
            st.markdown(f"""
            <div class="memory-item">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:5px;">
                    <div><div style="font-family:JetBrains Mono,monospace;font-size:8px;color:#3b82f6;letter-spacing:1px;margin-bottom:3px;">#{i+1} · {domain}</div>
                    <div style="font-weight:600;font-size:13px;color:#e8f4ff;">"{h["query"]}"</div></div>
                    <div style="font-family:JetBrains Mono,monospace;font-size:9px;color:#3a5a78;">{h["timestamp"]}</div>
                </div>
                <div style="font-size:11px;color:#3a5a78;line-height:1.5;margin-bottom:7px;">{snippet}</div>
                <div style="font-size:10px;color:#3b82f6;font-family:JetBrains Mono,monospace;">{n_ins} insights · {n_rec} recs · click restore →</div>
            </div>""",unsafe_allow_html=True)
            if st.button(f"♻ Restore #{i+1}",key=f"r_{i}"):
                st.session_state.results=h["results"]
                st.rerun()

        # Pattern analysis
        all_q=" ".join(h["query"].lower() for h in st.session_state.history)
        pats=[kw for kw in ["revenue","sales","customer","churn","growth","profit","cost","anomaly","trend","region","segment","forecast"] if kw in all_q]
        if pats:
            st.markdown(f"""
            <div class='glass-card violet' style='margin-top:18px;'>
                <div style='font-family:JetBrains Mono,monospace;font-size:10px;color:#8b5cf6;letter-spacing:1px;text-transform:uppercase;margin-bottom:10px;'>🔮 Your Analysis Patterns</div>
                <div style='font-size:13px;color:#7eb0d4;margin-bottom:10px;'>Based on {len(st.session_state.history)} sessions, you focus on:</div>
                {"".join(f'<span style="display:inline-block;background:rgba(139,92,246,0.1);border:1px solid rgba(139,92,246,0.3);border-radius:99px;padding:4px 13px;font-size:12px;color:#8b5cf6;margin:3px;">{p}</span>' for p in pats)}
            </div>""",unsafe_allow_html=True)

        if st.button("🗑 Clear All History",key="clear_hist"):
            st.session_state.history=[]
            st.rerun()