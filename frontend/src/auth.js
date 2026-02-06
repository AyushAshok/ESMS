// small helper to decode JWT payload without verification (for client-side UI decisions)
export function decodeToken(token){
  if(!token) return null
  try{
    const parts = token.split('.')
    if(parts.length < 2) return null
    const payload = parts[1]
    const json = atob(payload.replace(/-/g,'+').replace(/_/g,'/'))
    return JSON.parse(json)
  }catch(e){
    return null
  }
}

export function getCurrentUser(){
  try{
    const token = localStorage.getItem('esms_token')
    if(!token) return null
    return decodeToken(token)
  }catch(e){
    return null
  }
}
