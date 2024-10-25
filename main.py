from fastapi import FastAPI
from auth.interfaces.http.auth_controller import router as auth_router
from challenge.interfaces.rest.challenge_controller import router as challenge_router
from competition.interfaces.web_sockets.competition_socket import router as competition_socket_router
from competition.interfaces.rest.competition_controller import router as competition_controller_router
from feedback.interfaces.rest.feedback_controller import router as feedback_controller_router
from user_profile.interfaces.http.user_profile_controller import router as profile_controller_router
from cs_statistics.interfaces.rest.statistics_controller import router as statistics_controller_router
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],  # Métodos permitidos (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Encabezados permitidos
)

# Incluir las rutas de autenticación en la aplicación
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(challenge_router, prefix="/challenges", tags=["challenges"])
app.include_router(competition_socket_router, prefix="/ws", tags=["websockets"])
app.include_router(competition_controller_router, prefix="/competitions")
app.include_router(feedback_controller_router, prefix="/feedback")
app.include_router(profile_controller_router, prefix="/profile")
app.include_router(statistics_controller_router, prefix="/statistics")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
