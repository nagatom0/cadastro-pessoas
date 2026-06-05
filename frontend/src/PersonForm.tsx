import { useState } from "react"
import { createPerson, fetchAddressByCep, type PersonResponse } from "./services/api"

type FormValues = {
    fullName: string
    cpf: string
    email: string
    birthday: string
    cep: string
    address: string
    number: number | string
    state: string
    city: string
    neighborhood: string
}

const initialValues: FormValues = {
    fullName: "",
    cpf: "",
    email: "",
    birthday: "",
    cep: "",
    address: "",
    number: "",
    state: "",
    city: "",
    neighborhood: "",
}

const onlyDigits = (v: string) => v.replace(/\D/g, "")

function validate(values: FormValues): Partial<Record<keyof FormValues, string>> {
    const errors: Partial<Record<keyof FormValues, string>> = {}

    if (!values.fullName.trim()) errors.fullName = "Informe o nome completo"
    if (onlyDigits(values.cpf).length !== 11) errors.cpf = "CPF deve ter 11 dígitos"
    if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(values.email)) errors.email = "E-mail inválido"
    if (!values.birthday) errors.birthday = "Informe a data de nascimento"
    if (onlyDigits(values.cep).length !== 8) errors.cep = "CEP deve ter 8 dígitos"
    if (!values.address.trim()) errors.address = "Informe o endereço"
    if (!values.number) errors.number = "Informe o número"
    if (!values.state.trim()) errors.state = "Informe o estado"
    if (!values.city.trim()) errors.city = "Informe a cidade"
    if (!values.neighborhood.trim()) errors.neighborhood = "Informe o bairro"

    return errors
}

export function PersonForm() {
    const [values, setValues] = useState<FormValues>(initialValues)
    const [errors, setErrors] = useState<Partial<Record<keyof FormValues, string>>>({})
    const [loading, setLoading] = useState(false)
    const [apiError, setApiError] = useState<string | null>(null)
    const [result, setResult] = useState<PersonResponse | null>(null)

    function handleChange(field: keyof FormValues, value: string) {
    setValues((prev) => ({ ...prev, [field]: value }))
    }

    async function handleCepBlur() {
        const cep = onlyDigits(values.cep)
        if (cep.length !== 8) return

        try {
            const data = await fetchAddressByCep(cep)
            const address = data.address
            const city = data.city
            const state = data.state
            const neighborhood = data.neighborhood

            if (address && city && state && neighborhood) {
                setValues((prev) => ({ ...prev, address, city, state, neighborhood }))
                setErrors((prev) => ({ ...prev, cep: undefined }))
            }
        } catch {
            setErrors((prev) => ({ ...prev, cep: "CEP não encontrado" }))
            setValues((prev) => ({
                ...prev,
                address: "",
                city: "",
                state: "",
                neighborhood: "",
            }))
        }
    }

    async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setApiError(null)

    const validationErrors = validate(values)
    setErrors(validationErrors)
    if (Object.keys(validationErrors).length > 0) return

    setLoading(true)
    try {
        const person = await createPerson({
        ...values,
        cpf: onlyDigits(values.cpf),
        cep: onlyDigits(values.cep),
        })
        setResult(person)
        setValues(initialValues)
    } catch (err) {
        setApiError(err instanceof Error ? err.message : "Erro inesperado")
    } finally {
        setLoading(false)
    }
    }

    const formatCpf = (value:string) => {
        const cpf = value.replace(/\D/g, "").slice(0, 11);

        return cpf
            .replace(/^(\d{3})(\d)/, "$1.$2")
            .replace(/^(\d{3})\.(\d{3})(\d)/, "$1.$2.$3")
            .replace(/^(\d{3})\.(\d{3})\.(\d{3})(\d)/, "$1.$2.$3-$4");
    };

    const formatCep = (value:string) => {
        const cep = value.replace(/\D/g, "").slice(0, 8);

        return cep.replace(/^(\d{5})(\d)/, "$1-$2");
    };


    if (result) {
    return (
        <div className="card">
        <h2>Cadastro realizado! 🎉</h2>
        <p>O login gerado foi:</p>
        <div className="login-badge">{result.login}</div>
        <button className="btn" onClick={() => setResult(null)}>
            Cadastrar outra pessoa
        </button>
        </div>
    )
    }

    return (
    <form className="card" onSubmit={handleSubmit} noValidate>
        <h2>Cadastro de pessoa</h2>

        <Field label="Nome completo" error={errors.fullName}>
        <input
            value={values.fullName}
            onChange={(e) => handleChange("fullName", e.target.value)}
            placeholder="Maria Silva Souza"
        />
        </Field>

        <Field label="CPF" error={errors.cpf}>
        <input
            value={values.cpf}
            onChange={(e) =>
                handleChange("cpf", formatCpf(e.target.value))
            }
            placeholder="000.000.000-00"
            maxLength={14}
        />
        </Field>

        <Field label="E-mail" error={errors.email}>
        <input
            type="email"
            value={values.email}
            onChange={(e) => handleChange("email", e.target.value)}
            placeholder="maria@email.com"
        />
        </Field>

        <Field label="Data de nascimento" error={errors.birthday}>
        <input
            type="date"
            value={values.birthday}
            onChange={(e) => handleChange("birthday", e.target.value)}
        />
        </Field>

        <Field label="CEP" error={errors.cep}>
        <input
            value={values.cep}
            onChange={(e) =>
                handleChange("cep", formatCep(e.target.value))
            }
            onBlur={handleCepBlur}
            placeholder="00000-000"
            maxLength={9}
        />
        </Field>

        <Field label="Endereço" error={errors.address}>
        <input
            value={values.address}
            placeholder="Preenchido pelo CEP"
            disabled
            className="readonly-input"
        />
        </Field>

        <Field label="Número" error={errors.number}>
        <input
            value={values.number}
            onChange={(e) =>
                handleChange(
                    "number",
                    e.target.value.replace(/\D/g, "")
                )
            }
        />
        </Field>

        <Field label="Cidade" error={errors.city}>
        <input
            value={values.city}
            placeholder="Preenchido pelo CEP"
            disabled
            className="readonly-input"
        />
        </Field>

        <Field label="Estado" error={errors.state}>
        <input
            value={values.state}
            placeholder="Preenchido pelo CEP"
            disabled
            className="readonly-input"
        />
        </Field>

        <Field label="Bairro" error={errors.neighborhood}>
        <input
            value={values.neighborhood}
            placeholder="Preenchido pelo CEP"
            disabled
            className="readonly-input"
        />
        </Field>

        {apiError && <p className="api-error">{apiError}</p>}

        <button className="btn" type="submit" disabled={loading}>
        {loading ? "Cadastrando..." : "Cadastrar"}
        </button>
    </form>
    )
}

// Pequeno wrapper de campo para não repetir label + erro
function Field({
  label,
  error,
  children,
}: {
  label: string
  error?: string
  children: React.ReactNode
}) {
  return (
    <div className="field">
      <label>{label}</label>
      {children}
      {error && <span className="error">{error}</span>}
    </div>
  )
}