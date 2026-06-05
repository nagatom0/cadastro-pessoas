import httpx
from app.schemas.search_cep import SearchCepResponse

VIACEP_URL = "https://viacep.com.br/ws/{cep}/json/"


class CepInvalidoError(Exception):
    """CEP com formato inválido (não tem 8 dígitos)."""
class CepNaoEncontradoError(Exception):
    """CEP não existe na base do ViaCEP."""
class ViaCepUnavailableError(Exception):
    """Não foi possível alcançar o ViaCEP."""
    
async def search_cep(cep: str) -> SearchCepResponse:
    cep_limpo = "".join(filter(str.isdigit, cep))
    if len(cep_limpo) != 8:
        raise CepInvalidoError("CEP deve ter 8 dígitos")
    try:
        print(VIACEP_URL.format(cep=cep_limpo))
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(VIACEP_URL.format(cep=cep_limpo))
            resp.raise_for_status()
            data = resp.json()
    except httpx.RequestError:
        raise ViaCepUnavailableError()
    if data.get("erro") in (True, "true"):
        raise CepNaoEncontradoError(f"CEP {cep_limpo} não encontrado")
    return {
        "cep": data["cep"],
        "address": data["logradouro"],
        "city": data["localidade"],
        "state": data["estado"],        
        "neighborhood": data["bairro"],        
        } 