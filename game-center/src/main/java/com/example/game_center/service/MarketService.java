package com.example.game_center.service;

import com.example.game_center.entity.MarketItem;
import com.example.game_center.feign.WalletFeignClient;
import com.example.game_center.repository.MarketItemRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.scheduling.annotation.Scheduled;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;

@Service
@RequiredArgsConstructor
public class MarketService {

    private final MarketItemRepository marketItemRepository;
    private final WalletFeignClient walletFeignClient;

    @Transactional
    @Scheduled(fixedRate = 10000)
    public void simulateBotPurchases() {
        List<MarketItem> userItems = marketItemRepository.findBySellerNameAndIsSoldFalse("User");
        Random random = new Random();
        
        if (!userItems.isEmpty()) {
            for (MarketItem item : userItems) {
                if (random.nextInt(100) < 30) {
                    String botBuyer = "Bot_" + (random.nextInt(100)); // Should ideally be existing bot but this is just simulation
                    
                    try {
                        // In reality, bot needs to have money, but for simulation we just transfer from bot to user
                        Map<String, Object> payload = new HashMap<>();
                        payload.put("fromId", "Bot_Alex"); // Hardcode a wealthy bot for simulation
                        payload.put("toId", "User");
                        payload.put("amount", item.getPrice());
                        
                        Map<String, String> response = walletFeignClient.transferMoney(payload);
                        if ("SUCCESS".equals(response.get("status"))) {
                            item.setSold(true);
                            item.setSellerName(botBuyer);
                            marketItemRepository.save(item);
                        }
                    } catch (Exception e) {
                        // Ignore if bot doesn't have money
                    }
                }
            }
        }
        
        long currentMarketSize = marketItemRepository.countByIsSoldFalse();
        if (currentMarketSize < 20) {
            String[] botNames = {"Bot_Alex", "Bot_Zelda", "Bot_Mario", "Bot_Link"};
            String[] itemNames = {"Excalibur", "HP Potion", "Dragon Shield", "Magic Wand", "Iron Sword"};
            int itemsToGenerate = 20 - (int) currentMarketSize;
            
            for (int i = 0; i < itemsToGenerate; i++) {
                String seller = botNames[random.nextInt(botNames.length)];
                String item = itemNames[random.nextInt(itemNames.length)];
                int price = (random.nextInt(10) + 1) * 1000;
                marketItemRepository.save(new MarketItem(item, seller, price, false));
            }
        }
    }

    @Transactional(readOnly = true)
    public List<MarketItem> getMarketItems() {
        return marketItemRepository.findByIsSoldFalse();
    }

    @Transactional(readOnly = true)
    public List<MarketItem> getMyInventory(String memberId) {
        return marketItemRepository.findBySellerNameAndIsSoldTrue(memberId);
    }
    
    public Map<String, Object> getMemberInfo(String memberId) {
        try {
            return walletFeignClient.getWallet(memberId);
        } catch (Exception e) {
            return null;
        }
    }

    @Transactional
    public void buyItem(String memberId, Long itemId) {
        MarketItem item = marketItemRepository.findById(itemId)
                .orElseThrow(() -> new IllegalArgumentException("Item not found"));
        
        if (item.isSold()) {
            throw new IllegalArgumentException("Item already sold");
        }
        
        // Use Feign to transfer money from User to the item's Seller
        Map<String, Object> payload = new HashMap<>();
        payload.put("fromId", memberId);
        payload.put("toId", item.getSellerName());
        payload.put("amount", item.getPrice());
        
        Map<String, String> response = walletFeignClient.transferMoney(payload);
        if (!"SUCCESS".equals(response.get("status"))) {
            throw new IllegalArgumentException(response.get("message") != null ? response.get("message") : "Transfer failed");
        }

        item.setSold(true);
        item.setSellerName(memberId);
        marketItemRepository.save(item);
    }

    @Transactional
    public void sellItem(String memberId, Long itemId, int price) {
        MarketItem item = marketItemRepository.findById(itemId)
                .orElseThrow(() -> new IllegalArgumentException("Item not found"));
        
        if (!item.getSellerName().equals(memberId) || !item.isSold()) {
            throw new IllegalArgumentException("Invalid item");
        }
        
        item.setSold(false);
        item.setPrice(price);
        marketItemRepository.save(item);
    }
}
