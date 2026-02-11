export function ErrorFallback({ error, resetErrorBoundary }: { error: Error; resetErrorBoundary: () => void }) {
  return (
    <div style={{ padding: '20px', border: '1px solid red', borderRadius: '8px', margin: '20px' }}>
      <h2>Something went wrong:</h2>
      <pre style={{ color: 'red' }}>{error.message}</pre>
      <button onClick={resetErrorBoundary} style={{ padding: '10px', background: 'lightgreen', border: 'none', cursor: 'pointer' }}>
        Try again
      </button>
    </div>
  );
}