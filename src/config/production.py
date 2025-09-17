"""
Production configuration settings for enhanced performance and monitoring.
"""

import os
from typing import Dict, Any

# Database configuration
DATABASE_CONFIG = {
    "connection_timeout": 30,  # seconds
    "max_retries": 3,
    "retry_delay": 1.0,  # seconds
    "pool_size": 10,  # For future connection pooling
    "max_overflow": 20
}

# Rate limiting configuration
RATE_LIMIT_CONFIG = {
    "requests_per_window": 5,
    "window_duration": 300,  # 5 minutes in seconds
    "recovery_attempts_per_window": 3,
    "cleanup_interval": 300  # 5 minutes
}

# Monitoring configuration
MONITORING_CONFIG = {
    "log_level": "INFO",
    "enable_performance_tracking": True,
    "enable_user_analytics": True,
    "slow_operation_threshold": 5.0,  # seconds
    "session_cleanup_interval": 300  # 5 minutes
}

# Validation configuration
VALIDATION_CONFIG = {
    "max_weight_lbs": 1000,
    "min_weight_lbs": 1,
    "user_id_format": r"^[A-Za-z0-9]{3}-[A-Za-z0-9]{3}-[A-Za-z0-9]{3}$",
    "max_text_field_length": 1000,
    "max_list_items": 20
}

# Security configuration
SECURITY_CONFIG = {
    "enable_input_sanitization": True,
    "max_session_keys": 50,  # Prevent memory bloat
    "enable_admin_dashboard": os.getenv("ADMIN_MODE", "false").lower() == "true"
}

def get_config() -> Dict[str, Any]:
    """Get the complete production configuration."""
    return {
        "database": DATABASE_CONFIG,
        "rate_limiting": RATE_LIMIT_CONFIG,
        "monitoring": MONITORING_CONFIG,
        "validation": VALIDATION_CONFIG,
        "security": SECURITY_CONFIG
    }

def is_production() -> bool:
    """Check if running in production environment."""
    return os.getenv("ENVIRONMENT", "development").lower() == "production"

def get_log_level() -> str:
    """Get the appropriate log level for the environment."""
    if is_production():
        return "WARNING"
    return "INFO"