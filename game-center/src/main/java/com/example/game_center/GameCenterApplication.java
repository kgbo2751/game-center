package com.example.game_center;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;
import org.springframework.cloud.openfeign.EnableFeignClients;

@SpringBootApplication
@EnableScheduling
@EnableFeignClients
public class GameCenterApplication {

	public static void main(String[] args) {
		SpringApplication.run(GameCenterApplication.class, args);
	}

}
