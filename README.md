<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Mohammad Mahdi Azarbeik — Healthcare AI Researcher</title>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@300;400;600&family=Syne:wght@400;600;700;800&family=Crimson+Pro:ital,wght@0,300;0,400;1,300&display=swap" rel="stylesheet">
<style>
  :root {
    --bg: #050c12;
    --surface: #091520;
    --surface2: #0d1f2d;
    --teal: #00e5c8;
    --teal-dim: #00a38e;
    --amber: #f5a623;
    --red: #ff4757;
    --text: #c8dde8;
    --text-dim: #5a7a8a;
    --border: rgba(0,229,200,0.12);
    --glow: 0 0 20px rgba(0,229,200,0.15);
  }

  *, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }

  html { scroll-behavior: smooth; }

  body {
    background: var(--bg);
    color: var(--text);
    font-family: 'Syne', sans-serif;
    overflow-x: hidden;
    cursor: none;
  }

  /* Custom cursor */
  .cursor {
    position: fixed;
    width: 10px; height: 10px;
    background: var(--teal);
    border-radius: 50%;
    pointer-events: none;
    z-index: 9999;
    transform: translate(-50%,-50%);
    transition: width 0.2s, height 0.2s, opacity 0.2s;
    mix-blend-mode: screen;
  }
  .cursor-ring {
    position: fixed;
    width: 36px; height: 36px;
    border: 1px solid rgba(0,229,200,0.5);
    border-radius: 50%;
    pointer-events: none;
    z-index: 9998;
    transform: translate(-50%,-50%);
    transition: width 0.35s, height 0.35s, opacity 0.35s;
  }

  /* Background grid */
  body::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
      linear-gradient(rgba(0,229,200,0.03) 1px, transparent 1px),
      linear-gradient(90deg, rgba(0,229,200,0.03) 1px, transparent 1px);
    background-size: 40px 40px;
    z-index: 0;
    pointer-events: none;
  }

  /* Ambient blobs */
  .blob {
    position: fixed;
    border-radius: 50%;
    filter: blur(80px);
    opacity: 0.06;
    pointer-events: none;
    z-index: 0;
  }
  .blob-1 { width: 600px; height: 600px; background: var(--teal); top: -200px; left: -200px; animation: drift 18s ease-in-out infinite alternate; }
  .blob-2 { width: 400px; height: 400px; background: #0066ff; bottom: -100px; right: -100px; animation: drift 22s ease-in-out infinite alternate-reverse; }
  .blob-3 { width: 300px; height: 300px; background: var(--amber); top: 40%; right: 20%; animation: drift 14s ease-in-out infinite alternate; }

  @keyframes drift { from { transform: translate(0,0) scale(1); } to { transform: translate(40px, 30px) scale(1.1); } }

  /* Scanline overlay */
  body::after {
    content: '';
    position: fixed;
    inset: 0;
    background: repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,0.05) 2px, rgba(0,0,0,0.05) 4px);
    pointer-events: none;
    z-index: 1;
  }

  /* NAV */
  nav {
    position: fixed;
    top: 0; left: 0; right: 0;
    z-index: 100;
    padding: 20px 48px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: linear-gradient(to bottom, rgba(5,12,18,0.95), transparent);
    backdrop-filter: blur(2px);
  }

  .nav-logo {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 13px;
    color: var(--teal);
    letter-spacing: 0.1em;
    text-transform: uppercase;
  }
  .nav-logo span { color: var(--text-dim); }

  .nav-links {
    display: flex;
    gap: 36px;
    list-style: none;
  }
  .nav-links a {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    color: var(--text-dim);
    text-decoration: none;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    transition: color 0.2s;
    position: relative;
  }
  .nav-links a::after {
    content: '';
    position: absolute;
    bottom: -4px; left: 0; right: 100%;
    height: 1px;
    background: var(--teal);
    transition: right 0.3s ease;
  }
  .nav-links a:hover { color: var(--teal); }
  .nav-links a:hover::after { right: 0; }

  /* HERO */
  .hero {
    position: relative;
    z-index: 2;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 120px 48px 80px;
    max-width: 1200px;
    margin: 0 auto;
  }

  .hero-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    color: var(--teal);
    letter-spacing: 0.25em;
    text-transform: uppercase;
    margin-bottom: 28px;
    display: flex;
    align-items: center;
    gap: 12px;
    opacity: 0;
    animation: fadeUp 0.8s 0.2s forwards;
  }
  .hero-label::before {
    content: '';
    display: block;
    width: 24px;
    height: 1px;
    background: var(--teal);
  }

  .hero-name {
    font-family: 'Syne', sans-serif;
    font-size: clamp(44px, 7vw, 100px);
    font-weight: 800;
    line-height: 0.95;
    letter-spacing: -0.03em;
    margin-bottom: 20px;
    opacity: 0;
    animation: fadeUp 0.8s 0.35s forwards;
  }
  .hero-name .line1 { color: var(--text); display: block; }
  .hero-name .line2 { color: var(--teal); display: block; }

  .hero-tagline {
    font-family: 'Crimson Pro', serif;
    font-style: italic;
    font-size: clamp(18px, 2.5vw, 28px);
    font-weight: 300;
    color: var(--text-dim);
    max-width: 600px;
    line-height: 1.5;
    margin-bottom: 48px;
    opacity: 0;
    animation: fadeUp 0.8s 0.5s forwards;
  }

  .hero-stats {
    display: flex;
    gap: 48px;
    margin-bottom: 60px;
    opacity: 0;
    animation: fadeUp 0.8s 0.65s forwards;
  }
  .stat {
    border-left: 1px solid var(--teal);
    padding-left: 16px;
  }
  .stat-num {
    font-size: 36px;
    font-weight: 800;
    color: var(--teal);
    line-height: 1;
  }
  .stat-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    color: var(--text-dim);
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-top: 4px;
  }

  .hero-ctas {
    display: flex;
    gap: 16px;
    flex-wrap: wrap;
    opacity: 0;
    animation: fadeUp 0.8s 0.8s forwards;
  }

  .btn {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 14px 28px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    text-decoration: none;
    border: none;
    cursor: none;
    transition: all 0.25s;
    position: relative;
    overflow: hidden;
  }
  .btn-primary {
    background: var(--teal);
    color: var(--bg);
    font-weight: 600;
  }
  .btn-primary:hover {
    background: #00fff0;
    box-shadow: 0 0 30px rgba(0,229,200,0.4);
    transform: translateY(-2px);
  }
  .btn-ghost {
    background: transparent;
    color: var(--teal);
    border: 1px solid var(--border);
  }
  .btn-ghost:hover {
    border-color: var(--teal);
    background: rgba(0,229,200,0.06);
    transform: translateY(-2px);
  }

  /* Vital signs monitor strip */
  .vitals-strip {
    position: absolute;
    right: 48px;
    top: 50%;
    transform: translateY(-50%);
    width: 280px;
    opacity: 0;
    animation: fadeIn 1s 1s forwards;
  }
  .vitals-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 2px;
    padding: 20px;
    margin-bottom: 8px;
    position: relative;
    box-shadow: var(--glow);
  }
  .vitals-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
    background: var(--teal);
  }
  .vitals-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 9px;
    color: var(--text-dim);
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-bottom: 6px;
  }
  .vitals-value {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 22px;
    font-weight: 600;
    color: var(--teal);
  }
  .vitals-value .unit {
    font-size: 11px;
    color: var(--text-dim);
    margin-left: 4px;
  }
  .vitals-sparkline {
    margin-top: 8px;
    height: 32px;
  }

  /* ECG animation */
  .ecg-line {
    position: relative;
    height: 48px;
    overflow: hidden;
    margin: 24px 0;
    opacity: 0;
    animation: fadeIn 1s 1.2s forwards;
  }
  .ecg-line svg {
    position: absolute;
    left: 0;
    animation: ecgScroll 3s linear infinite;
  }
  @keyframes ecgScroll {
    from { transform: translateX(0); }
    to { transform: translateX(-50%); }
  }

  /* SECTIONS */
  section {
    position: relative;
    z-index: 2;
    max-width: 1200px;
    margin: 0 auto;
    padding: 100px 48px;
  }

  .section-header {
    display: flex;
    align-items: baseline;
    gap: 20px;
    margin-bottom: 64px;
  }
  .section-num {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    color: var(--teal);
    letter-spacing: 0.2em;
  }
  .section-title {
    font-size: clamp(28px, 4vw, 48px);
    font-weight: 800;
    letter-spacing: -0.02em;
    color: var(--text);
  }
  .section-line {
    flex: 1;
    height: 1px;
    background: var(--border);
    align-self: center;
  }

  /* RESEARCH CARDS */
  .research-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2px;
  }
  .research-card {
    background: var(--surface);
    border: 1px solid var(--border);
    padding: 36px;
    position: relative;
    overflow: hidden;
    transition: all 0.3s;
    cursor: none;
  }
  .research-card::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(0,229,200,0.03), transparent);
    opacity: 0;
    transition: opacity 0.3s;
  }
  .research-card:hover::before { opacity: 1; }
  .research-card:hover { border-color: rgba(0,229,200,0.3); transform: translateY(-2px); }

  .card-icon {
    width: 44px; height: 44px;
    background: rgba(0,229,200,0.08);
    border: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    margin-bottom: 20px;
  }
  .card-title {
    font-size: 18px;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 10px;
    letter-spacing: -0.01em;
  }
  .card-desc {
    font-family: 'Crimson Pro', serif;
    font-size: 16px;
    color: var(--text-dim);
    line-height: 1.6;
  }
  .card-featured {
    grid-column: 1 / -1;
    background: var(--surface2);
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0;
  }
  .card-featured-content { padding: 48px; }
  .card-featured-visual {
    padding: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-left: 1px solid var(--border);
  }

  /* Flow diagram */
  .flow {
    display: flex;
    flex-direction: column;
    gap: 6px;
    width: 100%;
  }
  .flow-node {
    background: rgba(0,229,200,0.08);
    border: 1px solid rgba(0,229,200,0.2);
    padding: 10px 16px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px;
    color: var(--teal);
    position: relative;
    animation: pulse 2s ease-in-out infinite;
  }
  .flow-node:nth-child(2) { animation-delay: 0.4s; }
  .flow-node:nth-child(3) { animation-delay: 0.8s; }
  .flow-node:nth-child(4) { animation-delay: 1.2s; }
  .flow-node:nth-child(5) { animation-delay: 1.6s; background: rgba(0,229,200,0.15); font-weight: 600; }

  .flow-arrow {
    text-align: center;
    color: var(--teal-dim);
    font-size: 16px;
    line-height: 1;
  }

  @keyframes pulse {
    0%, 100% { box-shadow: 0 0 0 rgba(0,229,200,0); }
    50% { box-shadow: 0 0 12px rgba(0,229,200,0.15); }
  }

  /* PUBLICATIONS */
  .pub-list { display: flex; flex-direction: column; gap: 1px; }
  .pub-item {
    background: var(--surface);
    border: 1px solid var(--border);
    padding: 28px 36px;
    display: grid;
    grid-template-columns: auto 1fr auto;
    align-items: start;
    gap: 24px;
    transition: all 0.25s;
    cursor: none;
    text-decoration: none;
  }
  .pub-item:hover {
    border-color: rgba(0,229,200,0.3);
    background: var(--surface2);
    transform: translateX(4px);
  }
  .pub-year {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px;
    color: var(--teal);
    letter-spacing: 0.05em;
    padding-top: 2px;
  }
  .pub-title {
    font-size: 17px;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 6px;
    letter-spacing: -0.01em;
  }
  .pub-venue {
    font-family: 'Crimson Pro', serif;
    font-style: italic;
    font-size: 15px;
    color: var(--text-dim);
  }
  .pub-tag {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    padding: 4px 10px;
    border: 1px solid;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    white-space: nowrap;
  }
  .tag-rl { color: var(--teal); border-color: rgba(0,229,200,0.3); }
  .tag-nlp { color: var(--amber); border-color: rgba(245,166,35,0.3); }
  .tag-robotics { color: #a78bfa; border-color: rgba(167,139,250,0.3); }

  /* TECH STACK */
  .stack-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
    gap: 1px;
  }
  .stack-item {
    background: var(--surface);
    border: 1px solid var(--border);
    padding: 20px 24px;
    display: flex;
    align-items: center;
    gap: 12px;
    transition: all 0.2s;
    cursor: none;
  }
  .stack-item:hover {
    border-color: rgba(0,229,200,0.3);
    background: var(--surface2);
  }
  .stack-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--teal);
    flex-shrink: 0;
    animation: blink 2s ease-in-out infinite;
  }
  .stack-item:nth-child(2) .stack-dot { animation-delay: 0.3s; }
  .stack-item:nth-child(3) .stack-dot { animation-delay: 0.6s; }
  .stack-item:nth-child(4) .stack-dot { animation-delay: 0.9s; background: var(--amber); }
  .stack-item:nth-child(5) .stack-dot { animation-delay: 1.2s; background: #a78bfa; }
  .stack-item:nth-child(6) .stack-dot { background: var(--amber); }
  @keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.3} }

  .stack-name {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 13px;
    color: var(--text);
  }

  /* TIMELINE */
  .timeline { position: relative; padding-left: 32px; }
  .timeline::before {
    content: '';
    position: absolute;
    left: 0; top: 12px; bottom: 0;
    width: 1px;
    background: var(--border);
  }
  .timeline-item {
    position: relative;
    margin-bottom: 48px;
  }
  .timeline-item::before {
    content: '';
    position: absolute;
    left: -36px; top: 6px;
    width: 10px; height: 10px;
    border-radius: 50%;
    background: var(--teal);
    box-shadow: 0 0 12px rgba(0,229,200,0.5);
  }
  .timeline-date {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    color: var(--teal);
    letter-spacing: 0.1em;
    margin-bottom: 8px;
  }
  .timeline-role {
    font-size: 20px;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 4px;
  }
  .timeline-org {
    font-family: 'Crimson Pro', serif;
    font-size: 16px;
    font-style: italic;
    color: var(--text-dim);
    margin-bottom: 10px;
  }
  .timeline-desc {
    font-family: 'Crimson Pro', serif;
    font-size: 16px;
    color: var(--text-dim);
    line-height: 1.6;
    max-width: 600px;
  }

  /* FOOTER/CONTACT */
  .contact-section {
    position: relative;
    z-index: 2;
    max-width: 1200px;
    margin: 0 auto;
    padding: 80px 48px 120px;
    border-top: 1px solid var(--border);
  }
  .contact-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 80px;
    align-items: center;
  }
  .contact-headline {
    font-size: clamp(36px, 5vw, 64px);
    font-weight: 800;
    line-height: 1;
    letter-spacing: -0.03em;
  }
  .contact-headline em {
    font-style: normal;
    color: var(--teal);
    display: block;
  }
  .contact-links { display: flex; flex-direction: column; gap: 12px; }
  .contact-link {
    display: flex;
    align-items: center;
    gap: 16px;
    text-decoration: none;
    padding: 16px 20px;
    background: var(--surface);
    border: 1px solid var(--border);
    transition: all 0.25s;
    cursor: none;
  }
  .contact-link:hover {
    border-color: rgba(0,229,200,0.3);
    background: var(--surface2);
    transform: translateX(6px);
  }
  .link-icon {
    width: 36px; height: 36px;
    background: rgba(0,229,200,0.08);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    flex-shrink: 0;
  }
  .link-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    color: var(--text-dim);
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 2px;
  }
  .link-value {
    font-size: 15px;
    color: var(--text);
    font-weight: 600;
  }

  /* Status indicator */
  .status-bar {
    position: fixed;
    bottom: 0; left: 0; right: 0;
    z-index: 100;
    background: rgba(5,12,18,0.9);
    border-top: 1px solid var(--border);
    padding: 8px 48px;
    display: flex;
    align-items: center;
    gap: 32px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    color: var(--text-dim);
    letter-spacing: 0.1em;
    backdrop-filter: blur(8px);
  }
  .status-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--teal);
    animation: blink 1.5s ease-in-out infinite;
    flex-shrink: 0;
  }
  .status-item { display: flex; align-items: center; gap: 8px; }
  .status-sep { color: var(--border); }

  /* Philosophy quote */
  .philosophy {
    position: relative;
    z-index: 2;
    max-width: 1200px;
    margin: 0 auto;
    padding: 60px 48px;
  }
  .philosophy-text {
    font-family: 'Crimson Pro', serif;
    font-style: italic;
    font-size: clamp(20px, 3vw, 32px);
    line-height: 1.5;
    color: var(--text-dim);
    max-width: 800px;
    border-left: 2px solid var(--teal);
    padding-left: 32px;
  }
  .philosophy-text strong { color: var(--text); font-style: normal; }

  /* Keyframes */
  @keyframes fadeUp {
    from { opacity: 0; transform: translateY(24px); }
    to { opacity: 1; transform: translateY(0); }
  }
  @keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
  }

  /* Scroll reveal */
  .reveal {
    opacity: 0;
    transform: translateY(32px);
    transition: opacity 0.7s ease, transform 0.7s ease;
  }
  .reveal.visible {
    opacity: 1;
    transform: translateY(0);
  }

  /* Responsive */
  @media (max-width: 900px) {
    nav { padding: 16px 24px; }
    .nav-links { display: none; }
    .hero { padding: 100px 24px 60px; }
    .vitals-strip { display: none; }
    section { padding: 60px 24px; }
    .research-grid { grid-template-columns: 1fr; }
    .card-featured { grid-template-columns: 1fr; }
    .card-featured-visual { border-left: none; border-top: 1px solid var(--border); }
    .contact-grid { grid-template-columns: 1fr; gap: 40px; }
    .hero-stats { gap: 28px; }
    .status-bar { padding: 8px 24px; gap: 16px; }
    body { cursor: auto; }
    .cursor, .cursor-ring { display: none; }
  }
</style>
</head>
<body>

<div class="cursor" id="cursor"></div>
<div class="cursor-ring" id="cursorRing"></div>

<div class="blob blob-1"></div>
<div class="blob blob-2"></div>
<div class="blob blob-3"></div>

<!-- NAV -->
<nav>
  <div class="nav-logo">MMA<span>//</span>Research</div>
  <ul class="nav-links">
    <li><a href="#research">Research</a></li>
    <li><a href="#publications">Publications</a></li>
    <li><a href="#stack">Stack</a></li>
    <li><a href="#journey">Journey</a></li>
    <li><a href="#contact">Contact</a></li>
  </ul>
</nav>

<!-- HERO -->
<div class="hero">
  <div class="hero-label">Ph.D. Candidate · TU Wien · Healthcare AI</div>

  <h1 class="hero-name">
    <span class="line1">Mohammad Mahdi</span>
    <span class="line2">Azarbeik</span>
  </h1>

  <p class="hero-tagline">
    Deploying reinforcement learning in intensive care — where every algorithm has the potential to save a life.
  </p>

  <div class="hero-stats">
    <div class="stat">
      <div class="stat-num">3+</div>
      <div class="stat-label">Publications</div>
    </div>
    <div class="stat">
      <div class="stat-num">2</div>
      <div class="stat-label">Research Institutes</div>
    </div>
    <div class="stat">
      <div class="stat-num">ICU</div>
      <div class="stat-label">Decision Support</div>
    </div>
  </div>

  <div class="hero-ctas">
    <a href="https://scholar.google.com/citations?authuser=1&user=tVbfK3AAAAAJ" class="btn btn-primary" target="_blank">
      <span>View Publications</span>
      <span>→</span>
    </a>
    <a href="mailto:mm.azarbeik@gmail.com" class="btn btn-ghost">
      <span>Get in Touch</span>
    </a>
    <a href="https://www.linkedin.com/in/mohammad-mahdi-azarbeik-757597201/" class="btn btn-ghost" target="_blank">
      <span>LinkedIn</span>
    </a>
  </div>

  <!-- Vitals monitor panel -->
  <div class="vitals-strip">
    <div class="vitals-card">
      <div class="vitals-label">Current Status</div>
      <div class="vitals-value">Active <span class="unit">Researcher</span></div>
      <svg class="vitals-sparkline" viewBox="0 0 240 32" fill="none">
        <polyline points="0,24 20,24 30,8 40,28 50,14 60,20 70,10 80,22 90,18 100,24 120,24 130,10 140,26 150,16 160,20 170,12 180,22 200,20 220,24 240,24" stroke="#00e5c8" stroke-width="1.5" fill="none" opacity="0.8"/>
      </svg>
    </div>
    <div class="vitals-card">
      <div class="vitals-label">Affiliation 01</div>
      <div class="vitals-value" style="font-size:14px;line-height:1.4;">Ludwig Boltzmann Institute<br><span class="unit">Digital Health & Patient Safety</span></div>
    </div>
    <div class="vitals-card">
      <div class="vitals-label">Affiliation 02</div>
      <div class="vitals-value" style="font-size:14px;line-height:1.4;">Medical University<br><span class="unit">of Vienna</span></div>
    </div>
    <div class="vitals-card">
      <div class="vitals-label">Focus Area</div>
      <div class="vitals-value" style="font-size:14px;">Optimal Intervention Timing<br><span class="unit">via RL · ICU Patients</span></div>
    </div>
  </div>
</div>

<!-- ECG Strip -->
<div class="ecg-line" style="position:relative;z-index:2;padding:0 48px;max-width:1200px;margin:0 auto;">
  <svg width="2400" height="48" viewBox="0 0 2400 48">
    <polyline points="0,24 80,24 100,24 110,4 120,44 130,20 140,24 220,24 240,24 250,4 260,44 270,20 280,24 360,24 380,24 390,4 400,44 410,20 420,24 500,24 520,24 530,4 540,44 550,20 560,24 640,24 660,24 670,4 680,44 690,20 700,24 780,24 800,24 810,4 820,44 830,20 840,24 920,24 940,24 950,4 960,44 970,20 980,24 1060,24 1080,24 1090,4 1100,44 1110,20 1120,24 1200,24 1220,24 1230,4 1240,44 1250,20 1260,24 1340,24 1360,24 1370,4 1380,44 1390,20 1400,24 1480,24 1500,24 1510,4 1520,44 1530,20 1540,24 1620,24 1640,24 1650,4 1660,44 1670,20 1680,24 1760,24 1780,24 1790,4 1800,44 1810,20 1820,24 1900,24 1920,24 1930,4 1940,44 1950,20 1960,24 2040,24 2060,24 2070,4 2080,44 2090,20 2100,24 2180,24 2200,24 2210,4 2220,44 2230,20 2240,24 2320,24 2340,24 2350,4 2360,44 2370,20 2380,24 2400,24"
    stroke="#00e5c8" stroke-width="1.5" fill="none" opacity="0.4"/>
  </svg>
</div>

<!-- RESEARCH -->
<section id="research">
  <div class="section-header reveal">
    <span class="section-num">01</span>
    <h2 class="section-title">Research</h2>
    <div class="section-line"></div>
  </div>

  <div class="research-grid reveal">
    <!-- Featured card -->
    <div class="research-card card-featured">
      <div class="card-featured-content">
        <div class="card-icon">🏥</div>
        <div class="card-title" style="font-size:24px; margin-bottom:16px;">Reinforcement Learning<br>for Clinical Decision Support</div>
        <div class="card-desc" style="font-size:18px; margin-bottom:24px;">
          The core mission: deploying RL algorithms in intensive care units to determine optimal timing for medical interventions — where the cost of a wrong decision is measured in human lives.
        </div>
        <div style="display:flex;gap:8px;flex-wrap:wrap;">
          <span class="pub-tag tag-rl">Reinforcement Learning</span>
          <span class="pub-tag tag-rl">ICU</span>
          <span class="pub-tag tag-rl">Patient Safety</span>
        </div>
      </div>
      <div class="card-featured-visual">
        <div class="flow" style="width:100%;">
          <div class="flow-node">Clinical Data (EHR)</div>
          <div class="flow-arrow">↓</div>
          <div class="flow-node">RL Algorithm</div>
          <div class="flow-arrow">↓</div>
          <div class="flow-node">Optimal Intervention Timing</div>
          <div class="flow-arrow">↓</div>
          <div class="flow-node">Clinical Decision Support</div>
          <div class="flow-arrow">↓</div>
          <div class="flow-node">✓ Improved Patient Outcomes</div>
        </div>
      </div>
    </div>

    <div class="research-card">
      <div class="card-icon">🤖</div>
      <div class="card-title">Robotics & State Estimation</div>
      <div class="card-desc">Advanced sensor fusion combining inertial motion capture with SLAM using Extended and Square-Root Unscented Kalman Filters for high-precision robotics applications.</div>
    </div>

    <div class="research-card">
      <div class="card-icon">🔍</div>
      <div class="card-title">LLM Safety & Hallucination Detection</div>
      <div class="card-desc">Unifying model-agnostic and model-aware approaches to detect and mitigate hallucinations in large language models — making AI systems trustworthy for high-stakes environments.</div>
    </div>

    <div class="research-card">
      <div class="card-icon">🧬</div>
      <div class="card-title">Generative AI for Medicine</div>
      <div class="card-desc">Exploring the intersection of large language models and clinical NLP — from medical text analysis to information extraction from unstructured health records.</div>
    </div>

    <div class="research-card">
      <div class="card-icon">🔐</div>
      <div class="card-title">Federated Learning</div>
      <div class="card-desc">Privacy-preserving healthcare AI through federated architectures that allow collaborative model training without exposing sensitive patient data across institutions.</div>
    </div>
  </div>
</section>

<!-- PUBLICATIONS -->
<section id="publications">
  <div class="section-header reveal">
    <span class="section-num">02</span>
    <h2 class="section-title">Publications</h2>
    <div class="section-line"></div>
  </div>

  <div class="pub-list reveal">
    <a href="https://scholar.google.com/citations?authuser=1&user=tVbfK3AAAAAJ" class="pub-item" target="_blank">
      <div class="pub-year">2025</div>
      <div>
        <div class="pub-title">Optimal timing for renal replacement therapy using reinforcement learning</div>
        <div class="pub-venue">Journal of Critical Care</div>
      </div>
      <span class="pub-tag tag-rl">RL · ICU</span>
    </a>

    <a href="https://scholar.google.com/citations?authuser=1&user=tVbfK3AAAAAJ" class="pub-item" target="_blank">
      <div class="pub-year">2024</div>
      <div>
        <div class="pub-title">TU Wien at SemEval-2024: Hallucination detection in LLMs</div>
        <div class="pub-venue">SemEval-2024 · ACL Anthology</div>
      </div>
      <span class="pub-tag tag-nlp">NLP · LLM</span>
    </a>

    <a href="https://scholar.google.com/citations?authuser=1&user=tVbfK3AAAAAJ" class="pub-item" target="_blank">
      <div class="pub-year">2023</div>
      <div>
        <div class="pub-title">Augmenting inertial motion capture with SLAM using EKF and SRUKF</div>
        <div class="pub-venue">Measurement · Elsevier</div>
      </div>
      <span class="pub-tag tag-robotics">Robotics</span>
    </a>
  </div>

  <div style="margin-top:24px;text-align:right;" class="reveal">
    <a href="https://scholar.google.com/citations?authuser=1&user=tVbfK3AAAAAJ" class="btn btn-ghost" target="_blank">
      Full Publication List →
    </a>
  </div>
</section>

<!-- STACK -->
<section id="stack">
  <div class="section-header reveal">
    <span class="section-num">03</span>
    <h2 class="section-title">Technical Stack</h2>
    <div class="section-line"></div>
  </div>

  <div class="stack-grid reveal">
    <div class="stack-item"><div class="stack-dot"></div><span class="stack-name">Python</span></div>
    <div class="stack-item"><div class="stack-dot"></div><span class="stack-name">PyTorch</span></div>
    <div class="stack-item"><div class="stack-dot"></div><span class="stack-name">TensorFlow</span></div>
    <div class="stack-item"><div class="stack-dot"></div><span class="stack-name">MATLAB</span></div>
    <div class="stack-item"><div class="stack-dot"></div><span class="stack-name">scikit-learn</span></div>
    <div class="stack-item"><div class="stack-dot"></div><span class="stack-name">PostgreSQL</span></div>
    <div class="stack-item"><div class="stack-dot"></div><span class="stack-name">BigQuery</span></div>
    <div class="stack-item"><div class="stack-dot"></div><span class="stack-name">ROS</span></div>
    <div class="stack-item"><div class="stack-dot"></div><span class="stack-name">Kalman Filtering</span></div>
    <div class="stack-item"><div class="stack-dot"></div><span class="stack-name">Docker</span></div>
    <div class="stack-item"><div class="stack-dot"></div><span class="stack-name">Google Cloud</span></div>
    <div class="stack-item"><div class="stack-dot"></div><span class="stack-name">Linux / Ubuntu</span></div>
  </div>
</section>

<!-- JOURNEY -->
<section id="journey">
  <div class="section-header reveal">
    <span class="section-num">04</span>
    <h2 class="section-title">Journey</h2>
    <div class="section-line"></div>
  </div>

  <div style="display:grid;grid-template-columns:1fr 1fr;gap:80px;">
    <div class="timeline reveal">
      <div class="timeline-item">
        <div class="timeline-date">Jul 2025 — Present</div>
        <div class="timeline-role">Researcher</div>
        <div class="timeline-org">Medical University of Vienna</div>
        <div class="timeline-desc">Advancing AI applications in clinical settings, integrating reinforcement learning into critical care workflows.</div>
      </div>
      <div class="timeline-item">
        <div class="timeline-date">Feb 2025 — Present</div>
        <div class="timeline-role">Researcher</div>
        <div class="timeline-org">Ludwig Boltzmann Institute for Digital Health and Patient Safety</div>
        <div class="timeline-desc">Developing patient safety systems at the frontier of digital health and AI decision support.</div>
      </div>
      <div class="timeline-item">
        <div class="timeline-date">Oct 2023 — Jan 2025</div>
        <div class="timeline-role">University Assistant</div>
        <div class="timeline-org">TU Wien</div>
        <div class="timeline-desc">Research, teaching, and mentorship across Reinforcement Learning, Generative AI, and Data-oriented Programming.</div>
      </div>
    </div>

    <div class="reveal">
      <div style="margin-bottom:32px;">
        <div class="vitals-label" style="margin-bottom:16px;font-size:11px;letter-spacing:0.2em;">Teaching @ TU Wien</div>
        <div style="display:flex;flex-direction:column;gap:8px;">
          <div style="display:flex;align-items:center;gap:12px;padding:14px 18px;background:var(--surface);border:1px solid var(--border);">
            <div style="width:3px;height:36px;background:var(--teal);flex-shrink:0;"></div>
            <div>
              <div style="font-weight:700;font-size:15px;">Reinforcement Learning</div>
              <div style="font-family:'Crimson Pro',serif;font-size:13px;color:var(--text-dim);">From theory to real-world applications</div>
            </div>
          </div>
          <div style="display:flex;align-items:center;gap:12px;padding:14px 18px;background:var(--surface);border:1px solid var(--border);">
            <div style="width:3px;height:36px;background:var(--amber);flex-shrink:0;"></div>
            <div>
              <div style="font-weight:700;font-size:15px;">Generative AI</div>
              <div style="font-family:'Crimson Pro',serif;font-size:13px;color:var(--text-dim);">Large language models and creative AI systems</div>
            </div>
          </div>
          <div style="display:flex;align-items:center;gap:12px;padding:14px 18px;background:var(--surface);border:1px solid var(--border);">
            <div style="width:3px;height:36px;background:#a78bfa;flex-shrink:0;"></div>
            <div>
              <div style="font-weight:700;font-size:15px;">Data-oriented Programming</div>
              <div style="font-family:'Crimson Pro',serif;font-size:13px;color:var(--text-dim);">Modern paradigms for data science</div>
            </div>
          </div>
        </div>
      </div>

      <div>
        <div class="vitals-label" style="margin-bottom:16px;font-size:11px;letter-spacing:0.2em;">Currently Exploring</div>
        <div style="display:flex;flex-direction:column;gap:6px;">
          <div style="font-family:'IBM Plex Mono',monospace;font-size:12px;color:var(--teal);padding:8px 12px;background:rgba(0,229,200,0.05);border-left:2px solid var(--teal);">+ Multi-agent reinforcement learning</div>
          <div style="font-family:'IBM Plex Mono',monospace;font-size:12px;color:var(--teal);padding:8px 12px;background:rgba(0,229,200,0.05);border-left:2px solid var(--teal);">+ LLM alignment, safety & interpretability</div>
          <div style="font-family:'IBM Plex Mono',monospace;font-size:12px;color:var(--teal);padding:8px 12px;background:rgba(0,229,200,0.05);border-left:2px solid var(--teal);">+ Real-time clinical decision deployment</div>
          <div style="font-family:'IBM Plex Mono',monospace;font-size:12px;color:var(--teal);padding:8px 12px;background:rgba(0,229,200,0.05);border-left:2px solid var(--teal);">+ Federated learning for healthcare AI</div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- PHILOSOPHY -->
<div class="philosophy reveal">
  <p class="philosophy-text">
    "In the critical care unit, every algorithm has the potential to <strong>save a life</strong>. At the intersection of AI and healthcare, we're not just writing code — we're writing <strong>the future of medicine</strong>."
  </p>
</div>

<!-- CONTACT -->
<div class="contact-section" id="contact">
  <div class="contact-grid">
    <div class="reveal">
      <div class="contact-headline">
        Let's build
        <em>something</em>
        impactful.
      </div>
      <p style="font-family:'Crimson Pro',serif;font-style:italic;font-size:18px;color:var(--text-dim);margin-top:20px;line-height:1.6;">
        Open to collaborations in Healthcare AI, Reinforcement Learning, Robotics, and interdisciplinary research at the edge of AI and medicine.
      </p>
    </div>

    <div class="contact-links reveal">
      <a href="mailto:mm.azarbeik@gmail.com" class="contact-link">
        <div class="link-icon">✉</div>
        <div>
          <div class="link-label">Email</div>
          <div class="link-value">mm.azarbeik@gmail.com</div>
        </div>
      </a>
      <a href="https://www.linkedin.com/in/mohammad-mahdi-azarbeik-757597201/" class="contact-link" target="_blank">
        <div class="link-icon">in</div>
        <div>
          <div class="link-label">LinkedIn</div>
          <div class="link-value">Mohammad Mahdi Azarbeik</div>
        </div>
      </a>
      <a href="https://scholar.google.com/citations?authuser=1&user=tVbfK3AAAAAJ" class="contact-link" target="_blank">
        <div class="link-icon">🎓</div>
        <div>
          <div class="link-label">Google Scholar</div>
          <div class="link-value">Research Publications</div>
        </div>
      </a>
    </div>
  </div>
</div>

<!-- STATUS BAR -->
<div class="status-bar">
  <div class="status-item">
    <div class="status-dot"></div>
    <span>SYSTEM ONLINE</span>
  </div>
  <span class="status-sep">·</span>
  <span>TU WIEN · MEDUNI VIENNA · LBI DHPS</span>
  <span class="status-sep">·</span>
  <span>HEALTHCARE AI · REINFORCEMENT LEARNING</span>
  <span class="status-sep">·</span>
  <span style="margin-left:auto;">MM.AZARBEIK@GMAIL.COM</span>
</div>

<script>
  // Custom cursor
  const cursor = document.getElementById('cursor');
  const ring = document.getElementById('cursorRing');
  let mx = 0, my = 0, rx = 0, ry = 0;

  document.addEventListener('mousemove', e => {
    mx = e.clientX; my = e.clientY;
    cursor.style.left = mx + 'px';
    cursor.style.top = my + 'px';
  });

  function animateCursor() {
    rx += (mx - rx) * 0.12;
    ry += (my - ry) * 0.12;
    ring.style.left = rx + 'px';
    ring.style.top = ry + 'px';
    requestAnimationFrame(animateCursor);
  }
  animateCursor();

  document.querySelectorAll('a, button, .research-card, .stack-item').forEach(el => {
    el.addEventListener('mouseenter', () => {
      cursor.style.width = '18px';
      cursor.style.height = '18px';
      ring.style.width = '56px';
      ring.style.height = '56px';
    });
    el.addEventListener('mouseleave', () => {
      cursor.style.width = '10px';
      cursor.style.height = '10px';
      ring.style.width = '36px';
      ring.style.height = '36px';
    });
  });

  // Scroll reveal
  const reveals = document.querySelectorAll('.reveal');
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry, i) => {
      if (entry.isIntersecting) {
        setTimeout(() => {
          entry.target.classList.add('visible');
        }, 100);
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -60px 0px' });

  reveals.forEach(el => observer.observe(el));

  // Stagger children of grids
  document.querySelectorAll('.research-grid .reveal, .pub-list .reveal').forEach((el, i) => {
    el.style.transitionDelay = (i * 0.08) + 's';
  });
</script>
</body>
</html>
