"""
In default config, the FastAPI normalizes forwarding slashes by redirecting them, but includes the base URL in the redirect.
This is problematic for shared hostings (Namecheap, etc.) with reverse proxy, because then `/api/something` redirects => `http://<localhost base URL>/api/something/`
And `ProxyPassReverse` etc. doesn't work in Namecheap's shared hosting.
This middleware patches this by removing the base URL from the redirect, and making all redirects relative, which works for Namecheap
"""

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
