import React, { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import api from '../api'
import { getCurrentUser } from '../auth'
import RatingEditor from '../components/RatingEditor'

export default function EmployeeDetail(){
  const { id } = useParams()
  const [overview, setOverview] = useState([])
  const [error, setError] = useState(null)
  const [skillId, setSkillId] = useState('')
  const [assignMsg, setAssignMsg] = useState(null)
  
  const currentUser = getCurrentUser()

  useEffect(()=>{
    let mounted = true
    async function load(){
      try{
        const resp = await api.get(`/employees/${id}/skills`)
        if(mounted) setOverview(resp.data)
      }catch(err){
        setError(err.response?.data?.detail || 'Failed to load overview')
      }
    }
    load()
    return ()=>{ mounted = false }
  }, [id])

  async function handleAssign(e){
    e.preventDefault()
    setAssignMsg(null)
    try{
      const payload = { skill_id: Number(skillId) }
      await api.post(`/employees/${id}/assign-skill`, payload)
      setAssignMsg('Assigned — refresh to see changes')
    }catch(err){
      setAssignMsg(err.response?.data?.detail || 'Assign failed')
    }
  }

  async function handleUpdateRating(ratingId, data){
    try{
      await api.patch(`/skill-ratings/${ratingId}`, data)
      setAssignMsg('Updated — refresh to see changes')
    }catch(err){
      setAssignMsg(err.response?.data?.detail || 'Update failed')
    }
  }

  return (
    <div>
      <h2>Employee {id} — Skill Overview</h2>
      {error && <div style={{color:'red'}}>{error}</div>}
      <ul className="space-y-3">
        {overview.map(item=> (
          <li key={item.skill_id} className="card">
            <div className="flex justify-between items-start">
              <div>
                <div className="font-semibold">{item.skill_name} (#{item.skill_id})</div>
                <div className="text-sm text-gray-600">assigned: {String(item.assigned)} — expected: {item.expected_rating}</div>
              </div>
              <div className="space-y-2">
                {item.assigned && item.rating_id && (
                  <div>
                    <div className="text-sm">Manager rating: {String(item.manager_rating)}</div>
                    <div className="text-sm">Self rating: {String(item.self_rating)}</div>
                  </div>
                )}
              </div>
            </div>
            <div className="mt-3 flex gap-2">
              {item.assigned && item.rating_id && currentUser && (currentUser.employee_id === Number(id) || currentUser.is_manager) && (
                <RatingEditor item={item} onSave={handleUpdateRating} isManager={currentUser.is_manager} isSelf={currentUser.employee_id === Number(id)} />
              )}
            </div>
          </li>
        ))}
      </ul>

      <h3>Assign skill (manager only)</h3>
      <form onSubmit={handleAssign}>
        <label>Skill ID: <input value={skillId} onChange={e=>setSkillId(e.target.value)} /></label>
        <button type="submit">Assign</button>
      </form>
      {assignMsg && <div>{assignMsg}</div>}
    </div>
  )
}
