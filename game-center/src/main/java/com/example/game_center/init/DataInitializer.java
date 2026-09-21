package com.example.game_center.init;

import com.example.game_center.entity.MarketItem;
import com.example.game_center.repository.MarketItemRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

import java.util.Random;

@Component
@RequiredArgsConstructor
public class DataInitializer implements CommandLineRunner {

    private final MarketItemRepository marketItemRepository;

    @Override
    public void run(String... args) throws Exception {
        if (marketItemRepository.count() == 0) {
            String[] botNames = {"Bot_Alex", "Bot_Zelda", "Bot_Mario", "Bot_Link"};
            String[] itemNames = {"Excalibur", "HP Potion", "Dragon Shield", "Magic Wand", "Iron Sword"};
            Random random = new Random();

            for (int i = 0; i < 20; i++) {
                String seller = botNames[random.nextInt(botNames.length)];
                String item = itemNames[random.nextInt(itemNames.length)];
                int price = (random.nextInt(10) + 1) * 1000;
                
                marketItemRepository.save(new MarketItem(item, seller, price, false));
            }
        }
    }
}
