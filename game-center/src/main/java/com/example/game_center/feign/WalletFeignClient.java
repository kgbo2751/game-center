package com.example.game_center.feign;

import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;

import java.util.Map;

@FeignClient(name = "wallet-service", url = "http://localhost:8081/api/wallet")
public interface WalletFeignClient {

    @GetMapping("/{id}")
    Map<String, Object> getWallet(@PathVariable("id") String id);

    @PostMapping("/transfer")
    Map<String, String> transferMoney(@RequestBody Map<String, Object> payload);
}
