# LINE Trading Bot

A LINE messaging bot that provides trading and wallet functionality, built with Flask and the LINE Messaging API.

## Features

- LINE Bot webhook integration
- Ethereum wallet creation and management
- Trading interface
- Interactive menu system with carousel messages
- Status page dashboard

## Prerequisites

- Python 3.7+
- LINE Messaging API credentials
- Environment variables setup

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```plaintext
LINE_CHANNEL_SECRET=your_channel_secret
LINE_CHANNEL_ACCESS_TOKEN=your_channel_access_token
LINE_BASIC_ID=your_basic_id
SESSION_SECRET=your_session_secret
```

## Project Structure

```plaintext
├── main.py                 # Application entry point
├── app.py                  # Flask application and routes
├── config.py              # Configuration management
├── line_bot.py            # LINE Bot message handling
├── wallet_handler.py      # Wallet management
├── static/
│   └── css/
│       └── custom.css     # Custom styling
└── templates/
    ├── index.html         # Status page
    └── trading.html       # Trading interface
```

## Running the Application

1. Ensure all environment variables are set
2. Run the application:

```bash
python main.py
```

The server will start on `http://0.0.0.0:5000`

## Endpoints

- `/` - Status page showing bot information
- `/callback` - LINE webhook endpoint
- `/trading/<user_id>` - Trading interface for specific user

## LINE Bot Commands

- `hi`, `hello`, `hey` - Get greeting message with trading menu
- `create wallet` - Create new Ethereum wallet
- `show wallet` - Display wallet information
- Other commands trigger the trading menu

## Development

The application runs in debug mode by default. For production deployment, modify the following in `main.py`:

```python
app.run(host="0.0.0.0", port=5000, debug=False)
```

## Security Notes

- Current wallet storage is in-memory and for demonstration purposes only
- For production, implement secure database storage
- Never expose private keys in production environment
- Use HTTPS in production

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
