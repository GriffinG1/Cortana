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

MODULE_CREATOR_ID = 177939404243992578
CURR_CONFIG_VERSION = "1.0.1"
CONFIG_CONTENTS = {  # Allows me to expand this later if I choose
    "options": {
        "enable_logger": True,
        "log_moderator_actions": True,
        "log_all_messages": True,
        "authorized_users": []
    },
    "config_version": CURR_CONFIG_VERSION,
    "guild": 0
}


class Logger(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.path = os.path.dirname(os.path.realpath(__file__))
        self.config_path = os.path.join(self.path, "logger_config.json")
        if not os.path.exists(self.config_path):
            with open(self.config_path, "w") as f:
                json.dump(CONFIG_CONTENTS, f, indent=4)
            print(f"Config did not exist. Created config at {self.config_path}")
        with open(self.config_path, "r") as f:
            self.config = json.load(f)
        if self.config["config_version"] != CURR_CONFIG_VERSION:
            print("Logger config is outdated. Replacing config with latest...")
            with open(self.config_path, "w") as f:
                temp_config = CONFIG_CONTENTS
                try:
                    temp_config["guild"] = self.config["guild"]
                except KeyError:
                    print("Could not set 'guild'. Defaulting to 0. Logger will not run until a guild is provided and module is reloaded.")
                    temp_config["guild"] = 0
                for item in self.config["options"]:
                    try:
                        temp_config["options"][item] = self.config["options"][item]
                    except KeyError:
                        print(f"Could not set '{item}' as it has been deprecated.")
                self.config = temp_config
                json.dump(temp_config, f, indent=4)
                print("Finished replacing config. Please verify your settings.")
        self.enable_logging = self.config["options"]["enable_logger"]
        self.log_mod_actions = self.config["options"]["log_moderator_actions"]
        self.auth_users = self.config["options"]["authorized_users"]
        self.log_all = self.config["options"]["log_all_messages"]
        if not self.auth_users:
            print("No authorized users set in config. Defaulting to module creator.")
            self.auth_users.append(MODULE_CREATOR_ID)
        self.guild = self.config["guild"]
        if not os.path.isdir(os.path.join(self.path, "saves")):
            os.mkdir(os.path.join(self.path, "saves"))
        if not os.path.exists(os.path.join(self.path, "saves\\{}".format(self.config["guild"]))):
            os.mkdir(os.path.join(self.path, "saves\\{}".format(self.config["guild"])))
        self.storage_path = os.path.join(self.path, "saves\\{}".format(self.config["guild"]))
        auth_user_str = ", ".join(str(x) for x in self.auth_users)
        print(f"Addon \"{self.__class__.__name__}\" loaded")
        print(f"Current logging state is: {self.enable_logging}.")
        print(f"Current moderator action logging state is: {self.log_mod_actions}")
        print(f"Current log all messages state is: {self.log_all}")
        print(f"Active storage path: {self.storage_path}")
        print(f"Logged guild ID is: {self.guild}")
        print(f"Authorized user IDs are: {auth_user_str}")

    @commands.command(name="setguild")
    async def set_guild(self, ctx, id: int):
        """Sets config["guild"] to inputted ID"""
        if not ctx.author.id in self.auth_users:
            raise commands.CheckFailure
        try:
            await self.bot.fetch_guild(id)
        except discord.HTTPException:
            return await ctx.send("That's not a server!")
        self.guild = id
        self.storage_path = os.path.join(self.path, "saves\\{}".format(id))
        with open(self.config_path, "w") as f:
            json.dump(self.config, f, indent=4)
        await ctx.send(f"Set logging guild ID to `{id}`.")

    @commands.group(name="authusers")
    async def auth(self, ctx):
        """Group command for adjusting authorized users. Displays all auth users. Subcommands: add, remove"""
        if not ctx.invoked_subcommand:
            auth_users_str = ", ".join(str(x) for x in self.auth_users)
            return await ctx.send(f"Authorized user IDs: {auth_users_str}\nYou can use the subcommands `add` and `remove` to adjust authorized users.")
    
    @auth.command()
    async def add(self, ctx, id: int):
        """Adds an authorized user"""
        if not ctx.author.id in self.auth_users:
            raise commands.CheckFailure
        elif id == MODULE_CREATOR_ID and len(self.auth_users) == 1:
            self.auth_users.remove(id)
        elif id in self.auth_users:
            return await ctx.send("That user has already been added!")
        try:
            await self.bot.fetch_user(id)
        except discord.NotFound:
            return await ctx.send("That user could not be found!")
        self.auth_users.append(int(id))
        with open(self.config_path, "w") as f:
            json.dump(self.config, f, indent=4)
        await ctx.send(f"Authorized user with ID `{id}`")

    @auth.command()
    async def remove(self, ctx, id: int):
        """Removes an authorized user. If all users are removed, adds back bot creator ID."""
        if not ctx.author.id in self.auth_users:
            raise commands.CheckFailure
        elif id not in self.auth_users:
            return await ctx.send("That user isn't authorized!")
        elif id == ctx.author.id:
            return await ctx.send("As a safety measure, you cannot deauthorize yourself.")
        try:
            await self.bot.fetch_user(id)
        except discord.NotFound:
            return await ctx.send("That user could not be found!")
        self.auth_users.remove(int(id))
        with open(self.config_path, "w") as f:
            json.dump(self.config, f, indent=4)
        if len(self.auth_users) == 0:
            self.auth_users.append(MODULE_CREATOR_ID)
            return await ctx.send(f"Deauthorized user with ID `{id}`. This was the last authorized user, so the module creator was added to the RAM list.")
        await ctx.send(f"Deauthorized user with ID `{id}`.")


def setup(bot):
    bot.add_cog(Logger(bot))
