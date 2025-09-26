# Discord Bot

A basic Discord bot written in Python using the discord.py library.

## Features

- **Basic Commands**: Hello, ping, bot info, and user info commands
- **Message Handling**: Responds to user messages and commands
- **Error Handling**: Graceful error handling for common command errors
- **Embeds**: Rich embedded messages for better presentation
- **Status Display**: Shows bot activity status

## Commands

- `!hello` - Say hello to the user
- `!ping` - Check bot latency
- `!info` - Display bot information
- `!say <message>` - Make the bot repeat a message
- `!userinfo [@user]` - Get detailed information about a user including roles and timestamps (defaults to command author)
- `!doakes` - Get a random Sergeant Doakes GIF from Dexter TV series
- `!delete <amount> [@user]` - Delete messages (requires Manage Messages permission)
- `!addrole @user <role>` - Add role to user (requires Manage Roles permission)
- `!removerole @user <role>` - Remove role from user (requires Manage Roles permission)  
- `!listroles [@user]` - List server roles or user's roles
- `!help` - Show all available commands (built-in)

## Setup Instructions

### 1. Prerequisites

- Python 3.8 or higher
- A Discord account
- A Discord server where you can add bots (or admin permissions)

### 2. Create a Discord Application

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Go to the "Bot" section in the left sidebar
4. Click "Add Bot"
5. Under "Token", click "Copy" to copy your bot token
6. Under "Privileged Gateway Intents", enable "Message Content Intent"

### 3. Invite Bot to Server

1. In the Discord Developer Portal, go to the "OAuth2" > "URL Generator" section
2. Under "Scopes", select "bot"
3. Under "Bot Permissions", select the permissions your bot needs:
   - Send Messages
   - Read Message History
   - Use Slash Commands (optional)
   - Embed Links
   - Attach Files (if needed)
4. Copy the generated URL and visit it to invite the bot to your server

### 4. Install Dependencies

```bash
# Navigate to the project directory
cd discord-bot

# Install required packages
pip install -r requirements.txt
```

### 5. Configure Environment Variables

1. Copy the example environment file:
   ```bash
   copy .env.example .env
   ```

2. Edit the `.env` file and add your bot token:
   ```
   DISCORD_TOKEN=your_actual_bot_token_here
   COMMAND_PREFIX=!
   ```

### 6. Run the Bot

```bash
python bot.py
```

You should see a message indicating the bot has connected to Discord successfully.

## Railway Deployment (Recommended for 24/7 hosting)

This bot is ready for deployment on [Railway](https://railway.app), a modern hosting platform perfect for Discord bots.

### Quick Deploy to Railway

1. **Fork this repository** or use your own copy

2. **Sign up for Railway** at [railway.app](https://railway.app)

3. **Create a new project**:
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose this repository

4. **Set environment variables** in Railway dashboard:
   - Go to your project settings
   - Click "Variables" tab
   - Add `DISCORD_TOKEN` with your bot token value
   - Optionally add `COMMAND_PREFIX` (defaults to `!`)

5. **Deploy**: Railway will automatically build and deploy your bot!

### Railway Features Used

- **Procfile**: Specifies how to run the bot (`web: python bot.py`)
- **railway.json**: Configuration for build and deployment settings
- **Automatic restarts**: Bot will restart automatically if it crashes
- **Logging**: All bot activity is logged and viewable in Railway dashboard
- **Environment variables**: Secure token storage

### Railway Environment Variables

| Variable | Description | Required |
|----------|-------------|-----------|
| `DISCORD_TOKEN` | Your Discord bot token | ✅ Yes |
| `COMMAND_PREFIX` | Command prefix (default: `!`) | ❌ Optional |
| `BACK_ACCESS_USER_ID` | User ID for back access command | ❌ Optional |

### Monitoring Your Bot on Railway

- **Logs**: View real-time logs in the Railway dashboard
- **Metrics**: Monitor CPU, memory, and network usage
- **Deployments**: Track deployment history and rollback if needed
- **Settings**: Modify environment variables and deployment settings

## Project Structure

```
discord-bot/
├── bot.py              # Main bot file
├── requirements.txt    # Python dependencies
├── .env.example       # Environment variables template
├── .env              # Your actual environment variables (not in git)
├── .gitignore        # Git ignore file
├── Procfile          # Railway deployment configuration
├── railway.json      # Railway build and deploy settings
└── README.md         # This file
```

## Customization

### Adding New Commands

To add a new command, use the `@bot.command()` decorator:

```python
@bot.command(name='mycommand')
async def my_command(ctx, arg1, arg2):
    """Description of what the command does"""
    await ctx.send(f'You said: {arg1} and {arg2}')
```

### Changing the Command Prefix

Edit the `COMMAND_PREFIX` in your `.env` file:

```
COMMAND_PREFIX=?
```

### Adding Event Handlers

You can add more event handlers using `@bot.event`:

```python
@bot.event
async def on_member_join(member):
    """Event triggered when a new member joins the server"""
    channel = member.guild.system_channel
    if channel is not None:
        await channel.send(f'Welcome {member.mention}!')
```

## Troubleshooting

### Common Issues

1. **"Invalid token" error**: Make sure your bot token in the `.env` file is correct
2. **Bot doesn't respond**: Ensure "Message Content Intent" is enabled in the Discord Developer Portal
3. **Permission errors**: Make sure the bot has the necessary permissions in your Discord server
4. **Import errors**: Make sure you've installed all dependencies with `pip install -r requirements.txt`

### Logging

The bot includes basic logging that prints to the console. You can modify the logging behavior in the `on_message` and `on_command_error` functions.

## Security Notes

- Never share your bot token publicly
- The `.env` file is ignored by git to prevent accidental commits
- Consider using a virtual environment for Python packages

## Contributing

Feel free to fork this project and add your own features! Some ideas for improvements:

- Database integration for persistent data
- More advanced commands and features
- Music playback capabilities
- Moderation tools
- Integration with external APIs

## License

This project is open source and available under the MIT License.