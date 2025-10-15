#!/usr/bin/env python3
import asyncio
import httpx
import json
from typing import Optional

API_BASE_URL = "http://localhost:8000/api/v1"


async def check_health():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_BASE_URL}/health")
        print("Health Check:")
        print(json.dumps(response.json(), indent=2))
        print()
        return response.json()


async def send_message(session_id: str, message: str, include_context: bool = True):
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            f"{API_BASE_URL}/chat",
            json={
                "session_id": session_id,
                "message": message,
                "include_context": include_context,
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"User: {message}")
            print(f"Assistant: {data['message']}")
            print()
            return data
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            return None


async def get_chat_history(session_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_BASE_URL}/chat/history/{session_id}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\nChat History for session {session_id}:")
            print("=" * 60)
            for msg in data["messages"]:
                role = msg["role"].capitalize()
                print(f"{role}: {msg['content']}")
                print()
            return data
        else:
            print(f"Error: {response.status_code}")
            return None


async def streaming_chat_example(session_id: str, message: str):
    async with httpx.AsyncClient(timeout=30.0) as client:
        print(f"User: {message}")
        print("Assistant: ", end="", flush=True)
        
        async with client.stream(
            "POST",
            f"{API_BASE_URL}/chat/stream",
            json={
                "session_id": session_id,
                "message": message,
                "include_context": True,
            }
        ) as response:
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    data_str = line[6:]
                    try:
                        data = json.loads(data_str)
                        if "content" in data:
                            print(data["content"], end="", flush=True)
                    except json.JSONDecodeError:
                        pass
        
        print("\n")


async def main():
    print("NIST CSF Conversational Agent - Example Usage\n")
    print("=" * 60)
    
    health = await check_health()
    
    if not health.get("ollama_available"):
        print("⚠️  Ollama is not available. Please ensure Ollama is running.")
        print("Run: ollama serve")
        return
    
    if not health.get("model_available"):
        print(f"⚠️  Model {health.get('configured_model')} is not available.")
        print(f"Run: ollama pull {health.get('configured_model')}")
        return
    
    print("✅ Ollama is ready!\n")
    
    session_id = "example-session-123"
    
    print("Example 1: Non-streaming chat")
    print("-" * 60)
    await send_message(
        session_id,
        "Hello! I run a small accounting firm with 5 employees. "
        "Can you help me understand what security measures I should have in place?"
    )
    
    await send_message(
        session_id,
        "We mainly use QuickBooks and store client data in Excel files on our server."
    )
    
    print("\nExample 2: Streaming chat")
    print("-" * 60)
    await streaming_chat_example(
        session_id,
        "What should I know about backup and disaster recovery?"
    )
    
    await get_chat_history(session_id)


if __name__ == "__main__":
    asyncio.run(main())
