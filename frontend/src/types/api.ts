export interface ApiErrorPayload {
  code: string
  message: string
}

export interface ApiErrorResponse {
  error: ApiErrorPayload
}

export interface AuthUser {
  id: number
  email: string
  name: string
}

export interface AuthResponse {
  user: AuthUser
  access_token: string
  refresh_token: string
}

export interface RefreshResponse {
  access_token: string
}