# IA-EN-RVT 2026 - Dockerfile para Railway
# ========================================

FROM python:3.11-slim

# Configurar directorio de trabajo
WORKDIR /app

# Copiar requirements primero para cache
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY . .

# Crear directorio para comandos
RUN mkdir -p backend_ai/shared

# Variables de entorno
ENV PYTHONPATH=/app
ENV TELEGRAM_TOKEN=7537372382:AAF58awLAyaQ4fFpZfdhn88dP555zW9JAGI
ENV OPENAI_API_KEY=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
ENV COMMAND_PATH=backend_ai/shared/command_out.json
ENV PORT=8080

# Puerto de exposición
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Comando por defecto
CMD ["python", "bot_nlp_real.py"]