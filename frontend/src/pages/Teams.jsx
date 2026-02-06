import React, { useState } from 'react'
import api from '../api'

export default function Teams(){
  const [id, setId] = useState('')
  const [team, setTeam] = useState(null)
  const [error, setError] = useState(null)

  async function fetchTeam(e){
    e.preventDefault()
    setError(null)
    setTeam(null)
    try{
      const resp = await api.get(`/teams/${id}`)
      setTeam(resp.data)
    }catch(err){
      setError(err.response?.data?.detail || 'Failed to fetch')
    }
  }

  return (
    <div>
      <h2>Teams</h2>
      <form onSubmit={fetchTeam}>
        <label>Team ID: <input value={id} onChange={e=>setId(e.target.value)} /></label>
        <button type="submit">Fetch</button>
      </form>
      {error && <div style={{color:'red'}}>{error}</div>}
      {team && (
        <pre>{JSON.stringify(team, null, 2)}</pre>
      )}
    </div>
  )
}
