
import { FormEvent, useState } from 'react'
import './App.css'

type Cause = {
  cause: string
  likelihood: string
  reasoning: string
}

type Investigation = {
  summary: string
  evidence: string[]
  likely_causes: Cause[]
  reproduction_steps: string[]
  candidate_test: string
  confirmation_or_refutation: string[]
  limitations: string[]
}

type Result = {
  status?: string
  model?: string
  analysis?: string
  verified?: boolean
  detail?: string
}

export default function App() {
  const [title, setTitle] = useState('Function returns the wrong result')
  const [description, setDescription] = useState(
    'The calculate_total function should add the item prices, but the result is lower than expected.'
  )
  const [errorLog, setErrorLog] = useState('Expected: 30\nActual: 20')
  const [language, setLanguage] = useState('Python')
  const [result, setResult] = useState<Result | null>(null)
  const [loading, setLoading] = useState(false)

  async function investigate(event: FormEvent) {
    event.preventDefault()
    setLoading(true)
    setResult(null)

    try {
      const response = await fetch('http://127.0.0.1:8000/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          title,
          description,
          error_log: errorLog,
          language,
        }),
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || 'Investigation request failed.')
      }

      setResult(data)
    } catch (error) {
      setResult({
        detail:
          error instanceof Error
            ? error.message
            : 'Could not connect to the backend.',
      })
    } finally {
      setLoading(false)
    }
  }

  let report: Investigation | null = null

  if (result?.analysis) {
    try {
      report = JSON.parse(result.analysis) as Investigation
    } catch {
      report = null
    }
  }

  function resetReport() {
    setResult(null)
  }

  return (
    <main className="app-shell">
      <nav className="topbar">
        <div className="brand">
          <div className="brand-icon">R</div>
          <span>ReproTrace<span className="brand-ai"> AI</span></span>
        </div>

        <div className="topbar-right">
          <span className="offline-indicator">
            <span className="online-dot" />
            LOCAL ENGINE
          </span>
          <span className="version">MVP 1.0</span>
        </div>
      </nav>

      <section className="hero">
        <div className="hero-label">
          <span className="hero-star">✦</span>
          EVIDENCE-DRIVEN DEBUGGING
        </div>

        <h1>
          Stop guessing.
          <br />
          <span>Start reproducing.</span>
        </h1>

        <p>
          Turn confusing bug reports into structured evidence,
          likely causes and reproducible investigation steps.
        </p>

        <div className="hero-tags">
          <span>01 / REPORT</span>
          <span>02 / INVESTIGATE</span>
          <span>03 / VERIFY</span>
        </div>
      </section>

      <section className="workspace">
        <form className="panel input-panel" onSubmit={investigate}>
          <div className="section-heading">
            <div>
              <span className="section-number">01</span>
              <div>
                <h2>Bug report</h2>
                <p>Describe the issue you encountered.</p>
              </div>
            </div>
            <span className="ready-label">
              <span className="online-dot" /> READY
            </span>
          </div>

          <label>
            BUG TITLE
            <input
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              required
              minLength={3}
              maxLength={200}
              placeholder="e.g. Calculator returns incorrect output"
            />
          </label>

          <label>
            ISSUE DESCRIPTION
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              required
              minLength={5}
              maxLength={5000}
              rows={4}
              placeholder="What happened? What did you expect?"
            />
          </label>

          <label>
            ERROR LOG / EXPECTED VS ACTUAL
            <textarea
              className="code-input"
              value={errorLog}
              onChange={(e) => setErrorLog(e.target.value)}
              rows={5}
              placeholder="Paste your error log here..."
            />
          </label>

          <label>
            PROGRAMMING LANGUAGE
            <select
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
            >
              <option>Python</option>
              <option>JavaScript</option>
              <option>TypeScript</option>
              <option>C</option>
              <option>Java</option>
              <option>Other</option>
            </select>
          </label>

          <button className="analyze-button" disabled={loading}>
            {loading ? (
              <>
                <span className="spinner" />
                Investigating...
              </>
            ) : (
              <>
                <span>✦</span>
                Investigate bug
                <span className="button-arrow">→</span>
              </>
            )}
          </button>

          <p className="privacy-note">
            <span>◆</span> Runs locally using a rule-based debugging engine.
            No API key required.
          </p>
        </form>

        <section className="panel report-panel">
          <div className="section-heading report-heading">
            <div>
              <span className="section-number">02</span>
              <div>
                <h2>Evidence report</h2>
                <p>Investigation results and findings.</p>
              </div>
            </div>

            <span className={`status-chip ${report ? 'complete' : ''}`}>
              {report ? 'COMPLETE' : result?.detail ? 'ERROR' : 'AWAITING INPUT'}
            </span>
          </div>

          {!result && (
            <div className="empty-state">
              <div className="empty-icon">⌕</div>
              <h3>Your investigation starts here.</h3>
              <p>
                Submit a bug report to generate evidence,
                possible causes and reproduction steps.
              </p>
              <div className="empty-flow">
                <span>Bug report</span>
                <b>→</b>
                <span>Evidence</span>
                <b>→</b>
                <span>Investigation</span>
              </div>
            </div>
          )}

          {result?.detail && (
            <div className="error-box">
              <h3>Connection or investigation error</h3>
              <p>{result.detail}</p>
              <p>
                Check that the backend is running at
                http://127.0.0.1:8000.
              </p>
            </div>
          )}

          {result && !result.detail && !report && (
            <div className="error-box">
              <h3>Unexpected report format</h3>
              <p>The backend response could not be displayed.</p>
            </div>
          )}

          {report && (
            <div className="report-content">
              <div className="result-banner">
                <div>
                  <span className="result-eyebrow">INVESTIGATION SUMMARY</span>
                  <h3>{report.summary}</h3>
                </div>
                <span className="result-icon">✓</span>
              </div>

              <div className="report-section">
                <div className="report-section-title">
                  <span className="section-icon purple">◈</span>
                  <h3>Supporting evidence</h3>
                  <span className="count">{report.evidence.length}</span>
                </div>
                <div className="evidence-list">
                  {report.evidence.map((item, index) => (
                    <div className="evidence-item" key={index}>
                      <span>✓</span>
                      {item}
                    </div>
                  ))}
                </div>
              </div>

              <div className="report-section">
                <div className="report-section-title">
                  <span className="section-icon orange">⌁</span>
                  <h3>Likely causes</h3>
                  <span className="count">{report.likely_causes.length}</span>
                </div>

                <div className="cause-list">
                  {report.likely_causes.map((cause, index) => (
                    <article className="cause-card" key={index}>
                      <div className="cause-top">
                        <h4>{cause.cause}</h4>
                        <span
                          className={`likelihood ${cause.likelihood.toLowerCase()}`}
                        >
                          {cause.likelihood}
                        </span>
                      </div>
                      <p>{cause.reasoning}</p>
                    </article>
                  ))}
                </div>
              </div>

              <div className="report-section">
                <div className="report-section-title">
                  <span className="section-icon blue">01</span>
                  <h3>Reproduction steps</h3>
                </div>
                <ol className="steps-list">
                  {report.reproduction_steps.map((step, index) => (
                    <li key={index}>
                      <span>{String(index + 1).padStart(2, '0')}</span>
                      {step}
                    </li>
                  ))}
                </ol>
              </div>

              <div className="report-section">
                <div className="report-section-title">
                  <span className="section-icon green">⌘</span>
                  <h3>Candidate test</h3>
                </div>
                <div className="candidate-box">
                  <span>TEST IDEA</span>
                  <p>{report.candidate_test}</p>
                </div>
              </div>

              <div className="report-section">
                <div className="report-section-title">
                  <span className="section-icon blue">✓</span>
                  <h3>Confirmation checklist</h3>
                </div>
                <ul className="check-list">
                  {report.confirmation_or_refutation.map((check, index) => (
                    <li key={index}>
                      <span>□</span>
                      {check}
                    </li>
                  ))}
                </ul>
              </div>

              <div className="verification-banner">
                <span className="verification-icon">!</span>
                <div>
                  <h4>Not yet verified</h4>
                  <p>
                    This is a rule-based investigation. Source code
                    has not been executed, tests have not been run,
                    and no fix has been verified.
                  </p>
                </div>
              </div>

              <div className="report-actions">
                <button
                  type="button"
                  className="secondary-button"
                  onClick={() => {
                    navigator.clipboard.writeText(
                      JSON.stringify(report, null, 2)
                    )
                  }}
                >
                  Copy report ↗
                </button>
                <button
                  type="button"
                  className="secondary-button"
                  onClick={resetReport}
                >
                  New investigation +
                </button>
              </div>
            </div>
          )}
        </section>
      </section>

      <footer className="footer">
        <span>REPROTRACE AI · OFFLINE DEMO</span>
        <span>AI proposes. Evidence supports. Tests verify.</span>
      </footer>
    </main>
  )
}
