const {SlashCommandBuilder} = require('@discordjs/builders');
const { ActionRowBuilder, ButtonBuilder, SelectMenuComponent, EmbedBuilder, ButtonStyle, resolveColor } = require('discord.js');
const fs = require('fs');
const Character = require('../characters.js');


module.exports = 
{
	data: new SlashCommandBuilder()
	.setName('inventory')
	.setDescription('Check a character\'s inventory!')
	.addStringOption(option =>
		option.setName('name')
		.setRequired(true)
		.setDescription('Name of character to mark xp on')),
	rows: [],
	char: null,
	async execute(interaction, characters)
	{
		this.rows = [];
		let name = interaction.options.getString('name');
		this.char = null;
		for(character in Object.keys(characters))
		{
			if(Object.keys(characters)[character] === name)
			{
				this.char = characters[Object.keys(characters)[character]];
			}
		}
		if(this.char === null)
		{
			await interaction.reply(`I couldn't find character ${name}`);
		}
		else
		{
			let inventory = this.char.Inventory();
			let description = '';
			if(Object.keys(inventory).length == 0)
			{
				description = ' ';
			}
			else
			{
				description = Object.keys(inventory).join('\n');
			}
			let embed = new EmbedBuilder().setTitle(`${name}'s Inventory`).setDescription(description);
			for(let item = 0; item < Object.keys(inventory).length; item++)
			{
				if(item%5 == 0)
				{
					this.rows.push(new ActionRowBuilder());
				}
				this.rows[this.rows.length-1].addComponents(new ButtonBuilder().setCustomId(`inventoryShow${Object.keys(inventory)[item]}`).setLabel(`${Object.keys(inventory)[item]}`).setStyle(ButtonStyle.Primary));
			}
			await interaction.reply({embeds: [embed], components: this.rows});
		}
	},
	async ShowItem(interaction, item)
	{
		this.rows = [];
		let inventory = this.char.Inventory();
		let embed = new EmbedBuilder().setTitle('Not found').setDescription(`I couldn't find item ${item}`);
		if(Object.keys(inventory).includes(item))
		{
			embed = new EmbedBuilder().setTitle(`${this.char.alias}'s ${item}`).setDescription(inventory[item]);
		}
		let row0 = new ActionRowBuilder();
		row0.addComponents(new ButtonBuilder().setCustomId('inventoryGoBack').setLabel('Back').setStyle(ButtonStyle.Primary));
		row0.addComponents(new ButtonBuilder().setCustomId(`inventoryDelete${item}`).setLabel('Delete').setStyle(ButtonStyle.Danger));
		this.rows.push(row0);
		await interaction.update({embeds: [embed], components: this.rows});

	},
	async ShowInventory(interaction)
	{
		this.rows = [];
		let inventory = this.char.Inventory();
		let description = '';
		if(Object.keys(inventory).length == 0)
		{
			description = ' ';
		}
		else
		{
			description = Object.keys(inventory).join('\n');
		}
		let embed = new EmbedBuilder().setTitle(`${this.char.alias}'s Inventory`).setDescription(description);
		for(let item = 0; item < Object.keys(inventory).length; item++)
		{
			if(item%5 == 0)
			{
				this.rows.push(new ActionRowBuilder());
			}
			this.rows[this.rows.length-1].addComponents(new ButtonBuilder().setCustomId(`inventoryShow${Object.keys(inventory)[item]}`).setLabel(`${Object.keys(inventory)[item]}`).setStyle(ButtonStyle.Primary));
		}
		await interaction.update({embeds: [embed], components: this.rows});
	},
	async DeleteItem(interaction, item)
	{
		let inventory = this.char.Inventory();
		delete inventory[item];
		fs.writeFileSync(`./Character Stuff/Inventories/${this.char.alias}.json`, JSON.stringify(inventory, null, 2));
		await this.ShowInventory(interaction);
	}
}