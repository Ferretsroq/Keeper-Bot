const {ActionRowBuilder, SelectMenuBuilder, ButtonBuilder, ButtonStyle, SelectMenuOptionBuilder, EmbedBuilder} = require('discord.js');
fs = require('fs');
const {PDFDocument} = require('pdf-lib');


let emptyBox = String.fromCharCode(parseInt('2610', 16));
let xBox = String.fromCharCode(parseInt('2612', 16));
let mEmoji = String.fromCharCode(parseInt('1F1F2', 16));
let starEmoji = String.fromCharCode(parseInt('2B50', 16));
let listEmoji = String.fromCharCode(parseInt('1f4dc', 16));
let toolsEmoji = String.fromCharCode(parseInt('1F6E0', 16));
let upEmoji = String.fromCharCode(parseInt('23EB', 16));

const playbooks = ['Chosen', 'Crooked', 'Divine', 'Expert', 'Flake', 'Initiate', 'Monstrous', 'Mundane', 'Professional', 'Spell-Slinger', 'Spooky', 'Wronged'];

class Character
{
    constructor(manifest, sheetFields, alias='')
    {
        this.manifest = manifest;
        this.fields = {};
        let keys = Object.keys(sheetFields.fields);
        for(let fieldIndex = 0; fieldIndex < keys.length; fieldIndex++)
        {
            if(sheetFields.fields[keys[fieldIndex]].includes('/V'))
            {
                this.fields[keys[fieldIndex]] = sheetFields.fields[keys[fieldIndex]]['/V'];
            }
            else if(typeof(sheetFields.fields[keys[fieldIndex]]) == 'string')
            {
                this.fields[keys[fieldIndex]] = sheetFields.fields[keys[fieldIndex]];
            }
        }
        if(alias != '')
        {
            this.alias = alias
        }
        else
        {
            this.alias = this.fields['name']
        }
        this.moves = [];
        let fieldKeys = Object.keys(this.fields);
        for(let moveIndex = 0; moveIndex < fieldKeys.length; moveIndex++)
        {
            if(fieldKeys[moveIndex].startsWith('move') && Object.keys(this.manifest).includes(fieldKeys[moveIndex]))
            {
                this.moves.push(this.manifest[fieldKeys[moveIndex]]);
            }
        }
        for(let fieldIndex = 0; fieldIndex < fieldKeys.length; fieldIndex++)
        {
            if(fieldKeys[fieldIndex].startsWith('move') && !Object.keys(this.manifest).includes(fieldKeys[fieldIndex]))
            {
                let movePlaybook = fieldKeys[fieldIndex].replace('move', '');
                while(!isNaN(movePlaybook.slice(-1)))
                {
                    movePlaybook = movePlaybook.slice(0, movePlaybook.length-1);
                }
                let targetManifestFile = fs.readFileSync(`./Character Stuff/Field Data/${movePlaybook} Fields.json`);
                let targetManifest = JSON.parse(targetManifestFile);
                let targetMove = targetManifest[fieldKeys[fieldIndex].replace(movePlaybook, '')];
                this.moves.push(targetMove);
            }
        }


        this.harm = Object.keys(this.fields).filter(field => field.startsWith('harm')).length;
        this.luck = Object.keys(this.fields).filter(field => field.startsWith('luck')).length;
        this.xp = Object.keys(this.fields).filter(field => field.startsWith('xp')).length;
        this.charm = this.fields['charm'];
        this.cool = this.fields['cool'];
        this.sharp = this.fields['sharp'];
        this.tough = this.fields['tough'];
        this.weird = this.fields['weird'];
        [this.improvements, this.advanced] = this.PopulateImprovements();
        this.inventory = this.Inventory();
        this.playbook = '';
        this.playbookMessage = null;
    }
    Playbook()
    {
        return ''
    }
    toString()
    {
        let returnString = '';
        let fieldKeys = Object.keys(this.fields);
        for(let fieldIndex = 0; fieldIndex < fieldKeys.length; fieldIndex++)
        {
            if(Object.keys(this.manifest).includes(this.fields[fieldKeys[fieldIndex]]))
            {
                returnString += `${this.fields[fieldKeys[fieldIndex]]}: ${this.manifest[this.fields[fieldKeys[fieldIndex]]]}\n`;
            }
            else
            {
                returnString += `${fieldKeys[fieldIndex]}: ${this.fields[fieldKeys[fieldIndex]]}\n`;
            }
        }
        return returnString;
    }
    toEmbed()
    {
        let stats = `Charm: ${this.charm}\nCool: ${this.cool}\nSharp: ${this.sharp}\nTough: ${this.tough}\nWeird: ${this.weird}`;
        let harm = "**Harm:** " + xBox.repeat(this.harm) + emptyBox.repeat(7-this.harm);
        let luck = "**Luck:** " + xBox.repeat(this.luck) + emptyBox.repeat(7-this.luck);
        let xp = "**Experience:** " + xBox.repeat(this.xp) + emptyBox.repeat(5-this.xp);
        let improvements = this.improvements;
        let advanced = this.advanced
        let moves = this.moves.join('\n');
        let helpText = ""
        let description = stats + '\n' + harm + '\n' + luck + '\n' + xp;
        let embed = new EmbedBuilder().setTitle(`**The ${this.Playbook()} — ${this.alias}**`).setDescription(description);
        for(let move = 0; move < this.moves.length; move++)
        {
            embed.addFields({name: this.moves[move].split('\n')[0], value: this.moves[move].split('\n').splice(1).join('\n')});
        }
        let improvementList = [];
        let advancedList = [];
        let emoji = '';
        for(let improvement = 0; improvement < this.improvements.length; improvement++)
        {
            if(this.improvements[improvement][1])
            {
                emoji = xBox;
            }
            else
            {
                emoji = emptyBox;
            }
            improvementList.push(`${emoji} ${this.manifest[this.improvements[improvement][0]]}`);
        }
        for(let advanced = 0; advanced < this.advanced.length; advanced++)
        {
            if(this.advanced[advanced][1])
            {
                emoji = xBox;
            }
            else
            {
                emoji = emptyBox;
            }
            advancedList.push(`${emoji} ${this.manifest[this.advanced[advanced][0]]}`);
        }

        embed.addFields({name: '**Improvements**', value: improvementList.join('\n'), inline: true});
        embed.addFields({name: '**Advanced**', value: advancedList.join('\n'), inline: true});
        return embed;        
    }
    PopulateImprovements()
    {
        let improvements = [];
        let advanced = [];
        let manifestKeys = Object.keys(this.manifest);
        for(let itemIndex = 0; itemIndex < manifestKeys.length; itemIndex++)
        {
            if(manifestKeys[itemIndex].startsWith('improvement'))
            {
                if(Object.keys(this.fields).includes(manifestKeys[itemIndex]))
                {
                    improvements.push([manifestKeys[itemIndex], true]);
                }
                else
                {
                    improvements.push([manifestKeys[itemIndex], false]);
                }
            }
            else if(manifestKeys[itemIndex].startsWith('advanced'))
            {
                if(Object.keys(this.fields).includes(manifestKeys[itemIndex]))
                {
                    advanced.push([manifestKeys[itemIndex], true]);
                }
                else
                {
                    advanced.push([manifestKeys[itemIndex], false]);
                }
            }
        }
        return [improvements, advanced];
    }
    Inventory()
    {
        if(fs.existsSync(`./Character Stuff/Inventories/${this.alias}.json`))
        {
            let inventoryFile = fs.readFileSync(`./Character Stuff/Inventories/${this.alias}.json`);
            let inventory = JSON.parse(inventoryFile);
            return inventory;
            //return inventoryFile.split(',');
        }
        else
        {
            return [];
        }
    }
    TakeHarm(harm)
    {
        this.harm += harm;
        if(this.harm > 7)
        {
            this.harm = 7;
        }
        else if (this.harm < 0)
        {
            this.harm = 0;
        }
        this.UpdateFields();
    }
    MarkXP(xp)
    {
        this.xp += xp;
        if(this.xp < 0)
        {
            this.xp = 0;
        }
        this.UpdateFields;
    }
    MarkLuck(luck)
    {
        this.luck += luck;
        if(this.luck > 7)
        {
            this.luck = 7;
        }
        else if(this.luck < 0)
        {
            this.luck = 0;
        }
        this.UpdateFields();
    }
    UpdateFields()
    {
        // Harm
        for(let harm = 0; harm < this.harm; harm++)
        {
            this.fields[`harm${harm}`] = '/Yes';
        }
        let harmFields = Object.keys(this.fields).filter(field => field.startsWith('harm'));
        for(let harmField = 0; harmField < harmFields.length; harmField++)
        {
            if(~isNaN(harmFields[harmField].slice(-1)) && parseInt(harmFields[harmField].slice(-1)) >= this.harm)
            {
                delete(this.fields[harmFields[harmField]]);
            }
        }
        // XP
        for(let xp = 0; xp < this.xp; xp++)
        {
            this.fields[`xp${xp}`] = '/Yes';
        }
        let xpFields = Object.keys(this.fields).filter(field => field.startsWith('xp'));
        for(let xpField = 0; xpField < xpFields.length; xpField++)
        {
            if(~isNaN(xpFields[xpField].slice(-1)) && parseInt(xpFields[xpField].slice(-1)) >= this.xp)
            {
                delete(this.fields[xpFields[xpField]]);
            }
        }
        // Luck
        for(let luck = 0; luck < this.luck; luck++)
        {
            this.fields[`luck${luck}`] = '/Yes';
        }
        let luckFields = Object.keys(this.fields).filter(field => field.startsWith('luck'));
        for(let luckField = 0; luckField < luckFields.length; luckField++)
        {
            if(~isNaN(luckFields[luckField].slice(-1)) && parseInt(luckFields[luckField].slice(-1)) >= this.xp)
            {
                delete(this.fields[luckFields[luckField]]);
            }
        }
    }
    Save(directory = 'Demo Characters')
    {
        this.UpdateFields();
        let path = `./Character Stuff/${directory}`;
        fs.writeFileSync(`${path}/${this.alias}.json`, JSON.stringify(this, null, 2), 'utf8');
    }
    FromJSON(name = '', playbook = null, activeGame = 'Demo Characters')
    {
        let directory = `./Character Stuff/${activeGame}/`;
        let manifestPath = './Character Stuff/Field Data/';
        if(fs.existsSync(`${directory}${name}.json`))
        {
            let characterFile = fs.readFileSync(`${directory}${name}.json`);
            let fields = JSON.parse(characterFile);
            let manifestFile = fs.readFileSync(`${manifestPath}${playbook.Playbook()} Fields.json`);
            let manifest = JSON.parse(manifestFile);
            return new playbook(manifest, fields);
        }
    }
}

class Chosen extends Character
{
    constructor(manifest, sheetFields, alias='')
    {
        super(manifest, sheetFields, alias);
        this.moves.push(this.manifest['move5']);
        this.moves.push(this.manifest['move6']);
        this.weapon = this.SetWeapon();
        this.playbook = 'Chosen';
    }
    static Playbook()
    {
        return 'Chosen';
    }
    SetWeapon()
    {
        let forms = Object.keys(this.fields).filter(field => field.startsWith('form'));
        let form = '';
        if(forms.length != 0)
        {
            form = forms[0];
        }
        let ends = Object.keys(this.fields).filter(field => field.startsWith('end')).slice(0,3);
        let harm = 0;
        let tags = [];
        let name = '';
        let endNames = [];
        if(form == 'form0')
        {
            name = 'staff';
            harm += 1;
            tags.push('hand/close');
        }
        else if(form == 'form1')
        {
            name = 'haft';
            harm += 2;
            tags.push('hand');
            tags.push('heavy');
        }
        else if(form == 'form2')
        {
            name = 'handle';
            harm += 1;
            tags.push('hand');
            tags.push('balanced');
        }
        else if(form == 'form3')
        {
            name = 'chain';
            harm += 1;
            tags.push('hand');
            tags.push('area');
        }
        if(ends.includes('end0'))
        {
            endNames.push('artifact');
            tags.push('magic');
        }
        if(ends.includes('end1'))
        {
            endNames.push('spikes');
            harm += 1;
            tags.push('messy');
        }
        if(ends.includes('end2'))
        {
            endNames.push('blade');
            harm += 1;
        }
        if(ends.includes('end3'))
        {
            endNames.push('heavy');
            harm += 1;
        }
        if(ends.includes('end4'))
        {
            endNames.push('long');
            tags.push('close');
        }
        if(ends.includes('end5'))
        {
            endNames.push('throwable');
            tags.push('close');
        }
        if(ends.includes('end6'))
        {
            endNames.push('chain');
            tags.push('area');
        }
        tags.push(`${harm}-harm`);
        return `**${this.fields['material']} ${name}** form with ${endNames.join(', ')} (${tags.join(' ')})`;
    }
    playbookEmbed()
    {
        let embed = this.toEmbed();
        embed.setTitle(`**The Chosen — ${this.alias}**`)
        embed.addFields({name: '**Weapon**', value: this.weapon});
        return embed;
    }
}

class Crooked extends Character
{
   constructor(manifest, sheetFields, alias='')
    {
        super(manifest, sheetFields, alias)
        this.heat = this.FillHeat()
        this.underworld = this.manifest[Object.keys(this.fields).filter(field => field.startsWith('underworld'))[0]];
        this.background = this.manifest[Object.keys(this.fields).filter(field => field.startsWith('background'))[0]];
        this.playbook = 'Crooked';
    }
    static Playbook()
    {
        return 'Crooked';
    }
    FillHeat()
    {
        // Populate the heat based on what the player has input
        let heatText = Object.keys(this.fields).filter(field => field.startsWith('heatText'));
        let heats = Object.keys(this.fields).filter(field => field.startsWith('heat') && !field.startsWith('heatText'));
        let returnHeat = ''
        for(let heat = 0; heat < heats.length; heat++)
        {
            returnHeat += `${this.manifest[heats[heat]]}${this.fields[heatText[heat]]}\n`;
        }
        return returnHeat;
    }
    playbookEmbed()
    {
        let embed = this.toEmbed();
        embed.setTitle(`**The Crooked — ${this.alias}**`);
        embed.addFields({name: '**Heat**', value: this.heat});
        embed.addFields({name: '**Underworld**', value: this.underworld});
        embed.addFields({name: '**Background**', value: this.background});
        return embed;
    }
}

class Divine extends Character
{
    constructor(manifest, sheetFields, alias='')
    {
        super(manifest, sheetFields, alias);
        this.mission = this.manifest[Object.keys(field).filter(field => field.startsWith('mission'))[0]];
        this.weapon = this.manifest[Object.keys(field).filter(field => field.startsWith('gear'))[0]];
        this.playbook = 'Divine';
    }
    static Playbook()
    {
        return 'Divine';
    }
    playbookEmbed()
    {
        let embed = this.toEmbed();
        embed.setTitle(`**The Divine — ${this.alias}**`);
        embed.addFields({name: '**Mission**', value: this.mission});
        embed.addFields({name: '**Weapon**', value: this.weapon});
        return embed;
    }
}

class Expert extends Character
{
    constructor(manifest, sheetFields, alias='')
    {
        super(manifest, sheetFields, alias);
        let havenFields = Object.keys(this.fields).filter(field => field.startsWith('haven'));
        this.haven = [];
        for(let field = 0; field < havenFields.length; field++)
        {
            this.haven.push(this.manifest[havenFields[field]]);
        }
        this.playbook = 'Expert';
    }
    static Playbook()
    {
        return 'Expert';
    }
    playbookEmbed()
    {
        let embed = this.toEmbed();
        embed.setTitle(`**The Expert — ${this.alias}**`);
        embed.addFields({name: '**Haven**', value: this.haven.join('\n')});
        return embed;
    }
}

class Flake extends Character
{
    constructor(manifest, sheetFields, alias='')
    {
        super(manifest, sheetFields, alias);
        this.playbook = 'Flake';
    }
    static Playbook()
    {
        return 'Flake';
    }
    playbookEmbed()
    {
        let embed = this.toEmbed();
        embed.setTitle(`**The Flake — ${this.alias}**`);
        return embed;
    }
}

class Initiate extends Character
{
    constructor(manifest, sheetFields, alias='')
    {
        super(manifest, sheetFields, alias);
        let goodFields = Object.keys(this.fields).filter(field => field.startsWith('good'));
        let badFields = Object.keys(this.fields).filter(field => field.startsWith('bad'));
        this.good = [];
        this.bad = [];
        for(let good = 0; good < goodFields.length; good++)
        {
            this.good.push(this.manifest[goodFields[good]]);
        }
        for(let bad = 0; bad < badFields.length; bad++)
        {
            this.bad.push(this.manifest[badFields[bad]]);
        }
        this.playbook = 'Initiate';
    }
    static Playbook()
    {
        return 'Initiate';
    }
    playbookEmbed()
    {
        let embed = this.toEmbed();
        embed.setTitle(`**The Initiate — ${this.alias}**`);
        embed.addFields({name: '**Order Good Traits**', value: this.good.join('\n'), inline: true});
        embed.addFields({name: '**Order Bad Traits**', value: this.bad.join('\n'), inline: true});
        return embed;
    }
}

class Monstrous extends Character
{
    constructor(manifest, sheetFields, alias='')
    {
        super(manifest, sheetFields, alias);
        this.attacks = this.NaturalAttack()
        this.curse = this.manifest[Object.keys(this.fields).filter(field => field.startsWith('curse'))[0]];
        this.playbook = 'Monstrous';
    }
    static Playbook()
    {
        return 'Monstrous';
    }
    NaturalAttack()
    {
        let bases = Object.keys(this.fields).filter(field => field.startsWith('base'));
        let extras = Object.keys(this.fields).filter(field => field.startsWith('extra'));
        let attacks = [];
        for(let base = 0; base < bases.length; base++)
        {
            let baseName = '';
            let baseHarm = 0;
            let baseTags = [];
            if(bases[base] == 'base0')
            {
                baseName = 'Teeth';
                baseHarm = 3;
                baseTags.push('intimate');
            }
            else if(bases[base] == 'base1')
            {
                baseName = 'Claws';
                baseHarm = 2;
                baseTags.push('hand');
            }
            else if(bases[base] == 'base2')
            {
                baseName = 'Magical Force';
                baseHarm = 1;
                baseTags.push('magical');
                baseTags.push('close');
            }
            else if(bases[base] == 'base3')
            {
                baseName = 'Life-Drain';
                baseHarm = 1;
                baseTags.push('intimate');
                baseTags.push('life-drain');
            }
            // Instead of extras applying to one base, apply to all bases
            // This is against the rules but way easier to manage automatically
            for(let extra = 0; extra < extras.length; extra++)
            {
                if(extras[extra] == 'extra0')
                {
                    baseHarm += 1;
                }
                else if(extrax[extra] == 'extra1')
                {
                    baseTags.push('ignore-armour');
                }
                else if(extras[extra] == 'extra2')
                {
                    baseTags.push('close');
                }
            }
            attacks.push(new MonstrousAttack(baseName, baseHarm, baseTags));
        }
        return attacks;
    }
    playbookEmbed()
    {
        let embed = this.toEmbed();
        embed.setTitle(`**The Monstrous — ${this.alias}**`);
        embed.addFields({name: '**Curse**', value: this.curse});
        let attacks = '';
        for(let attack = 0; attack < this.attacks.length; attack++)
        {
            attacks += this.attacks[attack].toString()+'\n';
        }
        embed.addFields({name: '**Attacks**', value: attacks});
        return embed;
    }
}
class MonstrousAttack
{
    constructor(base='', harm=0, tags=[])
    {
        this.base = base;
        this.harm = harm;
        this.tags = tags;
    }
    toString()
    {
        return `Base: ${this.base} (${this.harm}-harm ${this.tags.join(' ')})`;
    }
}

class Mundane extends Character
{
    constructor(manifest, sheetFields, alias='')
    {
        super(manifest, sheetFields, alias);
        this.playbook = 'Mundane';
    }
    static Playbook()
    {
        return 'Mundane'
    }
    playbookEmbed()
    {
        let embed = this.toEmbed();
        embed.setTitle(`**The Mundane — ${this.alias}**`);
        return embed;
    }
}

class Professional extends Character
{
    constructor(manifest, sheetFields, alias='')
    {
        super(manifest, sheetFields, alias);
        let resourceFields = Object.keys(this.fields).filter(field => field.startsWith('resource'));
        let redTapeFields = Object.keys(this.fields).filter(field => field.startsWith('redtape'));
        this.resources = [];
        this.redtape = [];
        for(let resource = 0; resource < resourceFields.length; resource++)
        {
            this.resources.push(this.manifest[resourceFields[resource]]);
        }
        for(let redtape = 0; redtape < redTapeFields.length; redtape++)
        {
            this.redtape.push(this.manifest[redTapeFields[redtape]]);
        }
        this.moves.push(this.manifest['move7']);
        this.playbook = 'Professional';
    }
    static Playbook()
    {
        return 'Professional';
    }
    playbookEmbed()
    {
        let embed = this.toEmbed();
        embed.setTitle(`**The Professional — ${this.alias}**`);
        embed.addFields({name: '**Resources**', value: this.resources.join('\n'), inline: false});
        embed.addFields({name: '**Redtape**', value: this.redtape.join('\n'), inline: true});
        return embed;
    }
}

class SpellSlinger extends Character
{
    constructor(manifest, sheetFields, alias='')
    {
        super(manifest, sheetFields, alias);
        this.techniques = this.Techniques();
        this.combatMagic = this.CombatMagic();
        this.playbook = 'Spell-Slinger';
    }
    static Playbook()
    {
        return 'Spell-Slinger'
    }
    Techniques()
    {
        // Check the 3 that you do use, leave the one you don't need blank
        let techniqueFields = Object.keys(this.fields).filter(field => field.startsWith('technique'));
        let techniques = [];
        for(let technique = 0; technique < techniqueFields.length; technique++)
        {
            techniques.push(this.manifest[techniqueFields[technique]]);
        }
        return techniques;
    }
    CombatMagic()
    {
        let bases = Object.keys(this.fields).filter(field => field.startsWith('base'));
        let effects = Object.keys(this.fields).filter(field => field.startsWith('effect'));
        let spells = [];
        for(let base = 0; base < bases.length; base++)
        {
            let baseName = ''
            let baseHarm = 0
            let baseTags = []
            let spellEffects = []
            if(bases[base] == 'base0')
            {
                baseName = 'Blast';
                baseHarm = 2;
                baseTags = ['Magic', 'Close', 'Obvious', 'Loud'];
            }
            else if(bases[base] == 'base1')
            {
                baseName = 'Ball';
                baseHarm = 1;
                baseTags = ['Magic', 'Area', 'Close', 'Obvious', 'Loud'];
            }
            else if(bases[base] == 'base2')
            {
                baseName = 'Missile';
                baseHarm = 1;
                baseTags = ['Magic', 'Far', 'Obvious', 'Loud'];
            }
            else if(bases[base] == 'base3')
            {
                baseName = 'Wall';
                baseHarm = 1;
                baseTags = ['Magic', 'Barrier', 'Close', '1-Armour', 'Obvious', 'Loud'];
            }
            for(let effect = 0; effect < effects.length; effect++)
            {
                if(effects[effect] == 'effect0')
                {
                    spellEffects.push('Fire');
                    baseHarm += 2;
                    baseTags.push('Fire');
                    baseTags.push('[if you get a 10+ on a combat magic roll, the fire won\'t spread.]');
                }
                else if(effects[effect] == 'effect1')
                {
                    spellEffects.push('Force/Wind');
                    baseHarm += 1;
                    baseTags.push('Forceful');
                    if(baseName == 'Wall')
                    {
                        baseTags.push('+1 Armour');
                    }
                }
                else if(effects[effect] == 'effect2')
                {
                    spellEffects.push('Lightning/Entropy');
                    baseHarm += 1;
                    baseTags.push('messy');
                }
                else if(effects[effect] == 'effect3')
                {
                    spellEffects.push('Frost/Ice');
                    if(baseName == 'Wall')
                    {
                        baseHarm -= 1;
                        baseTags.push('+2 Armour');
                    }
                    else
                    {
                        baseHarm += 1;
                        baseTags.push('Restraining');
                    }
                }
                else if(effects[effect] == 'effect4')
                {
                    spellEffects.push('Earth');
                    baseTags.push('Forceful');
                    baseTags.push('Restraining');
                }
                else if(effects[effect] == 'effect5')
                {
                    spellEffects.push('Necromantic');
                    baseTags.push('Life-Drain');
                }
            }
            spells.push(new CombatSpell(baseName, spellEffects, baseHarm, baseTags));
        }
        return spells;
    }
    playbookEmbed()
    {
        let embed = this.toEmbed();
        embed.setTitle(`**The Spell-Slinger — ${this.alias}**`);
        let spells = [];
        for(let spell = 0; spell < this.combatMagic; spell++)
        {
            spells.push(this.combatMagic[spell].toString());
        }
        embed.addFields({name: '**Techniques**', value: this.techniques.join('\n'), inline: true});
        embed.addFields({name: '**Combat Magic**', value: spells.join('\n'), inline: true});
        return embed;
    }
}

class CombatSpell
{
    constructor(base='', effects=[], harm=0, tags=[])
    {
        this.base = base;
        this.harm = harm;
        this.tags = tags;
        this.effects = effects;
    }
    toString()
    {
        return `Base: ${this.base} (${this.effects.join(', ')}) (${this.harm}-harm ${this.tags.join(' ')})`;
    }
}

class Spooky extends Character
{
    constructor(manifest, sheetFields, alias='')
    {
        super(manifest, sheetFields, alias);
        let darksideFields = Object.keys(this.fields).filter(field => field.startsWith('darkside'));
        this.darkside = [];
        for(let field = 0; field < darksideFields.length; field++)
        {
            this.darkside.push(this.manifest[darksideFields[field]]);
        }
        this.playbook = 'Spooky';
    }
    static Playbook()
    {
        return 'Spooky';
    }
    playbookEmbed()
    {
        let embed = this.toEmbed();
        embed.setTitle(`**The Spooky — ${this.alias}**`);
        embed.addFields({name: '**Dark Side**', value: this.darkside.join('\n')});
        return embed;
    }
}

class Wronged extends Character
{
    constructor(manifest, sheetFields, alias='')
    {
        super(manifest, sheetFields, alias);
        this.lost = this.Loss();
        this.prey = this.fields['prey'];
        let guiltFields = Object.keys(this.fields).filter(field => field.startsWith('save'));
        this.guilt = [];
        for(let guilt = 0; guilt < guiltFields.length; guilt++)
        {
            this.guilt.push(this.manifest[guiltFields[guilt]]);
        }
        let weaponFields = Object.keys(this.fields).filter(field => field.startsWith('signature'));
        this.signatureWeapon = [];
        for(let weapon = 0; weapon < weaponFields.length; weapon++)
        {
            this.signatureWeapon.push(this.manifest[weaponFields[weapon]]);
        }
        this.playbook = 'Wronged';
    }
    static Playbook()
    {
        return 'Wronged';
    }
    Loss()
    {
        let lossFields = Object.keys(this.fields).filter(field => field.startsWith('lost') && !field.startsWith('lostText'));
        let lossTextFields = Object.keys(this.fields).filter(field => field.startsWith('lostText'));
        let yourLosses = [];
        if(lossFields.length == lossTextFields.length)
        {
            for(let loss = 0; loss < lossFields.length; loss++)
            {
                yourLosses.push(`${this.manifest[lossFields[loss]]}, ${this.fields[lossTextFields[loss]]}`);
            }
        }
        else
        {
            yourLosses = ['I think you filled this out wrong.'];
        }
        return yourLosses;
    }
    playbookEmbed()
    {
        let embed = this.toEmbed();
        embed.setTitle(`**The Wronged — ${this.alias}**`);
        embed.addFields({name: '**Signature Weapon**', value: this.signatureWeapon.join('\n')});
        embed.addFields({name: '**Guilt**', value: this.guilt.join('\n')});
        return embed;
    }
}

class Searcher extends Character
{
    constructor(manifest, sheetFields, alias='')
    {
        super(manifest, sheetFields, alias);
        let encounterFields = Object.keys(this.fields).filter(field => field.startsWith('firstencounter'));
        this.firstEncounter = [this.manifest['firstEncounter0']];
        for(let field = 0; field < encounterFields.length; field++)
        {
            this.firstEncounter.push(this.manifest[encounterFields[field]]);
        }
        this.playbook = 'Searcher';
    }
    static Playbook()
    {
        return 'Searcher'
    }
    playbookEmbed()
    {
        let embed = this.toEmbed();
        embed.setTitle(`**The Searcher — ${this.alias}**`);
        embed.addFields({name: '**First Encounter**', value: this.firstEncounter[1]});
        return embed;
    }
}

/*
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

class SearcherMessage(CharacterMessage):
    def __init__(self, character, user):
        CharacterMessage.__init__(self, character, user)
        self.embed.title = "THE SEARCHER - {}".format(self.character['name'])
        self.firstEncounter = self.character.firstEncounter
    async def PlaybookFields(self):
        self.embed.clear_fields()
        description = self.firstEncounter[0]
        name, value = self.firstEncounter[1].split('\n', maxsplit=1)
        self.embed.add_field(name=name, value=value, inline=False)
        self.embed.description = description
        await self.message.edit(embed=self.embed)
        await self.SetReactions()

*/
function LoadAllCharacters(playerCharacters=[], activeGame='Demo Characters')
{
    let playbookClasses =  [Chosen, Crooked, Divine, Expert, Flake, Initiate, Monstrous, Mundane, Professional, SpellSlinger, Spooky, Wronged];
    let characters = {};
    for(let playbook = 0; playbook < playbookClasses.length; playbook++)
    {
        [data, fields] = LoadCharacter(playbookClasses[playbook].Playbook());
        let character = playbook(data, fields, alias=playbook.Playbook());
        characters[playbook.Playbook()] = character;
    }
    for(let playerCharacter = 0; playerCharacter < playerCharacters.length; playerCharacter++)
    {
        [data, fields] = LoadCharacter(playbook=playerCharacters[playerCharacter][1].Playbook(), sheetPath=`./Character Stuff/${activeGame}`, name=playerCharacters[playerCharacter][0]);
        let character = playerCharacters[playerCharacter][1](data, fields, alias=playerCharacters[playerCharacter][0]);
        characters[playerCharacters[playerCharacter][0]] = character;
    }
    return characters;
}

function LoadAllCharactersFromJSON(playerCharacters=[], activeGame='Demo Characters')
{
    let playbookClasses = [Chosen, Crooked, Divine, Expert, Flake, Initiate, Monstrous, Mundane, Professional, SpellSlinger, Spooky, Wronged, Searcher];
    let characters = {};
    for(let playbook = 0; playbook < playbookClasses.length; playbook++)
    {
        if(fs.existsSync(`./Character Stuff/${activeGame}/${playbookClasses[playbook].Playbook()}.json`))
        {
            let manifestFile = fs.readFileSync(`./Character Stuff/Field Data/${playbookClasses[playbook].Playbook()} Fields.json`);
            let manifest = JSON.parse(manifestFile);
            let fieldsFile = fs.readFileSync(`./Character Stuff/${activeGame}/${playbookClasses[playbook].Playbook()}.json`);
            let fields = JSON.parse(fieldsFile);
            characters[playbookClasses[playbook].Playbook()] = playbookClasses[playbook](manifest, fields, alias=playbookClasses[playbook].Playbook());
        }
    }
    for(let playerCharacter = 0; playerCharacter < playerCharacters.length; playerCharacter++)
    {
        console.log(playerCharacters[playerCharacter][0]);
        if(fs.existsSync(`./Character Stuff/${activeGame}/${playerCharacters[playerCharacter][0]}.json`))
        {
            let playbook = playerCharacters[playerCharacter][1];
            let name = playerCharacters[playerCharacter][0];
            console.log(name);
            let manifestFile = fs.readFileSync(`./Character Stuff/Field Data/${playbook.Playbook()} Fields.json`);
            let manifest = JSON.parse(manifestFile);
            let fieldsFile = fs.readFileSync(`./Character Stuff/${activeGame}/${name}.json`);
            let fields = JSON.parse(fieldsFile);
            characters[name] = new playbook(manifest, fields, alias=name);
        }
    }
    return characters;
}


async function DumpPDFToJSON(directory = 'Demo Characters', name='Chosen', playbook=Chosen)
{
    let path = `./Character Stuff/${directory}/`;
    [data, fields] = await LoadCharacter(playbook.Playbook(), sheetPath=path, name=name);
    let character = new playbook(data, fields);
    character.Save();
    return character;
}


async function LoadCharacter(playbook='Chosen', sheetPath='./Character Stuff/Demo Characters/', name=null)
{
    let fieldPath = './Character stuff/Field Data/';
    if(name == null)
    {
        name = `The_${playbook}`;
    }
    let pdfFileObj = fs.readFileSync(`${sheetPath}${name}.pdf`);
    const pdfDoc = await PDFDocument.load(pdfFileObj);
    const form = pdfDoc.getForm();
    const fields = form.getFields();
    let blankBoxes = [];
    let returnFields = {'fields': {}};

    for(let field = 0; field < fields.length; field++)
    {
        if(fields[field].constructor.name == 'PDFCheckBox' && !fields[field].isChecked())
        {
            blankBoxes.push(fields[field].getName());
        }
    }
    for(let field = 0; field < fields.length; field++)
    {
        if(!blankBoxes.includes(fields[field].getName()))
        {
            if(fields[field].constructor.name == 'PDFCheckBox')
            {
                returnFields['fields'][fields[field].getName()] = fields[field].getName();   
            }
            else if(fields[field].constructor.name == 'PDFTextField')
            {
                returnFields['fields'][fields[field].getName()] = fields[field].getText();
            }
        }
    }
    let fieldData = fs.readFileSync(`${fieldPath}${playbook} Fields.json`);
    let data = JSON.parse(fieldData);
    return [data, returnFields];
}

function PlaybookByName(name='Chosen')
{
    let playbooks = [Chosen, Crooked, Divine, Expert, Flake, Initiate, Monstrous, Mundane, Professional, SpellSlinger, Spooky, Wronged, Searcher];
    for(let playbook = 0; playbook < playbooks.length; playbook++)
    {
        if(playbooks[playbook].Playbook() == name)
        {
            return playbooks[playbook];
        }
    }
}


module.exports = {Chosen, Crooked, Divine, Expert, Flake, Initiate, Monstrous, Mundane, Professional, SpellSlinger, Spooky, Wronged, Searcher, LoadCharacter, LoadAllCharactersFromJSON, PlaybookByName,DumpPDFToJSON};