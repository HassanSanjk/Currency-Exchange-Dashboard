import { useState, useEffect } from 'react'

function CurrencyForm({ onConvert, loading }) {
  const [base, setBase] = useState('')
  const [target, setTarget] = useState('')
  const [amount, setAmount] = useState('')
  const [currencies, setCurrencies] = useState(null)
  const [currenciesError, setCurrenciesError] = useState(false)

  useEffect(() => {
    fetch('/api/currencies')
      .then(r => r.json())
      .then(data => setCurrencies(data.currencies))
      .catch(() => setCurrenciesError(true))
  }, [])

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

  function flagImg(code) {
    if (!currencies) return null
    const c = currencies.find(c => c.code === code)
    return c?.flag_country ? `https://flagcdn.com/w20/${c.flag_country}.png` : null
  }

  if (currenciesError) {
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
            <button type="button" className="swap-btn" onClick={handleSwap} title="Swap currencies">⇅</button>
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

  if (!currencies) {
    return (
      <div className="form-card">
        <h2 className="form-title">Currency Converter</h2>
        <p className="form-subtitle">Loading currencies...</p>
      </div>
    )
  }

  function CurrencySelect({ value, onChange, label, id }) {
    const src = flagImg(value)
    return (
      <div className="input-group">
        <label htmlFor={id}>{label}</label>
        <div className="input-wrapper select-wrapper">
          {src ? <img className="currency-flag" src={src} alt="" /> : <span className="currency-flag currency-flag--fallback" />}
          <select id={id} value={value} onChange={(e) => onChange(e.target.value)} required>
            <option value="" disabled>Select currency</option>
            {currencies.map(c => (
              <option key={c.code} value={c.code}>
                {c.code} - {c.name}
              </option>
            ))}
          </select>
        </div>
      </div>
    )
  }

  return (
    <div className="form-card">
      <h2 className="form-title">Currency Converter</h2>
      <p className="form-subtitle">Check real-time official and market rates.</p>

      <form onSubmit={handleSubmit}>
        <CurrencySelect value={base} onChange={setBase} label="From" id="base" />

        <div className="swap-wrapper">
          <button type="button" className="swap-btn" onClick={handleSwap} title="Swap currencies">
            ⇅
          </button>
        </div>

        <CurrencySelect value={target} onChange={setTarget} label="To" id="target" />

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
