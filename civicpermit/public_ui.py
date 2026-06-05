"""Public UI shell for CivicPermit v0.2.2."""

from __future__ import annotations


def render_public_lookup_page() -> str:
    """Render the public-facing CivicPermit lookup page."""

    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CivicPermit Pre-Application Intake</title>
<style>
  :root { --ink:#17202a; --muted:#56606a; --paper:#fbfaf5; --blue:#1f5b78; --green:#2f6b50; --gold:#d8b45b; --line:#d7c8a8; --warn:#8f4126; --field:#ffffff; }
  * { box-sizing: border-box; }
  body { margin:0; color:var(--ink); font-family:"Aptos","Segoe UI",sans-serif; background:var(--paper); }
  .skip-link { position:absolute; left:1rem; top:-4rem; background:var(--ink); color:white; padding:.7rem 1rem; border-radius:8px; }
  .skip-link:focus { top:1rem; }
  header, main, footer { width:min(1120px, calc(100% - 32px)); margin:0 auto; }
  header { padding:48px 0 24px; }
  .eyebrow { color:var(--blue); text-transform:uppercase; letter-spacing:0; font-weight:800; font-size:.78rem; }
  h1 { max-width:960px; margin:0; font-family:Georgia,"Times New Roman",serif; font-size:4.75rem; line-height:1; letter-spacing:0; }
  .lede { max-width:820px; font-size:1.35rem; line-height:1.55; color:#31404a; }
  .badge { display:inline-flex; width:fit-content; padding:.45rem .75rem; border-radius:8px; background:var(--green); color:white; font-weight:900; }
  .grid { display:grid; grid-template-columns:repeat(12,1fr); gap:18px; }
  .card { grid-column:span 6; min-width:0; padding:24px; border:1px solid var(--line); border-radius:8px; background:white; box-shadow:0 18px 40px rgba(35,43,50,.08); }
  .card.large { grid-column:span 12; }
  h2,h3 { font-family:Georgia,"Times New Roman",serif; letter-spacing:0; }
  h2 { margin:0 0 14px; font-size:2.4rem; }
  p, li { line-height:1.65; }
  form { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:16px; margin-top:22px; }
  label { display:grid; gap:7px; font-weight:800; color:#26333c; }
  label.full { grid-column:1 / -1; }
  input, textarea { width:100%; min-width:0; border:1px solid #aebac0; border-radius:8px; background:var(--field); color:var(--ink); font:inherit; padding:.82rem .92rem; }
  textarea { min-height:92px; resize:vertical; }
  button { justify-self:start; border:0; border-radius:8px; background:var(--blue); color:white; font:900 1rem "Aptos","Segoe UI",sans-serif; padding:.9rem 1.1rem; cursor:pointer; }
  button:disabled { background:#748591; cursor:wait; }
  .help { margin:0; color:var(--muted); font-size:.92rem; }
  .result { margin-top:18px; padding:18px; border-left:6px solid var(--green); border-radius:8px; background:white; }
  .result[hidden] { display:none; }
  .warning { border-left-color:var(--warn); background:#fff8f4; }
  .status-line { min-height:1.6rem; color:var(--muted); font-weight:800; }
  .materials { padding-left:1.2rem; }
  .kicker { color:var(--muted); font-size:.86rem; font-weight:900; letter-spacing:0; text-transform:uppercase; }
  footer { padding:38px 0 56px; color:var(--muted); }
  :focus-visible { outline:4px solid var(--gold); outline-offset:3px; }
  @media (max-width:760px) { header,main,footer{margin:0;max-width:390px;width:100%;padding-left:24px;padding-right:24px}header{padding-top:34px}h1{font-size:2.55rem}.lede{font-size:1.08rem}h2{font-size:1.9rem}.card{grid-column:span 12;padding:20px;border-radius:8px}form{grid-template-columns:1fr}button{width:100%} }
</style>
</head>
<body>
<a class="skip-link" href="#main">Skip to main content</a>
<header>
  <p class="eyebrow">CivicSuite / CivicPermit public intake</p>
  <h1>Help applicants arrive with the right first packet.</h1>
  <p class="lede">CivicPermit gives pre-application requirement context, intake-readiness signals, and records-ready outlines without becoming the permitting system of record.</p>
  <p><span class="badge">v0.2.2 permit pre-application + staff review queues</span></p>
</header>
<main id="main" tabindex="-1">
  <section class="grid" aria-labelledby="lookup-title">
    <article class="card large">
      <p class="kicker">Requirement lookup</p>
      <h2 id="lookup-title">Find the first checklist</h2>
      <p>Enter a permit project type and location context. CivicPermit returns requirement context from configured local records when available, otherwise from deterministic sample guidance.</p>
      <form id="lookup-form">
        <label>Project type
          <input id="project-type" name="project_type" autocomplete="off" value="ADU" required maxlength="255">
        </label>
        <label>Location context
          <input id="location-context" name="location_context" autocomplete="off" value="R-2 parcel" maxlength="500">
        </label>
        <label class="full">Proposal note
          <textarea id="proposal-note" name="proposal_note" maxlength="5000">Applicant proposes an ADU at 100 Main Street with a site plan and utility description.</textarea>
        </label>
        <button id="lookup-submit" type="submit">Lookup checklist</button>
        <p class="help">This page does not submit a formal application or create an official completeness decision.</p>
      </form>
      <p id="lookup-status" class="status-line" role="status" aria-live="polite"></p>
      <div id="lookup-result" class="result" hidden>
        <p class="kicker" id="result-project-type"></p>
        <h3 id="result-title"></h3>
        <p id="result-citation"></p>
        <ul id="result-materials" class="materials"></ul>
        <p id="result-staff-note"></p>
        <p id="result-disclaimer"></p>
      </div>
    </article>
    <article class="card"><p class="kicker">Intake readiness</p><h2>Follow-up before submittal</h2><div class="result"><p>Missing items are returned as actionable applicant follow-up and can be routed to a staff-only review queue, not as an official completeness decision.</p></div></article>
    <article class="card"><p class="kicker">Records-ready export</p><h2>Keep provenance</h2><div class="result"><p>Exports preserve inquiry text, checklist, staff reviewer, generated outline, staff queue status, and final staff edits.</p></div></article>
    <article class="card"><p class="kicker">Boundary</p><h2>No permit approval</h2><div class="result warning"><p>CivicPermit does not approve permits, calculate official fees, schedule inspections, or replace the permitting system of record.</p></div></article>
  </section>
</main>
<footer><p>CivicPermit is part of the Apache 2.0 CivicSuite open-source municipal AI project.</p></footer>
<script>
(() => {
  const form = document.querySelector("#lookup-form");
  const status = document.querySelector("#lookup-status");
  const result = document.querySelector("#lookup-result");
  const submit = document.querySelector("#lookup-submit");
  const materials = document.querySelector("#result-materials");

  function setStatus(message, isError = false) {
    status.textContent = message;
    status.style.color = isError ? "var(--warn)" : "var(--muted)";
  }

  function renderRequirement(payload) {
    document.querySelector("#result-project-type").textContent = payload.project_type || "";
    document.querySelector("#result-title").textContent = payload.title || "Permit checklist";
    document.querySelector("#result-citation").textContent = payload.citation || "";
    document.querySelector("#result-staff-note").textContent = payload.staff_note || "";
    document.querySelector("#result-disclaimer").textContent = payload.disclaimer || "";
    materials.replaceChildren(
      ...(payload.required_materials || []).map((item) => {
        const li = document.createElement("li");
        li.textContent = item;
        return li;
      })
    );
    result.hidden = false;
  }

  async function lookupRequirement(event) {
    event.preventDefault();
    submit.disabled = true;
    result.hidden = true;
    setStatus("Looking up checklist...");
    try {
      const response = await fetch("/api/v1/civicpermit/requirements/lookup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          project_type: document.querySelector("#project-type").value,
          location_context: document.querySelector("#location-context").value,
        }),
      });
      const payload = await response.json();
      if (!response.ok) {
        const detail = payload.detail || {};
        throw new Error([detail.message, detail.fix].filter(Boolean).join(" "));
      }
      renderRequirement(payload);
      setStatus("Checklist loaded for staff-reviewed pre-application guidance.");
    } catch (error) {
      setStatus(error.message || "CivicPermit could not load the checklist.", true);
    } finally {
      submit.disabled = false;
    }
  }

  form.addEventListener("submit", lookupRequirement);
})();
</script>
</body>
</html>
"""
