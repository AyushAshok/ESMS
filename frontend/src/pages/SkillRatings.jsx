import React, { useState, useEffect } from 'react'
import api from '../api'

export default function SkillRatings(){
  const [ratings, setRatings] = useState([])
  const [error, setError] = useState(null)

  useEffect(()=>{
    let mounted = true
    async function load(){
      try{
        const resp = await api.get('/skill-ratings')
        if(mounted) setRatings(resp.data)
      }catch(err){
        setError(err.response?.data?.detail || 'Failed to load ratings')
      }
    }
    load()
    return ()=>{ mounted = false }
  }, [])

  return (
    <div>
      <h2>Skill Ratings</h2>
      {error && <div style={{color:'red'}}>{error}</div>}
      <ul>
        {ratings.map(r=> (
          <li key={r.id}>{r.id} — emp:{r.emp_id} skill:{r.skill_id} manager_rating:{r.manager_rating} self_rating:{r.self_rating}</li>
        ))}
      </ul>
    </div>
  )
}
