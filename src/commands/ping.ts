import { SlashCommandBuilder } from "discord.js";
import { client, Command } from "@/index";
import { translate } from "@/translations/translate";

const ping: Command = {
  data: new SlashCommandBuilder()
    .setName("ping")
    .setDescription("Une commande ping !"),
  execute: async (interaction) => {
    const ping = client.ws.ping;
    await interaction.reply({
      embeds: [
        {
          title: "Pong !",
          description: await translate(
            interaction,
            "commands.ping.embed.description",
            { ping }
          ),
        },
      ],
    });
  },
};

export default ping;
