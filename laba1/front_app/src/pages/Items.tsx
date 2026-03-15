import { useCallback, useEffect, useState } from 'react'
import { useAuth } from '../context/AuthContext'
import { getErrorMessage } from '../api/client'
import {
  createItem,
  deleteItem,
  getItems,
  updateItem,
} from '../api/items'
import { CAN_DELETE, CAN_EDIT } from '../constants/roles'
import type { Item } from '../types'

export function Items() {
  const { user } = useAuth()
  const [items, setItems] = useState<Item[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [editingId, setEditingId] = useState<number | null>(null)
  const [creating, setCreating] = useState(false)
  const [formTitle, setFormTitle] = useState('')
  const [formDesc, setFormDesc] = useState('')

  const load = useCallback(async () => {
    setError('')
    try {
      const list = await getItems()
      setItems(list)
    } catch (err) {
      setError(getErrorMessage(err, 'Ошибка загрузки'))
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    load()
  }, [load])

  const canEdit = user && CAN_EDIT.includes(user.role)
  const canDelete = user && CAN_DELETE.includes(user.role)

  async function handleCreate(e: React.FormEvent) {
    e.preventDefault()
    setError('')
    try {
      const created = await createItem({ title: formTitle, description: formDesc || null })
      setItems((prev) => [...prev, created])
      setFormTitle('')
      setFormDesc('')
      setCreating(false)
    } catch (err) {
      setError(getErrorMessage(err, 'Ошибка создания'))
    }
  }

  async function handleUpdate(id: number, e: React.FormEvent) {
    e.preventDefault()
    setError('')
    try {
      await updateItem(id, { title: formTitle, description: formDesc || null })
      setEditingId(null)
      setFormTitle('')
      setFormDesc('')
      await load()
    } catch (err) {
      setError(getErrorMessage(err, 'Ошибка обновления'))
    }
  }

  async function handleDelete(id: number) {
    if (!confirm('Удалить?')) return
    setError('')
    try {
      await deleteItem(id)
      await load()
    } catch (err) {
      setError(getErrorMessage(err, 'Ошибка удаления'))
    }
  }

  function startEdit(item: Item) {
    setEditingId(item.id)
    setFormTitle(item.title)
    setFormDesc(item.description ?? '')
  }

  function startCreate() {
    setCreating(true)
    setFormTitle('')
    setFormDesc('')
  }

  if (loading) return <div className="page">Загрузка...</div>

  return (
    <div className="page">
      <div className="page-header">
        <h1>Сущности</h1>
        {canEdit && (
          <button type="button" className="btn primary" onClick={startCreate}>
            Создать
          </button>
        )}
      </div>
      {error && <p className="error">{error}</p>}

      {creating && (
        <form onSubmit={handleCreate} className="card form inline-form">
          <input
            value={formTitle}
            onChange={(e) => setFormTitle(e.target.value)}
            placeholder="Название"
            maxLength={256}
            required
          />
          <input
            value={formDesc}
            onChange={(e) => setFormDesc(e.target.value)}
            placeholder="Описание"
            maxLength={1024}
          />
          <button type="submit">Сохранить</button>
          <button type="button" onClick={() => setCreating(false)}>
            Отмена
          </button>
        </form>
      )}

      <ul className="items-list">
        {items.map((item) => (
          <li key={item.id} className="card item-card">
            {editingId === item.id ? (
              <form
                onSubmit={(e) => handleUpdate(item.id, e)}
                className="inline-form"
              >
                <input
                  value={formTitle}
                  onChange={(e) => setFormTitle(e.target.value)}
                  placeholder="Название"
                  maxLength={256}
                  required
                />
                <input
                  value={formDesc}
                  onChange={(e) => setFormDesc(e.target.value)}
                  placeholder="Описание"
                  maxLength={1024}
                />
                <button type="submit">Сохранить</button>
                <button
                  type="button"
                  onClick={() => {
                    setEditingId(null)
                    setFormTitle('')
                    setFormDesc('')
                  }}
                >
                  Отмена
                </button>
              </form>
            ) : (
              <>
                <div className="item-card__content">
                  <div className="item-title">{item.title}</div>
                  {item.description && (
                    <p className="description">{item.description}</p>
                  )}
                </div>
                <div className="item-actions">
                  {canEdit && (
                    <button
                      type="button"
                      className="btn small"
                      onClick={() => startEdit(item)}
                    >
                      Изменить
                    </button>
                  )}
                  {canDelete && (
                    <button
                      type="button"
                      className="btn small danger"
                      onClick={() => handleDelete(item.id)}
                    >
                      Удалить
                    </button>
                  )}
                </div>
              </>
            )}
          </li>
        ))}
      </ul>
      {items.length === 0 && !creating && (
        <p className="muted">Нет сущностей. {canEdit && 'Нажмите «Создать».'}</p>
      )}
    </div>
  )
}
