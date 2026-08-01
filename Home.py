import streamlit as st  # type: ignore[import]

st.set_page_config(
    page_title="UAS Data Mining - Diabetes & Gerai Kopi",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<div class="identity-strip">
    <span class="pill strong">Dzaka Nur Ahmad Shafy</span>
    <span class="pill">NIM 23146014</span>
    
    
</div>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# Custom styling — dark indigo/violet base with warm amber (kopi) and
# electric cyan (diabetes/klinis) accents, tampilan lebih modern & bold.
# ----------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&family=JetBrains+Mono:wght@500&display=swap');

:root{
    --bg:#0F1220;
    --bg-soft:#171B2E;
    --panel:#1B2036;
    --amber:#F2A65A;
    --amber-soft:#3A2C1E;
    --cyan:#4CD6C0;
    --cyan-soft:#12332F;
    --violet:#8B7CF6;
    --paper:#F5F3EE;
    --ink-soft:#B7BBD1;
}

#MainMenu, footer, header {visibility: hidden;}

.stApp{
    background:
        radial-gradient(circle at 12% -10%, rgba(139,124,246,0.28), transparent 42%),
        radial-gradient(circle at 100% 0%, rgba(76,214,192,0.16), transparent 40%),
        var(--bg);
}

.block-container{padding-top:2.4rem; padding-bottom:3.5rem; max-width:1100px;}
html, body, [class*="css"]{font-family:'Sora', sans-serif; color:var(--paper);}

/* ---------- Eyebrow ---------- */
.eyebrow{
    font-family:'JetBrains Mono', monospace;
    font-size:0.72rem;
    letter-spacing:0.22em;
    text-transform:uppercase;
    color:var(--cyan);
    display:flex;
    align-items:center;
    gap:10px;
    margin-bottom:0.9rem;
}
.eyebrow::before{
    content:"";
    width:30px; height:2px;
    background:linear-gradient(90deg, var(--cyan), var(--violet));
    display:inline-block;
    border-radius:2px;
}

/* ---------- Hero ---------- */
.hero-title{
    font-family:'Space Grotesk', sans-serif;
    font-weight:700;
    font-size:2.9rem;
    line-height:1.12;
    color:var(--paper);
    margin:0 0 1rem 0;
    letter-spacing:-0.01em;
}
.hero-title .accent{
    background:linear-gradient(90deg, var(--amber), var(--cyan));
    -webkit-background-clip:text;
    background-clip:text;
    color:transparent;
}
.hero-sub{
    font-size:1.04rem;
    color:var(--ink-soft);
    max-width:660px;
    line-height:1.7;
    margin-bottom:0.2rem;
}

.hero-divider{
    height:1px;
    margin:2rem 0 2.2rem 0;
    background:linear-gradient(90deg, var(--violet) 0%, rgba(255,255,255,0.08) 55%, var(--cyan) 100%);
    border-radius:2px;
}

/* ---------- Split cards ---------- */
.card{
    border-radius:20px;
    padding:1.9rem 1.7rem 1.6rem 1.7rem;
    height:100%;
    position:relative;
    overflow:hidden;
    border:1px solid rgba(255,255,255,0.06);
    box-shadow:0 18px 40px -22px rgba(0,0,0,0.6);
}
.card-coffee{
    background:linear-gradient(160deg, var(--panel) 0%, var(--amber-soft) 130%);
    color:var(--paper);
}
.card-health{
    background:linear-gradient(160deg, var(--panel) 0%, var(--cyan-soft) 130%);
    color:var(--paper);
}
.card-tag{
    font-family:'JetBrains Mono', monospace;
    font-size:0.68rem;
    letter-spacing:0.16em;
    text-transform:uppercase;
    opacity:0.85;
    margin-bottom:0.8rem;
    display:inline-block;
    padding:0.28rem 0.6rem;
    border-radius:999px;
    background:rgba(255,255,255,0.06);
}
.card-coffee .card-tag{color:var(--amber);}
.card-health .card-tag{color:var(--cyan);}

.card-title{
    font-family:'Space Grotesk', sans-serif;
    font-weight:600;
    font-size:1.45rem;
    margin:0.7rem 0 0.7rem 0;
}
.card-body{
    font-size:0.94rem;
    line-height:1.65;
    color:var(--ink-soft);
}
.card-ring{
    position:absolute;
    width:170px; height:170px;
    border-radius:50%;
    border:16px solid var(--amber);
    opacity:0.14;
    top:-60px; right:-60px;
}
.card-pulse{
    position:absolute;
    bottom:16px; right:18px;
    opacity:0.55;
}

/* ---------- Nav hint ---------- */
.nav-hint{
    margin-top:2.3rem;
    font-size:0.87rem;
    color:var(--ink-soft);
    display:flex;
    align-items:center;
    gap:8px;
    background:rgba(255,255,255,0.04);
    border:1px solid rgba(255,255,255,0.07);
    padding:0.7rem 1rem;
    border-radius:12px;
    width:fit-content;
}
.nav-hint b{color:var(--amber);}

/* ---------- Footer identity strip ---------- */
.identity-strip{
    margin-top:2.8rem;
    border-top:1px solid rgba(255,255,255,0.08);
    padding-top:1.5rem;
    display:flex;
    flex-wrap:wrap;
    gap:0.6rem 0.8rem;
    align-items:center;
}
.identity-label{
    font-family:'JetBrains Mono', monospace;
    font-size:0.68rem;
    letter-spacing:0.14em;
    text-transform:uppercase;
    color:#6B7086;
    margin-right:0.4rem;
}
.pill{
    font-size:0.83rem;
    padding:0.34rem 0.82rem;
    border-radius:999px;
    background:rgba(255,255,255,0.05);
    border:1px solid rgba(255,255,255,0.1);
    color:var(--ink-soft);
}
.pill.strong{
    background:linear-gradient(90deg, var(--violet), var(--cyan));
    color:#0F1220;
    border:none;
    font-weight:700;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# Hero
# ----------------------------------------------------------------------
st.markdown("""
<div class="eyebrow">UAS · Data Mining · SIF304</div>
<div class="hero-title">Aplikasi UAS <span class="accent">Data Mining</span></div>
<div class="hero-sub">
Implementasi Supervised dan Unsupervised Learning — dua model, satu aplikasi.
Dibangun untuk memenuhi tugas UAS mata kuliah <b>Data Mining </b>.
</div>
<div class="hero-divider"></div>
""", unsafe_allow_html=True)



