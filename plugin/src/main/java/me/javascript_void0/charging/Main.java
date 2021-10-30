package me.javascript_void0.charging;

import org.bukkit.plugin.java.JavaPlugin;

import me.javascript_void0.charging.commands.ChargingCommand;
import me.javascript_void0.charging.commands.WandCommand;
import me.javascript_void0.charging.events.WandEvent;
import me.javascript_void0.charging.files.Data;
import me.javascript_void0.charging.items.Wand;

public class Main extends JavaPlugin {

    @Override
    public void onEnable() {
        Wand.init();
        getServer().getPluginManager().registerEvents(new WandEvent(), this);
        new WandCommand(this);
        new ChargingCommand(this);
        
        Data.setup();
        Data.get().options().copyDefaults(true);
        Data.save();
    }
}