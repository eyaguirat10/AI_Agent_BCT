# auth.py
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, RedirectResponse
from authlib.integrations.starlette_client import OAuth
from dotenv import load_dotenv
import os

router = APIRouter()
load_dotenv()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

oauth = OAuth()
oauth.register(
    name="google",
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

@router.get("/api/user")
async def get_user(request: Request):
    user = request.session.get("user")
    if not user:
        return JSONResponse({"error": "Not authenticated"}, status_code=401)
    return user

@router.get("/login")
async def login_via_google(request: Request):
    # Build the exact redirect URI that matches Google Console
    redirect_uri = "http://localhost:8000/auth/callback"
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/auth/callback")
async def auth_callback(request: Request):
    token = await oauth.google.authorize_access_token(request)
    # Some providers put profile under "userinfo", others under "id_token" claims:
    user_info = token.get("userinfo") or {}
    if not user_info:
        # try to decode id_token claims if present (Authlib fills this for Google)
        user_info = {
            "email": token.get("email"),
            "name": token.get("name"),
            "picture": token.get("picture"),
            "sub": token.get("sub"),
        }
    # Save to session (Starlette will set Set-Cookie on the response)
    request.session["user"] = {k: v for k, v in user_info.items() if v is not None}

    # Send the browser back to Vue app
    return RedirectResponse(url="http://localhost:8081/")

@router.get("/logout")
async def logout(request: Request):
    # Clear the user from session
    request.session.pop("user", None)
    
    # Return JSON with the login page URL instead of RedirectResponse
    return JSONResponse({"redirect_url": "http://localhost:8081"})

@router.get("/debug-session")
async def debug_session(request: Request):
    return {"session": dict(request.session)}
