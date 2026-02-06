import React, { useState } from 'react'

const OPTIONS = [0,1,2,3,4,5]

export default function RatingEditor({ item, onSave, isManager, isSelf }){
  const [mgr, setMgr] = useState(item.manager_rating ? Number(item.manager_rating) : '')
  const [self, setSelf] = useState(item.self_rating ? Number(item.self_rating) : '')
  const [note, setNote] = useState('')

  function save(){
    const payload = {}
    if(isManager && mgr !== '') payload.manager_rating = mgr
    if(isSelf && self !== '') payload.self_rating = self
    if(note) payload.comments = note
    onSave(item.rating_id, payload)
  }

  return (
    <div className="flex items-center gap-2">
      {isManager && (
        <select value={mgr} onChange={e=>setMgr(e.target.value)} className="border rounded p-1">
          <option value="">Mgr rate</option>
          {OPTIONS.map(o=> <option key={o} value={o}>{o}</option>)}
        </select>
      )}
      {isSelf && (
        <select value={self} onChange={e=>setSelf(e.target.value)} className="border rounded p-1">
          <option value="">Self rate</option>
          {OPTIONS.map(o=> <option key={o} value={o}>{o}</option>)}
        </select>
      )}
      <input placeholder="notes" value={note} onChange={e=>setNote(e.target.value)} className="border rounded p-1" />
      <button onClick={save} className="bg-green-600 text-white px-3 py-1 rounded">Save</button>
    </div>
  )
}
