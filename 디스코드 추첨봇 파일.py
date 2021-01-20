import asyncio
import random
import discord
from discord.ext import commands


class Lottery:
    def __init__(self, owner):
        self.owner = owner
        self.signup = []

    def addUser(self, user):
        self.signup.append(user)

    def draw(self):
        return lotto_winner.format(random.choice([x.mention for x in self.signup]), 100 * 1 / len(self.signup))

lottos = []
lotto_emoji = '✅'
lotto_winner = '{}님이 {}%의 확률을 뚫고 이벤트에 당첨되셨습니다! 축하드립니다!'

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_reaction_add(reaction, user):
    if user.id == bot.user.id:
        return

    if reaction.message.id in [x.msg.id for x in lottos]:
        target_lotto = [x for x in lottos if x.msg.id == reaction.message.id][0]
        if reaction.emoji == lotto_emoji:
            if user in target_lotto.signup:  # already signed up
                return

            target_lotto.signup.append(user)
            signups = "\n".join([x.name for x in target_lotto.signup])

            await reaction.message.edit(content="""
{}
```
{}
```
            """.format("[{}님의 신청자 목록]".format(target_lotto.owner.mention), signups))

            try:
                await user.send("{}님의 이벤트 신청이 완료됬습니다!".format(target_lotto.owner.name))
            except:
                print("Failed to send DM " + user.name)

@bot.command()
async def 이벤트시작(ctx):
    if ctx.author in [x.owner for x in lottos]:
        await ctx.channel.send("{}님은 이미 진행중인 이벤트가 있습니다".format(ctx.author.mention))
        return

    print("New lottery by " + ctx.author.name)

    new_lotto = Lottery(ctx.author)
    new_lotto.msg = await ctx.channel.send("[{}님의 이벤트신청자 목록]".format(new_lotto.owner.mention))
    await new_lotto.msg.add_reaction(lotto_emoji)
    lottos.append(new_lotto)

@bot.command()
async def 이벤트마감(ctx):
    if ctx.author.id in [x.owner.id for x in lottos]:
        target_lotto = [x for x in lottos if x.owner.id == ctx.author.id][0]
        if len(target_lotto.signup) == 0:
            await ctx.channel.send("신청자가 없습니다!".format(ctx.author.mention))
            return

        winner = random.choice([x.mention for x in target_lotto.signup])
        await target_lotto.msg.channel.send(
            "{}님의 추첨 - {}님이 {}%의 확률을 뚫고 이벤트에 당첨되셨습니다! 축하드립니다!".format(target_lotto.owner.mention, winner, 100 * 1 / len(target_lotto.signup)))
        lottos.remove(target_lotto)

        print("Lottery by " + target_lotto.owner.name + " ended. " + winner.name + " won.")
    else:
        await ctx.channel.send("{}님은 진행중인 이벤트가 없습니다".format(ctx.author.mention))


bot.run('ODAwMjYwOTg1NjM3NDM3NDgw.YAPjHw.yI1G5g9vUFHaDkTsPyMAMXa47ko')
