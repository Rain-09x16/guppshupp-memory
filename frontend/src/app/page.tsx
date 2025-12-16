'use client'

import { useState } from 'react'

interface ExtractedMemories {
  preferences: string[]
  facts: string[]
  emotional_patterns: string[]
}

export default function Home() {
  const [messagesInput, setMessagesInput] = useState('')
  const [extractedMemories, setExtractedMemories] = useState<ExtractedMemories | null>(null)
  const [userMessage, setUserMessage] = useState('')
  const [personalities, setPersonalities] = useState({
    calm_mentor: '',
    witty_friend: '',
    therapist: ''
  })
  const [loading, setLoading] = useState(false)

  const loadSampleMessages = () => {
    const sampleMessages = `user: I hate waking up early, I'm not a morning person
assistant: That's totally understandable
user: My dog Luna is so annoying sometimes lol
assistant: Dogs can be a handful
user: I work in cybersecurity, lots of stress lately
assistant: That sounds challenging
user: Yeah, especially on Mondays
assistant: Mondays can be tough
user: I love pizza though, that's my go-to comfort food
assistant: Pizza is always a good choice`

    setMessagesInput(sampleMessages)
  }

  const extractMemories = async () => {
    setLoading(true)
    try {
      const lines = messagesInput.trim().split('\n')
      const messages = lines.map(line => {
        const [role, ...contentParts] = line.split(':')
        return {
          role: role.trim(),
          content: contentParts.join(':').trim()
        }
      })
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/extract_memory`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ messages })
      })

      const data = await response.json()

      if (!response.ok) {
        alert(data.detail || 'Failed to extract memories')
        setLoading(false)
        return
      }

      setExtractedMemories(data)
    } catch (error) {
      console.error('Error:', error)
      alert('Failed to extract memories')
    }
    setLoading(false)
  }

  const sleep = (ms: number) => new Promise(r => setTimeout(r, ms));

  const generateResponses = async () => {
    if (!extractedMemories) {
      alert('Please extract memories first!')
      return
    }

    setLoading(true)
    try {
      const types = ['calm_mentor', 'witty_friend', 'therapist']
      // Initialize with empty strings to clear old results
      let newPersonalities = { ...personalities, calm_mentor: '', witty_friend: '', therapist: '' }
      setPersonalities(newPersonalities)

      for (const type of types) {
        try {
          const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/transform_personality`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              user_message: userMessage,
              personality_type: type,
              memories: extractedMemories
            })
          })

          if (response.ok) {
            const data = await response.json()
            // Update state incrementally so you see them pop in one by one
            newPersonalities = { ...newPersonalities, [type]: data.response }
            setPersonalities(newPersonalities)
          } else {
             console.error(`Failed to fetch ${type}`);
          }

          // CRITICAL: Wait 2 seconds before the next request to respect Rate Limits
          await sleep(4000); 
          
        } catch (err) {
          console.error(`Error fetching ${type}:`, err);
        }
      }

    } catch (error) {
      console.error('Error:', error)
      alert('Failed to generate responses')
    }
    setLoading(false)
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-4xl font-bold text-center mb-8 text-gray-800">
          GUPPSHUPP Memory AI
        </h1>

        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <h2 className="text-2xl font-semibold mb-4 text-gray-700">
            Step 1: Extract Memories
          </h2>

          <textarea
            value={messagesInput}
            onChange={(e) => setMessagesInput(e.target.value)}
            placeholder="Paste 30 chat messages here (format: role: message)..."
            className="w-full h-64 p-4 border rounded-lg mb-4 text-gray-900 bg-white"
            rows={10}
          />

          <div className="flex gap-3">
            <button
              onClick={loadSampleMessages}
              className="bg-gray-600 text-white px-6 py-2 rounded-lg hover:bg-gray-700"
            >
              Load Sample Messages
            </button>

            <button
              onClick={extractMemories}
              disabled={loading || !messagesInput}
              className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 disabled:bg-gray-400"
            >
              {loading ? 'Extracting...' : 'Extract Memories'}
            </button>
          </div>

          {extractedMemories && (
            <div className="mt-6 p-4 bg-gray-50 rounded-lg">
              <h3 className="text-xl font-semibold mb-3 text-gray-700">Extracted Memories:</h3>

              <div className="mb-4">
                <h4 className="font-semibold text-gray-600">Preferences:</h4>
                <ul className="list-disc list-inside text-gray-700">
                  {extractedMemories.preferences.map((pref: string, i: number) => (
                    <li key={i}>{pref}</li>
                  ))}
                </ul>
              </div>

              <div className="mb-4">
                <h4 className="font-semibold text-gray-600">Facts:</h4>
                <ul className="list-disc list-inside text-gray-700">
                  {extractedMemories.facts.map((fact: string, i: number) => (
                    <li key={i}>{fact}</li>
                  ))}
                </ul>
              </div>

              <div>
                <h4 className="font-semibold text-gray-600">Emotional Patterns:</h4>
                <ul className="list-disc list-inside text-gray-700">
                  {extractedMemories.emotional_patterns.map((pattern: string, i: number) => (
                    <li key={i}>{pattern}</li>
                  ))}
                </ul>
              </div>
            </div>
          )}
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-2xl font-semibold mb-4 text-gray-700">
            Step 2: Test Personality Responses
          </h2>

          <input
            type="text"
            value={userMessage}
            onChange={(e) => setUserMessage(e.target.value)}
            placeholder="Enter a message to see different personality responses..."
            className="w-full p-4 border rounded-lg mb-4 text-gray-900 bg-white"
          />

          <button
            onClick={generateResponses}
            disabled={loading || !userMessage || !extractedMemories}
            className="bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700 disabled:bg-gray-400"
          >
            {loading ? 'Generating...' : 'Generate Responses'}
          </button>

          {(personalities.calm_mentor || personalities.witty_friend || personalities.therapist) && (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
              <div className="bg-blue-50 p-4 rounded-lg">
                <h3 className="text-lg font-semibold mb-2 text-blue-800">Calm Mentor</h3>
                <p className="text-gray-700">{personalities.calm_mentor}</p>
              </div>

              <div className="bg-yellow-50 p-4 rounded-lg">
                <h3 className="text-lg font-semibold mb-2 text-yellow-800">Witty Friend</h3>
                <p className="text-gray-700">{personalities.witty_friend}</p>
              </div>

              <div className="bg-purple-50 p-4 rounded-lg">
                <h3 className="text-lg font-semibold mb-2 text-purple-800">Therapist</h3>
                <p className="text-gray-700">{personalities.therapist}</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}