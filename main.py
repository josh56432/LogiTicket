import subprocess
subprocess.run(["pip","install","git+https://github.com/Rapptz/discord.py@master"])


import keepalive
keepalive.keep_alive()
import os
import discord
import discord.utils
import io
import time
from replit import db
from dotenv import load_dotenv
from PIL import Image
from discord.ext import tasks
import asyncio



load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
messagelist=[[]]
intents = discord.Intents.all()
client = discord.Client(intents=intents)


def split(word):
    return [char for char in word]

global regions
global towns
global message_id

global commandChannel
global orderChannel
global ticketChannel

selectList = [discord.SelectOption(label = 'Error', value ='Error')]

class verifyButton(discord.ui.View):
  @discord.ui.button(style=1, label='Verify', disabled=False)
  async def click_me_button(self, button: discord.ui.Button, interaction: discord.Interaction):
    msg=interaction.message
    i = int(str(interaction.message.embeds[0].title).split("#")[1].split(":")[0])
    if str(interaction.user.id) == db[str(i)].split("_")[0]:
      person = str(db[str(i)].split("#")[1])
      try:
          db["stats"] = db["stats"].replace(person+str(int(db["stats"].split(person)[1].split("//")[0])),person+str(int(db["stats"].split(person)[1].split("//")[0])+1))
      except:
          db["stats"] = db["stats"]+(person+"1"+"//")
      info = db[str(i)]
      info = info.split("#")[0].split("//")
      del info[0]
      msgidlist=info
      x=""
      try:
        x = msg.embeds[0].title.split("P")[1].split(" ")[0]
      except:
        x = "rivate"
      y=0
      for guild in client.guilds:
        ticketChannel = client.get_channel(int(str(db[str(guild.id)+"info"]).split(" ")[3]))
        orderChannel = client.get_channel(int(str(db[str(guild.id)+"info"]).split(" ")[2]))
        try:
          msg = await ticketChannel.fetch_message(msgidlist[y][0:18])
          await msg.delete()
          if x== "ublic":
           await orderChannel.send("Order #"+str(i)+" Completed by "+client.get_user(int(person)).display_name+": \n "+'*"'+db[str(i)].split("_")[3].split("//")[0]+'"*')
          else:
            await orderChannel.send("Order #"+str(i)+" Completed by <@"+person+">: \n "+'*"'+db[str(i)].split("_")[3].split("//")[0]+'"*')
        except:
          x=x
        y+=1
      await interaction.message.delete()
      db["Errorlist"] = db["Errorlist"].replace(str(i)+" ","")
      del db[str(i)]

  @discord.ui.button(style=4, label='Reject')
  async def click_me_button3(self, button: discord.ui.Button, interaction: discord.Interaction):
    keys = db.keys()
    keys = str(keys).replace("{","").replace("}","").replace("'","").split(', ')
    for guild in client.guilds:
      channel = client.get_channel(int(str(db[str(guild.id)+"info"]).split(" ")[3]))
      try:
        i = int(str(interaction.message.embeds[0].title).split("#")[1].split(":")[0])
        try:
          if str(keys[i])!="stats":
            for y in range(1,(len(str(db[str(keys[i])]).split("#")[0].split("//")))):
              message_id = int((str(db[str(keys[i])]).split("#")[0].split("//")[y])[0:18])
              print(str(keys[i]))
              msg = await channel.fetch_message(message_id)
              if len(str(db[str(keys[i])]).split("#")) != 2:
                await msg.edit(embed=msg.embeds[0], view=ViewWithButton())
              if len(str(db[str(keys[i])]).split("#")) == 2:
                await msg.edit(embed=msg.embeds[0], view=ReserveButton())
        except:
          try:
            if str(keys[i])!="stats":
              message_id = int((str(db[str(keys[i])]).split("#")[0].split("//")[(len(str(db[str(keys[i])]).split("#")[0].split("//")))-1])[0:18])
              print(str(keys[i]))
              msg = await channel.fetch_message(message_id)
              if len(str(db[str(keys[i])]).split("#")) != 2:
                await msg.edit(embed=msg.embeds[0], view=ViewWithButton())
              if len(str(db[str(keys[i])]).split("#")) == 2:
                await msg.edit(embed=msg.embeds[0], view=ReserveButton())
          except:
            if str(keys[i])!="stats" and str(keys[i])[18:22]!="info" and str(keys[i])!="TicketNum" and str(keys[i])!="Errorlist":
              check = db["Errorlist"].split(" ")
              z=0
              for y in range(len(check)):
                if str(keys[i]) != check[y]:
                  z+=1
              if z == len(check):
                del db[str(keys[i])]
                print("Deleted order #"+str(keys[i]))        
      except Exception as e:
        print(e)

    await interaction.message.delete()
    db["VerifList"] = db["VerifList"].replace(str(i)+" ","")


class awaitButton(discord.ui.View):
  @discord.ui.button(style=2, label='Verifying...', disabled=False)
  async def click_me_button2(self, button: discord.ui.Button, interaction: discord.Interaction):
    print("Click disabled button")

  @discord.ui.button(style=1, label='Resend Request', disabled=False)
  async def click_me_button(self, button: discord.ui.Button, interaction: discord.Interaction):
    ticketChannel = db[str(interaction.message.guild.id)+"info"].split(" ")[3]
    orderChannel = db[str(interaction.message.guild.id)+"info"].split(" ")[2]
    print("Button press: "+str(interaction.message.id))
    channel = client.get_channel(int(ticketChannel))
    msg = await channel.fetch_message(interaction.message.id)
    i = int(str(msg.embeds[0].title).split("#")[1].split(":")[0])
    if str(interaction.user.id) == db[str(i)].split("#")[1] or str(interaction.user.id) == db[str(i)].split("_")[0]:
      info = db[str(i)]
      info = info.split("#")[0].split("//")
      del info[0]
      msgidlist=info
      x=""
      try:
        x = msg.embeds[0].title.split("P")[1].split(" ")[0]
      except:
        x = "rivate"
      
      orderChannel = client.get_channel(int(str(db[str(interaction.message.guild.id)+"info"]).split(" ")[2]))
      msg = interaction.message
      await msg.edit(embed=msg.embeds[0], view=awaitButton2())
      person = str(db[str(i)].split("_")[0])
      print(person)
      auth = await client.fetch_user(person)
      embedVar = discord.Embed(title='*RE-REQUEST Verify Completed Order #'+str(i)+':*')
      embedVar.add_field(name='Town: ', value= msg.embeds[0].fields[1].value, inline = True)
      embedVar.add_field(name='Order: ', value= msg.embeds[0].fields[2].value, inline = True)
      embedVar.add_field(name='Driver: ',value=  msg.embeds[0].fields[3].value, inline = False)
      embedVar.add_field(name='Driver: ',value=  msg.embeds[0].fields[3].value, inline = False)
      await auth.send(embed=embedVar, view=verifyButton())

class awaitButton2(discord.ui.View):
  @discord.ui.button(style=2, label='Verifying...', disabled=True)
  async def click_me_button2(self, button: discord.ui.Button, interaction: discord.Interaction):
    print("Click disabled button")

  @discord.ui.button(style=3, label='Request Resent ✅', disabled=True)
  async def click_me_button(self, button: discord.ui.Button, interaction: discord.Interaction):
    print("Click disabled button")

class ReserveButton(discord.ui.View):
    @discord.ui.button(style=4, label='Reserved', disabled=True)
    async def click_me_button(self, button: discord.ui.Button, interaction: discord.Interaction):
      print("Click disabled button")

    @discord.ui.button(style=3, label='Complete', disabled=False)
    async def click_me_button2(self, button: discord.ui.Button, interaction: discord.Interaction):
      ticketChannel = db[str(interaction.message.guild.id)+"info"].split(" ")[3]
      orderChannel = db[str(interaction.message.guild.id)+"info"].split(" ")[2]
      print("Button press: "+str(interaction.message.id))
      channel = client.get_channel(int(ticketChannel))
      msg = await channel.fetch_message(interaction.message.id)
      i = int(str(msg.embeds[0].title).split("#")[1].split(":")[0])
      if str(interaction.user.id) == db[str(i)].split("#")[1]:
        info = db[str(i)]
        info = info.split("#")[0].split("//")
        del info[0]
        msgidlist=info
        x=""
        try:
          x = msg.embeds[0].title.split("P")[1].split(" ")[0]
        except:
          x = "rivate"
        
        orderChannel = client.get_channel(int(str(db[str(interaction.message.guild.id)+"info"]).split(" ")[2]))
        msg = interaction.message
        await msg.edit(embed=msg.embeds[0], view=awaitButton())
        person = str(db[str(i)].split("_")[0])
        print(person)
        auth = await client.fetch_user(person)
        embedVar = discord.Embed(title='*Verify Completed Order #'+str(i)+':*')
        embedVar.add_field(name='Town: ', value= msg.embeds[0].fields[1].value, inline = True)
        embedVar.add_field(name='Order: ', value= msg.embeds[0].fields[2].value, inline = True)
        embedVar.add_field(name='Driver: ',value=  msg.embeds[0].fields[3].value, inline = False)
        embedVar.set_footer(text="***If error occurs request resend by pressing button on relevant ticket***")
        await auth.send(embed=embedVar, view=verifyButton())
        db["VerifList"] = db["VerifList"]+str(i)+" "



class ViewWithButton(discord.ui.View):
    @discord.ui.button(style=1, label='Begin')
    async def click_me_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        ticketChannel = db[str(interaction.message.guild.id)+"info"].split(" ")[3]
        orderChannel = db[str(interaction.message.guild.id)+"info"].split(" ")[2]
        print("Button press: "+str(interaction.message.id))
        channel = client.get_channel(int(ticketChannel))
        msg = await channel.fetch_message(interaction.message.id)
        i = int(str(msg.embeds[0].title).split("#")[1].split(":")[0])
        title1 = "LogiTicketBot"
        x=""
        try:
          x = msg.embeds[0].title.split("P")[1].split(" ")[0]
        except:
          x = "rivate"
        
          embedVar.set_author(name=title1,icon_url="https://cdn.discordapp.com/attachments/867837759518146583/899405909531447346/141.png")
          info = db[str(i)]
          uname=interaction.message.embeds[0].fields[0].value
          embedVar.add_field(name="Recipient: ", value=uname, inline = True)
          embedVar.add_field(name='Town: ', value="```"+info.split("_")[2]+", "+info.split("_")[1]+"```", inline = True)
          embedVar.add_field(name='Order: ', value="```"+str(info.split("_")[3].split("//")[0]).split("//")[0]+"```", inline = True)
          embedVar.add_field(name='Driver: ', value=str(interaction.user.display_name)+"  ["+interaction.message.guild.name+"]", inline = False)
          db[str(i)]=str(db[str(i)])+"#"+str(interaction.user.id) 
          msgidlist = info.split("//")
          del msgidlist[0]
          for y in range(len(msgidlist)):
            ticketChannel = client.get_channel(int(str(db[msgidlist[y][18:36]+"info"]).split(" ")[3]))
            orderChannel = client.get_channel(int(str(db[msgidlist[y][18:36]+"info"]).split(" ")[2]))
            try:
              msg = await ticketChannel.fetch_message(msgidlist[y][0:18])
              await msg.edit(embed=embedVar, view=ReserveButton())
            except:
              await ticketChannel.send(embed=embedVar, view=ReserveButton())
            await orderChannel.send(str(interaction.user.display_name)+"  ["+interaction.message.guild.name+"] reserved Order #"+str(i))
        else:
          
          embedVar = discord.Embed(title='```Order #'+str(i)+':```')
          embedVar.set_author(name=title1,icon_url="https://cdn.discordapp.com/attachments/867837759518146583/899405909531447346/141.png")
          info = db[str(i)]
          user1 = interaction.message.guild.get_member(int(info.split("_")[0]))
          uname=user1.display_name
          embedVar.add_field(name="Recipient: ", value="```"+uname+"```", inline = True)
          embedVar.add_field(name='Town: ', value="```"+info.split("_")[2]+", "+info.split("_")[1]+"```", inline = True)
          embedVar.add_field(name='Order: ', value="```"+str(info.split("_")[3].split("//")[0]).split("//")[0]+"```", inline = True)
          embedVar.add_field(name='Driver: ', value=str(interaction.user.display_name)+"  ["+interaction.message.guild.name+"]", inline = False)
          channel = client.get_channel(int(ticketChannel))
          db[str(i)] = db[str(i)]+"#"+str(interaction.user.id)
          print(db[str(i)])
          await msg.edit(embed=embedVar, view=ReserveButton())
          channel = client.get_channel(int(orderChannel))
          await channel.send("<@"+str(interaction.user.id)+"> reserved Order #"+str(i))

      
    @discord.ui.button(style=3, label='Complete', disabled=True)
    async def click_me_button2(self, button: discord.ui.Button, interaction: discord.Interaction):
      print("Click disabled button")




  

locations = ['Origin', ['Arise', 'Cado', 'Dormio', "The Dreamer's Road", 'The Echo', 'Exorior', 'Finis', 'Initium', 'The Sundering', 'Teichotima', 'Temple Field', 'World Star']], ["Basin Sionnach", ['Basinhome', 'Cunning Cross', 'Cuttail Station', 'The Den', 'The Foxfields', 'Lamplight', 'Radiant Shore', 'Sess', 'Stoic']], ['Speaking Woods', ['Calmland', 'Cursed Court', 'The Filament', 'Fort Blather', 'Hush', 'Inari Base', 'Mount Rell', 'Mute', 'Reaching River', 'Rell Foothills', 'Sotto Bank', 'Stem', 'Tine', 'Wound']], ['Howl County', ['Austriaca Reservoir', 'Checkpoint Titim', 'Fort Red', 'Fort Rider', 'Great Warden Dam', 'Hungry Wolf', 'Little Lamb', 'Sickleshire', 'Slipgate Outpost', 'Snakewell', 'Teller Farm', 'The Hunting Grounds', 'Viperwalk']], ["Callum's Cape", ["Callum's Keep", 'Camp Hollow', 'The Dreg', 'The Gunwall', 'Holdout', 'Hollowhill', 'Ire', 'Lookout', 'Naofa', 'Princefal Burn', 'The River Vein', 'Scouts Jest', 'Trail of the Dead', 'Valta Downs', 'Windy Way']], ['Reaching Trail', ['The Ark', 'Brodytown', 'The Cairns', 'Camp Eos', 'Caragtais', 'The Chicken Coop', 'The Deckard',"Dungan's Approach", 'Dwyersfield', 'Dwyerstown', 'Elksford', 'Featherfield', 'Harpy', 'Ice Ranch', 'Limestone Holdfast', 'Mousetrap', 'Nightchurch', 'Pitfall', 'Puncta', 'The Reaching Heights', 'Reprieve', 'The Rousing Fields', 'The Scar', 'Scorpion', 'Thylak']], ['Clanshead Valley', ["The Bastard's Channel", 'Bramble Field', 'Fallen Crown', 'Fort Ealar', 'Fort Esterwild', 'The King', 'Lost Orphans', 'Fort Windham', 'The Pike', 'Sweetholt', 'Tallowild', 'Throne of Druiminn', 'The Weathered Expanse']], ["Nevish Line", ['The Aging Ocean', 'The Arrow', 'Blackcoat Way', 'Blinding Stones', 'Grief Mother', 'Mistle Shrine', 'Nevish Trail', 'Plumage', 'Princefal', 'Princefal Burn', 'The Scrying Belt', 'Tear Road', 'Tomb Father', 'Unruly']], ['The Moors', ["Aillen's Burrow", 'Bitter Bramble', 'Borderlane', "Callum's Pass", 'The Cut', 'The Finger', 'The Graveyard', 'Headstone', "Luch's Workshop", "Lyon's Wood", 'MacConmara Barrows', "Moon's Walk", "Morrighan's Grave", 'The Mound', 'Ogmaran', 'Reaching River', 'Riverhill', 'Scáth Copse', 'Wiccwalk', 'Wiccwood', 'The Wind Hills']], ['Viper Pit', ["Afric's Approach", 'Austriaca River', 'Blackthroat', 'The Bloody Bowery', 'Deadsteps', 'Earl Crowley', "Earl's Welcome", 'Fleck Crossing', 'Fort Viper', 'The Friars', 'Hardcaps', 'Kirknell', "The Lady's Lake", 'Lake Mioira', 'Moltworth', 'Path of the Charmed', 'The Rockaway', "Serenity's Blight", 'The Slithering Scales', 'Snakehead Lake', 'The Tongue', 'Twin Fangs']], ["Morgen's Crossing", ['Allsight', 'The Bastard Sea', "Bastard's Block", "Callum's Descent", 'Crimson Thread', 'Eversus', 'Lividus', 'Quietus', 'Rising Calm', 'Ultimus', 'Velian Storm', 'Warmonger Bay']], ['Stonecradle', ['The Ageing Ocean', 'Buckler Sound', 'The Cord', 'Fading Lights', "The Heir's Knife", 'The Loneliest Shore', 'The Long Fast', 'Longing', 'The Pram', 'The Reach', 'The Roiling Comets', 'Trammel Pool', "World's End"]], ["Callahan's Passage", ["Callahan's Eye", 'Chapel Access', 'Cragsfield', 'Cragsroad', 'Cragstown', 'The Crumbling Passage', 'Crumbling Post', 'The Key', 'The Latch', 'Lingering Lashes', 'Lochan', 'Lochan Berth', 'Overlook Hill', 'The Procession', 'The Rust Road', 'Scáth Passing', 'Sioc Approach', 'Solas Gateway', 'Solas Gorge', 'The Stern', 'Twisted Mumble', 'White Chapel']], ['Weathered Expanse', ['Bannerwatch', 'Barrowsfield', "Crow's Nest", "Dullahan's Crest", 'Eapoe', 'Foxcatcher', 'Frostmarch', 'Huntsfort', 'The Ivory Bank', 'The Ivory Sea', 'Kirkyard', 'Necropolis', 'Port of Rime', "Revenant's Path", 'Rime Wastes', 'Shattered Advance', 'The Spear', 'Spirit Watch', 'The Stand', 'The Weathered Wall', 'The Weathering Halls', 'Wightwalk', "Wraith's Gate"]], ["The Oarbreaker Isles", ['Alabastor Island', 'Barrenson', 'Base Akris', 'Bronze', 'Castor', 'The Conclave', 'Crach Woods', 'Damsel', 'The Emblem', 'Fogwood', 'Gold', 'Grisly Refuge', 'The Ides', 'Integrum', "Lion's Head", 'Mount Marce', "Neptune's Throne", 'Oasis', 'Oblitum', 'Posterus', "Raven's Beak Fort", 'Reliqua', 'Silver', 'Skelter Course', 'Thunder Row']], ['The Linn of Mercy', ['Blackroad', 'The Crimson Gardens', 'The Drone', 'The First Coin', 'Fort Duncan', 'Gallant Gough Boulevard', 'The Great Scale', 'Hardline', 'The Last Grove', 'Lathair', 'The Long Whine', 'Merciful Strait', 'Mudhole', 'Nathair', 'Outwich Ranch', 'The Prairie Bazaar', 'The River Mercy', 'Rotdust', 'Solas Burn', 'Ulster Falls']], ['Marban Hollow', ['Bleating Plateau', 'Bubble Basin', 'Checkpoint Bua', 'The Clutch', 'The Curse', 'Deepfleet Valley', 'Gaping Maw', 'Lockheed', 'Lockheed Breakers', 'Lughbone Dam', "Maiden's Veil", 'Mount Mac Tire', 'Mox', 'Oster Wall', 'Pilgrimage', 'The Claim', 'Sanctum', 'Slender Cove', 'The Spitrocks']], ['Godcrofts', ['Anchor Beach', 'Argosa', 'The Axehead', 'Bagh Mor', "Barreller's Bay", 'Blackwatch', 'Chamil Ravine', 'Den of Thieves', 'The Dice Road', 'The Fleece Road', "Gambler's Gulf", 'Isawa', 'Kolas', 'The Kris Ford', 'Lipsia', 'Peripti Depths', 'Perpetua Channel', 'Primus Trames', 'Promithiens', 'Protos', 'Saegio', 'Skodio', 'Ursa Trail', 'Vicit Lagoon']], ['Farranac Coast', ['The Bone Haft','Cormac Beach', 'The Heart Road', 'Huskhollow', 'The Iron Beach', 'Iuxta Homestead', 'The Jade Cove', 'Kardia', 'Lushlands', "Macha's Keening", 'Mara', 'Pleading Wharf', 'The Reaping Fields', 'The River Mercy', 'Scarp of Ambrose', 'Scythe', 'Sickle Hill', 'Skeleton Road', 'The Snag', 'The Spearhead', 'Sunder Beach', 'Terra', 'Victa', 'The Winged Walk']], ["Deadlands", ['Abandoned Ward', 'The Abbey Drag',  'The Boneyard', 'Border Concourse', 'Brine Glen', "Callahan's Boot", "Callahan's Gate", "Callahan's Pass", 'Carpal Trail', 'Crumbling Passage', "Hope's Causeway", 'The Iron Passage', 'The Iron Road', "Iron's End",'Liberation Point', 'Marrow Copse', 'Mercy Meadow', "Mercy's End", 'Overgrown Pasture','The Pits',  'The Salt Farms', 'The Salt March', 'The Spine', 'The Steppes', "Sun's Hollow"]], ['Endless Shore', ["Balor's Crown", 'Brackish Point', 'The Dannan Coast', 'Dannan Ridge', 'The Dark Road', "Dearg's Fang", 'Enduring Wake', 'The Evil Eye', 'Iron Junction', "Kelpie's Mane", "Kelpie's Tail", "Merrow's Rest", 'The North Star', 'The Old Jack Tar', 'The Overland', 'Saltbrook Channel', 'The Selkie Bluffs', 'Sídhe Fall', 'The Styx', 'Tuath Watchpost', 'Vulpine Watch', 'Weakthered Landing', 'Wellchurch', 'The Whispering Waves', 'Woodbind']], ["Fisherman's Row", ['A Lost Sot', 'Arcadia', 'Bident Crossroads', 'Black Well', 'Cat Step', 'Dankana Post', 'The Dire Strings', 'Eidolo', 'Fort Ember', "Hangmen's Court", 'Heart of Rites', 'House Roloi', 'Lake Nerites', 'Liberty Hill', 'Oceanwatch', 'Partisan Island', 'Peripti Landing', 'Progonos Watch', 'The Rite Road', 'The Satyr Stones', 'The Three Sisters', 'Torch of Demeter']], ['Loch Mor', ["Bastard's Blade", 'Chattering Prairie', 'Escape', 'Fallen Fields', 'Feirmor', 'The Founding Fields', 'The Glean', 'Market Road', "Mercy's Wish", 'Missing Bones', "Moon's Copse", 'Ousterdown', 'Pockfields', 'The Reaping Road', 'Rip', 'The Roilfort', 'Tear', 'Tomb of the First', 'Westmarch', "Widow's Wail"]], ['The Drowned Vale', ['The Baths', 'Bootnap', 'Coaldrifter Stead', 'Eastmarch', 'Esterfal', 'Fleetsfall River', 'Loggerhead', 'The Other Vein', 'The Saltcaps', 'Singing Serpents', 'Sop Fields', 'Splinter Pens', "Sprite's Game", 'The Turtlerocks', 'The Wash', 'The Willow Wood', "Wisp's Warning"]], ['Tempest Island', ['Alchimio Estate', 'Cirris Valve', 'Eros Lagoon', 'The Gale', 'The Iris', 'Isle of Psyche', "Liar's Haven", 'Lost Airchal', 'The Outwood', 'Plana Fada', 'Reef', 'The Rush', 'Sclera', 'Stratos Valve', 'Surge Field']], ['Westgate', [ 'Ash Step',  'Ceo Highlands', 'Cinder Road', 'Coastway','Ember Hills', 'The Gallows', 'Handsome Hideaway', 'The Hem', 'Hillcrest', 'Holdfast', 'Kingstone', "The Knight's Edge", 'Longstone', "Lord's Mouth", 'Lost Partition', "Rancher's Fast", 'Sanctuary', "Triton's Curse", 'Warden Walk', 'Westgate Keep',  'Wyattwick', "Zeus' Demise"]], ["Allod's Bight", ["Allod's Children", 'Belaying Trace', 'Blunder Bight', 'Breath of Cetus', 'Gangrenous Hollow', "Harpy's Perch", 'Homesick', 'The List', "Mercy's Wail", 'Rumhold', 'The Rumroad', 'Scurvyshire', 'The Stone Plank', "Titan's End", 'The Turncoat', "Witch's Last Flight"]], ['Umbral Wildwood', ['Adze Crossroads', 'Amethyst', "Atropos' Fate", "Clotho's Refuge", 'Dredgefield', 'The Dredgewood', 'The Foundry', 'The Frontier', 'The Gap', 'Golden Concourse', 'GoldenRoot Ranch', "Hermit's Rest", "Lachesis' Tally", 'Leatherback Pathway', 'Sentry', 'Steely Fields', 'The Strands', 'Stray', 'Terrapin Woods', 'Thunder Row', 'Thunderfoot', 'Vagrant Bastion', 'Wasting Holt', "Weaver's Trail"]], ['The Heartlands', ['18th Sideroad', 'Barronstown', 'Barronswall', 'Barrony Ranch', 'Barrony Road', 'The Blemish', 'The Breach', 'Deeplaw Post', 'Erimos Ranch', 'Fort Providence', 'The Fuming Pen', 'Greenfield Orchard', "Havester's Range", 'Janus Field', 'Kos Meadows', 'Lower Barrony Field', 'Oleander Fields', 'Oleander Homestead', 'Pandora Compound', 'The Plough', 'Proexí', 'Providence Field', 'The Rollcage', 'Upper Heartlands']], ['Shackled Chasm', ['A Careless Net', 'A New Spring', 'Autumn Pyres', 'The Bell Toll', 'The Blue', 'Final Step', 'The First Rung', 'Firstmarch', 'The Foolish Maidens', 'Gorgon Grove', 'The Grave of Rastus', 'Hades Ladder', "Legion's Dawn",'Limewood Holdfast', 'Manky Hills', 'The Plunging', 'Reflection', 'Silk Farms', "Simo's Run", 'Southreach', 'The Vanguard', "Widow's Web"]], ['The Fingers', ["Captain's Dread", 'Cavitatis', 'Cementum', 'Fort Barley', "Headman's Villa", 'Mount Talio', 'The Old Captain', 'Plankhouse', 'The Routed', 'Second Man', 'Tears of Tethys', 'Titancall', 'The Tusk', 'The Wary Nymphae']], ['Ash Fields', ['Ash Step', 'The Ashfort', 'Ashtown', 'The Calamity', 'Camp Omega', 'Cinder Road', 'Cometa', 'Electi', 'Ember Hills', "Gunslinger's Pass", 'Mount Blackmoth', 'Mount Brimstone', 'Omega Valley', 'Sootflow', 'The Stillness', 'Tar Creek', 'Twin Flames', 'Wasteful Calm']], ['Great March', ['The Black Wing', 'Dendro Field', 'Fateless Grove', 'Fengari', 'Halting Valley', 'Jackboot Creek', 'Legacy Pasture', 'Leto', 'The Midmarch', 'Milowood', 'Mors Range', "Myrmidon's Stay", 'Remnant Acreage', 'Remnant Villa', 'The River Senti', 'Schala Estate', 'Serpent Charm', 'Sitaria', 'The Spice Road', 'The Swan', 'Violet Fields', 'Violethome', 'The White Wing', 'Zealous Approach']], ['Terminus', ['Aspisa', 'Bay of the Ward', 'Bloody Palm Fort', 'Cerberus Wake', 'Dogbone', "The Legion's Bounty", "Martyr's Fang", 'The Phalanx', 'The Respite', 'Rising Loom', 'Sever', 'Therizo', 'Three Siblings', 'Thunder Plains', 'Thunderbolt', "Warlord's Stead", 'Winding Bolas']], ['Red River', ['Camp Upsilon', 'Cannonsmoke', 'Climb', 'Fort Matchwood', 'Fragment Knolls', 'Gunpowder Lane', 'Judicium', 'Minos', 'Penance', 'Perish', 'Red Crossing', 'The Red River', 'Twelve Drops', 'Victoria Hill']], ['Acrithia', ["Astero's Spear", 'The Brinehold', 'Camp Omicron', 'Duelling Kegs', 'Fated Heel', 'Final March', 'Heir Apparent', 'Legion Ranch', 'Nereid Keep', 'Patridia', 'Riverlands', 'Swordfort', 'Thetus Ring', 'Weary Slumber']], ['Kalokai', ['Baccae Ridge', 'Bleary', 'Camp Tau', 'Clarity Meadow', 'Hallow', 'Lost Greensward', "Night's Regret", 'Sourtooth', 'South March', 'Sweethearth']]

@client.event
async def on_guild_join(guild):
    await guild.text_channels[0].send("```Type %launch to start Logi-Ticket-Bot```")
    x=client.guilds      
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=str(len(x))+" servers"))

@client.event
async def on_ready():
    keys = db.keys()
    keys = str(keys).replace("{","").replace("}","").replace("'","").split(', ')
    x=client.guilds      
    buttonReset.start()
    print("Ready!")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=str(len(x))+" servers"))
    for guild in client.guilds:
      try:
        prefix = str(db[str(guild.id)+"info"]).split(" ")[0]
        commandChannel = str(db[str(guild.id)+"info"]).split(" ")[1]
        orderChannel = str(db[str(guild.id)+"info"]).split(" ")[2]
        ticketChannel = str(db[str(guild.id)+"info"]).split(" ")[3]
      except:   
        db[str(guild.id)+"info"]= "% "
        prefix = "%"
        category = await guild.create_category("Logi Ticket Bot")
        channel = await guild.create_text_channel("logi-commands", category=category)
        msg = await channel.send(embed=helpEmbed(prefix,"ticket"))
        await msg.pin()
        db[str(guild.id)+"info"] += str(channel.id)+" "
        channel = await guild.create_text_channel("logi-order-log", category=category)
        db[str(guild.id)+"info"] += str(channel.id)+" "
        msg = await channel.send(embed=helpEmbed(prefix,"log"))
        await msg.pin()
        channel = await guild.create_text_channel("active-logi-tickets", category=category)
        await channel.set_permissions(guild.default_role, send_messages=False)
        db[str(guild.id)+"info"] += str(channel.id)+" "
    
      

@client.event
async def on_message(message, user=discord.Member):
  if message.author.id != 915715481112023051:
    #print(message.content)
    try:
      prefix = str(db[str(message.guild.id)+"info"]).split(" ")[0]
      commandChannel = str(db[str(message.guild.id)+"info"]).split(" ")[1]
      orderChannel = str(db[str(message.guild.id)+"info"]).split(" ")[2]
      ticketChannel = str(db[str(message.guild.id)+"info"]).split(" ")[3]
    except:   
      db[str(message.guild.id)+"info"]= "% "
      prefix = "%"
      category = await message.guild.create_category("Logi Ticket Bot")
      channel = await message.guild.create_text_channel("logi-commands", category=category)
      msg = await channel.send(embed=helpEmbed(prefix,"ticket"))
      await msg.pin()
      db[str(message.guild.id)+"info"] += str(channel.id)+" "
      channel = await message.guild.create_text_channel("logi-order-log", category=category)
      db[str(message.guild.id)+"info"] += str(channel.id)+" "
      msg = await channel.send(embed=helpEmbed(prefix,"log"))
      await msg.pin()
      channel = await message.guild.create_text_channel("active-logi-tickets", category=category)
      await channel.set_permissions(message.guild.default_role, send_messages=False)
      db[str(message.guild.id)+"info"] += str(channel.id)+" "
      prefix = str(db[str(message.guild.id)+"info"]).split(" ")[0]
      commandChannel = str(db[str(message.guild.id)+"info"]).split(" ")[1]
      orderChannel = str(db[str(message.guild.id)+"info"]).split(" ")[2]
      ticketChannel = str(db[str(message.guild.id)+"info"]).split(" ")[3]





    if message.content==prefix+"leaderboard" or message.content==prefix+"lb":
        stats= str(db["stats"]).replace("<","").replace(">","").replace("!","").replace("@","")
        stats= stats.split("//")
        statsplit = [[]]
        print(stats)
        for i in range(len(stats)-1):
          statsplit.append([stats[i][0:18], stats[i].split(stats[i][0:18])[1]])
        del statsplit[0]
        for i in range(len(statsplit)):
          statsplit[i][1] = int(statsplit[i][1])
        statsplit = sorted(statsplit,key=lambda l:l[1], reverse=True)
        for i in range(len(statsplit)):
          statsplit[i][1] = str(statsplit[i][1])
        print(statsplit)
        for i in range(len(statsplit)):
          for guild in client.guilds:
            user = guild.get_member(int(statsplit[i][0]))
            try:
              name = user.display_name + ": "+ guild.name
              break
            except:
              z=0
          statsplit[i][0] = name
        print(statsplit)
        embedVar = discord.Embed(title="Leaderboard")
        embedVar.set_footer(text= "- Made by Stolas")
        value1=""
        j=0
        for i in range(10):
          try:
            if(statsplit[i][1] != statsplit[i-1][1]):
              j+=1
          except:
            j+=1
          if j == 0:
            j=1
          try:
            value1=value1+"```#"+str(j)+": "+statsplit[i][0]+" ｜ "+statsplit[i][1]+"```\n"
          except:
            break
        embedVar.add_field(name="```Place:   Name:   Orders Completed:```",value=value1)
        title1 = "Top ten"
        embedVar.set_author(name=title1,icon_url="https://cdn.discordapp.com/attachments/867837759518146583/899405909531447346/141.png")
        await message.channel.send(embed=embedVar)
        await message.delete()




    if message.channel.id == int(commandChannel):
      keys = db.keys()
      keys = str(keys).replace("{","").replace("}","").replace("'","").split(', ')
      listmes = message.content.split(" ")
      role = discord.utils.find(lambda r: r.name == 'Logi Admin', message.guild.roles)
      







      if message.content.split(" ")[0]==prefix+"unreserve":
        if len(message.content.split(" "))==2 and len(db[message.content.split(" ")[1]].split("#")) == 2 and (db[message.content.split(" ")[1]].split("_")[0] == str(message.author.id) or db[message.content.split(" ")[1]].split("#")[1] == str(message.author.id)) or role in message.author.roles or message.author.id == 352829345863303168:
          channel = client.get_channel(int(ticketChannel))
          i = int(message.content.split(" ")[1])
          title1 = "LogiTicketBot"
          channel = client.get_channel(int(ticketChannel))
          db[str(i)] = db[str(i)].replace("#"+db[str(i)].split("#")[1],"")
          print(db[str(i)])
          info=db[str(i)]
          msgidlist = info.split("//")
          del msgidlist[0]
          for y in range(len(msgidlist)):
              try:
                ticketChannel = client.get_channel(int(str(db[msgidlist[y][18:36]+"info"]).split(" ")[3]))
              except:
                ticketChannel = client.get_channel(int(str(db[str(message.guild.id)+"info"]).split(" ")[3]))
              try:
                msg = await ticketChannel.fetch_message(msgidlist[y][0:18])
                break
              except:
                i=i
          
          embedVar = discord.Embed(title='```#'+str(i)+':```')
          embedVar.set_author(name=title1,icon_url="https://cdn.discordapp.com/attachments/867837759518146583/899405909531447346/141.png")
          info = db[str(i)]
          user1 = message.guild.get_member(int(info.split("_")[0]))
          uname=user1.display_name
          embedVar.add_field(name="Recipient: ", value="```"+uname+"```", inline = True)
          embedVar.add_field(name='Town: ', value="```"+info.split("_")[2]+", "+info.split("_")[1]+"```", inline = True)
          embedVar.add_field(name='Order: ', value="```"+str(info.split("_")[3].split("//")[0]).split("//")[0]+"```", inline = True)
          ticketChannel = client.get_channel(int(db[str(message.guild.id)+"info"].split(" ")[3]))
          try:
            msg = await ticketChannel.fetch_message(int(msgidlist[0]))
            await msg.edit(embed=embedVar, view=ViewWithButton())
          except:
            await ticketChannel.send(embed=embedVar, view=ViewWithButton())
        await message.channel.send("Order Unreserved")
      else:
        await message.channel.send("Input error, please type "+prefix+"unreserve [Your Order Number]")


      
      if message.content.split(" ")[0]==prefix+"commend":
        person = str(message.content.split(" ")[1]).replace("<","").replace(">","").replace("!","").replace("@","")
        if person != message.author.id:
          try:
              db["stats"] = db["stats"].replace(person+str(int(db["stats"].split(person)[1].split("//")[0])),person+str(int(db["stats"].split(person)[1].split("//")[0])+1))
              await message.channel.send("Player Commended")
          except:
              try:
                user = await message.guild.query_members(user_ids=[person])
                if len(user)==1:
                  db["stats"] = db["stats"]+(person+"1"+"//")
                  await message.channel.send("Player Commended")
                else:
                  await message.channel.send("Invalid User")
              except:
                await message.channel.send("Invalid User")
        else:
          await message.channel.send("You can't commend yourself")
      


      if message.content.split(" ")[0]==prefix+"cancel":#
        ticketChannel = str(db[str(message.guild.id)+"info"]).split(" ")[3]

        if len(message.content.split(" "))==2 and db[message.content.split(" ")[1]].split("_")[0] == str(message.author.id):
            index=message.content.split(" ")[1]
            try:
              info = db[message.content.split(" ")[1]]
              info = info.split("#")[0].split("//")
              del info[0]
              msgidlist=info
              for y in range(len(msgidlist)):
                  ticketChannel = client.get_channel(int(str(db[msgidlist[y][18:36]+"info"]).split(" ")[3]))
                  try:
                    msg = await ticketChannel.fetch_message(msgidlist[y][0:18])
                    await msg.delete()
                  except Exception as e:
                    print(e)
            except:
              message_id = db[message.content.split(" ")[1]].split("//")[1].split("#")[0][0:18]
              print(message_id)
              channel = client.get_channel(int(ticketChannel))
              try:
                msg = await channel.fetch_message(message_id)
                await msg.delete()
              except Exception as e:
                print(e)

            del db[message.content.split(" ")[1]]
            msg = await message.channel.send("Order Cancelled")
            time.sleep(2)
            del messagelist[0]
            for i in range(len(messagelist)):
              if messagelist[i][1] == index:
                delmesid = int(str(messagelist[i][0]).split("id=")[1].split(" channel=")[0])
                print(delmesid)
                msg = await message.channel.fetch_message(delmesid)
                await msg.delete()
            x=0
            for i in range(len(messagelist)):
              if messagelist[x][1] == index:
                del messagelist[x]
                x-=1;
              x+=1;
            await message.delete()
            await msg.delete()
        else:
            await message.channel.send("Input error, please type "+prefix+"cancel [Your Order Number]")



      
      
      listmes = message.content.split(" ")
      if listmes[0]==prefix+"prefix":
          if role in message.author.roles:
              if len(listmes)>1 and len(listmes[1].split(""))==1:
                  prefix = listmes[1]
                  db[str(message.guild.id)+"info"] = db[str(message.guild.id)+"info"].replace(db[str(message.guild.id)+"info"].split(" ")[0], prefix)
                  await message.channel.send("Prefix is now "+'"'+prefix+'"')
                  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="for "+prefix))
              else:
                  await message.channel.send("Prefix is still "+'"'+prefix+'"'+" this is because input error occured.")
          else:
              await message.channel.send("You do not have the 'Logi Admin' role please get this role before doing settings commands")




      if message.content==prefix+"ticket":
        waitmsg= await message.channel.send("```Loading Interface ....```")
        try:
          ticketnum = db["TicketNum"]
        except(Exception):
          db["TicketNum"] = -1
          ticketnum = 0
        db["TicketNum"] = ticketnum+1
        db["Errorlist"] = db["Errorlist"]+str(ticketnum)+" "
        db[str(ticketnum)] = str(message.author.id)
        embedVar = discord.Embed(title="Order #"+str(ticketnum)+":")
        image = Image.open("map.png")
        with io.BytesIO() as output:
          image.save(output, format="PNG")
          im = output.getvalue()
        f = io.BytesIO(im)
        file = discord.File(f, filename="output.png")
        embedVar.set_image(url="attachment://output.png")
        embedVar.set_footer(text="Select Region and press enter")
        title1 = "Compiling Ticket for: "+str(message.author.display_name)
        embedVar.set_author(name=title1,icon_url="https://cdn.discordapp.com/attachments/867837759518146583/899405909531447346/141.png")
        await message.channel.send(file=file, embed=embedVar,view = DropDown())
        await waitmsg.delete()
        await message.delete()

      if message.content==prefix+"map":
        image = Image.open("map.png")
        with io.BytesIO() as output:
          image.save(output, format="PNG")
          im = output.getvalue()
        f = io.BytesIO(im)
        file = discord.File(f, filename="output.png")
        await message.channel.send(file=file)

      if message.content==prefix+"help":
        await message.channel.send(embed=helpEmbed(prefix,"ticket"))

      if message.content.split(": ")[0]== "Info":
        print("msg")
        messagecontent = message.content.split(": ")[1].replace("#","").replace("//","")
        for i in range(len(db.keys())):
          if len(str(db[str(keys[i])]).split("_"))==3 and str(db[str(keys[i])]).split("_")[0] == str(message.author.id):
            info = db[str(keys[i])]
            embedVar = discord.Embed(title="Order Number #"+str(keys[i]))
            embedVar.set_footer(text='Order Recipient: '+str(message.author.display_name))
            embedVar.add_field(name='Region: ', value=info.split("_")[1], inline = False)
            embedVar.add_field(name='Town: ', value=info.split("_")[2], inline = True)
            embedVar.add_field(name='Order: ', value=message.content.split(":")[1], inline = False)
            title1 = "Completed Ticket: Select mode"
            embedVar.set_author(name=title1,icon_url="https://cdn.discordapp.com/attachments/867837759518146583/899405909531447346/141.png")
            db[str(keys[i])] = db[str(keys[i])]+"_"+messagecontent
            channel = client.get_channel(int(commandChannel))
            global msgarray
            if msgarray[0]== message.author.id:
              print(msgarray[1])
              msgdel = await channel.fetch_message(msgarray[1])
              await msgdel.delete()
            msgarray = []
            await message.channel.send(embed=embedVar, view=Dropinfo())
            await message.delete()
          
            



    
    
  @discord.ui.button(style=2, label='Place Order')
  async def click_me_button2(self, button: discord.ui.Button, interaction: discord.Interaction):
    ticketChannel = str(db[str(interaction.message.guild.id)+"info"]).split(" ")[3]
    y = int(str(interaction.message.embeds[0].title).split("#")[1].split(":")[0])
    keys = db.keys()
    keys = str(keys).replace("{","").replace("}","").replace("'","").split(', ')
    orderChannel = str(db[str(interaction.message.guild.id)+"info"]).split(" ")[2]
    print(db[str(y)])
    await update(interaction.message.guild,str(y),False, "", "")
    time.sleep(2)
    channel = client.get_channel(int(orderChannel))
    await channel.send("New Ticket in <#"+str(ticketChannel)+">")
    await interaction.message.delete()

  @discord.ui.button(style=4, label='Cancel')
  async def click_me_button3(self, button: discord.ui.Button, interaction: discord.Interaction):
      commandChannel = str(db[str(interaction.message.guild.id)+"info"]).split(" ")[1]
      print("Button press: "+str(interaction.message.id))
      channel = client.get_channel(int(commandChannel))
      msg = await channel.fetch_message(interaction.message.id)
      i = int(str(msg.embeds[0].title).split("#")[1].split(":")[0])
      if str(interaction.user.id) == db[str(i)].split("_")[0]:
        try:
          del db[str(i)]
        except:
          print("ERROR")
        await msg.delete()
      db["Errorlist"] = str(db["Errorlist"]).replace(str(i)+" ","")



class DropDown(discord.ui.View):
    @discord.ui.select(options = [discord.SelectOption(label = 'Acrithia', value ='Acrithia'),discord.SelectOption(label = "Allod's Bight", value ="Allod's Bight"),discord.SelectOption(label = 'Ash Fields', value ='Ash Fields'),discord.SelectOption(label = 'Basin Sionnach', value ='Basin Sionnach'),discord.SelectOption(label = "Callahan's Passage", value ="Callahan's Passage"),discord.SelectOption(label = "Callum's Cape", value ="Callum's Cape"),discord.SelectOption(label = 'Clanshead Valley', value ='Clanshead Valley'),discord.SelectOption(label = 'Endless Shore', value ='Endless Shore'),discord.SelectOption(label = 'Farranac Coast', value ='Farranac Coast'),discord.SelectOption(label = "Fisherman's Row", value ="Fisherman's Row"),discord.SelectOption(label = 'Godcrofts', value ='Godcrofts'),discord.SelectOption(label = 'Great March', value ='Great March'),discord.SelectOption(label = 'Howl County', value ='Howl County'),discord.SelectOption(label = 'Kalokai', value ='Kalokai'),discord.SelectOption(label = 'Loch Mor', value ='Loch Mor'),discord.SelectOption(label = 'Marban Hollow', value ='Marban Hollow'),discord.SelectOption(label = "Morgen's Crossing", value ="Morgen's Crossing"),discord.SelectOption(label = 'Nevish Line', value ='Nevish Line'),discord.SelectOption(label = 'Origin', value ='Origin'),discord.SelectOption(label = 'Reaching Trail', value ='Reaching Trail'),discord.SelectOption(label = 'Red River', value ='Red River'),discord.SelectOption(label = 'Shackled Chasm', value ='Shackled Chasm'),discord.SelectOption(label = 'Speaking Woods', value ='Speaking Woods'),discord.SelectOption(label = 'Stonecradle', value ='Stonecradle'),discord.SelectOption(label = 'Tempest Island', value ='Tempest Island')])
    async def click_me_select(self, select: discord.ui.Select, interaction: discord.Interaction):
      global bruh
      print(str(interaction.data))
      try:
        bruh= str(interaction.data).split("['")[1].split("'],")[0]
      except:
        bruh= str(interaction.data).split('["')[1].split('"],')[0]

    @discord.ui.button(style=3, label='Enter')
    async def click_me_button2(self, button: discord.ui.Button, interaction: discord.Interaction):
        keys = db.keys()
        keys = str(keys).replace("{","").replace("}","").replace("'","").split(', ')
        commandChannel = str(db[str(interaction.message.guild.id)+"info"]).split(" ")[1]
        print("Button press: "+str(interaction.message.id))
        channel = client.get_channel(int(commandChannel))
        msg = await channel.fetch_message(interaction.message.id)
        y = int(str(msg.embeds[0].title).split("#")[1].split(":")[0])
        print(y)
        for i in range(len(db.keys())):
          if len(str(db[str(keys[i])]).split("_"))==1 and str(db[str(keys[i])]).split("_")[0] == str(interaction.user.id) and len(split(bruh))>0:
            embedVar = discord.Embed(title="Order #"+str(y)+": "+str(bruh))
            image = Image.open(bruh+".png")
            with io.BytesIO() as output:
              image.save(output, format="PNG")
              im = output.getvalue()
            f = io.BytesIO(im)
            file = discord.File(f, filename="output.png")
            embedVar.set_image(url="attachment://output.png")
            embedVar.set_footer(text="Select Town Name as seen on Map")
            title1 = "Compiling Ticket for: "+str(interaction.user.display_name)
            embedVar.set_author(name=title1,icon_url="https://cdn.discordapp.com/attachments/867837759518146583/899405909531447346/141.png")
            await interaction.message.delete()
            global selectList
            selectList= locationList(locations,bruh)

            class DropDown2(discord.ui.View):
              @discord.ui.select(options = selectList)
              async def click_me_select(self, select: discord.ui.Select, interaction: discord.Interaction):
                global L
                print(str(interaction.data))
                try:
                  L= str(interaction.data).split("{'values': ['")[1].split("'],")[0]
                except:
                  L= str(interaction.data).split(': ["')[1].split('"],')[0]
                print(L)
                
              @discord.ui.button(style=3, label='Enter')
              async def click_me_button2(self, button: discord.ui.Button, interaction: discord.Interaction):
                keys = db.keys()
                keys = str(keys).replace("{","").replace("}","").replace("'","").split(', ')
                commandChannel = str(db[str(interaction.message.guild.id)+"info"]).split(" ")[1]
                print("Button press: "+str(interaction.message.id))
                channel = client.get_channel(int(commandChannel))
                msg = await channel.fetch_message(interaction.message.id)
                y = int(str(msg.embeds[0].title).split("#")[1].split(":")[0])
                for i in range(len(db.keys())):
                  if len(str(db[str(keys[i])]).split("_"))==2 and str(db[str(keys[i])]).split("_")[0] == str(interaction.user.id) and len(split(bruh))>0:
                    embedVar = discord.Embed(title="Order #"+str(y)+": "+str(bruh)+", "+str(L))
                    embedVar.add_field(name="Information: ",value='Type "Info: [Amount and item needed with precise location]"')
                    embedVar.set_footer(text="Ref. "+str(interaction.message.id))
                    
                    title1 = "Compiling Ticket for: "+str(interaction.user.display_name)
                    embedVar.set_author(name=title1,icon_url="https://cdn.discordapp.com/attachments/867837759518146583/899405909531447346/141.png")
                    await interaction.message.delete()
                    db[str(y)] =str(db[str(y)])+"_"+L
                    msg = await interaction.message.channel.send(embed=embedVar, view=DropDownCancel())
                    global msgarray
                    msgarray=[interaction.user.id,msg.id]





              @discord.ui.button(style=4, label='Cancel')
              async def click_me_button3(self, button: discord.ui.Button, interaction: discord.Interaction):
                commandChannel = str(db[str(interaction.message.guild.id)+"info"]).split(" ")[1]
                print("Button press: "+str(interaction.message.id))
                channel = client.get_channel(int(commandChannel))
                msg = await channel.fetch_message(interaction.message.id)
                i = int(str(msg.embeds[0].title).split("#")[1].split(":")[0])
                if str(interaction.user.id) == db[str(i)].split("_")[0]:
                  try:
                    del db[str(i)]
                  except:
                    print("ERROR")
                  await msg.delete()
                db["Errorlist"] = str(db["Errorlist"]).replace(str(i)+" ","")

              

            await interaction.message.channel.send(file=file,embed=embedVar,view=DropDown2())
            db[str(keys[i])] = str(interaction.user.id)+"_"+bruh
            db["Errorlist"] = str(db["Errorlist"])+str(y)+" "
            print(db[str(keys[i])])


    @discord.ui.button(style=4, label='Cancel')
    async def click_me_button3(self, button: discord.ui.Button, interaction: discord.Interaction):
        commandChannel = str(db[str(interaction.message.guild.id)+"info"]).split(" ")[1]
        print("Button press: "+str(interaction.message.id))
        channel = client.get_channel(int(commandChannel))
        msg = await channel.fetch_message(interaction.message.id)
        i = int(str(msg.embeds[0].title).split("#")[1].split(":")[0])
        if str(interaction.user.id) == db[str(i)].split("_")[0]:
          del db[str(i)]
          await msg.delete()

    @discord.ui.button(style=1, label='More Options')
    async def click_me_button4(self, button: discord.ui.Button, interaction: discord.Interaction):
        commandChannel = str(db[str(interaction.message.guild.id)+"info"]).split(" ")[1]
        print("Button press: "+str(interaction.message.id))
        channel = client.get_channel(int(commandChannel))
        msg = await channel.fetch_message(interaction.message.id)
        i = int(str(msg.embeds[0].title).split("#")[1].split(":")[0])
        if str(interaction.user.id) == db[str(i)].split("_")[0]:
          embed=interaction.message.embeds[0]
          await interaction.message.delete()
          await msg.channel.send(embed=embed, view=DropDownExtend())
          


class DropDownExtend(discord.ui.View):
    @discord.ui.select(options = [discord.SelectOption(label = 'Stonecradle', value ='Stonecradle'),discord.SelectOption(label = 'Tempest Island', value ='Tempest Island'),discord.SelectOption(label = 'Terminus', value ='Terminus'),discord.SelectOption(label = 'Deadlands', value ='Deadlands'),discord.SelectOption(label = 'The Drowned Vale', value ='The Drowned Vale'),discord.SelectOption(label = 'The Fingers', value ='The Fingers'),discord.SelectOption(label = 'The Heartlands', value ='The Heartlands'),discord.SelectOption(label = 'The Linn of Mercy', value ='The Linn of Mercy'),discord.SelectOption(label = 'The Moors', value ='The Moors'),discord.SelectOption(label = 'The Oarbreaker Isles', value ='The Oarbreaker Isles'),discord.SelectOption(label = 'Umbral Wildwood', value ='Umbral Wildwood'),discord.SelectOption(label = 'Viper Pit', value ='Viper Pit'),discord.SelectOption(label = 'Weathered Expanse', value ='Weathered Expanse'),discord.SelectOption(label = 'Westgate', value ='Westgate')])
    async def click_me_select(self, select: discord.ui.Select, interaction: discord.Interaction):
      global bruh
      bruh= str(interaction.data).split("{'values': ['")[1].split("'],")[0]

    @discord.ui.button(style=3, label='Enter')
    async def click_me_button2(self, button: discord.ui.Button, interaction: discord.Interaction):
        keys = db.keys()
        keys = str(keys).replace("{","").replace("}","").replace("'","").split(', ')
        commandChannel = str(db[str(interaction.message.guild.id)+"info"]).split(" ")[1]
        print("Button press: "+str(interaction.message.id))
        channel = client.get_channel(int(commandChannel))
        msg = await channel.fetch_message(interaction.message.id)
        y = int(str(msg.embeds[0].title).split("#")[1].split(":")[0])
        for i in range(len(db.keys())):
          if len(str(db[str(keys[i])]).split("_"))==1 and str(db[str(keys[i])]).split("_")[0] == str(interaction.user.id) and len(split(bruh))>0:
            embedVar = discord.Embed(title="Order #"+str(y)+": "+str(bruh))
            image = Image.open(bruh+".png")
            with io.BytesIO() as output:
              image.save(output, format="PNG")
              im = output.getvalue()
            f = io.BytesIO(im)
            file = discord.File(f, filename="output.png")
            embedVar.set_image(url="attachment://output.png")
            embedVar.set_footer(text="Select Town Name as seen on Map")
            title1 = "Compiling Ticket for: "+str(interaction.user.display_name)
            embedVar.set_author(name=title1,icon_url="https://cdn.discordapp.com/attachments/867837759518146583/899405909531447346/141.png")
            await interaction.message.delete()
            global selectList
            selectList= locationList(locations,bruh)
            db[str(keys[i])] = str(interaction.user.id)+"_"+bruh
            print(db[str(keys[i])])
            db["Errorlist"] = str(db["Errorlist"])+str(y)+" "

            class DropDown2(discord.ui.View):
              @discord.ui.select(options = selectList)
              async def click_me_select(self, select: discord.ui.Select, interaction: discord.Interaction):
                  global L
                  try:
                    L= str(interaction.data).split("{'values': ['")[1].split("'],")[0]
                  except:
                    L= str(interaction.data).split(': ["')[1].split('"],')[0]
                  print(L)
                  
              @discord.ui.button(style=3, label='Enter')
              async def click_me_button2(self, button: discord.ui.Button, interaction: discord.Interaction):
                keys = db.keys()
                keys = str(keys).replace("{","").replace("}","").replace("'","").split(', ')
                commandChannel = str(db[str(interaction.message.guild.id)+"info"]).split(" ")[1]
                print("Button press: "+str(interaction.message.id))
                channel = client.get_channel(int(commandChannel))
                msg = await channel.fetch_message(interaction.message.id)
                y = int(str(msg.embeds[0].title).split("#")[1].split(":")[0])
                for i in range(len(db.keys())):
                  if len(str(db[str(keys[i])]).split("_"))==2 and str(db[str(keys[i])]).split("_")[0] == str(interaction.user.id) and len(split(bruh))>0:
                    embedVar = discord.Embed(title="Order #"+str(y)+": "+str(bruh)+", "+str(L))
                    embedVar.add_field(name="Information: ",value='Type "Info: [Amount and item needed with precise location]"')
                    embedVar.set_footer(text="Ref. "+str(interaction.message.id))#
                    title1 = "Compiling Ticket for: "+str(interaction.user.display_name)
                    embedVar.set_author(name=title1,icon_url="https://cdn.discordapp.com/attachments/867837759518146583/899405909531447346/141.png")
                    await interaction.message.delete()
                    db[str(y)] =str(db[str(y)])+"_"+L
                    msg = await interaction.message.channel.send(embed=embedVar, view=DropDownCancel())
                    global msgarray
                    msgarray=[interaction.user.id,msg.id]






              @discord.ui.button(style=4, label='Cancel')
              async def click_me_button3(self, button: discord.ui.Button, interaction: discord.Interaction):
                commandChannel = str(db[str(interaction.message.guild.id)+"info"]).split(" ")[1]
                print("Button press: "+str(interaction.message.id))
                channel = client.get_channel(int(commandChannel))
                msg = await channel.fetch_message(interaction.message.id)
                i = int(str(msg.embeds[0].title).split("#")[1].split(":")[0])
                if str(interaction.user.id) == db[str(i)].split("_")[0]:
                  try:
                    del db[str(i)]
                  except:
                    print("ERROR")
                  await msg.delete()
                db["Errorlist"] = str(db["Errorlist"]).replace(str(i)+" ","")

             

            await interaction.message.channel.send(file=file, embed=embedVar,view=DropDown2())



    @discord.ui.button(style=4, label='Cancel')
    async def click_me_button3(self, button: discord.ui.Button, interaction: discord.Interaction):
        commandChannel = str(db[str(interaction.message.guild.id)+"info"]).split(" ")[1]
        print("Button press: "+str(interaction.message.id))
        channel = client.get_channel(int(commandChannel))
        msg = await channel.fetch_message(interaction.message.id)
        i = int(str(msg.embeds[0].title).split("#")[1].split(":")[0])
        if str(interaction.user.id) == db[str(i)].split("_")[0]:
          del db[str(i)]
          await msg.delete()

    @discord.ui.button(style=1, label='First Options')
    async def click_me_button4(self, button: discord.ui.Button, interaction: discord.Interaction):
        commandChannel = str(db[str(interaction.message.guild.id)+"info"]).split(" ")[1]
        print("Button press: "+str(interaction.message.id))
        channel = client.get_channel(int(commandChannel))
        msg = await channel.fetch_message(interaction.message.id)
        i = int(str(msg.embeds[0].title).split("#")[1].split(":")[0])
        if str(interaction.user.id) == db[str(i)].split("_")[0]:
          embed=interaction.message.embeds[0]
          await interaction.message.delete()
          await msg.channel.send(embed=embed, view=DropDown())

class DropDownCancel(discord.ui.View):
  @discord.ui.button(style=4, label='Cancel')
  async def click_me_button3(self, button: discord.ui.Button, interaction: discord.Interaction):
    commandChannel = str(db[str(interaction.message.guild.id)+"info"]).split(" ")[1]
    print("Button press: "+str(interaction.message.id))
    channel = client.get_channel(int(commandChannel))
    msg = await channel.fetch_message(interaction.message.id)
    i = int(str(msg.embeds[0].title).split("#")[1].split(":")[0])
    if str(interaction.user.id) == db[str(i)].split("_")[0]:
      try:
        del db[str(i)]
      except:
        print("ERROR")
      await msg.delete()
    db["Errorlist"] = str(db["Errorlist"]).replace(str(i)+" ","")

def locationList(locations,bruh):
  location = str(bruh)
  print(location)
  for i in range(len(locations)):
    if locations[i][0] == location:
      location = locations[i][1]
      break
  selectList1=[]
  for i in range(len(location)):
      selectList1.append(discord.SelectOption(label = location[i], value = location[i]))
  return selectList1

def helpEmbed(prefix,channel):
  embedVar = discord.Embed(title="Help")
  embedVar.set_author(name="Logi-ticket-bot",icon_url="https://cdn.discordapp.com/attachments/867837759518146583/899405909531447346/141.png")
  embedVar.set_footer(text= "- Contact Stolas (141CR) for support")
  if channel == "ticket":
    embedVar.add_field(name=prefix+"ticket", value="```Begins a new ticket, follow instructions to compile```", inline = False)
    embedVar.add_field(name=prefix+"commend [User @]", value="```Give a driver a point on the leaderboard for helping an order or completing an unticketed order.```", inline = False)
    embedVar.add_field(name=prefix+'unerserve [Order Number]', value="```Unreserves ticket```", inline = False)
    embedVar.add_field(name=prefix+'cancel [Order Number]', value="```Cancels ticket```", inline = False)
    embedVar.add_field(name=prefix+'prefix]', value="```Changes prefix, role named 'Logi Admin' needed```", inline = False)
  elif channel == "log":
    embedVar.add_field(name=prefix+'lb', value="```Shows inter-server leaderboard```", inline = False)
  return embedVar


@tasks.loop(seconds=600)          
async def buttonReset():
  for guild in client.guilds:
    try:
      #print(db[str(guild.id)+"info"])
      ticketChannel = db[str(guild.id)+"info"].split(" ")[3]
      #print(ticketChannel)
      keys = db.keys()
      keys = str(keys).replace("{","").replace("}","").replace("'","").split(', ')
      for i in range(len(db.keys())):
        channel = client.get_channel(int(ticketChannel))
        try:
          if str(keys[i])!="stats":
            for y in range(1,(len(str(db[str(keys[i])]).split("#")[0].split("//")))):
              message_id = int((str(db[str(keys[i])]).split("#")[0].split("//")[y])[0:18])
              #print(str(keys[i]))
              msg = await channel.fetch_message(message_id)
              if len(str(db[str(keys[i])]).split("#")) != 2:
                await msg.edit(embed=msg.embeds[0], view=ViewWithButton())
              if len(str(db[str(keys[i])]).split("#")) == 2:
                if str(keys[i]) in db["VerifList"].split(" "):
                  await msg.edit(embed=msg.embeds[0], view=awaitButton())
                else:
                  await msg.edit(embed=msg.embeds[0], view=ReserveButton())
        except:
          try:
            if str(keys[i])!="stats":
              message_id = int((str(db[str(keys[i])]).split("#")[0].split("//")[(len(str(db[str(keys[i])]).split("#")[0].split("//")))-1])[0:18])
              #print(str(keys[i]))
              msg = await channel.fetch_message(message_id)
              if len(str(db[str(keys[i])]).split("#")) != 2:
                await msg.edit(embed=msg.embeds[0], view=ViewWithButton())
              if len(str(db[str(keys[i])]).split("#")) == 2:
                if str(keys[i]) in db["VerifList"].split(" "):
                  await msg.edit(embed=msg.embeds[0], view=awaitButton())
                else:
                  await msg.edit(embed=msg.embeds[0], view=ReserveButton())
          except:
            #print(db[keys[i]])
            if str(keys[i])!="stats" and str(keys[i])[18:22]!="info" and str(keys[i])!="TicketNum" and str(keys[i])!="Errorlist":
              check = db["Errorlist"].split(" ")
              z=0
              for y in range(len(check)):
                if str(keys[i]) != check[y]:
                  z+=1
              if z == len(check):
                del db[str(keys[i])]
                print("Deleted order #"+str(keys[i]))
            

          
          
    except Exception as e:
     print(e)



async def update(guild,i,public,user1,guildname):
  if public == False:
    ticketChannel = db[str(guild.id)+"info"].split(" ")[3]
    title1 = "LogiTicketBot"
    embedVar = discord.Embed(title='```Private Order #'+str(i)+':```')
    embedVar.set_author(name=title1,icon_url="https://cdn.discordapp.com/attachments/867837759518146583/899405909531447346/141.png")
    info = db[str(i)]
    
    user1 = guild.get_member(int(info.split("_")[0]))
    uname=user1.display_name
    embedVar.add_field(name="Recipient: ", value="```"+uname+"```", inline = True)
    embedVar.add_field(name='Town: ', value="```"+info.split("_")[2]+", "+info.split("_")[1]+"```", inline = True)
    embedVar.add_field(name='Order: ', value="```"+info.split("_")[3].split("//")[0]+"```", inline = True)
    channel = client.get_channel(int(ticketChannel))
    message1 = await channel.send(embed=embedVar, view=ViewWithButton())
    message_id=str(message1.id)
    db[str(i)] = db[str(i)]+"//"+message_id
    #print(db[str(i)])

  else:
    title1 = "LogiTicketBot"
    embedVar = discord.Embed(title='```Public Order #'+str(i)+':```')
    embedVar.set_author(name=title1,icon_url="https://cdn.discordapp.com/attachments/867837759518146583/899405909531447346/141.png")
    info = db[str(i)]
    uname=user1.name+"#"+user1.discriminator + "["+user1.display_name+", "+guildname+"]"
    embedVar.add_field(name="Recipient: ", value="```"+uname+"```", inline = True)
    embedVar.add_field(name='Town: ', value="```"+info.split("_")[2]+", "+info.split("_")[1]+"```", inline = True)
    embedVar.add_field(name='Order: ', value="```"+info.split("_")[3].split("//")[0]+"```", inline = True)
    ticketChannel = db[str(guild.id)+"info"].split(" ")[3]
    channel = client.get_channel(int(ticketChannel))
    message1 = await channel.send(embed=embedVar, view=ViewWithButton())
    message_id=str(message1.id)
    db[str(i)] = db[str(i)]+"//"+message_id+str(message1.guild.id)
    #print(db[str(i)])


client.run(TOKEN)