import os
import json
import requests

# --- CONFIGURATION ---
OUTPUT_DIR = "./outputs/accounts"
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3" # Ensure you have pulled this model via Ollama

def setup_directories(account_id):
    """Creates the necessary v1 folder structure[cite: 178]."""
    v1_path = os.path.join(OUTPUT_DIR, account_id, "v1")
    os.makedirs(v1_path, exist_ok=True)
    return v1_path

def call_local_llm(prompt, system_prompt="You are a strict data extraction assistant. Always output valid JSON."):
    """Calls local Ollama instance to guarantee zero cost[cite: 32, 149]."""
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "system": system_prompt,
        "format": "json", # Forces the model to return a JSON object
        "stream": False
    }
    
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        return json.loads(response.json()['response'])
    except Exception as e:
        print(f"Error calling LLM: {e}")
        return None

def generate_account_memo(transcript):
    """Extracts operational data from the demo transcript [cite: 18, 20, 67-82]."""
    prompt = f"""
    Analyze the following demo call transcript and extract the business details into a JSON object.
    
    CRITICAL RULES:
    1. DO NOT invent or hallucinate data[cite: 114].
    2. If a detail is missing, set its value to null and add a description of what is missing to the 'questions_or_unknowns' list [cite: 115-116].
    
    Required JSON Schema:
    {{
        "company_name": "string or null",
        "business_hours": {{"days": "string or null", "start": "string or null", "end": "string or null", "timezone": "string or null"}},
        "office_address": "string or null",
        "services_supported": ["list of strings"],
        "emergency_definition": ["list of strings"],
        "emergency_routing_rules": "string or null",
        "non_emergency_routing_rules": "string or null",
        "call_transfer_rules": {{"timeouts": "string or null", "retries": "number or null", "what_to_say_if_fails": "string or null"}},
        "integration_constraints": "string or null",
        "after_hours_flow_summary": "string or null",
        "office_hours_flow_summary": "string or null",
        "questions_or_unknowns": ["list of missing info"],
        "notes": "string"
    }}
    
    Transcript:
    {transcript}
    """
    return call_local_llm(prompt)

def generate_agent_spec(memo_data):
    """Creates the Retell Agent Spec based on the extracted memo [cite: 21, 83-92]."""
    prompt = f"""
    Based on the following account memo, generate a Retell Agent Spec configuration in JSON.
    
    CRITICAL PROMPT HYGIENE RULES [cite: 117-123]:
    1. The system_prompt MUST include a business hours flow: greet, ask purpose, collect name/number, route/transfer, fallback if transfer fails, close.
    2. The system_prompt MUST include an after-hours flow: confirm emergency, collect name/number/address immediately if emergency, attempt transfer, fallback.
    3. NEVER mention "function calls" to the user[cite: 122].
    
    Memo Data:
    {json.dumps(memo_data)}
    
    Required JSON Schema:
    {{
        "agent_name": "string",
        "voice_style": "string (e.g., professional, empathetic)",
        "system_prompt": "string (the actual detailed prompt for the AI)",
        "key_variables": {{"timezone": "string or null", "business_hours": "string or null", "address": "string or null", "emergency_routing": "string or null"}},
        "tool_invocation_placeholders": ["list of tools needed, e.g., 'transfer_call'"],
        "call_transfer_protocol": "string",
        "fallback_protocol": "string",
        "version": "v1"
    }}
    """
    return call_local_llm(prompt)

def run_pipeline_a(account_id, transcript_text):
    """Executes Pipeline A end-to-end for a single account [cite: 17-23]."""
    print(f"[*] Starting Pipeline A for Account: {account_id}")
    v1_path = setup_directories(account_id)
    
    # Step 1: Extract Memo
    print("    -> Extracting Account Memo...")
    memo = generate_account_memo(transcript_text)
    if not memo:
        print("    [!] Failed to generate memo.")
        return
        
    memo["account_id"] = account_id # Ensure ID is explicitly set [cite: 69]
    
    # Step 2: Generate Agent Spec
    print("    -> Generating v1 Agent Spec...")
    agent_spec = generate_agent_spec(memo)
    if not agent_spec:
        print("    [!] Failed to generate agent spec.")
        return
        
    # Step 3: Save Artifacts [cite: 22]
    with open(os.path.join(v1_path, "memo.json"), "w") as f:
        json.dump(memo, f, indent=4)
        
    with open(os.path.join(v1_path, "agent_spec.json"), "w") as f:
        json.dump(agent_spec, f, indent=4)
        
    print(f"[*] Pipeline A Complete! Artifacts saved to {v1_path}\n")

# --- EXECUTION ---
if __name__ == "__main__":
    # Mock dataset entry [cite: 60-64]
    sample_account = "ACC_001"
    sample_transcript = """
    Agent: Hi, thanks for taking this demo of Clara. Can you tell me a bit about your business?
    Client: Sure, we're Apex Fire Protection. We handle sprinkler systems and fire alarms. 
    Agent: Great. How do you handle emergencies?
    Client: Right now, it's a mess. If a sprinkler breaks, we need someone to answer immediately and route it to our on-call tech, Mike. 
    Agent: Got it. And what are your standard hours?
    Client: We're 8 to 5, Monday through Friday. I'm not sure exactly how we want to handle non-emergencies after hours yet, maybe just take a message.
    """
    
    run_pipeline_a(sample_account, sample_transcript)