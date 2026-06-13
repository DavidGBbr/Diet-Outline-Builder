from __future__ import annotations

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from diet_outline_builder.graph import build_diet_outline


HTML = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Diet Outline Builder</title>
  <style>
    :root {
      color-scheme: light dark;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: #101312;
      color: #eef6ef;
    }
    body {
      margin: 0;
      min-height: 100vh;
      background:
        radial-gradient(circle at top left, rgba(85, 196, 134, 0.22), transparent 34rem),
        linear-gradient(135deg, #101312 0%, #18211e 100%);
    }
    main {
      width: min(1080px, calc(100% - 32px));
      margin: 0 auto;
      padding: 48px 0;
    }
    .hero {
      display: grid;
      grid-template-columns: 1fr;
      gap: 12px;
      margin-bottom: 28px;
    }
    h1 {
      margin: 0;
      max-width: 720px;
      font-size: clamp(2.3rem, 7vw, 5.8rem);
      line-height: 0.92;
      letter-spacing: -0.08em;
    }
    .subtitle {
      max-width: 640px;
      color: #b8c8bd;
      font-size: 1.08rem;
      line-height: 1.6;
    }
    .shell {
      display: grid;
      grid-template-columns: minmax(280px, 430px) 1fr;
      gap: 18px;
      align-items: start;
    }
    .panel {
      border: 1px solid rgba(238, 246, 239, 0.12);
      border-radius: 28px;
      background: rgba(20, 28, 25, 0.78);
      box-shadow: 0 24px 80px rgba(0, 0, 0, 0.28);
      backdrop-filter: blur(16px);
      padding: 22px;
    }
    form {
      display: grid;
      gap: 14px;
    }
    label {
      display: grid;
      gap: 7px;
      color: #d7e3da;
      font-size: 0.92rem;
      font-weight: 700;
    }
    input, select, button {
      width: 100%;
      box-sizing: border-box;
      border: 1px solid rgba(238, 246, 239, 0.16);
      border-radius: 16px;
      padding: 13px 14px;
      background: rgba(255, 255, 255, 0.06);
      color: #eef6ef;
      font: inherit;
    }
    select option {
      color: #111;
    }
    button {
      margin-top: 6px;
      cursor: pointer;
      border: 0;
      background: #7ee787;
      color: #0e1511;
      font-weight: 900;
    }
    .cards {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 12px;
      margin-bottom: 16px;
    }
    .card {
      border-radius: 20px;
      background: rgba(255, 255, 255, 0.07);
      padding: 16px;
    }
    .card span {
      display: block;
      color: #9fb0a5;
      font-size: 0.78rem;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      margin-bottom: 8px;
    }
    .card strong {
      font-size: 1.6rem;
    }
    pre {
      overflow: auto;
      border-radius: 20px;
      background: rgba(0, 0, 0, 0.34);
      padding: 16px;
      color: #c8f7ce;
    }
    .muted {
      color: #aebdb3;
      line-height: 1.55;
    }
    .error {
      display: none;
      margin-bottom: 14px;
      border-radius: 16px;
      padding: 12px;
      background: rgba(255, 90, 90, 0.14);
      color: #ffc7c7;
    }
    @media (max-width: 820px) {
      main { padding: 30px 0; }
      .shell { grid-template-columns: 1fr; }
      .cards { grid-template-columns: 1fr; }
    }
  </style>
</head>
<body>
  <main>
    <section class="hero">
      <h1>Diet Outline Builder</h1>
      <p class="subtitle">Run the LangGraph diet calculator locally. Fill the form, calculate BMI, energy target, and macros, then inspect the raw JSON response.</p>
    </section>
    <section class="shell">
      <div class="panel">
        <form id="diet-form">
          <label>Sex
            <select name="sex">
              <option value="male">Male</option>
              <option value="female">Female</option>
            </select>
          </label>
          <label>Age
            <input name="age" type="number" min="13" max="120" value="22" required />
          </label>
          <label>Height in cm
            <input name="heightCM" type="number" min="100" max="250" step="0.1" value="178" required />
          </label>
          <label>Weight in kg
            <input name="weightKG" type="number" min="30" max="300" step="0.1" value="87.4" required />
          </label>
          <label>Activity level
            <select name="activityLevel">
              <option value="low">Low</option>
              <option value="moderate" selected>Moderate</option>
              <option value="high">High</option>
            </select>
          </label>
          <label>Goal
            <select name="goal">
              <option value="lose_fat" selected>Lose fat</option>
              <option value="lose_weight">Lose weight</option>
              <option value="maintain">Maintain</option>
              <option value="gain_muscle">Gain muscle</option>
            </select>
          </label>
          <button type="submit">Build diet outline</button>
        </form>
      </div>
      <div class="panel">
        <div id="error" class="error"></div>
        <div class="cards">
          <div class="card"><span>BMI</span><strong id="imc">-</strong></div>
          <div class="card"><span>Target kcal</span><strong id="target">-</strong></div>
          <div class="card"><span>Macros</span><strong id="macros">-</strong></div>
        </div>
        <p id="explanation" class="muted">Submit the form to generate your local diet outline.</p>
        <pre id="json">{}</pre>
      </div>
    </section>
  </main>
  <script>
    const form = document.querySelector('#diet-form');
    const errorBox = document.querySelector('#error');
    const jsonBox = document.querySelector('#json');

    function setError(message) {
      errorBox.textContent = message;
      errorBox.style.display = message ? 'block' : 'none';
    }

    function render(data) {
      document.querySelector('#imc').textContent = `${data.imc} (${data.imcClassification})`;
      document.querySelector('#target').textContent = data.targetSpend;
      document.querySelector('#macros').textContent = `${data.macros.protein}p / ${data.macros.fat}f / ${data.macros.carb}c`;
      document.querySelector('#explanation').textContent = `${data.explanation} ${data.safetyDisclaimer}`;
      jsonBox.textContent = JSON.stringify(data, null, 2);
    }

    form.addEventListener('submit', async (event) => {
      event.preventDefault();
      setError('');
      const formData = new FormData(form);
      const payload = Object.fromEntries(formData.entries());
      payload.age = Number(payload.age);
      payload.heightCM = Number(payload.heightCM);
      payload.weightKG = Number(payload.weightKG);

      const response = await fetch('/api/diet', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      const data = await response.json();
      if (!response.ok) {
        setError(data.detail || 'Unable to build the diet outline.');
        return;
      }
      render(data);
    });
  </script>
</body>
</html>
"""


def create_app() -> FastAPI:
    app = FastAPI(title="Diet Outline Builder")

    @app.get("/", response_class=HTMLResponse)
    def index() -> str:
        return HTML

    @app.post("/api/diet")
    def calculate_diet(payload: dict) -> dict:
        try:
            return build_diet_outline(payload)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    return app


app = create_app()


def main() -> None:
    uvicorn.run("diet_outline_builder.web:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    main()
