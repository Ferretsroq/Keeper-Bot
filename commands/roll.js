const {SlashCommandBuilder} = require('@discordjs/builders');
const {ActionRowBuilder, ButtonBuilder, ButtonStyle, EmbedBuilder} = require('discord.js');
const Character = require('../characters.js');

module.exports = 
{
	data: new SlashCommandBuilder()
	.setName('roll')
	.setDescription('Roll 2d6+stat!')
	.addStringOption(option =>
		option.setName('description')
		.setRequired(true)
		.setDescription('Description of your roll'))
	.addIntegerOption(option =>
		option.setName('bonus')
		.setRequired(false)
		.setDescription('Bonus to add to your roll')),
	character: null,
	bonus: 0,
	description: '',
	async execute(interaction, characters, players)
	{
		this.bonus = interaction.options.getInteger('bonus');
		this.description = interaction.options.getString('description');
		if(this.bonus === null)
		{
			this.bonus = 0;
		}
		let name = players[interaction.user.id.toString()];
		for(character in Object.keys(characters))
		{
			if(Object.keys(characters)[character] === name)
			{
				this.character = characters[Object.keys(characters)[character]];
			}
		}
		const buttonRow0 = new ActionRowBuilder();
		for(let stat of ['Charm', 'Cool', 'Sharp', 'Tough', 'Weird'])
		{
			buttonRow0.addComponents(new ButtonBuilder().setCustomId(`roll${stat}`).setLabel(`${stat}: +${this.character.fields[stat.toLowerCase()]}`).setStyle(ButtonStyle.Primary));
		}
		await interaction.reply({content: 'Choose a stat to roll with!', components: [buttonRow0]});
	},
	async Roll(interaction, stat)
	{
		let die1 = Math.floor(Math.random()*6)+1;
		let die2 = Math.floor(Math.random()*6)+1;
		let statBonus = parseInt(this.character[stat.toLowerCase()]);
		let total = die1+die2+statBonus+this.bonus;
		let result = '';
		if(total >= 10)
		{
			result = 'Full Success';
		}
		else if(total < 7)
		{
			result = 'Failure';
		}
		else
		{
			result = 'Mixed Success'
		}
		let embed = new EmbedBuilder().setTitle(`Roll for ${this.character.alias} — ${this.description}`).setDescription(`You rolled **${total}**\n**${result}**\n((${die1}+${die2}) + ${statBonus} for stat ${stat} + ${this.bonus} for ongoing/forward)`);
		await interaction.update({embeds: [embed], components: []});
		//await interaction.update({content: `**${result}**\n${die1}+${die2}+${statBonus}+${this.bonus} = ${total}\nRolled with ${stat}`, components: []})
	},
};
