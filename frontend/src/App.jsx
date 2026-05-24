import { useState } from 'react'
import CurrencyForm from './CurrencyForm'
import OfficialResult from './OfficialResult'
import MarketResult from './MarketResult'
import ErrorBanner from './ErrorBanner'

function App() {
  const [error, setError] = useState(null)
  const [official, setOfficial] = useState(null)
  const [market, setMarket] = useState(null)
  const [loading, setLoading] = useState(false)

  async function handleConvert(base, target, amount) {
    setLoading(true)
    setError(null)
    setOfficial(null)
    setMarket(null)

    try {
      const response = await fetch('/convert', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({ base, target, amount }),
      })

      const data = await response.json()

      if (data.error) {
        setError(data.error)
      } else {
        if (data.official) setOfficial(data.official)
        if (data.market) setMarket(data.market)
      }
    } catch (err) {
      setError('Failed to connect to server.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <h1>Currency Converter</h1>
      <CurrencyForm onConvert={handleConvert} loading={loading} />
      <ErrorBanner message={error} />
      <OfficialResult result={official} />
      <MarketResult result={market} />
    </div>
  )
}

export default App
