const {SlashCommandBuilder} = require('@discordjs/builders');
const { ActionRowBuilder, ButtonBuilder, SelectMenuComponent, EmbedBuilder, ButtonStyle, resolveColor } = require('discord.js');
const fs = require('fs');


module.exports = 
{
	data: new SlashCommandBuilder()
	.setName('moves')
	.setDescription('Show all moves!'),
	moves: [],
	index: 0,
	rows: [],
	async execute(interaction)
	{
		this.rows = [];
		this.moves = fs.readdirSync('./Moves').filter(file => file.endsWith('move')).map(function(x){return x.replace('.move', '')});
		this.index = 0;

		let buttonRow0 = new ActionRowBuilder();
		buttonRow0.addComponents(new ButtonBuilder().setCustomId(`movesLeft`).setLabel(`\u2190`).setStyle(ButtonStyle.Primary));
		buttonRow0.addComponents(new ButtonBuilder().setCustomId(`movesRight`).setLabel(`\u2192`).setStyle(ButtonStyle.Primary));
		buttonRow0.addComponents(new ButtonBuilder().setCustomId(`movesList`).setLabel('List').setStyle(ButtonStyle.Primary));
		buttonRow0.addComponents(new ButtonBuilder().setCustomId(`movesExpand`).setLabel('Expand').setStyle(ButtonStyle.Primary));

		this.rows.push(buttonRow0);

		let embed = this.FormatMove(this.moves[this.index]);
		await interaction.reply({embeds: [embed], components: this.rows});
	},
	FormatMove(moveName)
	{
		const color = resolveColor('0xababab');
		let move = fs.readFileSync(`./Moves/${moveName}.move`, 'utf8');
		const embed = new EmbedBuilder().setColor(color).setDescription(move).setTitle(moveName);
		return embed;
	},
	async MoveLeft(interaction)
	{
		this.index -= 1;
		if(this.index < 0)
		{
			this.index = this.moves.length-1;
		}
		await interaction.update({embeds: [this.FormatMove(this.moves[this.index])], components: this.rows});
	},
	async MoveRight(interaction)
	{
		this.index += 1;
		if(this.index >= this.moves.length)
		{
			this.index = 0;
		}
		await interaction.update({embeds: [this.FormatMove(this.moves[this.index])], components: this.rows});
	},
	async ListMoves(interaction)
	{
		const color = resolveColor('0xababab');
		let description = this.moves.join('\n');
		this.rows = [];
		let buttonRow0 = new ActionRowBuilder();
		let buttonRow1 = new ActionRowBuilder();
		for(let index = 0; index < 5; index++)
		{
			buttonRow0.addComponents(new ButtonBuilder().setCustomId(`movesGoTo${index}`).setLabel(this.moves[index]).setStyle(ButtonStyle.Primary));
		}
		for(let index = 5; index < 8; index++)
		{
			buttonRow1.addComponents(new ButtonBuilder().setCustomId(`movesGoTo${index}`).setLabel(this.moves[index]).setStyle(ButtonStyle.Primary));
		}
		this.rows.push(buttonRow0);
		this.rows.push(buttonRow1);
		let embed = new EmbedBuilder().setTitle('List of Moves').setDescription(description);
		await interaction.update({embeds: [embed], components: this.rows});
	},
	async GoToMove(interaction, moveIndex)
	{
		this.index = parseInt(moveIndex);
		this.rows = [];
		let buttonRow0 = new ActionRowBuilder();
		buttonRow0.addComponents(new ButtonBuilder().setCustomId(`movesLeft`).setLabel(`\u2190`).setStyle(ButtonStyle.Primary));
		buttonRow0.addComponents(new ButtonBuilder().setCustomId(`movesRight`).setLabel(`\u2192`).setStyle(ButtonStyle.Primary));
		buttonRow0.addComponents(new ButtonBuilder().setCustomId(`movesList`).setLabel('List').setStyle(ButtonStyle.Primary));
		buttonRow0.addComponents(new ButtonBuilder().setCustomId(`movesExpand`).setLabel('Expand').setStyle(ButtonStyle.Primary));


		this.rows.push(buttonRow0);
		let embed = this.FormatMove(this.moves[this.index]);
		await interaction.reply({embeds: [embed], components: this.rows});
	},
	async ExpandMove(interaction)
	{
		const color = resolveColor('0xababab');
		let description = fs.readFileSync(`./Moves/${this.moves[this.index]}.details`, 'utf8');
		let embeds = [];
		let index = 0;
		for(let embedNum = 0; embedNum < description.length/4000; embedNum++)
		{
			embeds.push(new EmbedBuilder().setColor(color).setDescription(description.substr(embedNum*4000, (embedNum+1)*4000)).setTitle(this.moves[this.index]));
		}
		//const embed = new EmbedBuilder().setColor(color).setDescription(description).setTitle(this.moves[this.index]);
		await interaction.update({embeds: embeds, components: this.rows});
	}
}