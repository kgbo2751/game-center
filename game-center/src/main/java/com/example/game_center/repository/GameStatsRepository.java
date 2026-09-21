package com.example.game_center.repository;

import com.example.game_center.entity.GameStats;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface GameStatsRepository extends JpaRepository<GameStats, String> {
}
