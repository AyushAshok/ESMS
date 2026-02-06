import React, { useState, useEffect } from 'react'
import api from '../api'

export default function Skills(){
  const [skills, setSkills] = useState([])
  const [error, setError] = useState(null)

  useEffect(()=>{
    let mounted = true
    async function load(){
      try{
        const resp = await api.get('/skills')
        if(mounted) setSkills(resp.data)
      }catch(err){
        setError(err.response?.data?.detail || 'Failed to load skills')
      }
    }
    load()
    return ()=>{ mounted = false }
  }, [])

  return (
    <div>
      <h2>Skills</h2>
      {error && <div style={{color:'red'}}>{error}</div>}
      <ul>
        {skills.map(s=> (
          <li key={s.id}>{s.id} — {s.name} — {s.category}</li>
        ))}
      </ul>
    </div>
  )
}
