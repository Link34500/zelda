import constant
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

