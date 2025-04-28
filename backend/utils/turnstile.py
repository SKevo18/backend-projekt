import requests
from pydantic import BaseModel, Field
from utils.settings import get_setting


class SiteVerifyRequest(BaseModel):
    secret: str
    response: str
    remoteip: str | None = None


class SiteVerifyResponse(BaseModel):
    success: bool
    challenge_ts: str | None = None
    hostname: str | None = None
    error_codes: list[str] = Field(alias="error-codes", default_factory=list)
    action: str | None = None
    cdata: str | None = None


def validate_turnstile(
    turnstile_response: str, user_ip: str | None = None
) -> SiteVerifyResponse:
    secret_key = get_setting("turnstile_secret_key")

    if not secret_key:
        model = SiteVerifyResponse(success=False, hostname=None)
        model.error_codes.append("Turnstile secret key not configured")
        return model

    if not turnstile_response:
        model = SiteVerifyResponse(success=False, hostname=None)
        model.error_codes.append("Submitted with no cloudflare client response")
        return model

    url = "https://challenges.cloudflare.com/turnstile/v0/siteverify"
    model = SiteVerifyRequest(
        secret=secret_key, response=turnstile_response, remoteip=user_ip
    )
    try:
        resp = requests.post(url, data=model.model_dump())
        if resp.status_code != 200:
            model = SiteVerifyResponse(success=False, hostname=None)
            model.error_codes.extend(
                [
                    f"Failure status code: {resp.status_code}",
                    f"Failure details: {resp.text}",
                ]
            )
            return model

        site_response = SiteVerifyResponse(**resp.json())
        return site_response
    except Exception as x:
        model = SiteVerifyResponse(success=False, hostname=None)
        model.error_codes.extend(
            ["Failure status code: Unknown", f"Failure details: {x}"]
        )
        return model
