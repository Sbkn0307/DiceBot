import discord
from discord.ext import commands
from discord import app_commands

from keep_alive import keep_alive

import random

from config import TOKEN
from dice import DiceEvaluator

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

dice = DiceEvaluator()

keep_alive()

@bot.event
async def on_ready():

    await bot.tree.sync()
    print(bot.user)


@bot.event
async def on_message(message):

    if message.author.bot:
        return

    text = message.content.strip()

    if text.startswith("!"):

        expr = text[1:]

        try:

            result, logs = dice.evaluate(expr)

            embed = discord.Embed(
                title="🎲 ダイス結果",
                color=0x00AAFF
            )

            embed.add_field(
                name="入力",
                value=f"`{expr}`",
                inline=False
            )

            embed.add_field(
                name="ダイス",
                value="\n".join(logs),
                inline=False
            )

            embed.add_field(
                name="結果",
                value=str(result),
                inline=False
            )

            await message.reply(embed=embed)

        except Exception as e:
            await message.reply(f"エラー\n{e}")

    await bot.process_commands(message)


@bot.tree.command(
    name="choose",
    description="ランダム選択"
)
@app_commands.describe(
    elements="要素をカンマ区切りで入力",
    duplicate="重複を許可",
    count="選択回数"
)
async def choose(
        interaction: discord.Interaction,
        elements: str,
        duplicate: bool = True,
        count: int = 1
):

    items = [
        x.strip()
        for x in elements.split(",")
        if x.strip()
    ]

    if len(items) == 0:
        await interaction.response.send_message("要素がありません")
        return

    if duplicate:

        result = [
            random.choice(items)
            for _ in range(count)
        ]

    else:

        if count > len(items):

            await interaction.response.send_message(
                "重複なしでは要素数を超えて選択できません"
            )
            return

        result = random.sample(
            items,
            count
        )

    embed = discord.Embed(
        title="🎲 Choose",
        color=0x00AAFF
    )

    embed.add_field(
        name="結果",
        value="\n".join(
            f"{i+1}. {v}"
            for i, v in enumerate(result)
        ),
        inline=False
    )

    await interaction.response.send_message(embed=embed)


@bot.tree.command(
    name="help",
    description="ヘルプ"
)
async def help_command(interaction: discord.Interaction):

    embed = discord.Embed(
        title="ダイスBot Help",
        color=0x00AAFF
    )

    embed.add_field(
        name="ダイス",
        value=
        """
`!1d100`

`!2d6+3`

`!(2d100+4d50)*1d100/1d6`
""",
        inline=False
    )

    embed.add_field(
        name="/choose",
        value=
        """
要素をランダムに選択します。

例
