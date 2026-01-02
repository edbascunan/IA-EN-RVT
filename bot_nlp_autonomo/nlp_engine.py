from app.config import client, CONFIG

def ask_openai(prompt: str) -> str:
    """
    Procesar prompt con OpenAI usando SDK 1.0.0+
    """
    try:
        response = client.chat.completions.create(
            model=CONFIG["model"],
            messages=[
                {"role": "system", "content": CONFIG["system_prompt"]},
                {"role": "user", "content": prompt}
            ],
            temperature=CONFIG["temperature"],
            max_tokens=CONFIG["max_tokens"]
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"Error procesando con IA: {str(e)}"

def process_natural_language(text: str) -> dict:
    """
    Procesar lenguaje natural y estructurar respuesta
    """
    # Detectar tipo de comando
    text_lower = text.lower()
    
    if any(word in text_lower for word in ["crear", "hacer", "añadir"]):
        command_type = "crear"
    elif any(word in text_lower for word in ["analizar", "revisar", "examinar"]):
        command_type = "analizar"
    elif any(word in text_lower for word in ["medir", "cuantificar", "contar"]):
        command_type = "medir"
    else:
        command_type = "consulta"
    
    # Obtener respuesta de OpenAI
    ai_response = ask_openai(text)
    
    return {
        "command_type": command_type,
        "ai_response": ai_response,
        "timestamp": "2026-01-02T04:11:30Z"
    }