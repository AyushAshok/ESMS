import React, { useState, useEffect } from 'react'
import api from '../api'

export default function Employees(){
  const [employees, setEmployees] = useState([])
  const [error, setError] = useState(null)

  useEffect(()=>{
    let mounted = true
    async function load(){
      try{
        const resp = await api.get('/employees')
        if(mounted) setEmployees(resp.data)
      }catch(err){
        setError(err.response?.data?.detail || 'Failed to load employees')
      }
    }
    load()
    return ()=>{ mounted = false }
  }, [])

  return (
    <div>
      <h2>Employees</h2>
      {error && <div style={{color:'red'}}>{error}</div>}
      <ul>
        {employees.map(emp=> (
          <li key={emp.id}><a href={`#/employees/${emp.id}`}>{emp.id} — {emp.name} — {emp.email}</a></li>
        ))}
      </ul>
    </div>
  )
}
