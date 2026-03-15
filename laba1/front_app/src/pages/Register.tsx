import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { getErrorMessage } from '../api/client'
import { register as apiRegister } from '../api/auth'
import { ROLES } from '../constants/roles'
import type { Role } from '../types'

export function Register() {
  const [username, setUsername] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [role, setRole] = useState<Role>('viewer')
  const [error, setError] = useState('')
  const { login } = useAuth()
  const navigate = useNavigate()

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setError('')
    try {
      await apiRegister({ username, email, password, role })
      await login(username, password)
      navigate('/')
    } catch (err) {
      setError(getErrorMessage(err, 'Ошибка регистрации'))
    }
  }

  return (
    <div className="page auth-page">
      <h1>Регистрация</h1>
      <form onSubmit={handleSubmit} className="card form">
        {error && <p className="error">{error}</p>}
        <label>
          Имя пользователя
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            minLength={2}
            maxLength={64}
            required
            autoComplete="username"
          />
        </label>
        <label>
          Email
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            autoComplete="email"
          />
        </label>
        <label>
          Пароль
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            minLength={6}
            required
            autoComplete="new-password"
          />
        </label>
        <label>
          Роль
          <select value={role} onChange={(e) => setRole(e.target.value as Role)}>
            {ROLES.map((r) => (
              <option key={r} value={r}>
                {r}
              </option>
            ))}
          </select>
        </label>
        <button type="submit">Зарегистрироваться</button>
        <p className="hint">
          Уже есть аккаунт? <Link to="/login">Вход</Link>
        </p>
      </form>
    </div>
  )
}
