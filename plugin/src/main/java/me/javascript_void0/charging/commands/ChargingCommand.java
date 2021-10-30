package me.javascript_void0.charging.commands;

import org.bukkit.command.Command;
import org.bukkit.command.CommandExecutor;
import org.bukkit.command.CommandSender;
import org.bukkit.entity.Player;

import me.javascript_void0.charging.Main;
import me.javascript_void0.charging.files.Data;

public class ChargingCommand implements CommandExecutor {
    
    private Main plugin;

    public ChargingCommand(Main plugin) {
        this.plugin = plugin;
        plugin.getCommand("charging").setExecutor(this);
    }

    @Override
    public boolean onCommand(CommandSender sender, Command cmd, String label, String[] args) {
        Player player = (Player) sender;
        if (cmd.getName().equalsIgnoreCase("charging")) {
            if (args.length == 0) {
                sender.sendMessage("Usage: /charging");
            } else if (args[0].equalsIgnoreCase("reload")) {
                Data.reload();
                player.sendMessage("Config has been reloaded");
            }
        }
        return true;
    }
}