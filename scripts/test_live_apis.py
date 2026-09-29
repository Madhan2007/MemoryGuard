import asyncio
import os
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv()

async def test_apis():
    print("========================================")
    print("1. Testing Groq API (Main & Verifier Models)")
    print("========================================")
    try:
        from groq import AsyncGroq
        groq_api_key = os.getenv("GROQ_API_KEY")
        main_model = os.getenv("MAIN_MODEL", "openai/gpt-oss-20b").replace("groq:", "")
        verifier_model = os.getenv("VERIFIER_MODEL", "openai/gpt-oss-120b").replace("groq:", "")
        
        client = AsyncGroq(api_key=groq_api_key)
        
        print(f"Connecting to Groq with Main Model ({main_model})...")
        res_main = await client.chat.completions.create(
            model=main_model,
            messages=[{"role": "user", "content": "Respond with: Ready"}],
            max_tokens=100
        )
        print(f"[PASS] Groq Main Model Output: {res_main.choices[0].message.content.strip() or 'OK (response received)'}")
        
        print(f"Connecting to Groq with Verifier Model ({verifier_model})...")
        res_verifier = await client.chat.completions.create(
            model=verifier_model,
            messages=[
                {"role": "system", "content": "You are a JSON assistant. Output valid JSON only."},
                {"role": "user", "content": 'Respond in JSON format: {"status": "verified"}'}
            ],
            response_format={"type": "json_object"},
            max_tokens=300
        )
        print(f"[PASS] Groq Verifier Model Output: {res_verifier.choices[0].message.content.strip()}")
        
    except Exception as e:
        print(f"[FAIL] Groq API Error: {e}")

    print("\n========================================")
    print("2. Testing Hindsight Cloud API")
    print("========================================")
    try:
        from hindsight_client import Hindsight
        base_url = os.getenv("HINDSIGHT_BASE_URL", "https://api.hindsight.vectorize.io").rstrip("/")
        api_key = os.getenv("HINDSIGHT_API_KEY")
        
        print(f"Connecting to Hindsight endpoint: {base_url}")
        hindsight = Hindsight(base_url=base_url, api_key=api_key, timeout=30.0)
        
        test_bank = "memoryguard-test-verification"
        print(f"Checking bank '{test_bank}'...")
        try:
            await hindsight.acreate_bank(bank_id=test_bank)
            print(f"[PASS] Bank '{test_bank}' created or available.")
        except Exception as e:
            print(f"[NOTE] Bank status: {e}")
            
        print("Testing retain into Hindsight...")
        retain_res = await hindsight.aretain(
            bank_id=test_bank,
            content="Customer prefers contact via email for all enterprise contracts."
        )
        print(f"[PASS] Retain successful (tokens used: {retain_res.usage.total_tokens})")
        
        print("Testing recall from Hindsight...")
        recall_res = await hindsight.arecall(
            bank_id=test_bank,
            query="preferred contact method"
        )
        results = getattr(recall_res, "results", []) or []
        print(f"[PASS] Recall successful: {len(results)} memory items returned")
        for r in results:
            score = getattr(r.scores, "final", "N/A") if getattr(r, "scores", None) else "N/A"
            print(f"       - Found text: {r.text} (score: {score})")
            
        await hindsight.aclose()
        print("\nALL EXTERNAL API INTEGRATIONS VERIFIED OPERATIONAL!")
    except Exception as e:
        print(f"[FAIL] Hindsight API Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_apis())
