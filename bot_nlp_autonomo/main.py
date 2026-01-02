from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import os

from app.nlp_engine import process_natural_language
from app.schemas import PromptRequest, PromptResponse, HealthResponse

# Crear aplicación FastAPI
app = FastAPI(
    title="IA-EN-RVT Bot NLP",
    description="Bot NLP autónomo para automatización BIM con OpenAI",
    version="1.0.0"
)

# Configurar CORS para permitir requests desde pyRevit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios exactos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def health_check():
    """Endpoint de salud - verifica que el bot esté funcionando"""
    return HealthResponse(
        status="online",
        version="1.0.0",
        timestamp=datetime.now().isoformat()
    )

@app.post("/ask", response_model=PromptResponse)
async def ask_nlp(prompt: PromptRequest):
    """
    Endpoint principal para procesar comandos en lenguaje natural
    
    Args:
        prompt: Request con el texto a procesar
        
    Returns:
        Response con el tipo de comando y respuesta de IA
    """
    try:
        # Procesar el texto con nuestro motor NLP
        result = process_natural_language(prompt.text)
        
        return PromptResponse(
            command_type=result["command_type"],
            ai_response=result["ai_response"],
            timestamp=result["timestamp"],
            success=True
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error procesando solicitud: {str(e)}"
        )

@app.post("/revit-command")
async def revit_command(prompt: PromptRequest):
    """
    Endpoint específico para comandos de Revit
    Optimizado para uso desde pyRevit
    """
    try:
        result = process_natural_language(prompt.text)
        
        # Formatear respuesta específicamente para Revit
        formatted_response = f"""
🤖 **Bot IA-EN-RVT**
📋 **Comando**: {result['command_type']}
💬 **Respuesta**: {result['ai_response']}
⏰ **Tiempo**: {result['timestamp']}
"""
        
        return PromptResponse(
            command_type=result["command_type"],
            ai_response=formatted_response,
            timestamp=result["timestamp"],
            success=True
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error procesando comando de Revit: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)