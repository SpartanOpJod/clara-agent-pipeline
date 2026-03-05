def process_demo_call(account_id, transcript_text):
    """
    Simulates Pipeline A: Ingests a demo transcript, extracts data, and saves v1 assets [cite: 17-23, 125].
    """
    print(f"Starting Pipeline A for {account_id}...")
    v1_path, _ = setup_account_dirs(account_id)
    
    # 1. Initialize empty schemas
    memo = get_empty_account_memo(account_id)
    agent_spec = get_empty_agent_spec(version="v1")
    
    # 2. Simulate LLM Extraction (Mocked for the 20% implementation)
    # In the next phase, this is where we inject the prompt and call the local LLM.
    memo["company_name"] = "Mocked Fire Protection Co."
    memo["questions_or_unknowns"].append("Exact after-hours start time not mentioned in demo.")
    
    agent_spec["agent_name"] = "Clara - Mocked Fire Protection"
    agent_spec["system_prompt"] = "You are an AI assistant. Business hours flow: Greeting -> Collect name/number -> Route -> Close. Do not mention function calls." # Enforcing prompt hygiene [cite: 118-123]
    
    # 3. Save outputs as JSON files [cite: 20-22]
    memo_file = os.path.join(v1_path, "memo.json")
    spec_file = os.path.join(v1_path, "agent_spec.json")
    
    with open(memo_file, "w") as f:
        json.dump(memo, f, indent=4)
        
    with open(spec_file, "w") as f:
        json.dump(agent_spec, f, indent=4)
        
    print(f"Success! v1 assets saved to {v1_path}")

# --- TEST RUN ---
if __name__ == "__main__":
    test_account = "ACC_1001"
    test_transcript = "Client: We are a fire protection company. We need help routing emergency sprinkler leaks."
    process_demo_call(test_account, test_transcript)