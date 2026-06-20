import re
import time
from core.config import settings
from core.utils import get_logger

logger = get_logger("SecurityFirewall")

class SecurityException(Exception):
    \"\"\"Custom exception for security violations bounded by the firewall.\"\"\"
    pass

class SecurityFirewall:
    \"\"\"
    V2 Advanced Security Layer.
    Implements a strict defense in depth: Length limits -> Regex Heuristics -> Rate limit tracking.
    \"\"\"
    
    JAILBREAK_PATTERNS = [
        r"(?i)ignore previous instructions",
        r"(?i)ignore all previous commands",
        r"(?i)disregard previous",
        r"(?i)forget previous instructions",
        r"(?i)system prompt",
        r"(?i)developer prompt",
        r"(?i)you are now",
        r"(?i)simulate a",
        r"(?i)bypassing restrictions",
        r"(?i)override protocol",
        r"(?i)act as an uncensored",
        r"(?i)\\[System:"
    ]

    def __init__(self):
        self.request_logs = []

    def validate_input(self, user_input: str) -> bool:
        if not user_input or not user_input.strip():
            logger.warning("Empty payload rejected.")
            raise SecurityException("Input cannot be empty.")
            
        if len(user_input) > settings.MAX_INPUT_LENGTH:
            logger.warning(f"Oversized payload rejected: {len(user_input)} chars.")
            raise SecurityException(f"Input exceeds maximum allowed length of {settings.MAX_INPUT_LENGTH} characters.")
            
        return True

    def detect_prompt_injection(self, user_input: str) -> bool:
        for pattern in self.JAILBREAK_PATTERNS:
            if re.search(pattern, user_input):
                logger.critical(f"Prompt Injection Attempt Blocked! Triggered pattern: {pattern}")
                raise SecurityException("Security Firewall Alert: Potential prompt injection or jailbreak attempt detected and blocked.")
        return False
        
    def check_abuse(self):
        \"\"\" Rudimentary IP-less rate limiter spanning current session memory \"\"\"
        now = time.time()
        # Clean old logs > 1 min
        self.request_logs = [t for t in self.request_logs if now - t < 60]
        if len(self.request_logs) > 20: # Over 20 requests a minute triggers abuse protocol
            logger.error("Rate limit threshold met.")
            raise SecurityException("Too many requests. Please slow down. (Anti-Abuse mechanism)")
        self.request_logs.append(now)

    def sanitize(self, user_input: str) -> str:
        \"\"\" Default Sanitization entrypoint for inbound String data \"\"\"
        self.check_abuse()
        self.validate_input(user_input)
        self.detect_prompt_injection(user_input)
        
        # Simple HTML/JS strip for safe rendering context
        safe_input = user_input.replace("<script>", "").replace("</script>", "")
        return safe_input.strip()

security_manager = SecurityFirewall()
