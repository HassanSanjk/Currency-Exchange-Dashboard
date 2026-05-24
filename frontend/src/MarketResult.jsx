function MarketResult({ result }) {
  if (!result) return null

  return (
    <div>
      <p style={{ color: 'red' }}>
        This value uses Sudan parallel market data (from: alsoug.com).
        Official SDG rates may not reflect real market prices.
      </p>
      <h3>Market Rate (SDG)</h3>
      <p>{result.amount} {result.base} = <strong>{result.converted} {result.target}</strong></p>
      <p>Rate: {result.rate}</p>
      {result.ref && result.base !== 'USD' && (
        <p>Reference (USD/SDG): 1 USD = {result.ref} SDG</p>
      )}
      <p>Status: {result.status}</p>
      <p>Updated: {result.updated} (UTC) / {result.updatedMyt} (MYT)</p>
    </div>
  )
}

export default MarketResult
