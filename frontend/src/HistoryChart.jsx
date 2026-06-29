import { useMemo } from 'react'
import {
  ResponsiveContainer, LineChart, Line, XAxis, YAxis,
  CartesianGrid, Tooltip, Legend,
} from 'recharts'

function formatDate(ts) {
  const d = new Date(ts * 1000)
  return `${String(d.getMonth() + 1).padStart(2, '0')}/${String(d.getDate()).padStart(2, '0')}`
}

function formatTooltip(ts) {
  const d = new Date(ts * 1000)
  return d.toLocaleDateString('en-US', {
    month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit',
  })
}

function CustomTooltip({ active, payload, label }) {
  if (!active || !payload || !payload.length) return null
  return (
    <div style={{
      background: 'rgba(0,0,0,0.8)', color: '#fff',
      padding: '8px 12px', borderRadius: 6,
      fontSize: 13, fontFamily: 'system-ui, sans-serif',
    }}>
      <div style={{ marginBottom: 4 }}>{formatTooltip(label)}</div>
      {payload.map(p => (
        <div key={p.dataKey} style={{ color: p.color }}>
          {p.name}: {Number(p.value).toFixed(2)}
        </div>
      ))}
    </div>
  )
}

function HistoryChart({ official = [], market = [] }) {
  const mergedData = useMemo(() => {
    const map = {}
    official.forEach(p => {
      if (!map[p.timestamp]) map[p.timestamp] = { timestamp: p.timestamp }
      map[p.timestamp].official = p.rate
    })
    market.forEach(p => {
      if (!map[p.timestamp]) map[p.timestamp] = { timestamp: p.timestamp }
      map[p.timestamp].market = p.rate
    })
    return Object.values(map).sort((a, b) => a.timestamp - b.timestamp)
  }, [official, market])

  const hasOfficial = official.length > 0
  const hasMarket = market.length > 0

  if (!hasOfficial && !hasMarket) {
    return (
      <div className="chart-container">
        <div style={{ textAlign: 'center', color: '#666', padding: '130px 0', fontSize: 14 }}>
          No history data yet
        </div>
      </div>
    )
  }

  return (
    <div className="chart-container">
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={mergedData} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e5e5e5" />
          <XAxis
            dataKey="timestamp"
            tickFormatter={formatDate}
            tick={{ fontSize: 12, fill: '#666' }}
            tickLine={false}
            dy={6}
          />
          <YAxis
            tick={{ fontSize: 12, fill: '#666' }}
            tickLine={false}
            dx={-4}
            width={50}
          />
          <Tooltip content={<CustomTooltip />} />
          <Legend
            wrapperStyle={{ fontSize: 13, paddingTop: 8 }}
            iconType="line"
          />
          {hasOfficial && (
            <Line
              dataKey="official"
              stroke="#22c55e"
              strokeWidth={2}
              dot={false}
              name="Official"
              connectNulls={false}
            />
          )}
          {hasMarket && (
            <Line
              dataKey="market"
              stroke="#f97316"
              strokeWidth={2}
              dot={false}
              name="Market"
              connectNulls={false}
            />
          )}
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}

export default HistoryChart
