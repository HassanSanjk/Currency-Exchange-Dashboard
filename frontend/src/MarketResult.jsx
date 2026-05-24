function MarketResult({ result }) {
  if (!result) return null

  return (
    <div className="result-card result-card--orange">
      <div className="result-card__header">
        <h3 className="result-card__title result-card__title--orange">Market Rate (SDG)</h3>
        <span className={`badge badge--${result.status === 'Live' ? 'live' : 'cached'}`}>
          {result.status}
        </span>
      </div>

      <p className="market-warning">
        This value uses Sudan parallel market data (from: alsoug.com).
        Official SDG rates may not reflect real market prices.
      </p>

      <div className="result-card__body">
        <div className="result-card__amount">
          <span className="result-card__value">{result.converted}</span>
          <span className="result-card__currency">{result.target}</span>
        </div>
        <p className="result-card__rate">
          Exchange Rate: <strong>1 {result.base} = {result.rate} {result.target}</strong>
        </p>
        {result.ref && result.base !== 'USD' && (
          <p className="result-card__ref">
            Reference: 1 USD = {result.ref} SDG
          </p>
        )}
      </div>

      <div className="result-card__footer">
        <p>{result.updated} UTC</p>
        <p>{result.updatedMyt} MYT</p>
      </div>
    </div>
  )
}

export default MarketResult
