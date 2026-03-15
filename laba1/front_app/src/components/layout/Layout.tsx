import { lazy, Suspense } from 'react'
import { NavLink, Navigate, Route, Routes } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext'
import { ProtectedRoute } from '../auth/ProtectedRoute'

const Login = lazy(() => import('../../pages/Login').then((m) => ({ default: m.Login })))
const Register = lazy(() => import('../../pages/Register').then((m) => ({ default: m.Register })))
const Items = lazy(() => import('../../pages/Items').then((m) => ({ default: m.Items })))

export function Layout() {
  const { user, logout } = useAuth()
  return (
    <>
      <header className="header">
        <span className="logo">Трёхзвенная архитектура</span>
        <nav>
          <NavLink to="/" end className={({ isActive }) => (isActive ? 'nav-link active' : 'nav-link')}>
            Сущности
          </NavLink>
          {user ? (
            <>
              <span className="user" title={`${user.username}, ${user.role}`}>({user.username}, {user.role})</span>
              <button type="button" className="btn small" onClick={logout}>
                Выйти
              </button>
            </>
          ) : (
            <>
              <NavLink to="/login" className={({ isActive }) => (isActive ? 'nav-link active' : 'nav-link')}>
                Вход
              </NavLink>
              <NavLink to="/register" className={({ isActive }) => (isActive ? 'nav-link active' : 'nav-link')}>
                Регистрация
              </NavLink>
            </>
          )}
        </nav>
      </header>
      <main className="main">
        <Suspense fallback={<div className="page">Загрузка...</div>}>
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route
              path="/"
              element={
                <ProtectedRoute>
                  <Items />
                </ProtectedRoute>
              }
            />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </Suspense>
      </main>
    </>
  )
}
