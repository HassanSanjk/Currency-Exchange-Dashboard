import { useState } from 'react'
import CurrencyForm from './CurrencyForm'
import OfficialResult from './OfficialResult'
import MarketResult from './MarketResult'
import ErrorBanner from './ErrorBanner'
import HistoryChart from './HistoryChart'

function formatNumber(value) {
  if (value == null) return null
  return new Intl.NumberFormat('en-US', {
    minimumFractionDigits: 0,
    maximumFractionDigits: 3,
  }).format(value)
}

function App() {
  const [error, setError] = useState(null)
  const [official, setOfficial] = useState(null)
  const [market, setMarket] = useState(null)
  const [loading, setLoading] = useState(false)
  const [history, setHistory] = useState(null)
  const [showHistory, setShowHistory] = useState(false)

  async function handleConvert(base, target, amount) {
    setLoading(true)
    setError(null)
    setOfficial(null)
    setMarket(null)
    setHistory(null)
    setShowHistory(false)

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
        if (data.official) {
          setOfficial({
            ...data.official,
            converted: formatNumber(data.official.converted),
            rate: formatNumber(data.official.rate),
          })
        }
        if (data.market) {
          setMarket({
            ...data.market,
            converted: formatNumber(data.market.converted),
            rate: formatNumber(data.market.rate),
            ref: formatNumber(data.market.ref),
          })
        }

        if (base === 'SDG' || target === 'SDG') {
          const histRes = await fetch(`/api/history?base=${base}&target=${target}`)
          const histData = await histRes.json()
          setHistory(histData)
          setShowHistory(true)
        }
      }
    } catch (err) {
      setError('Failed to connect to server.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app-container">
      <div className="app-inner">
        <CurrencyForm onConvert={handleConvert} loading={loading} />
        <ErrorBanner message={error} />
        <div className="results-grid">
          <OfficialResult result={official} />
          <MarketResult result={market} />
        </div>
        {showHistory && history && (
          <HistoryChart official={history.official} market={history.market} />
        )}
      </div>
    </div>
  )
}

export default App
