import React, { useState, useRef } from 'react'
import axios from 'axios'

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export default function ChatWithVoice(){
  const [messages, setMessages] = useState([{ role: 'system', content: 'You are Vani, an audit assistant.' }])
  const [input, setInput] = useState('')
  const [listening, setListening] = useState(false)
  const [lang, setLang] = useState('en-IN')
  const recRef = useRef(null)

  const toggleListen = () => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
    if (!SpeechRecognition) { alert('Voice not supported'); return; }
    if (!recRef.current) {
      const r = new SpeechRecognition()
      r.lang = lang
      r.interimResults = false
      r.maxAlternatives = 1
      r.onresult = (e) => { const text = e.results[0][0].transcript; setInput(text); }
      r.onend = () => { setListening(false); recRef.current = null }
      recRef.current = r
      setListening(true)
      r.start()
    } else { recRef.current.stop(); recRef.current = null; setListening(false) }
  }

  const send = async () => {
    if (!input.trim()) return
    const userMsg = { role: 'user', content: input.trim() }
    const newMsgs = [...messages, userMsg]
    setMessages(newMsgs)
    setInput('')
    try {
      const token = localStorage.getItem('fat_token')
      const res = await axios.post(`${API}/ai/chat`, { messages: newMsgs }, { headers: { Authorization: `Bearer ${token}` } })
      const reply = res.data.reply
      setMessages(prev => [...newMsgs, { role: 'assistant', content: reply }])
      if ('speechSynthesis' in window) {
        const msg = new SpeechSynthesisUtterance(reply)
        if (lang.startsWith('hi')) msg.lang = 'hi-IN'
        else if (lang.startsWith('mr')) msg.lang = 'mr-IN'
        else msg.lang = 'en-IN'
        window.speechSynthesis.cancel()
        window.speechSynthesis.speak(msg)
      }
    } catch (err) {
      console.error(err)
      setMessages(prev => [...newMsgs, { role: 'assistant', content: 'Sorry — AI error.' }])
    }
  }

  return (
    <div style={{maxWidth:720, margin:'0 auto', padding:16, border:'1px solid #eee', borderRadius:8}}>
      <div style={{display:'flex', gap:12, alignItems:'center'}}>
        <img src='/public/logo.svg' alt='logo' style={{height:40}} />
        <h3 style={{margin:0}}>Hey Vani</h3>
        <select value={lang} onChange={e=>setLang(e.target.value)} style={{marginLeft:12}}>
          <option value='en-IN'>English</option>
          <option value='hi-IN'>हिन्दी (Hindi)</option>
          <option value='mr-IN'>मराठी (Marathi)</option>
        </select>
      </div>
      <div style={{height:320, overflowY:'auto', padding:12, marginTop:8, background:'#fafafa', borderRadius:6}}>
        {messages.filter(m=>m.role!=='system').map((m,i)=>(
          <div key={i} style={{marginBottom:10}}>
            <div style={{fontSize:12, color:'#666'}}>{m.role}</div>
            <div style={{padding:8, borderRadius:6, background: m.role==='assistant' ? '#fff' : '#e8f0fe' }}>{m.content}</div>
          </div>
        ))}
      </div>
      <div style={{display:'flex', gap:8, marginTop:12}}>
        <button onClick={toggleListen} style={{padding:8}}>{listening ? 'Stop 🎤' : 'Voice 🎤'}</button>
        <input value={input} onChange={e=>setInput(e.target.value)} placeholder='Ask Vani something...' style={{flex:1, padding:8}} />
        <button onClick={send} style={{background:'#FCFAFC', color:'#fff', border:0, padding:'8px 12px'}}>Send</button>
      </div>
    </div>
  )
}
