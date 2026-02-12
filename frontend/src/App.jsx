import { useState } from 'react'
import './App.css'

function App() {
  const [input, setInput] = useState('')
  const [response, setResponse] = useState('')

  const sendMessage = async () => {
    const res = await fetch('http://127.0.0.1:8000/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: input })
    })
    const data = await res.json()
    setResponse(data.reply)
  }

  return (
    <div className="container">
      <h1>Hyde AI</h1>
      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Ask Hyde..."
      />
      <button onClick={sendMessage}>Send</button>
      <p className="response">{response}</p>
    </div>
  )
}

export default App