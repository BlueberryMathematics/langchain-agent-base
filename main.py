"""
Main entry point for the LangChain Agent Base Protocol Server.
Provides easy CLI access to run the protocol server and manage agents.
"""

import sys
import argparse
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from src.server import run_protocol_server
    SERVER_AVAILABLE = True
except ImportError:
    print("⚠️  FastAPI not installed. Server functionality disabled.")
    SERVER_AVAILABLE = False

try:
    from src.discovery import auto_discover_all, start_protocol_watcher
    DISCOVERY_AVAILABLE = True
except ImportError:
    print("⚠️  Discovery dependencies not available.")
    DISCOVERY_AVAILABLE = False

try:
    from examples.math_agent_evolution import demonstrate_math_agent_evolution
    EXAMPLES_AVAILABLE = True
except ImportError:
    print("⚠️  Example dependencies not available.")
    EXAMPLES_AVAILABLE = False


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="LangChain Agent Base Protocol Server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py server                    # Start protocol server
  python main.py server --port 8080       # Start on port 8080
  python main.py discover                 # Auto-discover agents and tools
  python main.py demo                     # Run math agent demonstration
  python main.py watch ./my_agents/       # Watch directory for new agents
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Server command
    server_parser = subparsers.add_parser('server', help='Start the protocol server')
    server_parser.add_argument('--host', default='0.0.0.0', help='Server host (default: 0.0.0.0)')
    server_parser.add_argument('--port', type=int, default=8000, help='Server port (default: 8000)')
    server_parser.add_argument('--reload', action='store_true', help='Enable auto-reload for development')
    
    # Discovery command
    discovery_parser = subparsers.add_parser('discover', help='Auto-discover agents and tools')
    discovery_parser.add_argument('--directories', nargs='*', help='Directories to scan for agents')
    
    # Demo command
    demo_parser = subparsers.add_parser('demo', help='Run math agent demonstration')
    
    # Watch command
    watch_parser = subparsers.add_parser('watch', help='Watch directories for new agents')
    watch_parser.add_argument('directories', nargs='+', help='Directories to watch')
    watch_parser.add_argument('--interval', type=int, default=30, help='Scan interval in seconds')
    
    args = parser.parse_args()
    
    if args.command == 'server':
        print(f"🚀 Starting LangChain Agent Base Protocol Server")
        print(f"📍 Host: {args.host}:{args.port}")
        print(f"📚 Documentation: http://{args.host}:{args.port}/docs")
        
        if SERVER_AVAILABLE and DISCOVERY_AVAILABLE:
            # Auto-discover agents before starting server
            print("🔍 Auto-discovering agents and tools...")
            auto_discover_all()
            
            # Start server
            run_protocol_server(
                host=args.host,
                port=args.port,
                reload=args.reload
            )
        else:
            print("❌ Server dependencies not available.")
            print("💡 Install with: pip install fastapi uvicorn qdrant-client langchain")
    
    elif args.command == 'discover':
        if DISCOVERY_AVAILABLE:
            print("🔍 Running agent and tool discovery...")
            results = auto_discover_all(watch_directories=args.directories)
        else:
            print("❌ Discovery not available. Install dependencies: pip install -e .")
        
        print(f"\n✅ Discovery Results:")
        print(f"   📋 Tools discovered: {len(results['tools'])}")
        print(f"   ⚡ Commands discovered: {len(results['commands'])}")
        print(f"   🤖 Agents discovered: {len(results['agents'])}")
        
        if results['tools']:
            print(f"\n📋 Tools by category:")
            from collections import defaultdict
            tools_by_category = defaultdict(list)
            for tool in results['tools']:
                tools_by_category[tool.category].append(tool.name)
            
            for category, tool_names in tools_by_category.items():
                print(f"   {category}: {', '.join(tool_names)}")
    
    elif args.command == 'demo':
        if EXAMPLES_AVAILABLE:
            print("🎭 Running Math Agent Evolution Demonstration")
            demonstrate_math_agent_evolution()
        else:
            print("❌ Demo not available. Install dependencies: pip install -e .")
    
    elif args.command == 'watch':
        if DISCOVERY_AVAILABLE:
            print(f"👀 Starting protocol watcher for directories: {args.directories}")
            print(f"⏱️  Scan interval: {args.interval} seconds")
            
            # Start file system watcher
            start_protocol_watcher(
                watch_directories=args.directories,
                scan_interval=args.interval
            )
        else:
            print("❌ Watch not available. Install dependencies: pip install -e .")
        
        # Keep running
        try:
            import time
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n👋 Protocol watcher stopped")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()