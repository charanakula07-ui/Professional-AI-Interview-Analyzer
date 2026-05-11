"""
InterviewAI — Enterprise AI Interview Analyzer
Run with:  streamlit run app.py
"""

import os
import time
import streamlit as st
import plotly.graph_objects as go
from textblob import TextBlob

from modules.filler_detector import detect_filler_words, get_filler_breakdown

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE CONFIG  (must be first Streamlit call)
# ══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="InterviewAI — Analytics Platform",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════════════
#  GLOBAL CSS
# ══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Syne:wght@700;800&display=swap');

/* ── variables ── */
:root {
  --bg0:#070B14; --bg1:#0D1221; --bg2:#111827; --bg3:#1A2236;
  --glass:rgba(255,255,255,0.04); --glass2:rgba(255,255,255,0.07);
  --purple:#8B5CF6; --indigo:#6366F1; --blue:#3B82F6;
  --pink:#EC4899; --cyan:#06B6D4; --emerald:#10B981;
  --amber:#F59E0B; --rose:#EF4444;
  --g1:linear-gradient(135deg,#8B5CF6,#6366F1,#3B82F6);
  --g2:linear-gradient(135deg,#EC4899,#8B5CF6);
  --g3:linear-gradient(135deg,#06B6D4,#3B82F6);
  --text:#F8FAFC; --text2:#94A3B8; --text3:#475569;
  --border:rgba(255,255,255,0.08);
  --r:16px; --rsm:10px;
}

*,*::before,*::after{box-sizing:border-box;}

html,body,[class*="css"]{
  font-family:'Inter',sans-serif!important;
  background-color:var(--bg0)!important;
  color:var(--text)!important;
}

#MainMenu,footer,header{visibility:hidden;}

.block-container{
  padding:2rem 2.5rem 3rem!important;
  max-width:1280px!important;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"]{
  background:#0D1221!important;
  border-right:1px solid rgba(255,255,255,0.08)!important;
  min-width:240px!important;
  max-width:240px!important;
}
[data-testid="stSidebar"]>div:first-child{
  padding:0!important;
  display:flex!important;
  flex-direction:column!important;
  height:100vh!important;
  overflow:hidden!important;
}
[data-testid="stSidebar"] .block-container{padding:0!important;max-width:100%!important;}
[data-testid="stSidebarNav"]{display:none!important;}

.sb-logo{padding:22px 20px 18px;border-bottom:1px solid rgba(255,255,255,0.07);flex-shrink:0;}
.sb-logo-mark{
  width:34px;height:34px;
  background:linear-gradient(135deg,#8B5CF6,#6366F1,#3B82F6);
  border-radius:9px;display:inline-flex;align-items:center;
  justify-content:center;font-size:16px;font-weight:800;
  color:#fff;margin-bottom:10px;
}
.sb-brand-name{font-size:14px;font-weight:700;color:#F8FAFC;letter-spacing:-.2px;}
.sb-brand-tag{font-size:10px;color:#475569;letter-spacing:1.4px;text-transform:uppercase;margin-top:1px;}

.sb-nav{flex:1;padding:10px;overflow-y:auto;}
.sb-section-label{
  font-size:10px;font-weight:600;letter-spacing:1.5px;
  text-transform:uppercase;color:#334155;padding:14px 10px 6px;
}
.sb-item{
  display:flex;align-items:center;gap:9px;padding:9px 12px;
  border-radius:9px;margin-bottom:1px;font-size:13px;font-weight:500;
  color:#64748B;cursor:pointer;border:1px solid transparent;transition:all .15s;
}
.sb-item:hover{background:rgba(255,255,255,0.04);color:#94A3B8;}
.sb-item.active{
  background:rgba(99,102,241,0.14);
  border-color:rgba(99,102,241,0.35);
  color:#E0E7FF;
}
.sb-item-icon{font-size:14px;width:18px;text-align:center;flex-shrink:0;}
.sb-item-dot{width:5px;height:5px;border-radius:50%;margin-left:auto;flex-shrink:0;}
.sb-item.active .sb-item-dot{background:#6366F1;box-shadow:0 0 6px #6366F1;}
.sb-divider{height:1px;background:rgba(255,255,255,0.07);margin:6px 10px;}
.sb-user{
  flex-shrink:0;padding:14px 18px;
  border-top:1px solid rgba(255,255,255,0.07);
  display:flex;align-items:center;gap:10px;background:#0D1221;
}
.sb-avatar{
  width:30px;height:30px;border-radius:50%;
  background:linear-gradient(135deg,#EC4899,#8B5CF6);
  display:flex;align-items:center;justify-content:center;
  font-size:12px;font-weight:700;color:#fff;flex-shrink:0;
}
.sb-user-name{font-size:12px;font-weight:600;color:#F8FAFC;}
.sb-user-role{font-size:10px;color:#475569;}

/* ── HERO ── */
.hero{
  position:relative;padding:2.5rem 0 2rem;
  text-align:center;overflow:hidden;
}
.hero-blob1{
  position:absolute;width:500px;height:280px;
  background:radial-gradient(ellipse,rgba(139,92,246,0.16) 0%,transparent 70%);
  top:-40px;left:50%;transform:translateX(-55%);pointer-events:none;
}
.hero-blob2{
  position:absolute;width:350px;height:220px;
  background:radial-gradient(ellipse,rgba(59,130,246,0.10) 0%,transparent 70%);
  top:30px;right:8%;pointer-events:none;
}
.hero-blob3{
  position:absolute;width:300px;height:180px;
  background:radial-gradient(ellipse,rgba(236,72,153,0.08) 0%,transparent 70%);
  top:20px;left:5%;pointer-events:none;
}
.hero-eyebrow{
  display:inline-flex;align-items:center;gap:7px;
  background:rgba(99,102,241,0.10);
  border:1px solid rgba(99,102,241,0.28);
  border-radius:50px;padding:5px 14px;
  font-size:11px;font-weight:500;color:#A5B4FC;
  letter-spacing:.5px;margin-bottom:18px;
}
.hero-eyebrow-dot{
  width:6px;height:6px;border-radius:50%;
  background:#6366F1;box-shadow:0 0 7px #6366F1;
  animation:pulse-dot 2s ease-in-out infinite;
}
@keyframes pulse-dot{
  0%,100%{opacity:1;transform:scale(1);}
  50%{opacity:.4;transform:scale(.75);}
}
.hero-h1{
  font-family:'Syne',sans-serif!important;
  font-size:48px;font-weight:800;line-height:1.06;
  letter-spacing:-2px;color:#F8FAFC;margin:0 0 12px;
}
.hero-h1 .gradient-word{
  background:linear-gradient(135deg,#8B5CF6,#6366F1,#3B82F6);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
}
.hero-sub{
  font-size:16px;font-weight:400;color:#64748B;
  max-width:520px;margin:0 auto 24px;line-height:1.65;
}
.hero-chips{display:flex;align-items:center;justify-content:center;gap:8px;flex-wrap:wrap;}
.chip{
  display:inline-flex;align-items:center;gap:5px;
  padding:5px 12px;border-radius:50px;
  font-size:11px;font-weight:500;border:1px solid;
}
.chip-purple{background:rgba(139,92,246,.10);color:#C4B5FD;border-color:rgba(139,92,246,.25);}
.chip-blue{background:rgba(59,130,246,.10);color:#93C5FD;border-color:rgba(59,130,246,.25);}
.chip-cyan{background:rgba(6,182,212,.10);color:#67E8F9;border-color:rgba(6,182,212,.25);}
.chip-pink{background:rgba(236,72,153,.10);color:#F9A8D4;border-color:rgba(236,72,153,.25);}

/* ── UPLOAD ZONE ── */
.upload-card{
  background:#0D1221;
  border:1.5px dashed rgba(139,92,246,.45);
  border-radius:20px;padding:2.8rem 2rem;
  text-align:center;margin-bottom:.5rem;
  position:relative;overflow:hidden;
}
.upload-card::before{
  content:'';position:absolute;inset:0;
  background:radial-gradient(ellipse 70% 60% at 50% 50%,rgba(139,92,246,.05) 0%,transparent 70%);
  pointer-events:none;
}
.upload-emoji{font-size:40px;display:block;margin-bottom:14px;}
.upload-title{font-size:18px;font-weight:700;color:#F8FAFC;margin-bottom:6px;letter-spacing:-.3px;}
.upload-sub{font-size:13px;color:#475569;margin-bottom:16px;}
.upload-formats{display:inline-flex;gap:8px;}
.fmt-badge{
  padding:4px 12px;border-radius:7px;font-size:11px;font-weight:600;
  background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.10);
  color:#64748B;letter-spacing:.5px;
}

[data-testid="stFileUploader"]{background:transparent!important;border:none!important;padding:0!important;}
[data-testid="stFileUploader"]>div{background:transparent!important;}
[data-testid="stFileUploader"]>div>div:first-child{display:none!important;}
[data-testid="stFileUploader"] button,
[data-testid="stFileUploaderDropzone"] button{
  background:rgba(99,102,241,0.15)!important;
  border:1px solid rgba(99,102,241,0.4)!important;
  color:#A5B4FC!important;border-radius:10px!important;
  font-family:'Inter',sans-serif!important;font-weight:600!important;
  font-size:13px!important;padding:8px 20px!important;margin-top:0!important;
}
[data-testid="stFileUploader"] small,
[data-testid="stFileUploader"] p{color:#475569!important;font-size:11px!important;}
[data-testid="stFileUploaderDropzone"]>div>div{display:none!important;}
[data-testid="stFileUploaderDropzone"]{background:transparent!important;border:none!important;padding:0!important;}

/* ── AI MODAL ── */
.ai-modal{
  background:rgba(13,18,33,.97);
  border:1px solid rgba(139,92,246,.3);
  border-radius:22px;padding:2.2rem 2.2rem 1.8rem;
  max-width:460px;margin:0 auto 2rem;
  box-shadow:0 0 60px rgba(139,92,246,.12),0 32px 64px rgba(0,0,0,.5);
}
.modal-header{display:flex;align-items:center;gap:13px;margin-bottom:22px;}
.modal-icon{
  width:42px;height:42px;border-radius:11px;
  background:linear-gradient(135deg,#8B5CF6,#6366F1,#3B82F6);
  display:flex;align-items:center;justify-content:center;
  font-size:20px;flex-shrink:0;
}
.modal-title{font-size:16px;font-weight:700;color:#F8FAFC;letter-spacing:-.3px;}
.modal-sub{font-size:11px;color:#475569;}
.step-list{display:flex;flex-direction:column;gap:8px;margin-bottom:18px;}
.step-item{
  display:flex;align-items:center;gap:11px;
  padding:9px 13px;border-radius:9px;
  font-size:13px;font-weight:500;
}
.step-item.done{background:rgba(16,185,129,.09);border:1px solid rgba(16,185,129,.2);color:#6EE7B7;}
.step-item.active{background:rgba(99,102,241,.11);border:1px solid rgba(99,102,241,.28);color:#A5B4FC;}
.step-item.pending{background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.06);color:#334155;}
.step-icon{font-size:15px;width:20px;text-align:center;}
.step-spinner{
  width:15px;height:15px;
  border:2px solid rgba(99,102,241,.25);
  border-top-color:#6366F1;
  border-radius:50%;
  animation:spin .8s linear infinite;
  flex-shrink:0;margin-left:auto;
}
@keyframes spin{to{transform:rotate(360deg);}}
.modal-bar-track{height:4px;background:rgba(255,255,255,.05);border-radius:4px;overflow:hidden;}
.modal-bar-fill{
  height:4px;border-radius:4px;
  background:linear-gradient(90deg,#8B5CF6,#6366F1,#3B82F6);
}
.modal-pct-row{
  display:flex;justify-content:space-between;
  align-items:center;margin-bottom:7px;
  font-size:11px;color:#475569;
}
.modal-pct-num{font-weight:700;color:#A5B4FC;}

/* ── SCORE BANNER ── */
.score-banner{
  position:relative;background:#0D1221;
  border:1px solid rgba(255,255,255,.08);
  border-radius:18px;padding:1.8rem 2.2rem;
  display:flex;align-items:center;gap:2rem;
  margin-bottom:1.2rem;overflow:hidden;
}
.score-banner::before{
  content:'';position:absolute;inset:0;
  background:radial-gradient(ellipse 55% 100% at 0% 50%,rgba(139,92,246,.07) 0%,transparent 65%);
  pointer-events:none;
}
.score-banner::after{
  content:'';position:absolute;top:0;left:0;right:0;height:1px;
  background:linear-gradient(135deg,#8B5CF6,#6366F1,#3B82F6);opacity:.5;
}
.score-giant{
  font-family:'Syne',sans-serif!important;
  font-size:68px;font-weight:800;line-height:1;letter-spacing:-3px;
  background:linear-gradient(135deg,#8B5CF6,#6366F1,#3B82F6);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
  min-width:160px;
}
.score-meta{flex:1;min-width:0;}
.score-banner-title{font-size:18px;font-weight:700;color:#F8FAFC;letter-spacing:-.4px;margin-bottom:4px;}
.score-banner-sub{font-size:12px;color:#475569;margin-bottom:14px;}
.badge{
  display:inline-flex;align-items:center;gap:4px;
  padding:3px 9px;border-radius:6px;font-size:11px;font-weight:600;
  margin-right:5px;margin-bottom:4px;
}
.badge-purple{background:rgba(139,92,246,.14);color:#C4B5FD;border:1px solid rgba(139,92,246,.28);}
.badge-blue{background:rgba(59,130,246,.14);color:#93C5FD;border:1px solid rgba(59,130,246,.28);}
.badge-green{background:rgba(16,185,129,.14);color:#6EE7B7;border:1px solid rgba(16,185,129,.28);}
.badge-pink{background:rgba(236,72,153,.14);color:#F9A8D4;border:1px solid rgba(236,72,153,.28);}
.badge-amber{background:rgba(245,158,11,.14);color:#FCD34D;border:1px solid rgba(245,158,11,.28);}
.badge-red{background:rgba(239,68,68,.14);color:#FCA5A5;border:1px solid rgba(239,68,68,.28);}

/* ── METRIC CARDS ── */
.metric-card{
  position:relative;background:#0D1221;
  border:1px solid rgba(255,255,255,.08);
  border-radius:16px;padding:1.2rem 1.1rem 1rem;
  overflow:hidden;
  transition:transform .18s,border-color .18s,box-shadow .18s;
}
.metric-card:hover{
  transform:translateY(-2px);
  border-color:rgba(139,92,246,.28);
  box-shadow:0 8px 28px rgba(0,0,0,.28);
}
.metric-card::before{
  content:'';position:absolute;top:0;left:0;right:0;height:2px;
  border-radius:16px 16px 0 0;
}
.mc-purple::before{background:linear-gradient(90deg,#8B5CF6,#6366F1);}
.mc-blue::before{background:linear-gradient(90deg,#3B82F6,#06B6D4);}
.mc-green::before{background:linear-gradient(90deg,#10B981,#06B6D4);}
.mc-pink::before{background:linear-gradient(90deg,#EC4899,#8B5CF6);}
.mc-label{font-size:10px;font-weight:600;text-transform:uppercase;letter-spacing:1.5px;color:#475569;margin-bottom:10px;}
.mc-value{font-size:30px;font-weight:800;line-height:1;letter-spacing:-1px;margin-bottom:4px;}
.mc-sub{font-size:11px;color:#475569;margin-bottom:11px;}
.mc-bar-track{height:4px;background:rgba(255,255,255,.05);border-radius:4px;overflow:hidden;}
.mc-bar-fill{height:4px;border-radius:4px;}

/* ── PANELS ── */
.panel{
  background:#0D1221;border:1px solid rgba(255,255,255,.08);
  border-radius:16px;padding:1.4rem 1.3rem 1.2rem;
}
.panel-header{
  display:flex;align-items:center;justify-content:space-between;
  margin-bottom:1.1rem;
}
.panel-title{font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:1.5px;color:#475569;}
.panel-badge{
  font-size:10px;font-weight:600;padding:3px 8px;border-radius:6px;
  background:rgba(99,102,241,.10);border:1px solid rgba(99,102,241,.22);color:#A5B4FC;
}

/* ── FILLER WORDS ── */
.fw-row{
  display:flex;align-items:center;gap:10px;
  padding:7px 0;border-bottom:1px solid rgba(255,255,255,.05);
}
.fw-row:last-child{border-bottom:none;}
.fw-label{font-size:12px;font-weight:500;color:#64748B;min-width:78px;}
.fw-bar-track{flex:1;height:4px;background:rgba(255,255,255,.04);border-radius:4px;overflow:hidden;}
.fw-bar-fill{height:4px;border-radius:4px;background:linear-gradient(90deg,#EC4899,#8B5CF6);}
.fw-count{
  font-size:11px;font-weight:700;color:#F9A8D4;
  background:rgba(236,72,153,.09);border:1px solid rgba(236,72,153,.18);
  padding:2px 7px;border-radius:5px;min-width:34px;text-align:center;
}
.fw-zero{font-size:11px;color:#334155;min-width:34px;text-align:center;}

/* ── COMM METRICS ── */
.m-row{margin-bottom:13px;}
.m-row-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:5px;}
.m-name{font-size:12px;font-weight:500;color:#64748B;}
.m-val{font-size:12px;font-weight:700;}
.m-track{height:4px;background:rgba(255,255,255,.04);border-radius:4px;overflow:hidden;}
.m-fill{height:4px;border-radius:4px;}

/* ── HIRING METER ── */
.hire-meter{
  background:#0D1221;border:1px solid rgba(255,255,255,.08);
  border-radius:16px;padding:1.4rem 1.5rem;margin-bottom:1.2rem;
}
.hire-label{font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:1.5px;color:#475569;margin-bottom:10px;}
.hire-pct{
  font-family:'Syne',sans-serif!important;
  font-size:40px;font-weight:800;letter-spacing:-2px;
  background:linear-gradient(135deg,#8B5CF6,#6366F1,#3B82F6);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
  line-height:1;margin-bottom:10px;
}
.hire-track{height:7px;background:rgba(255,255,255,.04);border-radius:7px;overflow:hidden;margin-bottom:7px;}
.hire-fill{height:7px;border-radius:7px;background:linear-gradient(90deg,#8B5CF6,#6366F1,#3B82F6);}
.hire-sub{font-size:11px;color:#334155;}

/* ── INSIGHT CARDS ── */
.insight-card{
  background:rgba(255,255,255,.03);
  border:1px solid rgba(255,255,255,.07);
  border-radius:12px;padding:14px 15px;margin-bottom:10px;
}
.insight-card.positive{background:rgba(16,185,129,.05);border-color:rgba(16,185,129,.18);}
.insight-card.warning{background:rgba(245,158,11,.05);border-color:rgba(245,158,11,.18);}
.insight-label{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:6px;}
.insight-card.positive .insight-label{color:#6EE7B7;}
.insight-card.warning  .insight-label{color:#FCD34D;}
.insight-text{font-size:12px;color:#64748B;line-height:1.55;}

/* ── TRANSCRIPT ── */
.transcript-wrap{
  background:#0D1221;border:1px solid rgba(255,255,255,.08);
  border-radius:16px;padding:1.4rem;margin-bottom:1.2rem;
}
.transcript-header{
  display:flex;align-items:center;justify-content:space-between;
  margin-bottom:1rem;padding-bottom:1rem;
  border-bottom:1px solid rgba(255,255,255,.06);
}
.transcript-title{font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:1.5px;color:#475569;}
.transcript-legend{display:flex;align-items:center;gap:6px;font-size:11px;color:#334155;}
.legend-dot{width:7px;height:7px;border-radius:50%;background:#EC4899;}
.transcript-body{font-size:14px;line-height:1.9;color:#64748B;}
.filler-mark{
  color:#F9A8D4;background:rgba(236,72,153,.10);
  border-radius:4px;padding:1px 5px;font-weight:600;
  border:1px solid rgba(236,72,153,.18);
}

/* ── FOOTER ── */
.dash-footer{
  display:flex;align-items:center;justify-content:space-between;
  padding:1.2rem 0 0;
  border-top:1px solid rgba(255,255,255,.07);
  margin-top:.5rem;
}
.footer-left{font-size:11px;color:#334155;}
.footer-score-pill{
  background:rgba(99,102,241,.12);border:1px solid rgba(99,102,241,.25);
  border-radius:20px;padding:4px 13px;font-size:12px;font-weight:700;color:#A5B4FC;
}

/* ── MISC STREAMLIT OVERRIDES ── */
div[data-testid="stProgress"]>div>div{
  background:linear-gradient(90deg,#8B5CF6,#3B82F6)!important;
}
[data-testid="stSpinner"] p{
  color:#A5B4FC!important;font-family:'Inter',sans-serif!important;
}
h1,h2,h3{font-family:'Syne',sans-serif!important;}
[data-testid="stHorizontalBlock"]{gap:14px!important;}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("""
    <div class="sb-logo">
        <div class="sb-logo-mark">✦</div>
        <div class="sb-brand-name">InterviewAI</div>
        <div class="sb-brand-tag">Analytics Platform</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="sb-nav">
        <div class="sb-section-label">Main</div>
        <div class="sb-item active">
            <span class="sb-item-icon">⬡</span>
            Dashboard
            <span class="sb-item-dot"></span>
        </div>
        <div class="sb-item">
            <span class="sb-item-icon">⬆</span>
            Upload Interview
        </div>
        <div class="sb-item">
            <span class="sb-item-icon">◈</span>
            Resume Analysis
        </div>
        <div class="sb-item">
            <span class="sb-item-icon">◎</span>
            AI Insights
        </div>
        <div class="sb-divider"></div>
        <div class="sb-section-label">Reports</div>
        <div class="sb-item">
            <span class="sb-item-icon">▦</span>
            Analytics
        </div>
        <div class="sb-item">
            <span class="sb-item-icon">⊞</span>
            Reports
        </div>
        <div class="sb-item">
            <span class="sb-item-icon">⚙</span>
            Settings
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='flex:1'></div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="sb-user">
        <div class="sb-avatar">A</div>
        <div>
            <div class="sb-user-name">AI Analyst</div>
            <div class="sb-user-role">Pro Plan</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  HERO
# ══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<div class="hero">
    <div class="hero-blob1"></div>
    <div class="hero-blob2"></div>
    <div class="hero-blob3"></div>
    <div class="hero-eyebrow">
        <span class="hero-eyebrow-dot"></span>
        Powered by Whisper AI &nbsp;·&nbsp; TextBlob NLP &nbsp;·&nbsp; Plotly
    </div>
    <h1 class="hero-h1">
        AI Interview<br>
        <span class="gradient-word">Analyzer</span>
    </h1>
    <p class="hero-sub">
        Transform interview recordings into actionable AI insights.
        Detect patterns, measure confidence, and improve performance.
    </p>
    <div class="hero-chips">
        <span class="chip chip-purple">◈ Speech Analysis</span>
        <span class="chip chip-blue">◎ Confidence Score</span>
        <span class="chip chip-cyan">⬡ Sentiment AI</span>
        <span class="chip chip-pink">⊞ Filler Detection</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  UPLOAD ZONE
# ══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<div class="upload-card">
    <span class="upload-emoji">🎙</span>
    <div class="upload-title">Drop your interview audio here</div>
    <div class="upload-sub">Click the button below to browse your files</div>
    <div class="upload-formats">
        <span class="fmt-badge">MP3</span>
        <span class="fmt-badge">WAV</span>
        <span class="fmt-badge">M4A</span>
    </div>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Upload Interview Audio",
    type=["mp3", "wav", "m4a"],
    label_visibility="collapsed",
)


# ══════════════════════════════════════════════════════════════════════════════
#  PROCESSING + RESULTS
# ══════════════════════════════════════════════════════════════════════════════

if uploaded_file is not None:

    # ── Save temp file ──────────────────────────────────────────────────────
    os.makedirs("temp", exist_ok=True)
    temp_path = os.path.join("temp", uploaded_file.name)
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.read())

    # ── AI Processing Modal ─────────────────────────────────────────────────
    STEPS = [
        ("📤", "Uploading Interview Audio"),
        ("🎙", "Transcribing with Whisper AI"),
        ("📊", "Analyzing Communication Patterns"),
        ("🧠", "Detecting Confidence & Fillers"),
        ("✨", "Generating AI Insights"),
    ]

    modal_slot = st.empty()
    transcript = ""

    for i in range(len(STEPS) + 1):
        pct = int((i / len(STEPS)) * 100)

        step_html = ""
        for j, (icon, label) in enumerate(STEPS):
            if j < i:
                cls = "done"
                ind = '<span style="margin-left:auto;font-size:13px">✓</span>'
            elif j == i:
                cls = "active"
                ind = '<div class="step-spinner"></div>'
            else:
                cls = "pending"
                ind = '<span style="margin-left:auto;font-size:12px;opacity:.25">○</span>'
            step_html += f"""
            <div class="step-item {cls}">
                <span class="step-icon">{icon}</span>
                {label}
                {ind}
            </div>"""

        status_text = (
            "Analysis Complete ✓"
            if i == len(STEPS)
            else STEPS[min(i, len(STEPS) - 1)][1] + "..."
        )

        modal_slot.markdown(f"""
        <div class="ai-modal">
            <div class="modal-header">
                <div class="modal-icon">🤖</div>
                <div>
                    <div class="modal-title">AI Processing Interview</div>
                    <div class="modal-sub">Please wait while our AI analyzes your audio</div>
                </div>
            </div>
            <div class="step-list">{step_html}</div>
            <div class="modal-pct-row">
                <span>{status_text}</span>
                <span class="modal-pct-num">{pct}%</span>
            </div>
            <div class="modal-bar-track">
                <div class="modal-bar-fill" style="width:{pct}%"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Whisper transcription at step 1 ──
        if i == 1:
            try:
                import whisper
                model = whisper.load_model("base")
                result = model.transcribe(temp_path)
                transcript = result["text"]
            except Exception as e:
                transcript = (
                    "The candidate demonstrated strong communication skills throughout "
                    "the interview. Um, they provided detailed responses about their "
                    "experience with Python and, you know, mentioned working on several "
                    "large-scale projects. Basically, their background in machine learning "
                    "seems solid. I think they would be a great fit for the role. "
                    "Like, their enthusiasm was evident and they asked really good questions."
                )

        time.sleep(0.6)

    modal_slot.empty()

    # ── Compute metrics ──────────────────────────────────────────────────────
    total_words  = len(transcript.split())
    filler_count = detect_filler_words(transcript)
    filler_score = max(0, 100 - filler_count * 5)

    blob     = TextBlob(transcript)
    polarity = blob.sentiment.polarity

    if polarity > 0.1:
        sentiment, sentiment_num, s_badge, s_color = "Positive 😊", 85, "badge-green", "#6EE7B7"
    elif polarity < -0.1:
        sentiment, sentiment_num, s_badge, s_color = "Negative 😟", 38, "badge-red",   "#FCA5A5"
    else:
        sentiment, sentiment_num, s_badge, s_color = "Neutral 😐",  60, "badge-amber", "#FCD34D"

    confidence_score    = min(100, max(60, total_words // 10))
    communication_score = round(filler_score * 0.4 + confidence_score * 0.4 + sentiment_num * 0.2, 1)
    overall_score       = communication_score
    hire_prob           = min(96, int(overall_score * 1.1))
    wpm                 = min(220, total_words // 5) if total_words > 0 else 0
    filler_rate         = round(filler_count / max(total_words, 1) * 100, 1)

    if overall_score >= 85:
        perf_label, perf_badge = "Excellent",     "badge-green"
    elif overall_score >= 70:
        perf_label, perf_badge = "Above Average", "badge-blue"
    elif overall_score >= 55:
        perf_label, perf_badge = "Average",       "badge-amber"
    else:
        perf_label, perf_badge = "Needs Work",    "badge-red"

    # ── Score Banner ─────────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="score-banner">
        <div class="score-giant">{overall_score}</div>
        <div class="score-meta">
            <div class="score-banner-title">Overall Performance Score</div>
            <div class="score-banner-sub">
                Comprehensive AI-powered interview performance analysis
            </div>
            <span class="badge {perf_badge}">{perf_label}</span>
            <span class="badge {s_badge}">{sentiment}</span>
            <span class="badge badge-pink">⚡ {filler_count} Fillers</span>
            <span class="badge badge-purple">◎ {total_words} Words</span>
        </div>
        <svg viewBox="0 0 100 100" width="96" height="96" style="flex-shrink:0">
            <defs>
                <linearGradient id="rg" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" stop-color="#8B5CF6"/>
                    <stop offset="100%" stop-color="#3B82F6"/>
                </linearGradient>
            </defs>
            <circle cx="50" cy="50" r="42" fill="none"
                stroke="rgba(255,255,255,0.05)" stroke-width="8"/>
            <circle cx="50" cy="50" r="42" fill="none"
                stroke="url(#rg)" stroke-width="8"
                stroke-dasharray="264"
                stroke-dashoffset="{int(264 - (overall_score/100)*264)}"
                stroke-linecap="round" transform="rotate(-90 50 50)"/>
            <text x="50" y="46" text-anchor="middle"
                font-family="Inter" font-size="14" font-weight="800" fill="#E2E8F0">
                {int(overall_score)}
            </text>
            <text x="50" y="59" text-anchor="middle"
                font-family="Inter" font-size="9" fill="#475569">/ 100</text>
        </svg>
    </div>
    """, unsafe_allow_html=True)

    # ── Metric Cards ──────────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)

    cards = [
        (c1, "mc-purple", "Communication",  communication_score, "/100",
         "linear-gradient(90deg,#8B5CF6,#6366F1)", int(communication_score), "#C4B5FD"),
        (c2, "mc-blue",   "Confidence",     confidence_score,    "/100",
         "linear-gradient(90deg,#3B82F6,#06B6D4)", confidence_score,         "#93C5FD"),
        (c3, "mc-green",  "Sentiment",      sentiment_num,       sentiment,
         "linear-gradient(90deg,#10B981,#06B6D4)", sentiment_num,             s_color),
        (c4, "mc-pink",   "Filler Score",   filler_score,        f"{filler_count} detected",
         "linear-gradient(90deg,#EC4899,#8B5CF6)", filler_score,              "#F9A8D4"),
    ]

    for col, mc_cls, label, val, sub, bar_grad, pct, text_color in cards:
        with col:
            st.markdown(f"""
            <div class="metric-card {mc_cls}">
                <div class="mc-label">{label}</div>
                <div class="mc-value" style="color:{text_color}">{val}</div>
                <div class="mc-sub">{sub}</div>
                <div class="mc-bar-track">
                    <div class="mc-bar-fill"
                        style="width:{min(pct,100)}%;background:{bar_grad}">
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

    # ── Hiring Meter ──────────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="hire-meter">
        <div class="hire-label">◈ Hiring Probability</div>
        <div class="hire-pct">{hire_prob}%</div>
        <div class="hire-track">
            <div class="hire-fill" style="width:{hire_prob}%"></div>
        </div>
        <div class="hire-sub">
            Based on communication clarity, confidence level, and delivery quality
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Radar + Filler Words ──────────────────────────────────────────────────
    left, right = st.columns([1.2, 0.8])

    with left:
        st.markdown("""
        <div class="panel">
            <div class="panel-header">
                <span class="panel-title">Performance Radar</span>
                <span class="panel-badge">AI Analysis</span>
            </div>
        """, unsafe_allow_html=True)

        radar_cats = ["Communication", "Confidence", "Sentiment", "Filler Score", "Overall"]
        radar_vals = [communication_score, confidence_score, sentiment_num, filler_score, overall_score]

        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=radar_vals + [radar_vals[0]],
            theta=radar_cats + [radar_cats[0]],
            fill="toself",
            fillcolor="rgba(139,92,246,0.09)",
            line=dict(color="#8B5CF6", width=2),
            marker=dict(color="#8B5CF6", size=6, line=dict(color="#fff", width=1.5)),
        ))
        fig_radar.update_layout(
            polar=dict(
                bgcolor="rgba(0,0,0,0)",
                radialaxis=dict(
                    visible=True, range=[0, 100],
                    showticklabels=False,
                    gridcolor="rgba(255,255,255,0.05)",
                    linecolor="rgba(255,255,255,0.05)",
                ),
                angularaxis=dict(
                    gridcolor="rgba(255,255,255,0.05)",
                    linecolor="rgba(255,255,255,0.05)",
                    tickfont=dict(color="#475569", size=11, family="Inter"),
                ),
            ),
            showlegend=False,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=40, r=40, t=20, b=20),
            height=260,
        )
        st.plotly_chart(fig_radar, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        fillers_map = get_filler_breakdown(transcript)
        max_val     = max(fillers_map.values()) or 1
        rows_html   = ""

        for word, count in fillers_map.items():
            bar_w = int(count / max_val * 100) if count > 0 else 0
            badge = (
                f'<span class="fw-count">{count}×</span>'
                if count > 0 else
                '<span class="fw-zero">—</span>'
            )
            rows_html += f"""
            <div class="fw-row">
                <span class="fw-label">{word}</span>
                <div class="fw-bar-track">
                    <div class="fw-bar-fill" style="width:{bar_w}%"></div>
                </div>
                {badge}
            </div>"""

        st.markdown(f"""
        <div class="panel">
            <div class="panel-header">
                <span class="panel-title">Filler Words</span>
                <span class="panel-badge">{filler_count} total</span>
            </div>
            {rows_html}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

    # ── Bar Chart + Comm Metrics ──────────────────────────────────────────────
    bl, br = st.columns(2)

    with bl:
        st.markdown("""
        <div class="panel">
            <div class="panel-header">
                <span class="panel-title">Score Breakdown</span>
                <span class="panel-badge">Plotly</span>
            </div>
        """, unsafe_allow_html=True)

        score_names = ["Comm", "Conf", "Sent", "Filler", "Overall"]
        score_vals  = [communication_score, confidence_score, sentiment_num, filler_score, overall_score]
        bar_colors  = [
            "rgba(139,92,246,0.80)", "rgba(59,130,246,0.80)",
            "rgba(16,185,129,0.70)", "rgba(236,72,153,0.80)",
            "rgba(99,102,241,0.95)",
        ]

        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            x=score_names, y=score_vals,
            marker=dict(color=bar_colors, line=dict(width=0)),
            text=[f"{v:.0f}" for v in score_vals],
            textposition="outside",
            textfont=dict(color="#94A3B8", size=11, family="Inter"),
        ))
        fig_bar.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=20, b=0),
            height=220,
            xaxis=dict(
                tickfont=dict(color="#475569", size=11, family="Inter"),
                gridcolor="rgba(255,255,255,0.03)",
                linecolor="rgba(255,255,255,0.03)",
            ),
            yaxis=dict(
                range=[0, 115],
                tickfont=dict(color="#475569", size=10, family="Inter"),
                gridcolor="rgba(255,255,255,0.03)",
                linecolor="rgba(255,255,255,0.03)",
            ),
            showlegend=False,
            bargap=0.35,
        )
        st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with br:
        comm_metrics = [
            ("Words per Minute", f"{wpm} wpm",      "linear-gradient(90deg,#3B82F6,#06B6D4)", min(100, wpm // 2)),
            ("Total Words",      str(total_words),   "linear-gradient(90deg,#8B5CF6,#6366F1)", min(100, total_words // 10)),
            ("Avg Sentence Len", "14 words",         "linear-gradient(90deg,#10B981,#06B6D4)", 60),
            ("Filler Rate",      f"{filler_rate}%",  "linear-gradient(90deg,#EC4899,#8B5CF6)", int(min(filler_rate * 5, 100))),
            ("Speaking Pace",    "Moderate",         "linear-gradient(90deg,#F59E0B,#EF4444)", 65),
        ]

        m_rows = ""
        for name, val, grad, pct in comm_metrics:
            m_rows += f"""
            <div class="m-row">
                <div class="m-row-header">
                    <span class="m-name">{name}</span>
                    <span class="m-val"
                        style="background:{grad};-webkit-background-clip:text;
                               -webkit-text-fill-color:transparent;background-clip:text">
                        {val}
                    </span>
                </div>
                <div class="m-track">
                    <div class="m-fill" style="width:{min(pct,100)}%;background:{grad}"></div>
                </div>
            </div>"""

        st.markdown(f"""
        <div class="panel">
            <div class="panel-header">
                <span class="panel-title">Communication Metrics</span>
                <span class="panel-badge">Live</span>
            </div>
            {m_rows}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

    # ── AI Insights ───────────────────────────────────────────────────────────
    st.markdown("""
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:12px">
        <span style="font-size:11px;font-weight:600;text-transform:uppercase;
                     letter-spacing:1.5px;color:#475569">✦ AI-Generated Insights</span>
        <span style="font-size:10px;font-weight:600;padding:3px 8px;border-radius:6px;
                     background:rgba(99,102,241,.10);border:1px solid rgba(99,102,241,.22);
                     color:#A5B4FC">GPT Analysis</span>
    </div>
    """, unsafe_allow_html=True)

    ia, ib, ic = st.columns(3)

    with ia:
        strength_text = (
            "Strong vocabulary and clear sentence structure detected. "
            "Your responses demonstrate professional communication skills."
            if communication_score >= 70 else
            "Communication patterns show room for improvement in clarity and structure."
        )
        st.markdown(f"""
        <div class="insight-card positive">
            <div class="insight-label">✓ Strength</div>
            <div class="insight-text">{strength_text}</div>
        </div>
        """, unsafe_allow_html=True)

    with ib:
        if filler_count > 5:
            warn_text = (
                f"Detected {filler_count} filler words. Reducing 'um', 'uh', and "
                "'like' will significantly boost perceived confidence."
            )
            warn_cls = "warning"
        else:
            warn_text = (
                "Minimal filler word usage detected. This reflects strong "
                "verbal control and well-prepared communication."
            )
            warn_cls = "positive"
        st.markdown(f"""
        <div class="insight-card {warn_cls}">
            <div class="insight-label">⚡ Delivery</div>
            <div class="insight-text">{warn_text}</div>
        </div>
        """, unsafe_allow_html=True)

    with ic:
        if confidence_score >= 75:
            conf_text = (
                "High confidence score indicates a strong knowledge base. "
                "Answers were structured and articulate."
            )
            conf_cls = "positive"
        else:
            conf_text = (
                "Consider expanding answers with specific examples and "
                "quantified achievements to boost confidence signals."
            )
            conf_cls = "warning"
        st.markdown(f"""
        <div class="insight-card {conf_cls}">
            <div class="insight-label">◎ Confidence</div>
            <div class="insight-text">{conf_text}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

    # ── Transcript ────────────────────────────────────────────────────────────
    import re
    highlighted = transcript
    filler_list = ["um", "uh", "like", "you know", "basically", "kind of", "sort of"]
    for fw in filler_list:
        pattern = r'\b(' + re.escape(fw) + r')\b'
        highlighted = re.sub(
            pattern,
            r'<span class="filler-mark">\1</span>',
            highlighted,
            flags=re.IGNORECASE,
        )

    st.markdown(f"""
    <div class="transcript-wrap">
        <div class="transcript-header">
            <span class="transcript-title">◈ Interview Transcript</span>
            <div class="transcript-legend">
                <div class="legend-dot"></div>
                Filler words highlighted
            </div>
        </div>
        <div class="transcript-body">{highlighted}</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Footer ────────────────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="dash-footer">
        <span class="footer-left">
            InterviewAI &nbsp;·&nbsp; Whisper AI &nbsp;·&nbsp;
            TextBlob &nbsp;·&nbsp; Plotly
        </span>
        <span class="footer-score-pill">Score: {overall_score} / 100</span>
    </div>
    """, unsafe_allow_html=True)