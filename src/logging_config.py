import logging
import sys
import structlog
import orjson
from typing import Any

# Detecta se estamos rodando localmente ou em prod (ajuste conforme sua env var)
# Em Big Tech, isso geralmente vem de os.getenv("ENV")
import os
IS_DEV = os.getenv("ENV", "development") == "development"

def configure_logging():
    """
    Configura o structlog globalmente para ser usado em toda a aplicação.
    Chame isso UMA VEZ no início do seu app (ex: main.py ou __init__.py).
    """

    # 1. Processadores Comuns (Rodam em Dev e Prod) 🧠
    common_processors = [
        structlog.contextvars.merge_contextvars, # Pega variáveis de contexto (ex: request_id)
        structlog.stdlib.add_logger_name,        # Adiciona o nome do logger
        structlog.stdlib.add_log_level,          # Adiciona o nível (INFO, ERROR)
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"), # Timestamp ISO 8601 universal
        structlog.processors.StackInfoRenderer(),
        structlog.processors.UnicodeDecoder(),
    ]

    # 2. Definição da "Renderização" (A cara do log) 🎨 vs 🤖
    if IS_DEV:
        # Modo DX Incrível: Cores, formatação visual e tratamento de exceções rico
        processors = common_processors + [
            structlog.dev.ConsoleRenderer(colors=True)
        ]
        # Formata exceções bonitas no console
        from rich.traceback import install
        install(show_locals=True)
    else:
        # Modo Big Tech Prod: JSON puro, rápido e estruturado
        processors = common_processors + [
            structlog.processors.dict_tracebacks, # Stack traces viram dicionários JSON
            structlog.processors.JSONRenderer(serializer=orjson.dumps), # Serialização ultra-rápida
        ]

    # 3. A Configuração Global (O "Big Bang") ⚡
    structlog.configure(
        processors=processors,
        # Wrapper class para compatibilidade com logging padrão do Python
        logger_factory=structlog.stdlib.LoggerFactory(),
        # Wrapper para garantir que o log seja thread-safe e contextual
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    # 4. Interceptar logs da Standard Library (Crucial!) 🛡️
    # Isso faz com que logs de bibliotecas (requests, sqlalchemy) também usem structlog
    logging.basicConfig(format="%(message)s", stream=sys.stdout, level=logging.INFO)

    # Opcional: Silenciar logs barulhentos de outras libs
    # logging.getLogger("uvicorn.access").setLevel(logging.WARNING)

    print(f"🚀 Logging configurado no modo: {'DEV (Human)' if IS_DEV else 'PROD (JSON)'}")
