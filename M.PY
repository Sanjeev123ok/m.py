from telethon import TelegramClient, events, Button
import asyncio
import random

# Replace with your values
bot_token = '7521932275:AAH6PZHYdzRiNR_690jWTW-ovmxzcwRq4zc'

client = TelegramClient('reaction_bot_buttons', (bot_token=bot_token)

# Initial config
config = {
    'channel': None,
    'reactions': ['❤️', '🔥', '😂'],
    'min_react': 1,
    'max_react': 3,
    'post_count': 5
}

# --- Start Handler with Buttons ---
@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond(
        "Welcome! Use the buttons below to configure reaction settings.",
        buttons=[
            [Button.inline("Set Channel", b"set_channel")],
            [Button.inline("Set Reactions", b"set_reactions")],
            [Button.inline("Set Reaction Range", b"set_range")],
            [Button.inline("Set Post Count", b"set_count")],
            [Button.inline("React Now", b"react_now")]
        ]
    )

# --- Callback Query Handler ---
@client.on(events.CallbackQuery)
async def callback(event):
    data = event.data.decode('utf-8')

    if data == "set_channel":
        await event.respond("Send me the channel username (e.g. @yourchannel):")
        client.add_event_handler(get_channel, events.NewMessage(from_users=event.sender_id))
    
    elif data == "set_reactions":
        await event.respond("Send emoji reactions separated by space (e.g. ❤️ 🔥 😂):")
        client.add_event_handler(get_reactions, events.NewMessage(from_users=event.sender_id))

    elif data == "set_range":
        await event.respond("Send min and max reaction count (e.g. 2 5):")
        client.add_event_handler(get_range, events.NewMessage(from_users=event.sender_id))

    elif data == "set_count":
        await event.respond("Send number of posts to react to (e.g. 10):")
        client.add_event_handler(get_post_count, events.NewMessage(from_users=event.sender_id))

    elif data == "react_now":
        await event.answer("Starting reactions...")
        await react_to_posts(event)

# --- Handlers for Inputs ---
async def get_channel(event):
    config['channel'] = event.raw_text.strip()
    await event.respond(f"Channel set to: {config['channel']}")
    client.remove_event_handler(get_channel)

async def get_reactions(event):
    config['reactions'] = event.raw_text.strip().split()
    await event.respond(f"Reactions set to: {' '.join(config['reactions'])}")
    client.remove_event_handler(get_reactions)

async def get_range(event):
    try:
        min_r, max_r = map(int, event.raw_text.strip().split())
        config['min_react'] = min_r
        config['max_react'] = max_r
        await event.respond(f"Range set to: {min_r} - {max_r}")
    except:
        await event.respond("Invalid input. Send two numbers like: 2 5")
    finally:
        client.remove_event_handler(get_range)

async def get_post_count(event):
    try:
        config['post_count'] = int(event.raw_text.strip())
        await event.respond(f"Post count set to: {config['post_count']}")
    except:
        await event.respond("Invalid input. Send a number like: 10")
    finally:
        client.remove_event_handler(get_post_count)

# --- Reaction Logic ---
async def react_to_posts(event):
    try:
        if not config['channel']:
            await event.respond("Please set a channel first.")
            return

        channel = await client.get_entity(config['channel'])

        async for message in client.iter_messages(channel, limit=config['post_count']):
            reaction_count = random.randint(config['min_react'], config['max_react'])
            chosen_reactions = [random.choice(config['reactions']) for _ in range(reaction_count)]

            for reaction in chosen_reactions:
                try:
                    await client.send_reaction(channel, message.id, reaction)
                    
                    
                    except Exception as e:
        print(f"Error setting reaction: {e}")
print("Bot is running...")
# Start the bot
bot.polling()
