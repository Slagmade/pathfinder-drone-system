'use client'
import { useEffect, useState } from 'react'

interface Victim {
  id: number
  lat: number
  lon: number
  timestamp: string
}

export default function Home() {
  const [data, setData] = useState<any>(null)
  const [victims, setVictims] = useState<Victim[]>([])
  const [alertMessage, setAlertMessage] = useState('')
  const [newVictim, setNewVictim] = useState({ lat: '', lon: '' })

  // Fetch data
  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await fetch('http://localhost:5000/api/data')
        setData(await res.json())
        
        const victimsRes = await fetch('http://localhost:5000/api/victims')
        setVictims(await victimsRes.json())
      } catch (err) {}
    }
    
    fetchData()
    const interval = setInterval(fetchData, 1000)
    return () => clearInterval(interval)
  }, [])

  // Handlers
  const handleAddVictim = async () => {
    await fetch('http://localhost:5000/api/victims', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        lat: parseFloat(newVictim.lat),
        lon: parseFloat(newVictim.lon)
      })
    })
    setNewVictim({ lat: '', lon: '' })
  }

  const handleBroadcastAlert = async () => {
    await fetch('http://localhost:5000/api/alert', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: alertMessage })
    })
    setAlertMessage('')
  }

  return (
    <main className="p-8">
      <h1 className="text-3xl font-bold mb-6">Disaster Response System</h1>

      {/* Victim Input */}
      <div className="bg-gray-100 p-4 rounded-lg mb-4">
        <h2 className="text-xl font-semibold mb-2">Simulate Victim Detection</h2>
        <div className="grid grid-cols-2 gap-2 mb-2">
          <input
            type="number"
            placeholder="Latitude"
            className="p-2 border rounded"
            value={newVictim.lat}
            onChange={(e) => setNewVictim({...newVictim, lat: e.target.value})}
            step="0.000001"
          />
          <input
            type="number"
            placeholder="Longitude"
            className="p-2 border rounded"
            value={newVictim.lon}
            onChange={(e) => setNewVictim({...newVictim, lon: e.target.value})}
            step="0.000001"
          />
        </div>
        <button
          onClick={handleAddVictim}
          className="w-full bg-red-500 text-white py-2 rounded hover:bg-red-600"
        >
          Mark Victim Location
        </button>
      </div>

      {/* Public Address */}
      <div className="bg-gray-100 p-4 rounded-lg mb-4">
        <h2 className="text-xl font-semibold mb-2">Public Address System</h2>
        <div className="flex gap-2">
          <input
            type="text"
            placeholder="Emergency message"
            className="flex-1 p-2 border rounded"
            value={alertMessage}
            onChange={(e) => setAlertMessage(e.target.value)}
          />
          <button
            onClick={handleBroadcastAlert}
            className="bg-orange-500 text-white py-2 px-4 rounded hover:bg-orange-600"
          >
            Broadcast
          </button>
        </div>
      </div>

      {/* Victim List */}
      <div className="bg-gray-100 p-4 rounded-lg">
        <h2 className="text-xl font-semibold mb-2">Detected Victims</h2>
        {victims.map(victim => (
          <div key={victim.id} className="mb-2 p-2 bg-white rounded">
            <p>Victim {victim.id}: {victim.lat.toFixed(6)}, {victim.lon.toFixed(6)}</p>
            <button
              onClick={async () => {
                await fetch('http://localhost:5000/api/relay', {
                  method: 'POST',
                  headers: { 'Content-Type': 'application/json' },
                  body: JSON.stringify({ victim_id: victim.id })
                })
              }}
              className="mt-1 bg-green-500 text-white px-2 py-1 rounded text-sm hover:bg-green-600"
            >
              Send to Rescue Team
            </button>
          </div>
        ))}
      </div>
    </main>
  )
}

