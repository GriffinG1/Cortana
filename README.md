# Cortana
A discord.py module for logging.

## Config options
The config will be automatically created the first time the module is loaded. Each setting is defined below.

### options

#### enable_logger
Boolean value on if the logger should be running or not. Can be changed via toggle_logger, provided your user id is allowed.

#### log_moderator_actions
Boolean value on if the logger should log mod actions such as kicks, bans, role changes, channel creation/deletion, etc. This may be split up into multiple options later.

#### authorized_users
A list of user ids of users who are authorized to use certain bot commands, such as toggle_logger.

### config_version
This defines the current version of the config, and should not be changed by the end user.

### guild
This is the guild that the logger will be operating on. For simplicity's sake, at this time the module is restricted to a single guild.