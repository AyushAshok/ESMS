import React from 'react'
import { Routes, Route, Link, useNavigate } from 'react-router-dom'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import Employees from './pages/Employees'
import Skills from './pages/Skills'
import SkillRatings from './pages/SkillRatings'
import Teams from './pages/Teams'
import EmployeeDetail from './pages/EmployeeDetail'
import ProtectedRoute from './components/ProtectedRoute'
import { setAuthToken } from './api'

export default function App(){
  const navigate = useNavigate()

  function handleLogout(){
    localStorage.removeItem('esms_token')
    setAuthToken(null)
    navigate('/login')
  }

  const token = typeof window !== 'undefined' ? localStorage.getItem('esms_token') : null

  return (
    <div>
      <nav>
        <Link to="/">Dashboard</Link> | <Link to="/employees">Employees</Link> | <Link to="/teams">Teams</Link> | <Link to="/skills">Skills</Link> | <Link to="/ratings">Ratings</Link> | {token ? <a href="#" onClick={e=>{e.preventDefault();handleLogout()}}>Logout</a> : (<><Link to="/login">Login</Link> | <Link to="/register">Register</Link></>)}
      </nav>
      <Routes>
        <Route path="/" element={<ProtectedRoute><Dashboard/></ProtectedRoute>} />
        <Route path="/employees" element={<ProtectedRoute><Employees/></ProtectedRoute>} />
        <Route path="/employees/:id" element={<ProtectedRoute><EmployeeDetail/></ProtectedRoute>} />
        <Route path="/teams" element={<ProtectedRoute><Teams/></ProtectedRoute>} />
        <Route path="/skills" element={<ProtectedRoute><Skills/></ProtectedRoute>} />
        <Route path="/ratings" element={<ProtectedRoute><SkillRatings/></ProtectedRoute>} />
        <Route path="/login" element={<Login/>} />
        <Route path="/register" element={<Register/>} />
      </Routes>
    </div>
  )
}
