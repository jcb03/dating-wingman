import os
import sys
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    """Main entry point for the AI Wingman MCP Server"""
    try:
        # Import and run the MCP server
        from mcp_server import mcp, BEARER_TOKEN
        
        port = int(os.getenv("PORT", 8000))
        
        print("🚀 AI Wingman MCP Server Starting...")
        print(f"📡 Port: {port}")
        print(f"🔐 Bearer Token: {BEARER_TOKEN}")
        print(f"🤖 OpenAI Model: {os.getenv('OPENAI_MODEL', 'gpt-4o')}")
        print("="*50)
        
        # Run the MCP server
        asyncio.run(mcp.run(port=port, host="0.0.0.0"))
        
    except KeyboardInterrupt:
        print("\n👋 AI Wingman MCP Server shutting down...")
    except Exception as e:
        print(f"❌ Error starting server: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
