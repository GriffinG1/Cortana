""" logger.py - A simple discord.py logger. Settings can be modified in logger_config.json. See readme at https://github.com/GriffinG1/Cortana for info on usage
    Copyright (C) 2020  GriffinG1

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>."""

import discord
import os
import json
from datetime import datetime
from discord.ext import commands

CURR_CONFIG_VERSION = "1.0.0"
CONFIG_CONTENTS = {  # Allows me to expand this later if I choose
    "options": {
        "enable_logger": True,
        "log_moderator_actions": True,
        "authorized_users": [0, 0]
    },
    "config_version": CURR_CONFIG_VERSION,
    "guild": 0
}


class Logger(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        if not os.path.exists("logger_config.json"):
            with open("logger_config.json", "w") as f:
                json.dump(CONFIG_CONTENTS, f, indent=4)
        with open("logger_config.py" "r") as f:
            self.config = json.load(f)
        if self.config["config_version"] != CURR_CONFIG_VERSION:
            print("Logger config is outdated. Replacing config with latest...")
            with open("logger_config.json", "w") as f:
                temp_config = CONFIG_CONTENTS
                try:
                    temp_config["guild"] = self.config["guild"]
                except KeyError:
                    print("Could not set 'guild'. Defaulting to 0. Logger will not run until a guild is provided and module is reloaded.")
                    temp_config["guild"] = 0
                for item in self.config["options"]:
                    try:
                        temp_config[item] = self.config["options"][item]
                    except KeyError:
                        print(f"Could not set '{item}' as it has been deprecated.")
                self.config = temp_config
                json.dump(temp_config, f, indent=4)
                print("Finished replacing config. Please verify your settings.")
        self.enable_logging = self.config["options"]["enable_logger"]
        self.log_mod_actions = self.config["options"]["log_moderator_actions"]
        if not os.path.isdir("saves/{}".format(self.config["guild"])):
            os.mkdir("saves/{}".format(self.config["guild"]))
        self.path = os.path.dirname(os.path.realpath(__file__))
        self.path = os.path.join(self.path, "saves/{}".format(self.config["guild"]))
        print(f"Current logging state is: {self.enable_logging}.")
        print(f"Current moderator action logging state is: {self.log_mod_actions}")
        print(f"Active storage path: {self.path}")


def setup(bot):
    bot.add_cog(Logger(bot))
