function OfficialResult({ result }) {
  if (!result) return null

  return (
    <div>
      <h3>Official Rate</h3>
      <p>{result.amount} {result.base} = <strong>{result.converted} {result.target}</strong></p>
      <p>Rate: {result.rate}</p>
      <p>Status: {result.status}</p>
      <p>Updated: {result.updated} (UTC) / {result.updatedMyt} (MYT)</p>
    </div>
  )
}

export default OfficialResult
