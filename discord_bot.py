import discord
from discord import app_commands
from discord.ext import commands
from subprocess import run
import os


bot = commands.Bot(command_prefix="!", intents = discord.Intents.all())

# Program path (use os.path.join for platform independence)
program_path = os.path.join(os.getcwd(), "get_matches.py")  # Replace with your actual file

async def execute_program(program):
    python_exe = "python.exe"  # Path to the Python interpreter
    # Run the program and capture output/errors
    try:
        result = run([python_exe, program], capture_output=True, text=True)
        output, error = result.stdout, result.stderr
    except Exception as e:
        error = f"Error running program: {e}"
        output = ""
    return output, error

async def send_message_to_all_servers(output, channel_name):
    # Iterate over all guilds the bot is a member of
    for guild in bot.guilds:
        # Get the channel by name or ID
        channel = discord.utils.get(guild.channels, name=channel_name) or guild.get_channel(int(channel_name))
        if channel is not None:
            try:
                await channel.send(f"```{output}```")
            except Exception as e:
                print(f"Error sending message to {guild.name}: {e}")

async def run_daily_task(channel_name):
    # Execute the program and get output/error
    output, error = await execute_program(program_path)

    # Handle errors or send output
    if error:
        print(error)
    else:
        # Send the output to all servers
        await send_message_to_all_servers(output, channel_name)

# Schedule the daily task to run at 12:00 PM UTC (adjust the time as needed)
schedule.every().day.at("06:00").do(asyncio.run, run_daily_task("betskins"))

# /getgames command - main output
@bot.tree.command(name="upcominggames")
async def get_matches(interaction: discord.Interaction):
  # Execute the program and get output/error
  output, error = await execute_program(program_path)

  # Handle errors or send output
  if error:
    await interaction.response.send_message(error, ephemeral=True)
  else:
    # Optionally format the output (e.g., using code blocks)
    formatted_output = f'''{output}'''
    await interaction.response.send_message(formatted_output, ephemeral=False)

# Start the bot and sync commands
@bot.event
async def on_ready():
	print("Bot is up and ready!")
	try:
		synced = await bot.tree.sync()
		print(f"Synced {len(synced)} command(s)")

	except Exception as e:
		print(e)

# /hello command - for testing
@bot.tree.command(name="hello")
async def hello(interatcion: discord.Interaction):
	await interatcion.response.send_message(f"Hey {interatcion.user.name}! Nice command you got there.", ephemeral=True)

bot.run('Add token here')
