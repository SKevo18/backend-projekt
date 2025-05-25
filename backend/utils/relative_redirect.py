from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from urllib.parse import urlparse, urlunparse


class RelativeRedirectMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        # only care about 3xx redirects…
        if 300 <= response.status_code < 400 and "location" in response.headers:
            loc = response.headers["location"]
            parts = urlparse(loc)

            if parts.scheme and parts.netloc:
                rel = urlunparse(
                    (
                        "",  # no scheme
                        "",  # no netloc
                        parts.path,
                        parts.params,
                        parts.query,
                        parts.fragment,
                    )
                )
                response.headers["location"] = rel or "/"

        return response
