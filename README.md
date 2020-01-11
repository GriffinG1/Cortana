# Cortana
A [discord.py](https://github.com/Rapptz/discord.py) module for logging.

## Config options
The config will be automatically created the first time the module is loaded. Each setting is defined below.

### options

#### enable_logger
Boolean value on if the logger should be running or not. Can be changed via toggle_logger, provided your user id is allowed.

#### log_moderator_actions
Boolean value on if the logger should log mod actions such as kicks, bans, role changes, channel creation/deletion, etc. This may be split up into multiple options later.

#### log_all_messages
Boolean value on if the logger should log all messages or not. If false, only logs deleted messages

#### authorized_users
A list of user ids of users who are authorized to use certain bot commands, such as toggle_logger.

### config_version
This defines the current version of the config, and should not be changed by the end user.

### guild
This is the guild that the logger will be operating on. For simplicity's sake, at this time the module is restricted to a single guild.

## Commands
All commands, unless noted otherwise, require the user to be an authorized user.

### setguild
Usage: `[p]setguild <id>`  
Sets the value at `config["guild"]` to id. Will only allow guilds that the bot is part of.

### authusers
Usage: `[p]authusers`, `[p]authusers add <id>`, `[p]authusers remove <id>`  
Group command that handles adding, removing, and displaying authorized users.
- **authusers**: This command will display all authorized users.
- **add**: This will add a valid user ID to the authorized users list.
- **remove**: This will remove a valid user ID from the authorized users list. If the list is fully emptied, my user ID will be automatically added to prevent lockouts. In addition, a user cannot deauthorize themselves.