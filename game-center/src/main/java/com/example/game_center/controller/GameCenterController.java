package com.example.game_center.controller;

import com.example.game_center.service.GameLauncherService;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.io.File;
import java.io.IOException;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

@Controller
public class GameCenterController {

    private final GameLauncherService launcherService;
    private final com.example.game_center.service.GameStatsService gameStatsService;

    public GameCenterController(GameLauncherService launcherService, com.example.game_center.service.GameStatsService gameStatsService) {
        this.launcherService = launcherService;
        this.gameStatsService = gameStatsService;
    }

    @GetMapping("/")
    public String index(Model model) {
        File baseDir = new File(System.getProperty("user.dir"), "games");

        List<String> games2d = scanPyFiles(new File(baseDir, "2d_pygame"));
        List<String> games3d = scanPyFiles(new File(baseDir, "3d_panda3d"));

        model.addAttribute("games2d", games2d);
        model.addAttribute("games3d", games3d);
        model.addAttribute("playCounts", gameStatsService.getAllPlayCounts());
        return "index";
    }

    @ResponseBody
    @PostMapping("/api/games/launch")
    public String launch(@RequestParam("category") String category,
                         @RequestParam("script") String script) {
        try {
            launcherService.launchGame(category, script);
            gameStatsService.incrementPlayCount(script);
            return "SUCCESS";
        } catch (IOException | IllegalArgumentException e) {
            return "FAIL: " + e.getMessage();
        }
    }

    @ResponseBody
    @PostMapping("/api/stats/increment")
    public String incrementStats(@RequestParam("script") String script) {
        gameStatsService.incrementPlayCount(script);
        return "SUCCESS";
    }

    @ResponseBody
    @GetMapping("/api/stats")
    public java.util.Map<String, Integer> getStats() {
        return gameStatsService.getAllPlayCounts();
    }

    private List<String> scanPyFiles(File folder) {
        if (!folder.exists() || !folder.isDirectory()) {
            return Collections.emptyList();
        }
        String[] files = folder.list((dir, name) -> name.endsWith(".py"));
        return (files != null) ? Arrays.asList(files) : Collections.emptyList();
    }
}