import React from 'react'
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'
import Home from './pages/Home'
import Login from './pages/Login'
import Chat from './pages/Chat'
export default function App(){
  return (
    <BrowserRouter>
      <nav style={{padding:12, borderBottom:'1px solid #eee'}}>
        <Link to='/' style={{marginRight:12}}>Home</Link>
        <Link to='/chat' style={{marginRight:12}}>Hey Vani</Link>
        <Link to='/login'>Login</Link>
      </nav>
      <Routes>
        <Route path='/' element={<Home/>} />
        <Route path='/login' element={<Login/>} />
        <Route path='/chat' element={<Chat/>} />
      </Routes>
    </BrowserRouter>
  )
}
