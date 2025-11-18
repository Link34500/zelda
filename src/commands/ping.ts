import { SlashCommandBuilder } from "discord.js";
import { client, Command } from "@/index";

const ping: Command = {
  data: new SlashCommandBuilder()
    .setName("ping")
    .setDescription("Une commande ping !"),
  execute: async (interaction) => {
    await interaction.reply({ embeds: [{ title: "Pong !" }] });
  },
};

export default ping;
