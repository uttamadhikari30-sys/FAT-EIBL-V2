import React, {useState} from 'react'
import axios from 'axios'
const API = import.meta.env.VITE_API_URL || 'http://localhost:8000'
export default function Login(){
  const [email, setEmail] = useState('uttam.singh@edmeinsurance.com')
  const [password, setPassword] = useState('123')
  const [error, setError] = useState('')
  const submit = async (e) => { e.preventDefault(); try { const res = await axios.post(`${API}/auth/token`, { username: email, password }); const token = res.data.access_token; localStorage.setItem('fat_token', token); window.location.href = '/'; } catch(err){ setError('Login failed') } }
  return (
    <div style={display:'flex', minHeight:'100vh', alignItems:'center', justifyContent:'center', background:'#fff'}>
      <div style={width:360, padding:20, border:'1px solid #ddd', borderRadius:8, background:'#fff'}>
        <div style={textAlign:'center'}>
          <img src='/public/logo.svg' alt='logo' style={height:80, marginBottom:12} />
          <h2 style={margin:0}>Welcome to FAT-EIBL</h2>
        </div>
        <form onSubmit={submit} style={marginTop:12}>
          <input placeholder='Email' value={email} onChange={e=>setEmail(e.target.value)} style={width:'100%', padding:8, marginBottom:8} />
          <input placeholder='Password' type='password' value={password} onChange={e=>setPassword(e.target.value)} style={width:'100%', padding:8, marginBottom:8} />
          <button type='submit' style={width:'100%', padding:10, background:'#FCFAFC', color:'#fff', border:'none', borderRadius:4}>Sign in</button>
        </form>
      </div>
    </div>
  )
}
