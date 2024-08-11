from endstone.event import event_handler, EventPriority, PlayerJoinEvent, PlayerQuitEvent, ServerListPingEvent
from endstone.plugin import Plugin


class Listener:
    def __init__(self, plugin: Plugin):
        self._plugin = plugin

    @event_handler
    def on_player_join(self, event: PlayerJoinEvent):
        player = event.player
        player.add_attachment(self._plugin, "minecraft.command.me", False)
        player.update_commands()
