package me.javascript_void0.charging.commands;

import me.javascript_void0.charging.Main;
import me.javascript_void0.charging.items.Wand;
import org.bukkit.command.Command;
import org.bukkit.command.CommandExecutor;
import org.bukkit.command.CommandSender;
import org.bukkit.entity.Player;

public class WandCommand implements CommandExecutor {
    
    private Main plugin;

    public WandCommand(Main plugin) {
        this.plugin = plugin;
        plugin.getCommand("givetest").setExecutor(this);
    }

    @Override
    public boolean onCommand(CommandSender sender, Command cmd, String label, String[] args) {
        if (!(sender instanceof Player)) {
            sender.sendMessage("no");
            return true;
        }
        Player player = (Player) sender;
        if (cmd.getName().equalsIgnoreCase("givetest")) {
            player.getInventory().addItem(Wand.wand);
        }
        return true;
    }

}
