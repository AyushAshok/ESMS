import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

export function setAuthToken(token){
  if(token){
    api.defaults.headers.common['Authorization'] = `Bearer ${token}`
  } else {
    delete api.defaults.headers.common['Authorization']
  }
}

// initialize token from localStorage if present
try{
  const token = localStorage.getItem('esms_token')
  if(token){
    setAuthToken(token)
  }
}catch(e){
  // ignore (server-side or unavailable localStorage)
}

export default api
