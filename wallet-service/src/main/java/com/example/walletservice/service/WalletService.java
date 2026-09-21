package com.example.walletservice.service;

import com.example.walletservice.entity.Member;
import com.example.walletservice.repository.MemberRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Random;

@Service
@RequiredArgsConstructor
public class WalletService {
    private final MemberRepository memberRepository;

    @Transactional(readOnly = true)
    public Member getWallet(String id) {
        return memberRepository.findById(id).orElse(null);
    }
    
    @Transactional(readOnly = true)
    public List<Member> getTopRanking() {
        return memberRepository.findTop5ByOrderByBalanceDesc();
    }

    @Transactional
    public void transferMoney(String fromId, String toId, int amount) {
        Member from = memberRepository.findById(fromId).orElseThrow(() -> new IllegalArgumentException("Sender not found"));
        Member to = memberRepository.findById(toId).orElseThrow(() -> new IllegalArgumentException("Receiver not found"));
        
        if (from.getBalance() < amount) {
            throw new IllegalArgumentException("Not enough balance");
        }
        
        from.setBalance(from.getBalance() - amount);
        to.setBalance(to.getBalance() + amount);
        
        memberRepository.save(from);
        memberRepository.save(to);
    }
    
    @Transactional
    @Scheduled(fixedRate = 5000)
    public void simulateBotEconomy() {
        String[] botNames = {"Bot_Alex", "Bot_Zelda", "Bot_Mario", "Bot_Link", "Bot_Cloud"};
        Random random = new Random();
        
        // Ensure bots exist
        if (memberRepository.count() < 2) {
            memberRepository.save(new Member("User", "Player1", 50000));
            for (String bot : botNames) {
                memberRepository.save(new Member(bot, bot, 10000 + random.nextInt(40000)));
            }
        }
        
        // Randomly fluctuate bot balances
        for (String bot : botNames) {
            memberRepository.findById(bot).ifPresent(m -> {
                int change = (random.nextInt(21) - 10) * 1000; // -10000 to +10000
                int newBalance = m.getBalance() + change;
                if (newBalance < 0) newBalance = 0;
                m.setBalance(newBalance);
                memberRepository.save(m);
            });
        }
    }
}
