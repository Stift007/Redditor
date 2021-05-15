import discord
import praw
import asyncio
import random
from discord.ext import commands

bot = commands.Bot(case_insensitive=True,description="test", command_prefix="./")
bot.remove_command("help")

reddit = praw.Reddit(client_id='Ir3M_dfRK9IrKA',
                     client_secret='oW21vpaDtgJ7PL3RNC4oMKpCYl7bZg',
                     user_agent='REDDITOR:v0001')

async def is_nsfw(subreddit):
    with open("nsfw.dat","r+") as f:
        content = f.read()
    if subreddit.lower()+" " in content.lower():
        return True
    return False

@bot.command(help="Show a random top-voted Image from a Subreddit",usage="./reddit r/yoursubreddit")
async def Reddit(ctx,subred="funny"):
    async with ctx.channel.typing():
        try:
            subred = subred.replace("r/","")

            if await is_nsfw(subred):
                print("NSFW!")
                if ctx.channel.is_nsfw():
                    print("Sent anyways!")
                    
                else:
                    print("Stopped!")
                    return await ctx.send("Cannot send NSFW Content to non-NSFW Channel!") 

            subreddit = reddit.subreddit(subred)
            all_subs = []

            top = subreddit.hot(limit=500)

            for submission in top:
                all_subs.append(submission)

            random_sub = random.choice(all_subs)

            name = random_sub.title
            url  = random_sub.url

            embed = discord.Embed(title=name,color=discord.Color.blue())

            author = random_sub.author
            embed.description=f"Posted by {author}"
            embed.set_image(url=url)

            if subreddit.over18:
                if ctx.channel.is_nsfw:
                        
                    msg = await ctx.send(submission.url)
                else:
                    await ctx.send("Cannot send NSFW Content to non-NSFW Channel!") 

            else:
                
                msg = await ctx.send(submission.url)
        except Exception as ex:
            embed=discord.Embed(color=discord.Color.red())
            embed.add_field(name="Whooops! That didn't work!",value=f"While looking for {subred}, I encountered the following Error:\n`{ex}`")
            embed.set_thumbnail(url="https://i.redd.it/bymxf1zb4mz11.jpg")
            await ctx.send(embed=embed)

@bot.command()
async def help(ctx):
    embed = discord.Embed(title=f"Help - {ctx.guild.name}",description="A List of Commands",color=discord.Color.blurple())
    embed.add_field(name="Redditor Help Page",value="<:verified:843167819629199430> In Order to use Redditor, use the Prefix `./` followed by the Command name!",inline=False)
    embed.add_field(name="<:reddit:843167248080044072> Reddit Commands",value="`reddit r/subreddit` `meme` `dankmeme` `redditor u/Redditor`")
    embed.add_field(name=":tools: Utility Commands",value="`ping` `botinfo`")
    await ctx.send(embed=embed)

@bot.command()
async def botinfo(ctx):
    embed = discord.Embed(description="Redditor Discord Bot")
    embed.add_field(name="Bot Version",value="0.2.1")
    embed.add_field(name="Total Guilds",value=len(bot.guilds))
    embed.add_field(name="Owner",value="DS_Stift007#9780")
    embed.add_field(name="Bot Prefix",value="Default: `./` - This Server: `./`")
    embed.set_footer(text="Redditor",icon_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSIQf5LWLGSqOgFNQ5eaa075wS6naQv42eig9ZI8R8LiLtI930Oz6VJqVOD0AGwtsKtqus&usqp=CAU")
    await ctx.send(embed=embed)

loopit = True

@bot.command()
async def subscribe(ctx,subred):
    if loopit == False:
        loopit = True
    if loopit == True:
        loopit = False
        
    while loopit == True:
        async with ctx.channel.typing():
            try:
                subred = subred.replace("r/","")

                if await is_nsfw(subred):
                    print("NSFW!")
                    if ctx.channel.is_nsfw():
                        print("Sent anyways!")
                        
                    else:
                        print("Stopped!")
                        return await ctx.send("Cannot send NSFW Content to non-NSFW Channel!") 

                subreddit = reddit.subreddit(subred)
                all_subs = []

                top = subreddit.hot(limit=500)

                for submission in top:
                    all_subs.append(submission)

                random_sub = random.choice(all_subs)

                name = random_sub.title
                url  = random_sub.url

                embed = discord.Embed(title=name,color=discord.Color.blue())

                author = random_sub.author
                embed.description=f"Posted by {author}"
                embed.set_image(url=url)

                if subreddit.over18:
                    if ctx.channel.is_nsfw:
                            
                        msg = await ctx.send(submission.url)
                    else:
                        await ctx.send("Cannot send NSFW Content to non-NSFW Channel!") 

                else:
                    
                    msg = await ctx.send(submission.url)
            except Exception as ex:
                embed=discord.Embed(color=discord.Color.red())
                embed.add_field(name="Whooops! That didn't work!",value=f"While looking for {subred}, I encountered the following Error:\n`{ex}`")
                embed.set_thumbnail(url="https://i.redd.it/bymxf1zb4mz11.jpg")
                await ctx.send(embed=embed)
        await asyncio.sleep(3600)

@bot.command()
async def redditor(ctx,user_name):
    user_name = user_name.replace("u/","")
    try:
        user = Reddit.redditor(user_name)

        subreddits = user.moderated()

        subreds = ""
        for subreddit in subreddits:
            subreds += str(subreddit)+"\n"
        if not subreds:
            subreds = ":/ None"

        trophies = user.trophies()

        url = user.icon_img
        embed = discord.Embed(title="Redditor Information",color=ctx.author.color)
        embed.set_thumbnail(url=url)
        embed.add_field(name="Redditor Name",value=f"{user_name}")
        embed.add_field(name="Redditor ID",value=f"{user.id}")
        unix_time = user.created_utc
        embed.add_field(name="Account Creation",value=f"Unix Time : {str(unix_time)}\nCreated at : { str(datetime.fromtimestamp(unix_time))}")
        embed.add_field(name="Verified Email?",value=str(user.has_verified_email))
        embed.add_field(name="Employee of Reddit?",value=str(user.is_employee))
        embed.add_field(name="Active Reddit Gold?",value=str(user.is_gold))
        embed.add_field(name="Does he follow me on Reddit?",value=str(user.is_friend))
        embed.add_field(name="Comment Karma",value=str(user.comment_karma))
        embed.add_field(name="Link Karma",value=str(user.link_karma))
        embed.add_field(name="Moderated Subreddits",value=str(subreds))


        await ctx.send(embed=embed)
    except Exception as ex:
        embed=discord.Embed(color=discord.Color.red())
        embed.add_field(name="Whooops! That didn't work!",value=f"While looking for u/{user_name}, I encountered the following Error:\n`{ex}`")
        embed.set_thumbnail(url="https://i.redd.it/bymxf1zb4mz11.jpg")
        await ctx.send(embed=embed)

@bot.command(aliases=["p"])
async def ping(ctx):
    embed=discord.Embed(title="Ping!",color=ctx.author.color)
    embed.add_field(name="Bot Latency",value=f"{round(bot.latency*1000)}ms")
    await ctx.send(embed=embed)

@bot.command(help="Random, good (Cough Cough) memes",usage="./meme")
async def Meme(ctx):
    async with ctx.channel.typing():
        try:
            subred = "memes"
            subreddit = reddit.subreddit(subred)
            all_subs = []

            top = subreddit.hot(limit=500)

            for submission in top:
                all_subs.append(submission)

            random_sub = random.choice(all_subs)

            name = random_sub.title
            url  = random_sub.url

            embed = discord.Embed(title=name,color=discord.Color.blue())

            author = random_sub.author
            embed.description=f"Posted by {author}"
            embed.set_image(url=url)

            if subreddit.over18:
                if ctx.channel.is_nsfw:
                        
                    msg = await ctx.send(submission.url)
                    await msg.add_reaction('👍')
                    await msg.add_reaction('👎')
                else:
                    await ctx.send("Cannot send NSFW Content to non-NSFW Channel!") 

            else:
                
                #msg = await ctx.send(embed=embed)
                msg = await ctx.send(submission.url)
                await msg.add_reaction('👍')
                await msg.add_reaction('👎')
        except Exception as ex:
            embed=discord.Embed(color=discord.Color.red())
            embed.add_field(name="Whooops! That didn't work!",value=f"While looking for {subred}, I encountered the following Error:\n`{ex}`")
            embed.set_thumbnail(url="https://i.redd.it/bymxf1zb4mz11.jpg")
            await ctx.send(embed=embed)


@bot.command(help="The BEST (cough, cough) Dank Memes in the World",usage="./dankmeme")
async def DankMeme(ctx):
    async with ctx.channel.typing():
        try:
            subred = "dankmemes"
            subreddit = reddit.subreddit(subred)
            all_subs = []

            top = subreddit.hot(limit=500)

            for submission in top:
                all_subs.append(submission)

            random_sub = random.choice(all_subs)

            name = random_sub.title
            url  = random_sub.url

            embed = discord.Embed(title=name,color=discord.Color.blue())

            author = random_sub.author
            embed.description=f"Posted by {author}"
            embed.set_image(url=url)

            if subreddit.over18:
                if ctx.channel.is_nsfw:
                        
                    msg = await ctx.send(submission.url)
                    await msg.add_reaction('👍')
                    await msg.add_reaction('👎')
                else:
                    await ctx.send("Cannot send NSFW Content to non-NSFW Channel!") 

            else:
                
                #msg = await ctx.send(embed=embed)
                msg = await ctx.send(submission.url)
                await msg.add_reaction('👍')
                await msg.add_reaction('👎')
        except Exception as ex:
            embed=discord.Embed(color=discord.Color.red())
            embed.add_field(name="Whooops! That didn't work!",value=f"While looking for {subred}, I encountered the following Error:\n`{ex}`")
            embed.set_thumbnail(url="https://i.redd.it/bymxf1zb4mz11.jpg")
            await ctx.send(embed=embed)



@bot.command()
async def invite(ctx):
    await ctx.author.send("Invite me at https://discord.com/oauth2/authorize?client_id=841703388848193536&permissions=52224&scope=bot")

bot.run('TOKEN')
