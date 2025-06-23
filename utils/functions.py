import constant
import json
import discord
import logging

def get_channeldata():
    """Récupérer le channel de donnée du BOT

    Returns:
        channel (discord.TextChannel): Le channel de donnée du bot
    """
    if not constant.CHANNEL_DATA is None:
        return constant.CHANNEL_DATA
    # Chargemment du serveur de donnés
    logging.info("Recherche du serveur de donnés")
    for guild in constant.BOT.guilds:
        if guild.id == 1352303484183249061:
            logging.info("Serveur de donnés trouvé")
            for channel in guild.channels:
                if channel.name == str(constant.BOT.user.id):
                    logging.info("Connexion avec le serveur de données du bot établi avec succès")
                    constant.CHANNEL_DATA = channel
                    return channel
            logging.critical(f"Nous ne sommes pas parvenu à établir une connexion avec le serveur de donnés du bot avec ID {constant.BOT.user.id}")
            return None
    logging.critical(f"Nous ne sommes pas parvenu à établir une connexion avec le serveur de donnés")
    return None

def get_discord_placeholders(interaction:discord.Interaction):
    return {
        # Le dictionnaire suivant à l'aide de Gemini
        # --- Informations sur le Serveur (Guild) ---
        "[SERVER_NAME]": interaction.guild.name if interaction.guild else "N/A",
        "[SERVER_ID]": interaction.guild.id if interaction.guild else "N/A",
        "[SERVER_MEMBER_COUNT]": interaction.guild.member_count if interaction.guild else "N/A",
        "[SERVER_OWNER_NAME]": interaction.guild.owner.display_name if interaction.guild and interaction.guild.owner else "N/A",
        "[SERVER_OWNER_ID]": interaction.guild.owner_id if interaction.guild else "N/A",
        "[SERVER_CREATED_AT]": interaction.guild.created_at.strftime("%Y-%m-%d %H:%M:%S") if interaction.guild else "N/A",
        "[SERVER_VERIFICATION_LEVEL]": str(interaction.guild.verification_level) if interaction.guild else "N/A",
        "[SERVER_FEATURES]": ", ".join(interaction.guild.features) if interaction.guild else "N/A",
        "[SERVER_ICON_URL]": interaction.guild.icon.url if interaction.guild and interaction.guild.icon else "N/A",

        # --- Informations sur l'Utilisateur (User/Member) qui a déclenché l'interaction ---
        "[USER_NAME]": interaction.user.display_name, # Nom d'affichage ou nom global
        "[USER_GLOBAL_NAME]": interaction.user.global_name if interaction.user.global_name else interaction.user.name, # Nom global (depuis le passage aux noms d'utilisateur)
        "[USER_USERNAME]": interaction.user.name, # L'ancien "discriminatorless" username
        "[USER_ID]": interaction.user.id,
        "[USER_MENTION]": interaction.user.mention, # Mentionne l'utilisateur (<@ID>)
        "[USER_AVATAR_URL]": interaction.user.avatar.url if interaction.user.avatar else "N/A",
        "[USER_CREATED_AT]": interaction.user.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        "[USER_IS_BOT]": "Oui" if interaction.user.bot else "Non",
        "[MEMBER_JOINED_AT]": interaction.user.joined_at.strftime("%Y-%m-%d %H:%M:%S") if interaction.guild and hasattr(interaction.user, 'joined_at') and interaction.user.joined_at else "N/A", # Date d'arrivée sur le serveur
        "[MEMBER_NICKNAME]": interaction.user.nick if interaction.guild and hasattr(interaction.user, 'nick') and interaction.user.nick else "N/A", # Surnom sur le serveur
        "[MEMBER_TOP_ROLE]": interaction.user.top_role.name if interaction.guild and hasattr(interaction.user, 'top_role') and interaction.user.top_role else "N/A", # Nom du rôle le plus élevé

        # --- Informations sur le Salon (Channel) ---
        "[CHANNEL_NAME]": interaction.channel.name if interaction.channel else "N/A",
        "[CHANNEL_ID]": interaction.channel.id if interaction.channel else "N/A",
        "[CHANNEL_TYPE]": str(interaction.channel.type) if interaction.channel else "N/A", # Ex: 'text', 'voice', 'category', 'private'
        "[CHANNEL_MENTION]": interaction.channel.mention if interaction.channel and hasattr(interaction.channel, 'mention') else "N/A",
        "[CHANNEL_TOPIC]": interaction.channel.topic if interaction.channel and hasattr(interaction.channel, 'topic') and interaction.channel.topic else "N/A",

        # --- Informations sur l'Interaction elle-même ---
        "[INTERACTION_TYPE]": str(interaction.type), # Ex: 'ApplicationCommand', 'MessageComponent', 'ModalSubmit'
        "[INTERACTION_ID]": interaction.id,
        "[INTERACTION_CREATED_AT]": interaction.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        "[INTERACTION_COMMAND_NAME]": interaction.command.name if interaction.command else "N/A", # Nom de la commande slash ou du composant

        # --- Informations supplémentaires (selon le type d'interaction) ---
        # Pour les interactions de MessageComponent (boutons, select menus) :
        "[COMPONENT_CUSTOM_ID]": interaction.data['custom_id'] if interaction.data and 'custom_id' in interaction.data else "N/A",
        "[COMPONENT_VALUE]": ", ".join(interaction.data['values']) if interaction.data and 'values' in interaction.data else "N/A", # Pour les select menus

        # Pour les interactions de ModalSubmit :
        # Si tu as des champs de texte dans ton modal, tu peux y accéder ici
        # Exemple pour un champ avec custom_id="my_text_input"
        # "[MODAL_INPUT_MY_TEXT_INPUT]": interaction.data['components'][0]['components'][0]['value'] if interaction.type == discord.InteractionType.modal_submit else "N/A",
        # (Note: l'accès aux valeurs des modaux est un peu plus complexe et dépend de la structure de ton modal)
    }

def get_placeholders():
    with open("servers/messages.json",'r') as f:
        categories:dict = json.load(f)['categories']
    placeholders = {}
    for key,value in categories.items():
        placeholders.update({"["+key.upper()+"]":value})

    return placeholders