import discord
from discord.ext import commands
import characters
import moves

TOKEN = open('token.token').read()

bot = commands.Bot(command_prefix='$')
bot.moveMessage = None

@bot.command()
async def test(ctx, *, arg):
	print(arg, arg1)
	await ctx.send('You said {}'.format(arg))

@bot.command()
async def chosen(ctx):
	chosen = characters.Load()
	#print(chosen)
	print(chosen['name'])
	print(chosen['charm'])
	embed = discord.Embed(title=chosen['name'].title())
	embed.description = str(chosen)
	await ctx.send(embed=embed)

@bot.command()
async def move(ctx):
	bot.moveMessage = moves.MovesMessage(ctx.author)
	await bot.moveMessage.Send(ctx.channel)

@bot.command()
async def logout(ctx):
	await bot.logout()
	await bot.close()

@bot.event
async def on_reaction_add(reaction, user):
	if(user != bot.user):
		if(bot.moveMessage != None):
			if(reaction.message.id == bot.moveMessage.message.id and bot.moveMessage.user == user):
				if(str(reaction) == moves.arrowLeft):
					await bot.moveMessage.Back()
				elif(str(reaction) == moves.arrowRight):
					await bot.moveMessage.Advance()
				elif(str(reaction) == moves.questionMark):
					await bot.moveMessage.ShowDetails()

if(__name__ == '__main__'):
	bot.run(TOKEN)