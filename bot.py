# File: bot.py
import os
import sys
from dotenv import load_dotenv
from pytcl import TCLIntegrationManager, Interpreter
import discord
from discord.ext import commands
import logging

# Load environment variables
load_dotenv()

# Discord Bot Token
DISCORD_TOKEN = "TOKEN"

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Initialize Tcl Manager
interpreter = Interpreter()
tcl_manager = TCLIntegrationManager(interpreter)
tcl_manager.load_tcl_scripts("./modules/")

# Set up the Discord bot
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    logging.info(f"{bot.user} has connected to Discord!")
    logging.info("Available Tcl scripts:")
    for script_name in tcl_manager.list_loaded_scripts():
        logging.info(f" - {script_name}")

@bot.command(name="run_tcl", help="Executes a Tcl script. Usage: !run_tcl <script_name> [args...]")
async def run_tcl(ctx, script_name: str, *args):
    result = tcl_manager.execute_tcl_script(script_name, *args)
    await ctx.send(f"**Result:**\n{result}")

@bot.command(name="list_tcl", help="Lists all loaded Tcl scripts.")
async def list_tcl(ctx):
    scripts = tcl_manager.list_loaded_scripts()
    await ctx.send(f"**Available Tcl Scripts:**\n{', '.join(scripts)}")

@bot.command(name="hello", help="A simple Python command.")
async def hello(ctx):
    await ctx.send("Hello! This is a Python command!")

if __name__ == "__main__":
    if not DISCORD_TOKEN:
        logging.error("Discord token not set. Please configure it in the .env file.")
        exit(1)
    bot.run(DISCORD_TOKEN)
