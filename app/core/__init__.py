from app.core.config import settings, validate_settings
from app.core.limiter import limiter
from app.core.routing import register_controllers
from app.core.scripts.generate_keys import ensure_keys_exist