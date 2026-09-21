package com.example.game_center.service;

import com.example.game_center.entity.GameStats;
import com.example.game_center.repository.GameStatsRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@RequiredArgsConstructor
public class GameStatsService {

    private final GameStatsRepository gameStatsRepository;

    @Transactional
    public void incrementPlayCount(String gameName) {
        GameStats stats = gameStatsRepository.findById(gameName)
                .orElse(new GameStats(gameName, 0));
        
        stats.setPlayCount(stats.getPlayCount() + 1);
        gameStatsRepository.save(stats);
    }

    @Transactional(readOnly = true)
    public int getPlayCount(String gameName) {
        return gameStatsRepository.findById(gameName)
                .map(GameStats::getPlayCount)
                .orElse(0);
    }

    @Transactional(readOnly = true)
    public java.util.Map<String, Integer> getAllPlayCounts() {
        return gameStatsRepository.findAll().stream()
                .collect(java.util.stream.Collectors.toMap(GameStats::getGameName, GameStats::getPlayCount));
    }
}
