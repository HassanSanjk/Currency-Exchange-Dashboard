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

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="From (e.g. USD)"
        value={base}
        onChange={(e) => setBase(e.target.value.toUpperCase())}
      />
      <input
        type="text"
        placeholder="To (e.g. SDG)"
        value={target}
        onChange={(e) => setTarget(e.target.value.toUpperCase())}
      />
      <input
        type="number"
        placeholder="Amount"
        value={amount}
        onChange={(e) => setAmount(e.target.value)}
        min="0"
        step="any"
      />
      <button type="submit" disabled={loading}>
        {loading ? 'Converting...' : 'Convert'}
      </button>
    </form>
  )
}

export default CurrencyForm
