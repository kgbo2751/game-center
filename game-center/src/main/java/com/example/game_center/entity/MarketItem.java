package com.example.game_center.entity;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Entity
@Getter
@Setter
@NoArgsConstructor
public class MarketItem {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    private String itemName;
    private String sellerName;
    private int price;
    private boolean isSold;

    public MarketItem(String itemName, String sellerName, int price, boolean isSold) {
        this.itemName = itemName;
        this.sellerName = sellerName;
        this.price = price;
        this.isSold = isSold;
    }
}
