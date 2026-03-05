import os
import json
from datetime import datetime

# --- CONFIGURATION ---
OUTPUT_DIR = "./outputs/accounts"

# --- HELPER FUNCTIONS ---
def setup_account_dirs(account_id):
    """
    Creates the required v1 and v2 directories for a specific account.
    """
    v1_path = os.path.join(OUTPUT_DIR, account_id, "v1")
    v2_path = os.path.join(OUTPUT_DIR, account_id, "v2")
    
    os.makedirs(v1_path, exist_ok=True)
    os.makedirs(v2_path, exist_ok=True)
    
    return v1_path, v2_path

# --- SCHEMAS ---
def get_empty_account_memo(account_id):
    """
    Returns the exact structured JSON schema required for the Account Memo [cite: 68-82].
    """
    return {
        "account_id": account_id,
        "company_name": None,
        "business_hours": {
            "days": None,
            "start": None,
            "end": None,
            "timezone": None
        },
        "office_address": None,
        "services_supported": [],
        "emergency_definition": [],
        "emergency_routing_rules": None,
        "non_emergency_routing_rules": None,
        "call_transfer_rules": {
            "timeouts": None,
            "retries": None,
            "fallback_message": None
        },
        "integration_constraints": None,
        "after_hours_flow_summary": None,
        "office_hours_flow_summary": None,
        "questions_or_unknowns": [], # Flags missing info to avoid hallucinations 
        "notes": ""
    }

def get_empty_agent_spec(version="v1"):
    """
    Returns the required Retell Agent Draft Spec schema [cite: 83-92].
    """
    return {
        "agent_name": None,
        "voice_style": "basic",
        "system_prompt": "",
        "key_variables": {
            "timezone": None,
            "business_hours": None,
            "address": None,
            "emergency_routing": None
        },
        "tool_invocation_placeholders": [], # Must not mention tools to caller [cite: 89, 122]
        "call_transfer_protocol": "",
        "fallback_protocol": "",
        "version": version
    }