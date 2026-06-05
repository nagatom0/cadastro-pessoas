import {formatApiError} from "../helpers/errorHelper"

const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000"

export interface PersonPayload {
  fullName: string
  cpf: string
  email: string
  birthday: string
  cep: string
  address: string
}

export interface PersonResponse {
  id: string
  fullName: string
  email: string
  login: string
}

export interface CepResponse {
  city?: string
  state?: string
  neighborhood?: string
  address?: string
}


export async function createPerson(payload: PersonPayload): Promise<PersonResponse> {
  const res = await fetch(`${API_URL}/person`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  })

  if (!res.ok) {
    const data = await res.json().catch(() => ({}))
    const errorMsg = formatApiError(data.detail) || `Erro ${res.status} ao cadastrar`;
    throw new Error(errorMsg)
  }

  return res.json()
}

export async function fetchAddressByCep(cep: string): Promise<CepResponse> {
  const res = await fetch(`${API_URL}/cep/${cep}`)
  if (!res.ok) throw new Error(`Erro ${res.status} ao consultar CEP`)
  return res.json()
}