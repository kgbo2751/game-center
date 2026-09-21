package com.example.game_center.controller;

import com.example.game_center.entity.MarketItem;
import com.example.game_center.service.MarketService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/market")
@RequiredArgsConstructor
public class MarketController {

    private final MarketService marketService;

    @GetMapping
    public Map<String, Object> getMarketData() {
        Map<String, Object> response = new HashMap<>();
        Map<String, Object> user = marketService.getMemberInfo("User");
        List<MarketItem> items = marketService.getMarketItems();
        
        response.put("balance", user != null && user.get("balance") != null ? user.get("balance") : 0);
        response.put("items", items);
        return response;
    }

    @GetMapping("/inventory")
    public List<MarketItem> getMyInventory() {
        return marketService.getMyInventory("User");
    }

    @PostMapping("/buy/{itemId}")
    public Map<String, String> buyItem(@PathVariable Long itemId) {
        Map<String, String> response = new HashMap<>();
        try {
            marketService.buyItem("User", itemId);
            response.put("status", "SUCCESS");
        } catch (Exception e) {
            response.put("status", "FAIL");
            response.put("message", e.getMessage());
        }
        return response;
    }

    @PostMapping("/sell/{itemId}")
    public Map<String, String> sellItem(@PathVariable Long itemId, @RequestBody Map<String, String> payload) {
        int price = Integer.parseInt(payload.get("price"));
        
        marketService.sellItem("User", itemId, price);
        
        Map<String, String> response = new HashMap<>();
        response.put("status", "SUCCESS");
        return response;
    }
}
