package me.javascript_void0.charging;

import me.javascript_void0.charging.commands.WandCommand;
import me.javascript_void0.charging.items.Wand;
import me.javascript_void0.charging.events.WandEvent;
import org.bukkit.plugin.java.JavaPlugin;

public class Main extends JavaPlugin {

    @Override
    public void onEnable() {
        Wand.init();
        getServer().getPluginManager().registerEvents(new WandEvent(), this);
        new WandCommand(this);
    }

    @Override
    public void onDisable() {

    }

}