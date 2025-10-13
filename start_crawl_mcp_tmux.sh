#!/bin/bash
# Start Crawl MCP server in tmux session

PROJECT_DIR="/home/milhy777/Develop/Development/crawl-mcp"
SESSION_NAME="crawl-mcp-server"

# Check if tmux session already exists
tmux has-session -t $SESSION_NAME 2>/dev/null

if [ $? == 0 ]; then
    echo "Tmux session '$SESSION_NAME' already exists. Attaching to it."
    tmux attach -t $SESSION_NAME
else
    echo "Starting new tmux session '$SESSION_NAME' for crawl-mcp server."
    tmux new-session -d -s $SESSION_NAME "cd $PROJECT_DIR && source venv/bin/activate && python -m uvicorn app.main:app --host 0.0.0.0 --port 8012"
    echo "Server started in tmux session '$SESSION_NAME'. To attach, run: tmux attach -t $SESSION_NAME"
    echo "To detach, press Ctrl+B then D."
    echo "To stop the server, attach to the session and press Ctrl+C."
fi
