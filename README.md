# Sample Agent + MCP Server (+ SDK + A2A)

This repository now includes three tracks you can test:

1. Raw MCP (no external SDK required): a hand-rolled MCP-style server/client.
2. MCP Python SDK: a server/client implemented with the official `mcp` package.
3. A2A: a minimal Agent2Agent server/client using `a2a-sdk`.

## What This Project Does

The project demonstrates how an agent process can call tools exposed by another process.

- In MCP examples, the server runs over `stdio` and responds to JSON-RPC requests.
- In A2A examples, the server exposes an HTTP endpoint and the client sends agent messages.

Both patterns show the same core flow:

1. Start a server that advertises capabilities.
2. Connect from an agent/client.
3. Call one or more tools/actions.
4. Receive structured results.

## Included Tools

The MCP server includes these tools:

- `echo(text)`: returns your text.
- `search_files(pattern)`: regex search in text files under the current directory (up to 20 matches).

## Files

- `mcp_server.py`: raw MCP-style stdio server (`initialize`, `tools/list`, `tools/call`).
- `sample_agent.py`: raw MCP-style agent/client with interactive chat loop.
- `sdk_mcp_server.py`: MCP server built with official Python MCP SDK (`FastMCP`).
- `sdk_agent.py`: MCP agent/client built with official Python MCP SDK.
- `a2a_server.py`: A2A server sample (HTTP) using `a2a-sdk`.
- `a2a_client.py`: A2A client sample sending a message to `a2a_server.py`.

## Requirements

- Python 3.10+
- `make` (optional, for shortcut commands)

Optional frameworks:

- For MCP SDK examples: `pip install "mcp[cli]"`
- For A2A examples: `pip install a2a-sdk uvicorn httpx`

## 1) Run Raw MCP Sample (No Extra Dependencies)

```bash
python3 sample_agent.py
```

Or:

```bash
make mcp
```

What happens:

1. Agent starts `mcp_server.py`.
2. Agent sends `initialize`.
3. Agent lists tools.
4. Agent runs one sample `echo` call.
5. Agent enters interactive mode.

Interactive commands:

- `/echo <text>`
- `/search <regex>`
- `/tools`
- `/quit`

Free text without a slash defaults to `echo`.

## 2) Run MCP SDK Sample

Install dependency:

```bash
pip install "mcp[cli]"
```

Or:

```bash
make install-mcp-sdk
```

Run:

```bash
python3 sdk_agent.py
```

Or:

```bash
make mcp-sdk
```

What happens:

1. `sdk_agent.py` launches `sdk_mcp_server.py` via stdio transport.
2. Client initializes session.
3. Client lists tools.
4. Client calls `echo` and `search_files`.

## 3) Run A2A Sample

Install dependencies:

```bash
pip install a2a-sdk uvicorn httpx
```

Or:

```bash
make install-a2a
```

Start A2A server (terminal 1):

```bash
python3 a2a_server.py
```

Or:

```bash
make a2a-server
```

Call with A2A client (terminal 2):

```bash
python3 a2a_client.py
```

Or:

```bash
make a2a-client
```

You can also use:

```bash
make a2a
```

This is an alias for `make a2a-server`.

What happens:

1. A2A server starts on `http://localhost:9999`.
2. Client sends a message.
3. Server responds with an echoed artifact payload.

## Notes

- Raw MCP scripts are fully self-contained and already verified locally in this repo.
- SDK/A2A scripts include dependency checks and print install instructions if packages are missing.
- `search_files` intentionally skips non-UTF8 files and hidden dotfiles, and limits output size.
