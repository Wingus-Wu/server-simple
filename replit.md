# Roblox Messaging Server

## Overview
A Flask-based RESTful API server designed to handle chat/messaging for Roblox games. The server receives messages from Roblox clients via HTTP requests, stores them temporarily in memory, and provides endpoints for retrieving messages. It also includes an automatic reply system that greets players when they send messages.

## Project Status
**Created:** November 22, 2025  
**Status:** MVP Complete  
**Technology:** Python 3.11, Flask, Flask-CORS

## Features
- RESTful API endpoints for message sending and retrieval
- In-memory message storage with timestamp tracking
- Automatic server replies with personalized greetings
- CORS enabled for cross-origin requests from Roblox
- Message filtering by player name or time range
- Thread-safe message operations
- Web-based test interface for API testing
- Auto-refreshing message display

## Project Structure
```
.
├── main.py              # Flask server with API endpoints
├── static/
│   └── test.html       # Web test interface for API
├── .gitignore          # Python gitignore configuration
└── replit.md           # This documentation file
```

## API Endpoints

### GET /
Serves the web-based test interface

### GET /api
Returns server status and available endpoints

### POST /api/send
Send a message from a Roblox client
- **Request Body:** 
  ```json
  {
    "player_name": "PlayerName",
    "message": "Message text"
  }
  ```
- **Response:**
  ```json
  {
    "success": true,
    "message": {...},
    "auto_reply": {...}
  }
  ```

### GET /api/messages
Retrieve all messages
- **Query Parameters:**
  - `limit` (optional): Maximum number of messages to return
  - `since` (optional): ISO timestamp to get messages after
- **Response:**
  ```json
  {
    "success": true,
    "count": 10,
    "messages": [...]
  }
  ```

### GET /api/messages/<player_name>
Get messages for a specific player
- **Query Parameters:**
  - `limit` (optional): Maximum number of messages to return
- **Response:**
  ```json
  {
    "success": true,
    "player_name": "PlayerName",
    "count": 5,
    "messages": [...]
  }
  ```

### POST /api/clear
Clear all stored messages
- **Response:**
  ```json
  {
    "success": true,
    "message": "All messages cleared"
  }
  ```

## Roblox Integration

### Example Roblox Script (HttpService)
```lua
local HttpService = game:GetService("HttpService")
local SERVER_URL = "https://your-replit-url.repl.co"

-- Send a message
local function sendMessage(playerName, messageText)
    local data = {
        player_name = playerName,
        message = messageText
    }
    
    local success, response = pcall(function()
        return HttpService:PostAsync(
            SERVER_URL .. "/api/send",
            HttpService:JSONEncode(data),
            Enum.HttpContentType.ApplicationJson
        )
    end)
    
    if success then
        local result = HttpService:JSONDecode(response)
        print("Message sent! Auto-reply:", result.auto_reply.message)
        return result
    else
        warn("Failed to send message:", response)
        return nil
    end
end

-- Fetch messages
local function getMessages(limit)
    local url = SERVER_URL .. "/api/messages"
    if limit then
        url = url .. "?limit=" .. tostring(limit)
    end
    
    local success, response = pcall(function()
        return HttpService:GetAsync(url)
    end)
    
    if success then
        local result = HttpService:JSONDecode(response)
        return result.messages
    else
        warn("Failed to get messages:", response)
        return nil
    end
end

-- Usage
sendMessage("Player123", "Hello from Roblox!")
local messages = getMessages(10)
```

**Important:** Enable HTTP requests in your Roblox game:
1. Open Game Settings in Roblox Studio
2. Go to Security tab
3. Enable "Allow HTTP Requests"

## Configuration

### Message Storage
- Maximum messages stored: 1000 (older messages are automatically removed)
- Storage type: In-memory (resets on server restart)
- Thread-safe: Yes (uses threading.Lock)

### Server Settings
- Host: 0.0.0.0 (all interfaces)
- Port: 5000
- CORS: Enabled for all origins
- Debug mode: Disabled (production-ready)

## Testing
1. Open the deployed URL in your browser to access the test interface
2. Enter a player name and message
3. Click "Send Message" to test the API
4. View messages in real-time (auto-refreshes every 5 seconds)
5. Use the "Clear All" button to reset message storage

## Architecture Decisions

### In-Memory Storage
- **Why:** Simple, fast, and sufficient for temporary messaging
- **Trade-off:** Messages are lost on server restart
- **Future:** Can be upgraded to database storage if persistence is needed

### Automatic Replies
- **Implementation:** Server automatically responds with "Hello <player>!" to every message
- **Customization:** Can be modified in the `send_message()` function in main.py
- **Future:** Can be enhanced with AI-powered responses or rule-based logic

### Thread Safety
- **Why:** Multiple Roblox clients may send requests simultaneously
- **Implementation:** Threading locks protect message list operations
- **Benefit:** Prevents race conditions and data corruption

## Future Enhancements
- Add database persistence for message history
- Implement message channels/rooms for organized conversations
- Add rate limiting to prevent spam
- Create admin dashboard for monitoring
- Add webhook support for real-time notifications
- Implement player authentication/authorization
- Add message filtering and moderation features

## User Preferences
None specified yet.

## Recent Changes
- **2025-11-22:** Initial project setup with Flask server, API endpoints, auto-reply system, and test interface
