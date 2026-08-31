"""
Auth client — talks to the central the_auth service over HTTP.

the_engine does not verify JWTs itself. It calls the_auth to log in, then
calls /auth/me with the returned token to confirm the token and read the
current user (including role). This keeps the shared JWT secret only in
the_auth.
"""

import os

import requests

AUTH_BASE_URL = os.environ.get("AUTH_BASE_URL", "https://the-auth.onrender.com")

# the_auth on the free tier can cold-start; allow a generous timeout.
_TIMEOUT = 60


class AuthError(Exception):
    """Raised when authentication fails or the auth service is unreachable."""


def login(username, password):
    """Log in against the_auth. Returns {'token', 'user'} on success.

    Raises AuthError with a user-facing message on failure.
    """
    try:
        resp = requests.post(
            f"{AUTH_BASE_URL}/auth/login",
            json={"username": username, "password": password},
            timeout=_TIMEOUT,
        )
    except requests.RequestException as exc:
        raise AuthError(f"Kunde inte nå inloggningstjänsten: {exc}") from exc

    if resp.status_code == 401:
        raise AuthError("Fel användarnamn eller lösenord")
    if resp.status_code == 403:
        raise AuthError("Kontot är avslutat")
    if not resp.ok:
        raise AuthError(f"Inloggning misslyckades ({resp.status_code})")

    data = resp.json()
    if not data.get("token"):
        raise AuthError("Inget token mottogs")
    return data


def me(token):
    """Verify a token by calling /auth/me. Returns the user dict, or None."""
    try:
        resp = requests.get(
            f"{AUTH_BASE_URL}/auth/me",
            headers={"Authorization": f"Bearer {token}"},
            timeout=_TIMEOUT,
        )
    except requests.RequestException:
        return None
    if not resp.ok:
        return None
    return resp.json().get("user")
