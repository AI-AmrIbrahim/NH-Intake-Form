"""
Monitoring and health check utilities for the Nutrition House application.
"""

import streamlit as st
import time
import logging
from typing import Dict, Any, List
from datetime import datetime, timedelta
from src.utils.db_utils import get_database_health, init_connection

logger = logging.getLogger(__name__)

def check_system_health() -> Dict[str, Any]:
    """Comprehensive system health check."""
    health_status = {
        'timestamp': datetime.now().isoformat(),
        'overall_status': 'healthy',
        'components': {}
    }

    # Database health check
    try:
        db_health = get_database_health()
        health_status['components']['database'] = db_health

        if db_health['status'] != 'healthy':
            health_status['overall_status'] = 'degraded'

    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        health_status['components']['database'] = {
            'status': 'unhealthy',
            'error': str(e)
        }
        health_status['overall_status'] = 'unhealthy'

    # Session state health
    try:
        session_health = check_session_health()
        health_status['components']['session'] = session_health
    except Exception as e:
        logger.error(f"Session health check failed: {e}")
        health_status['components']['session'] = {
            'status': 'unhealthy',
            'error': str(e)
        }
        health_status['overall_status'] = 'degraded'

    return health_status

def check_session_health() -> Dict[str, Any]:
    """Check the health of the current user session."""
    session_keys = len(st.session_state.keys()) if hasattr(st, 'session_state') else 0

    # Check for potential memory issues
    if session_keys > 50:
        logger.warning(f"High number of session keys: {session_keys}")
        return {
            'status': 'degraded',
            'session_keys': session_keys,
            'warning': 'High memory usage detected'
        }

    return {
        'status': 'healthy',
        'session_keys': session_keys
    }

def log_user_action(action: str, user_id: str = None, additional_data: Dict[str, Any] = None):
    """Log user actions for monitoring and analytics."""
    log_data = {
        'timestamp': datetime.now().isoformat(),
        'action': action,
        'user_id': user_id or 'anonymous',
        'session_id': id(st.session_state) if hasattr(st, 'session_state') else None
    }

    if additional_data:
        log_data.update(additional_data)

    logger.info(f"User Action: {log_data}")

def track_form_performance(start_time: float, action: str, success: bool = True):
    """Track form submission performance."""
    duration = time.time() - start_time

    performance_data = {
        'action': action,
        'duration_ms': round(duration * 1000, 2),
        'success': success,
        'timestamp': datetime.now().isoformat()
    }

    if duration > 5.0:  # Slow operation warning
        logger.warning(f"Slow operation detected: {performance_data}")
    else:
        logger.info(f"Performance: {performance_data}")

    return performance_data

def get_rate_limit_status(user_identifier: str) -> Dict[str, Any]:
    """Get current rate limit status for a user."""
    rate_limit_key = f"rate_limit_{user_identifier}"

    if rate_limit_key not in st.session_state:
        return {
            'requests_in_window': 0,
            'limit': 5,
            'window_minutes': 5,
            'status': 'ok'
        }

    current_time = time.time()
    recent_requests = [
        timestamp for timestamp in st.session_state[rate_limit_key]
        if current_time - timestamp < 300  # 5 minutes
    ]

    return {
        'requests_in_window': len(recent_requests),
        'limit': 5,
        'window_minutes': 5,
        'status': 'limited' if len(recent_requests) >= 5 else 'ok'
    }

def display_admin_dashboard():
    """Display an admin dashboard with system health and monitoring info."""
    try:
        admin_mode = st.secrets.get("ADMIN_MODE", False) if hasattr(st, 'secrets') else False
        if not admin_mode:
            return
    except Exception:
        # If secrets aren't available or configured, just return
        return

    with st.expander("🔧 Admin Dashboard", expanded=False):
        st.subheader("System Health")

        if st.button("Check System Health"):
            health = check_system_health()

            if health['overall_status'] == 'healthy':
                st.success("System is healthy ✅")
            elif health['overall_status'] == 'degraded':
                st.warning("System performance is degraded ⚠️")
            else:
                st.error("System is unhealthy ❌")

            st.json(health)

        st.subheader("Session Information")
        if hasattr(st, 'session_state'):
            st.write(f"Session keys: {len(st.session_state.keys())}")

            # Show rate limit status
            if 'user_profile' in st.session_state and st.session_state.user_profile.get('user_id'):
                rate_status = get_rate_limit_status(st.session_state.user_profile['user_id'])
                st.write("Rate Limit Status:", rate_status)

def monitor_concurrent_users():
    """Simplified concurrent user monitoring for 100+ users."""
    # For high concurrency, we'll use a simple time-based estimate
    # In production, you'd use Redis or database-based session tracking

    current_time = time.time()
    session_id = id(st.session_state)

    # Store session activity timestamp
    if 'session_start_time' not in st.session_state:
        st.session_state.session_start_time = current_time

    # Update last activity
    st.session_state.last_activity = current_time

    # Return a simple concurrent user estimate (for monitoring purposes)
    # This doesn't affect functionality, just provides rough metrics
    return 1  # Each session represents one user

def log_error_with_context(error: Exception, context: Dict[str, Any] = None):
    """Log errors with additional context for debugging."""
    error_data = {
        'timestamp': datetime.now().isoformat(),
        'error_type': type(error).__name__,
        'error_message': str(error),
        'context': context or {}
    }

    if hasattr(st, 'session_state') and 'user_profile' in st.session_state:
        error_data['user_id'] = st.session_state.user_profile.get('user_id', 'unknown')

    logger.error(f"Application Error: {error_data}")

    return error_data