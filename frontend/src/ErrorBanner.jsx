function ErrorBanner({ message }) {
  if (!message) return null

  return (
    <div style={{ color: 'red' }}>
      <p>{message}</p>
    </div>
  )
}

export default ErrorBanner
