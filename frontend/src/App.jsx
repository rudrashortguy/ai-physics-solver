import React, { useState, useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import axios from 'axios'

function LatexBlock({ formula }) {
  try {
    const Latex = React.lazy(() => import('react-latex'))
    return <React.Suspense fallback={<span className="italic">{formula}</span>}>
      <Latex>{formula}</Latex>
    </React.Suspense>
  } catch {
    return <span className="font-mono text-blue-700">{formula}</span>
  }
}

function SolutionDisplay({ data, error }) {
  if (error) return <div className="bg-red-50 p-4 rounded-lg text-red-700">{error}</div>
  if (!data) return null

  return <div className="space-y-6 mt-6">
    <div className="flex gap-2 flex-wrap">
      <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-medium">{data.topic}</span>
    </div>

    {data.formula_used && <div className="bg-white p-4 rounded-lg shadow">
      <h3 className="font-semibold text-gray-700 mb-2">Formula</h3>
      <LatexBlock formula={data.formula_used} />
    </div>}

    {data.variables?.length > 0 && <div className="bg-white p-4 rounded-lg shadow">
      <h3 className="font-semibold text-gray-700 mb-2">Variables</h3>
      <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
        {data.variables.map((v, i) => (
          <div key={i} className="bg-gray-50 p-2 rounded text-sm">
            <span className="font-mono">{v.name}</span> = {v.value} <span className="text-gray-500">{v.unit}</span>
          </div>
        ))}
      </div>
    </div>}

    {data.step_by_step_solution?.length > 0 && <div className="bg-white p-4 rounded-lg shadow">
      <h3 className="font-semibold text-gray-700 mb-2">Solution</h3>
      <ol className="list-decimal list-inside space-y-1">
        {data.step_by_step_solution.map((s, i) => (
          <li key={i} className="text-gray-600"><LatexBlock formula={s} /></li>
        ))}
      </ol>
    </div>}

    {data.common_ib_mistakes?.length > 0 && <div className="bg-yellow-50 p-4 rounded-lg shadow border border-yellow-200">
      <h3 className="font-semibold text-yellow-800 mb-2">Common IB Mistakes</h3>
      <ul className="list-disc list-inside space-y-1 text-yellow-700">
        {data.common_ib_mistakes.map((m, i) => <li key={i}>{m}</li>)}
      </ul>
    </div>}

    {data.graph_base64 && <div className="bg-white p-4 rounded-lg shadow">
      <h3 className="font-semibold text-gray-700 mb-2">Graph</h3>
      <img src={`data:image/png;base64,${data.graph_base64}`} alt="Graph" className="max-w-full" />
    </div>}

    {data.practice_questions?.length > 0 && <div className="bg-white p-4 rounded-lg shadow">
      <h3 className="font-semibold text-gray-700 mb-2">Practice Questions</h3>
      <ol className="list-decimal list-inside space-y-1">
        {data.practice_questions.map((q, i) => (
          <li key={i} className="text-gray-600">{q}</li>
        ))}
      </ol>
    </div>}
  </div>
}

export default function App() {
  const [file, setFile] = useState(null)
  const [preview, setPreview] = useState(null)
  const [loading, setLoading] = useState(false)
  const [data, setData] = useState(null)
  const [error, setError] = useState(null)
  const [tab, setTab] = useState('solution')

  const onDrop = useCallback(accepted => {
    const f = accepted[0]
    setFile(f)
    setPreview(URL.createObjectURL(f))
    setData(null)
    setError(null)
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'image/png': ['.png'], 'image/jpeg': ['.jpg', '.jpeg'] },
    maxFiles: 1,
  })

  const handleSolve = async () => {
    if (!file) return
    setLoading(true)
    setError(null)
    const form = new FormData()
    form.append('file', file)
    try {
      const res = await axios.post('http://localhost:8000/solve', form)
      setData(res.data)
    } catch (e) {
      setError(e.response?.data?.detail || e.message)
    }
    setLoading(false)
  }

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-3xl font-bold text-center text-gray-800 mb-8">AI Physics Solver</h1>

      <div {...getRootProps()} className={`border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-colors ${isDragActive ? 'border-blue-400 bg-blue-50' : 'border-gray-300 hover:border-blue-300'}`}>
        <input {...getInputProps()} />
        {preview ? <img src={preview} alt="Preview" className="max-h-64 mx-auto rounded" />
          : <p className="text-gray-500">{isDragActive ? 'Drop image here' : 'Drop an IB Physics problem image, or click to browse'}</p>}
      </div>

      <button onClick={handleSolve} disabled={!file || loading}
        className="mt-4 w-full py-3 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors">
        {loading ? 'Solving...' : 'Solve'}
      </button>

      <SolutionDisplay data={data} error={error} />
    </div>
  )
}
