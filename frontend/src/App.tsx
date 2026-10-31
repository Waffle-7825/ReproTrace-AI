import { FormEvent, useState } from 'react'

type Result = { status?: string; model?: string; analysis?: string; verified?: boolean; detail?: string }

export default function App() {
  const [title, setTitle] = useState('Function returns the wrong result')
  const [description, setDescription] = useState('The calculate_total function should add the item prices, but the result is lower than expected.')
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
        body: JSON.stringify({ title, description, error_log: errorLog, language }),
      })
      const data = await response.json()
      if (!response.ok) throw new Error(data.detail || 'Request failed')
      setResult(data)
    } catch (error) {
      setResult({ detail: error instanceof Error ? error.message : 'Unknown error' })
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="shell">
      <nav className="nav"><div className="brand-mark">R</div><span>ReproTrace <b>AI</b></span><span className="nav-tag">HACKATHON MVP</span></nav>
      <section className="hero">
        <p className="eyebrow">EVIDENCE-DRIVEN DEBUGGING</p>
        <h1>From bug report<br /><span>to reproducible evidence.</span></h1>
        <p className="subhead">Turn a confusing bug report into ranked hypotheses, reproduction steps, and a test idea — with uncertainty clearly labelled.</p>
      </section>
      <section className="workspace">
        <form className="panel form-panel" onSubmit={investigate}>
          <div className="panel-heading"><div><p className="eyebrow">01 / INPUT</p><h2>Bug report</h2></div><span className="live-dot">● Ready</span></div>
          <label>Bug title<input value={title} onChange={e => setTitle(e.target.value)} required minLength={3} maxLength={200} /></label>
          <label>What happened?<textarea value={description} onChange={e => setDescription(e.target.value)} required minLength={5} maxLength={5000} rows={4} /></label>
          <label>Error log / expected vs actual<textarea value={errorLog} onChange={e => setErrorLog(e.target.value)} rows={4} placeholder="Paste the error or expected/actual output…" /></label>
          <label>Language<select value={language} onChange={e => setLanguage(e.target.value)}><option>Python</option><option>JavaScript</option><option>TypeScript</option><option>C</option><option>Java</option><option>Other</option></select></label>
          <button disabled={loading}>{loading ? 'Investigating…' : '✦ Investigate with Meta AI'} <span>→</span></button>
          <p className="hint">Your API key stays on the backend. Never paste secrets into this form.</p>
        </form>
        <section className="panel result-panel">
          <div className="panel-heading"><div><p className="eyebrow">02 / INVESTIGATION</p><h2>Evidence report</h2></div><span className="status-chip">{result?.analysis ? 'RESULT' : 'AWAITING INPUT'}</span></div>
          {!result && <div className="empty"><div className="radar">◎</div><h3>Make the bug explain itself.</h3><p>Submit a report to get evidence, likely causes, reproduction steps, and a candidate test.</p><div className="empty-line">AI hypotheses <span>→</span> human review <span>→</span> real test verification</div></div>}
          {result?.detail && <div className="error-box"><b>Could not complete investigation</b><p>{result.detail}</p><p>Check that the backend is running and your API key / endpoint are configured.</p></div>}
          {result?.analysis && <><pre className="analysis">{result.analysis}</pre><div className="notice">⚠ AI analysis only. No code has been executed and no fix has been verified.</div></>}
        </section>
      </section>
      <footer><span>ReproTrace AI · Prototype</span><span>Hypotheses are not proof. Verification comes from tests.</span></footer>
    </main>
  )
}
