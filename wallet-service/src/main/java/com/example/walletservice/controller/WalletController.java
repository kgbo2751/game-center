package com.example.walletservice.controller;

import com.example.walletservice.entity.Member;
import com.example.walletservice.service.WalletService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/wallet")
@RequiredArgsConstructor
public class WalletController {
    private final WalletService walletService;

    @GetMapping("/{id}")
    public Member getWallet(@PathVariable String id) {
        return walletService.getWallet(id);
    }
    
    @GetMapping("/ranking")
    public List<Member> getRanking() {
        return walletService.getTopRanking();
    }

    @PostMapping("/transfer")
    public Map<String, String> transfer(@RequestBody Map<String, Object> payload) {
        String from = (String) payload.get("fromId");
        String to = (String) payload.get("toId");
        int amount = (Integer) payload.get("amount");
        
        Map<String, String> response = new HashMap<>();
        try {
            walletService.transferMoney(from, to, amount);
            response.put("status", "SUCCESS");
        } catch (Exception e) {
            response.put("status", "FAIL");
            response.put("message", e.getMessage());
        }
        return response;
    }
}
