import React, { useState } from 'react'
import api, { setAuthToken } from '../api'
import { useNavigate } from 'react-router-dom'

export default function Login(){
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState(null)
  const navigate = useNavigate()

  async function handleSubmit(e){
    e.preventDefault()
    try{
      const params = new URLSearchParams()
      params.append('username', email)
      params.append('password', password)
      const resp = await api.post('/auth/login', params, { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } })
      const { access_token } = resp.data
      localStorage.setItem('esms_token', access_token)
      setAuthToken(access_token)
      navigate('/')
    }catch(err){
      setError(err.response?.data?.detail || 'Login failed')
    }
  }

  return (
    <div className="card max-w-md mx-auto">
      <h2 className="text-xl font-bold mb-4">Login</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium">Email</label>
          <input className="mt-1 block w-full border rounded p-2" value={email} onChange={e=>setEmail(e.target.value)} />
        </div>
        <div>
          <label className="block text-sm font-medium">Password</label>
          <input className="mt-1 block w-full border rounded p-2" type="password" value={password} onChange={e=>setPassword(e.target.value)} />
        </div>
        <div>
          <button className="bg-blue-600 text-white px-4 py-2 rounded" type="submit">Login</button>
        </div>
        {error && <div className="text-red-600">{error}</div>}
      </form>
    </div>
  )
}
