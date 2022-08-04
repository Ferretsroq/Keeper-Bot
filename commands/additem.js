const {SlashCommandBuilder} = require('@discordjs/builders');
const {ActionRowBuilder, SelectMenuBuilder, ButtonBuilder, ButtonStyle, SelectMenuOptionBuilder, EmbedBuilder} = require('discord.js');
fs = require('fs');
Character = require('../characters.js');


module.exports = 
{
	data: new SlashCommandBuilder()
	.setName('additem')
	.setDescription('Add an item to your character!')
	.addStringOption(option =>
		option.setName('itemname')
		.setRequired(true)
		.setDescription('Name of item to add'))
	.addStringOption(option =>
		option.setName('itemdescription')
		.setRequired(true)
		.setDescription('Description of item to add'))
	.addStringOption(option =>
		option.setName('charname')
		.setRequired(false)
		.setDescription('Name of character to add item to')),
	async execute(interaction, characters, players)
	{
		let name = interaction.options.getString('charname');
		let item = interaction.options.getString('itemname');
		let description = interaction.options.getString('itemdescription');
		let char = null;
		if(name === null)
		{
			name = players[interaction.user.id.toString()];
		}
		for(character in Object.keys(characters))
		{
			if(Object.keys(characters)[character] === name)
			{
				char = characters[Object.keys(characters)[character]];
			}
		}
		if(char != null)
		{
			let inventory = {}
			if(fs.existsSync(`./Character Stuff/Inventories/${char.alias}.json`))
	        {
	            let inventoryFile = fs.readFileSync(`./Character Stuff/Inventories/${char.alias}.json`);
	            inventory = JSON.parse(inventoryFile);
	        }
	        inventory[item] = description;
            fs.writeFileSync(`./Character Stuff/Inventories/${char.alias}.json`, JSON.stringify(inventory, null, 2));
            await interaction.reply(`Added item ${item} to ${name}`);
		}
		else
		{
			await interaction.reply(`Could not find character ${name}\nCharacters: ${Object.keys(characters).join('\n')}`);
		}
	},
	
}