package com.example.game_center.repository;

import com.example.game_center.entity.MarketItem;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface MarketItemRepository extends JpaRepository<MarketItem, Long> {
    List<MarketItem> findByIsSoldFalse();
    List<MarketItem> findBySellerNameAndIsSoldTrue(String sellerName);
    List<MarketItem> findBySellerNameAndIsSoldFalse(String sellerName);
    long countByIsSoldFalse();
}
