import PyPDF2 as pdf
import json
import discord
from discord.ext import commands
import os
import csv

emptyBox = chr(0x2610)
xBox = chr(0x2612)
mEmoji = chr(0x1F1F2)
starEmoji = chr(0x2B50)
listEmoji = chr(0x1f4dc)
toolsEmoji = chr(0x1F6E0)
upEmoji = chr(0x23EB)

playbooks = ['Chosen', 'Crooked', 'Divine', 'Expert', 'Flake', 'Initiate', 'Monstrous', 'Mundane', 'Professional', 'Spell-Slinger', 'Spooky', 'Wronged']

class Character:
    def __init__(self, manifest, sheetFields, alias=''):
        self.manifest = manifest
        self.fields = {}
        for field in sheetFields:
            if('/V' in sheetFields[field]):
                self.fields[field] = sheetFields[field]['/V']
            elif(type(sheetFields[field]) == str):
                self.fields[field] = sheetFields[field]
        if(alias != ''):
            self.alias = alias
        else:
            self.alias = self.fields['name']
        self.moves = [self.manifest[move] for move in self.fields if move.startswith('move') and move in self.manifest]
        for field in self.fields:
        	if(field.startswith('move') and field not in self.manifest):
        		movePlaybook = field.replace('move', '')
        		while(movePlaybook[-1].isdigit() and len(movePlaybook) != 0):
        			movePlaybook = movePlaybook[:-1]
        		targetManifestFile = open('./Character Stuff/Field Data/{} Fields.json'.format(movePlaybook.title()))
        		targetManifest = json.load(targetManifestFile)
        		targetManifestFile.close()
        		targetMove = targetManifest[field.replace(movePlaybook, '')]
        		self.moves += [targetMove]


        self.harm = len([field for field in self.fields if field.startswith('harm')])
        self.luck = len([field for field in self.fields if field.startswith('luck')])
        self.xp = len([field for field in self.fields if field.startswith('xp')])
        self.charm = self.fields['charm']
        self.cool = self.fields['cool']
        self.sharp = self.fields['sharp']
        self.tough = self.fields['tough']
        self.weird = self.fields['weird']
        self.improvements, self.advanced = self.PopulateImprovements()
        self.inventory = self.Inventory()
        self.playbook = ''
        self.playbookMessage = None
    def Playbook():
        return ''
    def __repr__(self):
        reprString = ''
        for field in self.fields:
            if(field in self.manifest):
                reprString += '{}: {}\n'.format(field, self.manifest[field])
            else:
                reprString += '{}: {}\n'.format(field, self.fields[field])
        return reprString
    def __getitem__(self, key):
        if(key in self.fields and key in self.manifest):
            return self.manifest[key]
        elif(key in self.fields):
            return self.fields[key]
    def PopulateImprovements(self):
        improvements = []
        advanced = []
        for item in self.manifest:
            if(item.startswith('improvement')):
                if(item in self.fields):
                    improvements.append((item, True))
                else:
                    improvements.append((item, False))
            elif(item.startswith('advanced')):
                if(item in self.fields):
                    advanced.append((item, True))
                else:
                    advanced.append((item, False))
        return improvements, advanced
    def Inventory(self):
        #if(self.fields['name'].title()+'.csv' in os.listdir('./Character Stuff/Inventories/')):
        if(self.alias.title()+'.csv' in os.listdir('./Character Stuff/Inventories/')):
            #inventoryFile = open('./Character Stuff/Inventories/'+self.fields['name'].title()+'.csv')
            inventoryFile = open('./Character Stuff/Inventories/'+self.alias.title()+'.csv')
            reader = csv.reader(inventoryFile)
            inventoryList = []
            for row in list(reader):
                inventoryList += row
            return inventoryList
        else:
            return []
    def TakeHarm(self, harm):
        self.harm += harm
        if(self.harm > 7):
            self.harm = 7
        if(self.harm < 0):
            self.harm = 0
        self.UpdateFields()
    def MarkXP(self, xp):
        self.xp += xp
        #if(self.xp > 5):
        #    self.xp = 5
        if(self.xp < 0):
            self.xp = 0
        self.UpdateFields()
    def MarkLuck(self, luck):
        self.luck += luck
        if(self.luck > 7):
            self.luck = 7
        if(self.luck < 0):
            self.luck = 0
        self.UpdateFields()
    def UpdateFields(self):
        # Harm
        for harm in range(self.harm):
            self.fields['harm{}'.format(harm)] = '/Yes'
        for harmField in [field for field in self.fields if field.startswith('harm')]:
            if(harmField[-1].isdigit() and int(harmField[-1]) >= self.harm):
                self.fields.pop(harmField)
        # XP
        for xp in range(self.xp):
            self.fields['xp{}'.format(xp)] = '/Yes'
        for xpField in [field for field in self.fields if field.startswith('xp')]:
            if(xpField[-1].isdigit() and int(xpField[-1]) >= self.xp):
                self.fields.pop(xpField)
        # Luck
        for luck in range(self.luck):
            self.fields['luck{}'.format(luck)] = '/Yes'
        for luckField in [field for field in self.fields if field.startswith('luck')]:
            if(luckField[-1].isdigit() and int(luckField[-1]) >= self.luck):
                self.fields.pop(luckField)
    def Save(self, directory='Demo Characters'):
        self.UpdateFields()
        path = './Character Stuff/{}/'.format(directory)
        characterFile = open(path+self.alias+'.json', 'w')
        characterFile.write(json.dumps(self.fields))
        characterFile.close()
    def LoadFromJSON(name='', playbook=None, activeGame='Demo Characters'):
        directory = './Character Stuff/{}/'.format(activeGame)
        manifestPath = './Character Stuff/Field Data/'
        if(name+'.json' in os.listdir(directory) and issubclass(playbook, Character)):
            characterFile = open(directory+name+'.json', 'r')
            fields = json.load(characterFile)
            manifestFile = open(manifestPath+'{} Fields.json'.format(playbook.Playbook()), 'r')
            manifest = json.load(manifestFile)
            characterFile.close()
            manifestFile.close()
            return playbook(manifest, fields)


class Chosen(Character):
    def __init__(self, manifest, sheetFields, alias=''):
        Character.__init__(self, manifest, sheetFields, alias)
        self.moves.append(self.manifest['move5'])
        self.moves.append(self.manifest['move6'])
        self.weapon = self.SetWeapon()
        self.playbook = 'Chosen'
        self.playbookMessage = ChosenMessage
    def Playbook():
        return 'Chosen'
    def SetWeapon(self):
        forms = [form for form in self.fields if form.startswith('form')]
        if(forms != []):
            form = forms[0] # Only allowed to have one form
        ends = [end for end in self.fields if end.startswith('end')][0:3]
        harm = 0
        tags = []
        name = ''
        endNames = []
        if(form == 'form0'):
            name = 'staff'
            harm += 1
            tags.append('hand/close')
        elif(form == 'form1'):
            name = 'haft'
            harm += 2
            tags.append('hand')
            tags.append('heavy')
        elif(form == 'form2'):
            name = 'handle'
            harm += 1
            tags.append('hand')
            tags.append('balanced')
        elif(form == 'form3'):
            name = 'chain'
            harm += 1
            tags.append('hand')
            tags.append('area')
        if('end0' in ends):
            endNames.append('artifact')
            tags.append('magic')
        if('end1' in ends):
            endNames.append('spikes')
            harm += 1
            tags.append('messy')
        if('end2' in ends):
            endNames.append('blade')
            harm += 1
        if('end3' in ends):
            endNames.append('heavy')
            harm += 1
        if('end4' in ends):
            endNames.append('long')
            tags.append('close')
        if('end5' in ends):
            endNames.append('thorwable')
            tags.append('close')
        if('end6' in ends):
            endNames.append('chain')
            tags.append('area')
        tags.append('{}-harm'.format(harm))
        return '**{} {}** form with {} ({})'.format(self.fields['material'].title(), name.title(), ', '.join(endNames), ' '.join(tags))

class Crooked(Character):
    def __init__(self, manifest, sheetFields, alias=''):
        Character.__init__(self, manifest, sheetFields, alias)
        self.heat = self.FillHeat()
        self.underworld = self.manifest[[field for field in self.fields if field.startswith('underworld')][0]]
        self.background = self.manifest[[field for field in self.fields if field.startswith('background')][0]]
        self.playbook = 'Crooked'
        self.playbookMessage = CrookedMessage
    def Playbook():
        return 'Crooked'
    def FillHeat(self):
        # Populate the heat based on what the player has input
        heatText = [heat for heat in self.fields if heat.startswith('heatText')]
        heats = [heat for heat in self.fields if heat.startswith('heat') and not heat.startswith('heatText')]
        returnHeat = ''
        for heat in range(len(heats)):
            returnHeat += self.manifest[heats[heat]].format(self.fields[heatText[heat]]) + '\n'
        return returnHeat

class Divine(Character):
    def __init__(self, manifest, sheetFields, alias=''):
        Character.__init__(self, manifest, sheetFields, alias)
        self.mission = self.manifest[[field for field in self.fields if field.startswith('mission')][0]]
        self.weapon = self.manifest[[field for field in self.fields if field.startswith('gear')][0]]
        self.playbook = 'Divine'
        self.playbookMessage = DivineMessage
    def Playbook():
        return 'Divine'

class Expert(Character):
    def __init__(self, manifest, sheetFields, alias=''):
        Character.__init__(self, manifest, sheetFields, alias)
        self.haven = [self.manifest[field] for field in self.fields if field.startswith('haven')]
        self.playbook = 'Expert'
        self.playbookMessage = ExpertMessage
    def Playbook():
        return 'Expert'

class Flake(Character):
    def __init__(self, manifest, sheetFields, alias=''):
        Character.__init__(self, manifest, sheetFields, alias)
        self.playbook = 'Flake'
        self.playbookMessage = FlakeMessage
    def Playbook():
        return 'Flake'

class Initiate(Character):
    def __init__(self, manifest, sheetFields, alias=''):
        Character.__init__(self, manifest, sheetFields, alias)
        self.good = [self.manifest[field] for field in self.fields if field.startswith('good')]
        self.bad = [self.manifest[field] for field in self.fields if field.startswith('bad')]
        self.playbook = 'Initiate'
        self.playbookMessage = InitiateMessage
    def Playbook():
        return 'Initiate'

class Monstrous(Character):
    def __init__(self, manifest, sheetFields, alias=''):
        Character.__init__(self, manifest, sheetFields, alias)
        self.attacks = self.NaturalAttack()
        self.curse = [self.manifest[field] for field in self.fields if field.startswith('curse')][0]
        self.playbook = 'Monstrous'
        self.playbookMessage = MonstrousMessage
    def Playbook():
        return 'Monstrous'
    def NaturalAttack(self):
        bases = [base for base in self.fields if base.startswith('base')]
        extras = [extra for extra in self.fields if extra.startswith('extra')]
        attacks = []
        for base in range(len(bases)):
            baseName = ''
            baseHarm = 0
            baseTags = []
            if(bases[base] == 'base0'):
                baseName = 'Teeth'
                baseHarm = 3
                baseTags.append('intimate')
            elif(bases[base] == 'base1'):
                baseName = 'Claws'
                baseHarm = 2
                baseTags.append('hand')
            elif(bases[base] == 'base2'):
                baseName = 'Magical Force'
                baseHarm = 1
                baseTags.append('magical')
                baseTags.append('close')
            elif(bases[base] == 'base3'):
                baseName = 'Life-Drain'
                baseHarm = 1
                baseTags.append('intimate')
                baseTags.append('life-drain')
            # Instead of extras applying to one base, apply to all bases
            # This is against the rules but way easier to manage automatically
            for extra in extras:
                if(extra == 'extra0'):
                    baseHarm += 1
                elif(extra == 'extra1'):
                    baseTags.append('ignore-armour')
                elif(extra == 'extra2'):
                    baseTags.append('close')
            attacks.append(MonstrousAttack(baseName, baseHarm, baseTags))
        return attacks
class MonstrousAttack:
    def __init__(self, base='', harm=0, tags=[]):
        self.base = base
        self.harm = harm
        self.tags = tags
    def __repr__(self):
        return 'Base: {} ({}-harm {})'.format(self.base, self.harm, ' '.join(self.tags))

class Mundane(Character):
    def __init__(self, manifest, sheetFields, alias=''):
        Character.__init__(self, manifest, sheetFields, alias)
        self.playbook = 'Mundane'
        self.playbookMessage = MundaneMessage
    def Playbook():
        return 'Mundane'

class Professional(Character):
    def __init__(self, manifest, sheetFields, alias=''):
        Character.__init__(self, manifest, sheetFields, alias)
        self.resources = [self.manifest[field] for field in self.fields if field.startswith('resource')]
        self.redtape = [self.manifest[field] for field in self.fields if field.startswith('redtape')]
        self.playbook = 'Professional'
        self.playbookMessage = ProfessionalMessage
    def Playbook():
        return 'Professional'

class SpellSlinger(Character):
    def __init__(self, manifest, sheetFields, alias=''):
        Character.__init__(self, manifest, sheetFields, alias)
        self.techniques = self.Techniques()
        self.combatMagic = self.CombatMagic()
        self.playbook = 'Spell-Slinger'
        self.playbookMessage = SpellSlingerMessage
    def Playbook():
        return 'Spell-Slinger'
    def Techniques(self):
        # Check the 3 that you do use, leave the one you don't need blank
        techniques = [self.manifest[technique] for technique in self.fields if technique.startswith('technique')]
        return techniques
    def CombatMagic(self):
        bases = [base for base in self.fields if base.startswith('base')]
        effects = [effect for effect in self.fields if effect.startswith('effect')]
        spells = []
        for base in range(len(bases)):
            baseName = ''
            baseHarm = 0
            baseTags = []
            spellEffects = []
            if(bases[base] == 'base0'):
                baseName = 'Blast'
                baseHarm = 2
                baseTags = ['Magic', 'Close', 'Obvious', 'Loud']
            elif(bases[base] == 'base1'):
                baseName = 'Ball'
                baseHarm = 1
                baseTags = ['Magic', 'Area', 'Close', 'Obvious', 'Loud']
            elif(bases[base] == 'base2'):
                baseName = 'Missile'
                baseHarm = 1
                baseTags = ['Magic', 'Far', 'Obvious', 'Loud']
            elif(bases[base] == 'base3'):
                baseName = 'Wall'
                baseHarm = 1
                baseTags = ['Magic', 'Barrier', 'Close', '1-Armour', 'Obvious', 'Loud']
            for effect in range(len(effects)):
                if(effects[effect] == 'effect0'):
                    spellEffects.append('Fire')
                    baseHarm += 2
                    baseTags.append('Fire')
                    baseTags.append('[if you get a 10+ on a combat magic roll, the fire won\'t spread.]')
                elif(effects[effect] == 'effect1'):
                    spellEffects.append('Force/Wind')
                    baseHarm += 1
                    baseTags.append('Forceful')
                    if(baseName == 'Wall'):
                        baseTags.append('+1 Armour')
                elif(effects[effect] == 'effect2'):
                    spellEffects.append('Lightning/Entropy')
                    baseHarm += 1
                    baseTags.append('messy')
                elif(effects[effect] == 'effect3'):
                    spellEffects.append('Frost/Ice')
                    if(baseName == 'Wall'):
                        baseHarm -= 1
                        baseTags.append('+2 Armour')
                    else:
                        baseHarm += 1
                        baseTags.append('Restraining')
                elif(effects[effect] == 'effect4'):
                    spellEffects.append('Earth')
                    baseTags.append('Forceful')
                    baseTags.append('Restraining')
                elif(effects[effect] == 'effect5'):
                    spellEffects.append('Necromantic')
                    baseTags.append('Life-Drain')
            spells.append(CombatSpell(baseName, spellEffects, baseHarm, baseTags))
        return spells    
    
class CombatSpell:
    def __init__(self, base='', effects=[], harm=0, tags=[]):
        self.base = base
        self.harm = harm
        self.tags = tags
        self.effects = effects
    def __repr__(self):
        return 'Base: {} ({}) ({}-harm {})'.format(self.base,', '.join(self.effects), self.harm, ' '.join(self.tags))

class Spooky(Character):
    def __init__(self, manifest, sheetFields, alias=''):
        Character.__init__(self, manifest, sheetFields, alias)
        self.darkside = [self.manifest[dark] for dark in self.fields if dark.startswith('darkside')]
        self.playbook = 'Spooky'
        self.playbookMessage = SpookyMessage
    def Playbook():
        return 'Spooky'

class Wronged(Character):
    def __init__(self, manifest, sheetFields, alias=''):
        Character.__init__(self, manifest, sheetFields, alias)
        self.lost = self.Loss()
        self.prey = self.fields['prey']
        self.guilt = [self.manifest[field] for field in self.fields if field.startswith('save')]
        self.signatureWeapon = [self.manifest[field] for field in self.fields if field.startswith('signature')]
        self.playbook = 'Wronged'
        self.playbookMessage = WrongedMessage
    def Playbook():
        return 'Wronged'
    def Loss(self):
        losses = [loss for loss in self.fields if loss.startswith('lost') and not loss.startswith('lostText')]
        lossesText = [loss for loss in self.fields if loss.startswith('lostText')]
        if(len(losses) == len(lossesText)):
            yourLosses = ['{}, {}.'.format(self.manifest[losses[index]], self.fields[lossesText[index]]) for index in range(len(losses))]
        else:
            yourLosses = ['I think you filled this out wrong.']
        return yourLosses

'''
def LoadCharacter(playbook='Chosen'):
    sheetPath = './Character Stuff/Demo Characters/'
    fieldPath = './Character Stuff/Field Data/'
    pdfFileObj = open(sheetPath+'The_{}.pdf'.format(playbook), 'rb')
    pdfReader = pdf.PdfFileReader(pdfFileObj)
    fields = pdfReader.getFields()
    fieldData = open(fieldPath+'{} Fields.json'.format(playbook))
    data = json.load(fieldData)
    fieldData.close()
    pdfFileObj.close()
    return data,fields
'''

class CharacterMessage:
    def __init__(self, character, user):
        self.character = character
        self.user = user
        self.message = None
        self.embed = discord.Embed()
        self.stats = "Charm: {}\nCool: {}\nSharp: {}\nTough: {}\nWeird: {}".format(self.character.charm, self.character.cool, self.character.sharp, self.character.tough, self.character.weird)
        self.harm = "**Harm:** " + str(xBox)*self.character.harm + str(emptyBox)*(7-self.character.harm)
        self.luck = "**Luck:** " + str(xBox)*self.character.luck + str(emptyBox)*(7-self.character.luck)
        self.xp = "**Experience:** " + str(xBox)*self.character.xp + str(emptyBox)*(5-self.character.xp)
        self.improvements = self.character.improvements
        self.advanced = self.character.advanced
        self.moves = '\n'.join(self.character.moves)
        self.helpText = ""
        self.embed.description = self.stats + '\n' + self.harm + '\n' + self.luck + '\n' + self.xp
    async def Send(self, context):
        self.message = await context.send(embed=self.embed)
        await self.SetReactions()
    async def ShowMoves(self):
        self.embed.clear_fields()
        self.embed.description = "**Moves**"
        for move in self.character.moves:
            self.embed.add_field(name=move.split('\n')[0], value=move.split('\n', 1)[1], inline=False)
        await self.message.edit(embed=self.embed)
        await self.SetReactions()
    async def SetReactions(self):
        await self.message.clear_reactions()
        await self.message.add_reaction(listEmoji)
        await self.message.add_reaction(mEmoji)
        await self.message.add_reaction(starEmoji)
        await self.message.add_reaction(toolsEmoji)
        await self.message.add_reaction(upEmoji)
    async def ShowInfo(self):
        self.embed.clear_fields()
        self.embed.description = self.stats + '\n' + self.harm + '\n' + self.luck + '\n' + self.xp
        await self.message.edit(embed=self.embed)
        await self.SetReactions()
    async def ShowImprovements(self):
        self.embed.clear_fields()
        self.embed.description = ''
        improvementList = []
        advancedList = []
        for improvement in self.improvements:
            if(improvement[1]):
                emoji = xBox
            else:
                emoji = emptyBox
            improvementList.append('{} {}'.format(emoji, self.character.manifest[improvement[0]]))
        for advanced in self.advanced:
            if(advanced[1]):
                emoji = xBox
            else:
                emoji = emptyBox
            advancedList.append('{} {}'.format(emoji, self.character.manifest[advanced[0]]))
        self.embed.add_field(name='**Improvements**', value='\n'.join(improvementList))
        self.embed.add_field(name='**Advanced**', value='\n'.join(advancedList))
        await self.message.edit(embed=self.embed)
        await self.SetReactions()
    async def PlaybookFields(self):
        pass
    async def ShowInventory(self):
        self.embed.clear_fields()
        self.embed.description = ''
        self.character.inventory = self.character.Inventory()
        if(len(self.character.inventory) > 0):
            self.embed.add_field(name="**Inventory**", value='\n'.join(self.character.inventory))
        else:
            self.embed.add_field(name="**Inventory**", value='you have no items lol')
        await self.message.edit(embed=self.embed)
        await self.SetReactions()

class ChosenMessage(CharacterMessage):
    def __init__(self, character, user):
        CharacterMessage.__init__(self, character, user)
        self.embed.title = "THE CHOSEN - {}".format(self.character['name'])
        self.weapon = self.character.weapon
        self.fate = [self.character.manifest[field] for field in self.character.fields if field.startswith('fate')][0]
        self.heroic = '\n'.join([self.character.manifest[field] for field in self.character.fields if field.startswith('heroic')])
        self.doom = '\n'.join([self.character.manifest[field] for field in self.character.fields if field.startswith('doom')])
    async def PlaybookFields(self):
        self.embed.clear_fields()
        description = ''
        self.embed.add_field(name="**Your Special Weapon**", value=self.weapon, inline=False)
        self.embed.add_field(name="**You discovered your fate through**", value=self.fate, inline=False)
        self.embed.add_field(name="**Heroic Fate**", value=self.heroic, inline=True)
        self.embed.add_field(name="**Doomed Fate**", value=self.doom, inline=True)
        self.embed.description = description
        await self.message.edit(embed=self.embed)
        await self.SetReactions()

class CrookedMessage(CharacterMessage):
    def __init__(self, character, user):
        CharacterMessage.__init__(self, character, user)
        self.embed.title = "THE CROOKED - {}".format(self.character['name'])
        self.heat = self.character.heat
        self.underworld = self.character.underworld
        self.background = self.character.background
    async def PlaybookFields(self):
        self.embed.clear_fields()
        description = ''
        self.embed.add_field(name="**Heat**", value=self.heat, inline=False)
        self.embed.add_field(name="**Underworld**", value=self.underworld, inline=False)
        self.embed.add_field(name="**Background**", value=self.background, inline=False)
        self.embed.description = description
        await self.message.edit(embed=self.embed)
        await self.SetReactions()

class DivineMessage(CharacterMessage):
    def __init__(self, character, user):
        CharacterMessage.__init__(self, character, user)
        self.embed.title = "THE DIVINE - {}".format(self.character['name'])
        self.weapon = self.character.weapon
        self.mission = self.character.mission
    async def PlaybookFields(self):
        self.embed.clear_fields()
        description = ''
        self.embed.add_field(name="**Mission**", value=self.mission, inline=False)
        self.embed.add_field(name="**Holy Weapon**", value=self.weapon, inline=False)
        self.embed.description = description
        await self.message.edit(embed=self.embed)
        await self.SetReactions()

class ExpertMessage(CharacterMessage):
    def __init__(self, character, user):
        CharacterMessage.__init__(self, character, user)
        self.embed.title = "THE EXPERT - {}".format(self.character['name'])
        self.haven = self.character.haven
    async def PlaybookFields(self):
        self.embed.clear_fields()
        description = 'You have set up ahaven, a safe place to work. This haven has these properties:'
        for havenField in self.haven:
            self.embed.add_field(name=havenField.split('\n')[0], value=havenField.split('\n')[1], inline=False)
        self.embed.description = description
        await self.message.edit(embed=self.embed)
        await self.SetReactions()      
        
class FlakeMessage(CharacterMessage):
    def __init__(self, character, user):
        CharacterMessage.__init__(self, character, user)
        self.embed.title = "THE FLAKE - {}".format(self.character['name'])
    async def PlaybookFields(self):
        self.embed.clear_fields()
        description = 'Lorem ipsum idk Flake didn\'t have anything that fits here.'
        self.embed.description = description
        await self.message.edit(embed=self.embed)
        await self.SetReactions()

class InitiateMessage(CharacterMessage):
    def __init__(self, character, user):
        CharacterMessage.__init__(self, character, user)
        self.embed.title = "THE INITIATE - {}".format(self.character['name'])
        self.good = self.character.good
        self.bad = self.character.bad
    async def PlaybookFields(self):
        self.embed.clear_fields()
        description = ''
        self.embed.add_field(name="**Sect Good Traditions**", value='\n'.join(self.good), inline=True)
        self.embed.add_field(name="**Sect Bad Traditions**", value='\n'.join(self.bad), inline=True)
        self.embed.description = description
        await self.message.edit(embed=self.embed)
        await self.SetReactions()

class MonstrousMessage(CharacterMessage):
    def __init__(self, character, user):
        CharacterMessage.__init__(self, character, user)
        self.embed.title = "THE MONSTROUS - {}".format(self.character['name'])
        self.attacks = self.character.attacks
        self.curse = self.character.curse
    async def PlaybookFields(self):
        self.embed.clear_fields()
        description = ''
        self.embed.add_field(name="**CURSE -** " + self.curse.split('\n')[0], value=self.curse.split('\n')[1], inline=False)
        self.embed.add_field(name="**Natural Attacks**", value='\n'.join([str(attack) for attack in self.attacks]), inline=False)
        self.embed.description = description
        await self.message.edit(embed=self.embed)
        await self.SetReactions()

class MundaneMessage(CharacterMessage):
    def __init__(self, character, user):
        CharacterMessage.__init__(self, character, user)
        self.embed.title = "THE MUNDANE - {}".format(self.character['name'])
    async def PlaybookFields(self):
        self.embed.clear_fields()
        description = 'Lorem ipsum idk Flake didn\'t have anything that fits here.'
        self.embed.description = description
        await self.message.edit(embed=self.embed)
        await self.SetReactions()

class ProfessionalMessage(CharacterMessage):
    def __init__(self, character, user):
        CharacterMessage.__init__(self, character, user)
        self.embed.title = "THE PROFESSIONAL - {}".format(self.character['name'])
        self.resources = self.character.resources
        self.redtape = self.character.redtape
    async def PlaybookFields(self):
        self.embed.clear_fields()
        description = ''
        self.embed.add_field(name="**Agency Resources**", value='\n'.join(self.resources), inline=True)
        self.embed.add_field(name="**Agency Red Tape**", value='\n'.join(self.redtape), inline=True)
        self.embed.description = description
        await self.message.edit(embed=self.embed)
        await self.SetReactions()

class SpellSlingerMessage(CharacterMessage):
    def __init__(self, character, user):
        CharacterMessage.__init__(self, character, user)
        self.embed.title = "THE SPELL-SLINGER - {}".format(self.character['name'])
        self.techniques = self.character.techniques
        self.combatMagic = self.character.combatMagic
    async def PlaybookFields(self):
        self.embed.clear_fields()
        description = ''
        self.embed.add_field(name="**Techniques Needed for Combat Magic**", value='\n'.join(self.techniques))
        self.embed.add_field(name="**Combat Magic**", value='\n'.join([str(spell) for spell in self.combatMagic]))
        self.embed.description = description
        await self.message.edit(embed=self.embed)
        await self.SetReactions()

class SpookyMessage(CharacterMessage):
    def __init__(self, character, user):
        CharacterMessage.__init__(self, character, user)
        self.embed.title = "THE SPOOKY - {}".format(self.character['name'])
        self.darkside = self.character.darkside
    async def PlaybookFields(self):
        self.embed.clear_fields()
        description = ''
        self.embed.add_field(name="**Dark Side**", value='\n'.join(self.darkside))
        self.embed.description = description
        await self.message.edit(embed=self.embed)
        await self.SetReactions()

class WrongedMessage(CharacterMessage):
    def __init__(self, character, user):
        CharacterMessage.__init__(self, character, user)
        self.embed.title = "THE WRONGED - {}".format(self.character['name'])
        self.lost = self.character.lost
        self.guilt = self.character.guilt
        self.prey = self.character.prey
        self.signatureWeapon = self.character.signatureWeapon
    async def PlaybookFields(self):
        self.embed.clear_fields()
        description = ''
        self.embed.add_field(name="**Your Prey**", value=self.prey, inline=False)
        self.embed.add_field(name="**You Lost...**", value='\n'.join(self.lost), inline=True)
        self.embed.add_field(name="**Because You Were...**", value='\n'.join(self.guilt), inline=True)
        self.embed.add_field(name="**Your Signature Weapon**", value='\n'.join(self.signatureWeapon), inline=False)
        self.embed.description = description
        await self.message.edit(embed=self.embed)
        await self.SetReactions()


def LoadAllCharacters(playerCharacters=[], activeGame='Demo Characters'):
    playbookClasses = [Chosen, Crooked, Divine, Expert, Flake, Initiate, Monstrous, Mundane, Professional, SpellSlinger, Spooky, Wronged]
    characters = {}
    for playbook in playbookClasses:
        data, fields = LoadCharacter(playbook.Playbook())
        character = playbook(data, fields, alias=playbook.Playbook())
        characters[playbook.Playbook()] = character
    for playerCharacter in playerCharacters:
        data, fields = LoadCharacter(playbook=playerCharacter[1].Playbook(), sheetPath='./Character Stuff/{}/'.format(activeGame), name=playerCharacter[0])
        character = playerCharacter[1](data, fields, alias=playerCharacter[0])
        characters[playerCharacter[0]] = character
    return characters

def LoadAllCharactersFromJSON(playerCharacters=[], activeGame='Demo Characters'):
    playbookClasses = [Chosen, Crooked, Divine, Expert, Flake, Initiate, Monstrous, Mundane, Professional, SpellSlinger, Spooky, Wronged]
    characters = {}
    for playbook in playbookClasses:
        if('{}.json'.format(playbook.Playbook()) in os.listdir('./Character Stuff/{}/'.format(activeGame))):
            manifestFile = open('./Character Stuff/Field Data/{} Fields.json'.format(playbook.Playbook()), 'r')
            manifest = json.load(manifestFile)
            manifestFile.close()
            fieldsFile = open('./Character Stuff/{}/{}.json'.format(activeGame, playbook.Playbook()), 'r')
            fields = json.load(fieldsFile)
            fieldsFile.close()
            characters[playbook.Playbook()] = playbook(manifest, fields, alias=playbook.Playbook())
    for playerCharacter in playerCharacters:
        if('{}.json'.format(playerCharacter[0]) in os.listdir('./Character Stuff/{}/'.format(activeGame))):
            playbook = playerCharacter[1]
            name = playerCharacter[0]
            manifestFile = open('./Character Stuff/Field Data/{} Fields.json'.format(playbook.Playbook()), 'r')
            manifest = json.load(manifestFile)
            manifestFile.close()
            fieldsFile = open('./Character Stuff/{}/{}.json'.format(activeGame, name), 'r')
            fields = json.load(fieldsFile)
            fieldsFile.close()
            characters[name] = playbook(manifest, fields, alias=name)
    return characters

def DumpPDFToJSON(directory='Demo Characters', name='Chosen', playbook=Chosen):
    path = './Character Stuff/{}/'.format(directory)
    data, fields = LoadCharacter(playbook=playbook.Playbook(), sheetPath=path, name=name)
    character = playbook(data, fields)
    character.Save()


def LoadCharacter(playbook='Chosen', sheetPath='./Character Stuff/Demo Characters/', name=None):
    #sheetPath = './Character Stuff/Demo Characters/'
    fieldPath = './Character Stuff/Field Data/'
    if(name == None):
        name = 'The_{}'.format(playbook)
    #pdfFileObj = open(sheetPath+'The_{}.pdf'.format(playbook), 'rb')
    pdfFileObj = open(sheetPath+'{}.pdf'.format(name), 'rb')
    pdfReader = pdf.PdfFileReader(pdfFileObj)
    fields = pdfReader.getFields()
    blankBoxes = []
    for field in fields:
        if(fields[field]['/FT'] == '/Btn' and '/V' in fields[field] and fields[field]['/V'] == '/Off'):
            blankBoxes.append(field)
    for blank in blankBoxes:
        fields.pop(blank)
    fieldData = open(fieldPath+'{} Fields.json'.format(playbook))
    data = json.load(fieldData)
    fieldData.close()
    pdfFileObj.close()
    return data,fields

def PlaybookByName(name='Chosen'):
    for playbook in [Chosen, Crooked, Divine, Expert, Flake, Initiate, Monstrous, Mundane, Professional, SpellSlinger, Spooky, Wronged]:
        if(playbook.Playbook() == name.title()):
            return playbook