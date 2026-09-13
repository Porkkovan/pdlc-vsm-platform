import { Component } from 'react'

export default class ErrorBoundary extends Component {
  constructor(props) {
    super(props)
    this.state = { error: null }
  }

  static getDerivedStateFromError(error) {
    return { error }
  }

  render() {
    if (this.state.error) {
      return (
        <div className="min-h-screen flex items-center justify-center bg-gray-50 p-8">
          <div className="max-w-lg w-full bg-white rounded-2xl shadow-lg border border-sky-200 p-8 text-center">
            <div className="text-5xl mb-4">⚠️</div>
            <h2 className="text-xl font-bold text-gray-800 mb-2">Something went wrong</h2>
            <p className="text-sm text-gray-500 mb-4">An unexpected error occurred on this page.</p>
            <pre className="text-left bg-sky-50 border border-sky-200 rounded-lg p-3 text-xs text-sky-700 mb-6 overflow-auto max-h-32">
              {this.state.error?.message}
            </pre>
            <button
              onClick={() => { this.setState({ error: null }); window.location.href = '/dashboard' }}
              className="bg-blue-600 text-white px-6 py-2.5 rounded-lg font-semibold text-sm hover:bg-blue-700">
              ← Back to Dashboard
            </button>
          </div>
        </div>
      )
    }
    return this.props.children
  }
}
