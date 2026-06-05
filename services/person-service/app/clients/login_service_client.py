import os
import httpx

class LoginServiceError(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)
class LoginServiceUnavailableError(Exception):
    """Não foi possível alcançar o login-service."""


async def delete_login(login: str) -> str:
    base_url = os.environ["LOGIN_SERVICE_URL"]
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            await client.delete(f"{base_url}/logins/{login}")
    except httpx.RequestError:
        print(f"[WARN] não consegui liberar o login: {login}", flush=True)
        

async def gerar_login(full_name: str) -> str:
    base_url = os.environ["LOGIN_SERVICE_URL"]
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.post(
            f"{base_url}/logins/generate",
            json={"fullName": full_name},
        )
        resp.raise_for_status()
        return resp.json()["login"]
    except httpx.HTTPStatusError as e:
        detail = "Não foi possível gerar um login"
        try:
            detail = e.response.json().get("detail", detail)
        except Exception:
            pass
        raise LoginServiceError(e.response.status_code, detail)
    except httpx.RequestError:
        raise LoginServiceUnavailableError()