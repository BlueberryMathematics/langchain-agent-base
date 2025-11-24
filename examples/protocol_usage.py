"""
Complete Protocol System Usage Example
=====================================

This example demonstrates the full LangChain Agent Base Protocol system:
1. Creating custom agents with the @register_agent decorator
2. Automatic API generation and versioning  
3. Agent cards and metadata management
4. Dynamic discovery and tool registration
5. REST API usage and client interactions

Run this example to see the complete protocol in action.
"""

import asyncio
import time
from typing import List

from src.base import Agent
from src.protocol import register_agent, AgentStatus, get_agent_registry
from src.discovery import AutoRegisterMixin, auto_discover_all
from src.tools import get_math_tools, get_science_tools
from src.toolbox import get_toolbox
from src.tool_generator import generate_tool, ToolAssistant
from langchain_core.tools import tool


# Example 1: Custom Business Domain Agent
@tool  
def customer_lookup(customer_id: str) -> str:
    """Look up customer information by ID."""
    # Mock implementation
    customers = {
        "CUST001": "John Doe - Premium Account",
        "CUST002": "Jane Smith - Standard Account", 
        "CUST003": "Bob Johnson - Enterprise Account"
    }
    return customers.get(customer_id, f"Customer {customer_id} not found")


@tool
def process_order(product: str, quantity: int, customer_id: str) -> str:
    """Process a customer order."""
    # Mock implementation
    total = quantity * 29.99  # Mock price
    return f"Order processed: {quantity}x {product} for {customer_id}. Total: ${total:.2f}"


@tool
def inventory_check(product: str) -> str:
    """Check inventory levels for a product.""" 
    # Mock implementation
    inventory = {
        "laptop": 45,
        "mouse": 150,
        "keyboard": 78,
        "monitor": 23
    }
    stock = inventory.get(product.lower(), 0)
    return f"Product '{product}': {stock} units in stock"


@register_agent(
    name="business",
    version="1.0.0", 
    domain="business",
    category="specialist",
    description="Business operations agent for customer service and order processing",
    author="Business Team",
    status=AgentStatus.PRODUCTION
)
class BusinessAgent(Agent, AutoRegisterMixin):
    """Agent specialized for business operations."""
    
    def __init__(self):
        # Business-specific tools
        business_tools = [customer_lookup, process_order, inventory_check]
        
        super().__init__(
            system_prompt="""You are a business operations assistant specialized in:
            - Customer service and account management
            - Order processing and fulfillment
            - Inventory management and stock checking
            
            Always provide professional, helpful service and confirm important actions with customers.""",
            tools=business_tools,
            enable_commands=True
        )


# Example 2: Enhanced Science Agent with Custom Tools
@tool
def chemical_reaction_predictor(reactants: str) -> str:
    """Predict products of a chemical reaction."""
    # Mock implementation
    reactions = {
        "H2 + O2": "2H2O (water formation)",
        "Na + Cl2": "2NaCl (salt formation)",
        "CH4 + O2": "CO2 + H2O (combustion)"
    }
    
    reactants_clean = reactants.replace(" ", "").lower()
    for reaction, product in reactions.items():
        if reactants_clean in reaction.replace(" ", "").lower():
            return f"Predicted reaction: {reaction} → {product}"
    
    return f"Reaction prediction not available for: {reactants}"


@register_agent(
    name="science",
    version="2.0.0",
    domain="science", 
    category="specialist",
    description="Enhanced science agent with chemistry prediction capabilities",
    author="Science Team",
    status=AgentStatus.TESTING
)
class EnhancedScienceAgent(Agent, AutoRegisterMixin):
    """Enhanced science agent with additional chemistry tools."""
    
    def __init__(self):
        # Combine built-in science tools with custom chemistry tools
        tools = get_science_tools() + [chemical_reaction_predictor]
        
        super().__init__(
            system_prompt="""You are an advanced scientific assistant with expertise in:
            - Physics calculations and unit conversions
            - Chemistry reactions and molecular analysis  
            - Scientific methodology and analysis
            
            Provide accurate scientific information with proper units and methodology.""",
            tools=tools,
            enable_commands=True
        )


# Example 3: Multi-Domain Agent
@register_agent(
    name="consultant", 
    version="1.0.0",
    domain="general",
    category="multi-domain", 
    description="Multi-domain consultant combining math, science, and business expertise",
    author="Consultant Team",
    status=AgentStatus.DEVELOPMENT
)
class ConsultantAgent(Agent, AutoRegisterMixin):
    """Multi-domain agent for comprehensive consulting."""
    
    def __init__(self):
        # Combine tools from multiple domains
        tools = (get_math_tools() + 
                get_science_tools() + 
                [customer_lookup, process_order, inventory_check])
        
        super().__init__(
            system_prompt="""You are a multi-domain consultant with expertise across:
            
            MATHEMATICS:
            - Advanced calculations and equation solving
            - Statistical analysis and data modeling
            - Financial calculations and projections
            
            SCIENCE:
            - Physics and chemistry analysis
            - Unit conversions and scientific calculations
            - Research methodology and data analysis
            
            BUSINESS:
            - Customer service and account management  
            - Operations and process optimization
            - Strategic planning and analysis
            
            Provide comprehensive, professional advice drawing from your multi-domain expertise.""",
            tools=tools,
            enable_commands=True
        )


async def demonstrate_protocol_system():
    """Demonstrate the complete protocol system."""
    
    print("🌐 LangChain Agent Base Protocol System Demonstration")
    print("=" * 60)
    
    # 1. Auto-discovery
    print("\\n🔍 Step 1: Auto-Discovery")
    print("-" * 30)
    results = auto_discover_all()
    print(f"Discovered {len(results['agents'])} agents automatically registered")
    
    # 2. Registry inspection
    print("\\n📋 Step 2: Registry Inspection")  
    print("-" * 30)
    registry = get_agent_registry()
    
    # List all registered agents
    agents = registry.list_agents()
    print(f"Total registered agents: {len(agents)}")
    
    for agent in agents:
        print(f"  📦 {agent.name} v{agent.version} ({agent.status.value})")
        print(f"     Domain: {agent.domain} | Tools: {len(agent.tools)}")
    
    # 3. Agent creation and testing
    print("\\n🤖 Step 3: Agent Creation & Testing")
    print("-" * 30)
    
    test_cases = [
        {
            "agent_name": "business",
            "version": "1.0.0", 
            "query": "Look up customer CUST001 and check laptop inventory"
        },
        {
            "agent_name": "science",
            "version": "2.0.0",
            "query": "Convert 100 mph to m/s and predict the reaction between H2 and O2"
        },
        {
            "agent_name": "consultant", 
            "version": "1.0.0",
            "query": "Calculate the kinetic energy for mass=5kg, velocity=10m/s, then check inventory for mouse"
        }
    ]
    
    for test in test_cases:
        try:
            print(f"\\n   Testing {test['agent_name']} v{test['version']}:")
            agent = registry.create_agent_instance(test["agent_name"], test["version"])
            
            response = agent.chat(test["query"])
            print(f"   Query: {test['query']}")
            print(f"   Response: {response[:100]}..." if len(response) > 100 else f"   Response: {response}")
            
        except Exception as e:
            print(f"   Error testing {test['agent_name']}: {e}")
    
    # 4. Agent card inspection
    print("\\n📄 Step 4: Agent Card Details")
    print("-" * 30)
    
    business_card = registry.get_agent_card("business", "1.0.0")
    if business_card:
        print(f"Agent Card: {business_card.name} v{business_card.version}")
        print(f"  Description: {business_card.description}")
        print(f"  Domain: {business_card.domain}")
        print(f"  Status: {business_card.status.value}")
        print(f"  Tools: {business_card.tools}")
        print(f"  Created: {business_card.created_at}")
        print(f"  Config Hash: {business_card.config_hash}")
    
    # 5. Command system demonstration
    print("\\n⚡ Step 5: Command System")
    print("-" * 30)
    
    try:
        business_agent = registry.create_agent_instance("business", "1.0.0")
        commands = business_agent.list_commands()
        print(f"Available commands: {commands}")
        
        # Execute a command directly
        if "/help" in commands:
            help_result = business_agent.execute_command("/help")
            print(f"Help command result: {help_result[:200]}...")
            
    except Exception as e:
        print(f"Command system error: {e}")
    
    # 6. Toolbox integration demonstration
    print("\n🧰 Step 6: Toolbox Integration")
    print("-" * 30)
    
    print("Generating custom tool for business agent...")
    success, message, tool = generate_tool(
        "Calculate customer lifetime value (CLV) based on average purchase, frequency, and years",
        category="business"
    )
    
    if success:
        print(f"✅ {message}")
        
        # Add to business agent
        try:
            business_agent = registry.create_agent_instance("business", "1.0.0")
            business_agent.add_tool(tool)
            print(f"Tool added to business agent. Total tools: {len(business_agent.list_tools())}")
        except Exception as e:
            print(f"Business agent integration: {e}")
    
    # Show toolbox capabilities
    toolbox = get_toolbox()
    assistant = ToolAssistant()
    
    print("\nSuggesting tools for task...")
    suggestions = assistant.suggest_tools_for_task("I need to analyze customer orders and inventory")
    if suggestions:
        print(f"Found {len(suggestions)} relevant existing tools:")
        for sugg in suggestions[:3]:
            print(f"  • {sugg['name']} - {sugg['description'][:50]}...")
    
    print("\n✅ Protocol demonstration complete!")
    print("\n🚀 To run the full API server:")
    print("   python main.py server")
    print("\n📚 API docs will be available at:")
    print("   http://localhost:8000/docs")


def demonstrate_api_usage():
    """Show how to use the protocol via REST API."""
    
    print("\\n🌐 REST API Usage Examples")
    print("=" * 40)
    
    api_examples = [
        {
            "name": "List All Agents",
            "method": "GET",
            "url": "http://localhost:8000/agents",
            "description": "Get list of all registered agents"
        },
        {
            "name": "Chat with Business Agent", 
            "method": "POST",
            "url": "http://localhost:8000/chat",
            "body": {
                "message": "Look up customer CUST001",
                "agent_name": "business",
                "agent_version": "1.0.0",
                "session_id": "user123"
            },
            "description": "Send message to business agent"
        },
        {
            "name": "Execute Command",
            "method": "POST", 
            "url": "http://localhost:8000/command",
            "body": {
                "command": "calc",
                "agent_name": "math",
                "agent_version": "3.0.0",
                "parameters": {"expression": "sin(pi/2)"}
            },
            "description": "Execute math command directly"
        },
        {
            "name": "Get Agent Info",
            "method": "GET", 
            "url": "http://localhost:8000/agents/business?version=1.0.0",
            "description": "Get detailed info about business agent"
        },
        {
            "name": "List Agent Tools",
            "method": "GET",
            "url": "http://localhost:8000/agents/business/tools",
            "description": "Get all tools available to business agent"
        }
    ]
    
    for example in api_examples:
        print(f"\\n📡 {example['name']}")
        print(f"   {example['method']} {example['url']}")
        if 'body' in example:
            import json
            print(f"   Body: {json.dumps(example['body'], indent=2)}")
        print(f"   Purpose: {example['description']}")
        
        # Generate curl command
        if example['method'] == 'GET':
            print(f"   curl \"{example['url']}\"")
        else:
            body_str = json.dumps(example['body']) if 'body' in example else '{}'
            print(f"   curl -X {example['method']} \"{example['url']}\" \\\\")
            print(f"        -H \"Content-Type: application/json\" \\\\")
            print(f"        -d '{body_str}'")


def main():
    """Run the complete protocol demonstration."""
    
    print("🎭 Complete Protocol System Demonstration")
    print("=" * 50)
    
    # Run async demonstration
    asyncio.run(demonstrate_protocol_system())
    
    # Show API usage examples
    demonstrate_api_usage()
    
    print("\\n🎯 Next Steps:")
    print("1. Run 'python main.py server' to start the protocol server")
    print("2. Visit http://localhost:8000/docs for interactive API documentation")
    print("3. Try the curl commands above to interact with agents via REST API")
    print("4. Create your own agents using the @register_agent decorator")
    print("5. Add custom tools and commands for your specific domain")


if __name__ == "__main__":
    main()