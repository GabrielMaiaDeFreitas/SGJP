import os

# ============================================================================
# API
# ============================================================================

GOOGLE_MAPS_API_KEY = os.getenv(
    "GOOGLE_MAPS_API_KEY"
)

URL_ROUTES = (
    "https://routes.googleapis.com/"
    "directions/v2:computeRoutes"
)

FIELD_MASK = (
    "routes.distanceMeters,"
    "routes.duration"
)

# ============================================================================
# Base da Empresa
# ============================================================================

LATITUDE_BASE = -16.637255531065655
LONGITUDE_BASE = -49.2553876282103

# ============================================================================
# Configuração da Rota
# ============================================================================

TRAVEL_MODE = "DRIVE"
ROUTING_PREFERENCE = "TRAFFIC_AWARE"