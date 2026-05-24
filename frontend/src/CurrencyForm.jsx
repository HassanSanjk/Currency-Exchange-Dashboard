import { useState } from 'react'

function CurrencyForm({ onConvert, loading }) {
  const [base, setBase] = useState('')
  const [target, setTarget] = useState('')
  const [amount, setAmount] = useState('')

  function handleSubmit(e) {
    e.preventDefault()
    if (base && target && amount) {
      onConvert(base, target, amount)
    }
  }

  function handleSwap() {
    const temp = base
    setBase(target)
    setTarget(temp)
  }

  return (
    <div className="form-card">
      <h2 className="form-title">Currency Converter</h2>
      <p className="form-subtitle">Check real-time official and market rates.</p>

      <form onSubmit={handleSubmit}>
        <div className="input-group">
          <label htmlFor="base">From</label>
          <div className="input-wrapper">
            <input
              id="base"
              type="text"
              placeholder="e.g. USD"
              value={base}
              onChange={(e) => setBase(e.target.value.toUpperCase())}
              maxLength={3}
              required
            />
          </div>
        </div>

        <div className="swap-wrapper">
          <button type="button" className="swap-btn" onClick={handleSwap} title="Swap currencies">
            ⇅
          </button>
        </div>

        <div className="input-group">
          <label htmlFor="target">To</label>
          <div className="input-wrapper">
            <input
              id="target"
              type="text"
              placeholder="e.g. SDG"
              value={target}
              onChange={(e) => setTarget(e.target.value.toUpperCase())}
              maxLength={3}
              required
            />
          </div>
        </div>

        <div className="input-group">
          <label htmlFor="amount">Amount</label>
          <div className="input-wrapper">
            <input
              id="amount"
              type="number"
              placeholder="0.00"
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
              min="0"
              step="any"
              required
            />
          </div>
        </div>

        <button type="submit" className="convert-btn" disabled={loading}>
          {loading ? 'Converting...' : 'Convert'}
        </button>
      </form>
    </div>
  )
}

export default CurrencyForm
