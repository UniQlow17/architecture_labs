import type { Role } from '../types'

/** Роли, доступные при регистрации */
export const ROLES: Role[] = ['viewer', 'moderator', 'admin']

/** Роли с правом редактирования сущностей */
export const CAN_EDIT: Role[] = ['moderator', 'admin']

/** Роли с правом удаления сущностей */
export const CAN_DELETE: Role[] = ['admin']
