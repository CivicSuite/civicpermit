"""Static public UI shell for CivicPermit v1.0.0."""

from __future__ import annotations


def render_public_lookup_page() -> str:
    """Render the public-facing CivicPermit sample page."""

    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CivicPermit Pre-Application Intake</title>
<style>
  :root { --ink:#17202a; --muted:#56606a; --paper:#fffdf7; --blue:#1f5b78; --green:#2f6b50; --gold:#d8b45b; --line:#d7c8a8; }
  * { box-sizing: border-box; }
  body { margin:0; color:var(--ink); font-family:"Aptos","Segoe UI",sans-serif; background:linear-gradient(135deg,#f7f1e6,#edf6fb); }
  .skip-link { position:absolute; left:1rem; top:-4rem; background:var(--ink); color:white; padding:.7rem 1rem; border-radius:8px; }
  .skip-link:focus { top:1rem; }
  header, main, footer { width:min(1120px, calc(100% - 32px)); margin:0 auto; }
  header { padding:48px 0 24px; }
  .eyebrow { color:var(--blue); text-transform:uppercase; letter-spacing:0; font-weight:800; font-size:.78rem; }
  h1 { max-width:960px; margin:0; font-family:Georgia,"Times New Roman",serif; font-size:4.75rem; line-height:1; letter-spacing:0; }
  .lede { max-width:820px; font-size:1.35rem; line-height:1.55; color:#31404a; }
  .badge { display:inline-flex; width:fit-content; padding:.45rem .75rem; border-radius:8px; background:var(--green); color:white; font-weight:900; }
  .grid { display:grid; grid-template-columns:repeat(12,1fr); gap:18px; }
  .card { grid-column:span 6; min-width:0; padding:24px; border:1px solid var(--line); border-radius:8px; background:rgba(255,253,247,.92); box-shadow:0 18px 40px rgba(35,43,50,.10); }
  .card.large { grid-column:span 12; }
  h2,h3 { font-family:Georgia,"Times New Roman",serif; letter-spacing:0; }
  h2 { margin:0 0 14px; font-size:2.4rem; }
  p, li { line-height:1.65; }
  .sample-box { padding:18px; border:1px solid #b9c6cc; border-radius:8px; background:#f3f7f8; color:var(--ink); }
  .result { margin-top:18px; padding:18px; border-left:6px solid var(--green); border-radius:8px; background:white; }
  .warning { border-left-color:#b2603f; background:#fff8f4; }
  .kicker { color:var(--muted); font-size:.86rem; font-weight:900; letter-spacing:0; text-transform:uppercase; }
  footer { padding:38px 0 56px; color:var(--muted); }
  :focus-visible { outline:4px solid var(--gold); outline-offset:3px; }
  @media (max-width:760px) { header,main,footer{margin:0;max-width:390px;width:100%;padding-left:24px;padding-right:24px}header{padding-top:34px}h1{font-size:2.55rem}.lede{font-size:1.08rem}h2{font-size:1.9rem}.card{grid-column:span 12;padding:20px;border-radius:8px} }
</style>
</head>
<body>
<a class="skip-link" href="#main">Skip to main content</a>
<header>
  <p class="eyebrow">CivicSuite / CivicPermit public sample</p>
  <h1>Help applicants arrive with the right first packet.</h1>
  <p class="lede">CivicPermit demonstrates permit pre-application support: sample requirement lookup, intake-readiness review, and records-ready submittal outlines without becoming the permitting system of record.</p>
  <p><span class="badge">v1.0.0 permit pre-application + staff review queues</span></p>
</header>
<main id="main" tabindex="-1">
  <section class="grid" aria-labelledby="lookup-title">
    <article class="card large">
      <p class="kicker">Sample requirement lookup</p>
      <h2 id="lookup-title">ADU pre-application checklist</h2>
      <p class="kicker">Static sample proposal</p>
      <div class="sample-box">Applicant proposes an ADU at 100 Main Street with a site plan and utility description.</div>
      <div class="result" role="status" aria-live="polite">
        <h3>Materials to gather</h3>
        <ul><li>Site plan showing existing and proposed structures.</li><li>Parking and access narrative.</li><li>Utility connection description.</li></ul>
      </div>
    </article>
    <article class="card"><p class="kicker">Intake readiness</p><h2>Follow-up before submittal</h2><div class="result"><p>Missing items are returned as actionable applicant follow-up and can be routed to a staff-only review queue, not as an official completeness decision.</p></div></article>
    <article class="card"><p class="kicker">Records-ready export</p><h2>Keep provenance</h2><div class="result"><p>Exports preserve inquiry text, checklist, staff reviewer, generated outline, staff queue status, and final staff edits.</p></div></article>
    <article class="card"><p class="kicker">Boundary</p><h2>No permit approval</h2><div class="result warning"><p>CivicPermit does not approve permits, calculate official fees, schedule inspections, or replace the permitting system of record.</p></div></article>
  </section>
</main>
<footer><p>CivicPermit is part of the Apache 2.0 CivicSuite open-source municipal AI project.</p></footer>
</body>
</html>
"""
