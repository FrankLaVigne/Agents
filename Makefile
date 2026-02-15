PYTHON ?= python3

.PHONY: help mcp mcp-sdk a2a a2a-server a2a-client acp acp-server acp-client install-mcp-sdk install-a2a install-acp

help:
	@echo "Targets:"
	@echo "  make mcp           - Run raw MCP sample agent"
	@echo "  make install-mcp-sdk - Install MCP SDK dependency"
	@echo "  make mcp-sdk       - Run MCP SDK sample agent"
	@echo "  make install-a2a   - Install A2A sample dependencies"
	@echo "  make a2a-server    - Start A2A server on localhost:9999"
	@echo "  make a2a-client    - Run A2A client against localhost:9999"
	@echo "  make a2a           - Alias for make a2a-server"
	@echo "  make install-acp   - Install ACP sample dependencies"
	@echo "  make acp-server    - Start ACP server on localhost:8001"
	@echo "  make acp-client    - Run ACP client against localhost:8001"
	@echo "  make acp           - Alias for make acp-server"

mcp:
	$(PYTHON) mcp/raw/sample_agent.py

install-mcp-sdk:
	$(PYTHON) -m pip install "mcp[cli]"

mcp-sdk:
	$(PYTHON) mcp/sdk/sdk_agent.py

install-a2a:
	$(PYTHON) -m pip install a2a-sdk uvicorn httpx

a2a-server:
	$(PYTHON) a2a/a2a_server.py

a2a-client:
	$(PYTHON) a2a/a2a_client.py

a2a: a2a-server

install-acp:
	$(PYTHON) -m pip install acp-sdk uvicorn httpx

acp-server:
	$(PYTHON) acp/acp_server.py

acp-client:
	$(PYTHON) acp/acp_client.py

acp: acp-server
