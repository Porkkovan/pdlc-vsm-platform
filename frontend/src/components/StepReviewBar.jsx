import { useState, useEffect } from 'react'
import { useApp } from '../contexts/AppContext'
import { stepReviewsApi } from '../services/api'

const STATUS_CONFIG = {
  draft:    { label: 'Draft',    bg: 'bg-gray-100',   text: 'text-gray-600',   border: 'border-gray-300',   icon: '📝' },
  reviewed: { label: 'Reviewed', bg: 'bg-blue-50',    text: 'text-blue-700',   border: 'border-blue-300',   icon: '👁️' },
  approved: { label: 'Approved', bg: 'bg-green-50',   text: 'text-green-700',  border: 'border-green-300',  icon: '✅' },
  rejected: { label: 'Rejected', bg: 'bg-red-50',     text: 'text-red-700',    border: 'border-red-300',    icon: '❌' },
}

export default function StepReviewBar({ stepKey, stepLabel, onEditContent, editedContent }) {
  const { project, addNotification } = useApp()
  const [review, setReview] = useState(null)
  const [loading, setLoading] = useState(false)
  const [showNotes, setShowNotes] = useState(false)
  const [notes, setNotes] = useState('')
  const [reviewer, setReviewer] = useState('')

  useEffect(() => {
    if (!project?.id || !stepKey) return
    stepReviewsApi.getReview(project.id, stepKey)
      .then(r => {
        setReview(r)
        setNotes(r.reviewer_notes || '')
        setReviewer(r.reviewed_by || '')
      })
      .catch(() => {})
  }, [project?.id, stepKey])

  const save = async (status) => {
    if (!project?.id) return
    setLoading(true)
    try {
      const body = {
        status,
        reviewer_notes: notes || null,
        edited_content: editedContent || null,
        reviewed_by: reviewer || null,
      }
      const r = await stepReviewsApi.upsertReview(project.id, stepKey, body)
      setReview(r)
      addNotification(`${stepLabel || stepKey} marked as ${status}`, 'success')
      setShowNotes(false)
    } catch (e) {
      addNotification(`Failed to save review: ${e.message}`, 'error')
    } finally {
      setLoading(false)
    }
  }

  const currentStatus = review?.status || 'draft'
  const cfg = STATUS_CONFIG[currentStatus] || STATUS_CONFIG.draft

  return (
    <div className={`border rounded-xl ${cfg.border} ${cfg.bg} px-4 py-3`}>
      <div className="flex items-center justify-between gap-3 flex-wrap">
        {/* Status badge */}
        <div className="flex items-center gap-2">
          <span className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold border ${cfg.border} ${cfg.bg} ${cfg.text}`}>
            {cfg.icon} {cfg.label}
          </span>
          <span className="text-xs text-gray-500">
            {stepLabel || stepKey}
            {review?.reviewed_at && (
              <> · reviewed {new Date(review.reviewed_at).toLocaleDateString()}</>
            )}
            {review?.reviewed_by && (
              <> by <b>{review.reviewed_by}</b></>
            )}
          </span>
        </div>

        {/* Action buttons */}
        <div className="flex items-center gap-2">
          {onEditContent && (
            <button
              onClick={onEditContent}
              className="px-3 py-1.5 text-xs font-semibold rounded-lg bg-white border border-gray-300 text-gray-700 hover:bg-gray-50 transition-colors"
            >
              ✏️ Edit
            </button>
          )}
          <button
            onClick={() => setShowNotes(v => !v)}
            className="px-3 py-1.5 text-xs font-semibold rounded-lg bg-white border border-gray-300 text-gray-700 hover:bg-gray-50 transition-colors"
          >
            💬 Notes
          </button>
          <button
            onClick={() => save('reviewed')}
            disabled={loading}
            className="px-3 py-1.5 text-xs font-semibold rounded-lg bg-blue-500 text-white hover:bg-blue-600 transition-colors disabled:opacity-50"
          >
            👁️ Mark Reviewed
          </button>
          <button
            onClick={() => save('approved')}
            disabled={loading}
            className="px-3 py-1.5 text-xs font-semibold rounded-lg bg-green-500 text-white hover:bg-green-600 transition-colors disabled:opacity-50"
          >
            ✅ Approve
          </button>
          <button
            onClick={() => { setShowNotes(true) }}
            disabled={loading}
            className="px-3 py-1.5 text-xs font-semibold rounded-lg bg-white border border-red-300 text-red-600 hover:bg-red-50 transition-colors disabled:opacity-50"
          >
            ❌ Reject
          </button>
        </div>
      </div>

      {/* Notes panel */}
      {showNotes && (
        <div className="mt-3 pt-3 border-t border-gray-200 space-y-2">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-2">
            <div className="md:col-span-3">
              <label className="block text-xs font-semibold text-gray-600 mb-1">Review Notes / Feedback</label>
              <textarea
                value={notes}
                onChange={e => setNotes(e.target.value)}
                placeholder="Enter your review notes, feedback, or reasons for rejection..."
                rows={2}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-gray-600 mb-1">Reviewer Name</label>
              <input
                type="text"
                value={reviewer}
                onChange={e => setReviewer(e.target.value)}
                placeholder="Your name"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <div className="flex gap-2 mt-2">
                <button
                  onClick={() => save('rejected')}
                  disabled={loading}
                  className="flex-1 px-3 py-1.5 text-xs font-semibold rounded-lg bg-red-500 text-white hover:bg-red-600 transition-colors disabled:opacity-50"
                >
                  Reject with Notes
                </button>
              </div>
            </div>
          </div>
          {review?.reviewer_notes && currentStatus !== 'draft' && (
            <div className="bg-white rounded-lg border border-gray-200 p-3 text-xs text-gray-700">
              <span className="font-bold text-gray-500">Previous notes: </span>{review.reviewer_notes}
            </div>
          )}
        </div>
      )}
    </div>
  )
}
