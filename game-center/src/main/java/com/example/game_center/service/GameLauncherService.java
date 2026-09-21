package com.example.game_center.service;

import org.springframework.stereotype.Service;
import java.io.File;
import java.io.IOException;

@Service
public class GameLauncherService {

    public void launchGame(String category, String scriptName) throws IOException {
        if (category.contains("..") || scriptName.contains("..") || !scriptName.endsWith(".py")) {
            throw new IllegalArgumentException("Invalid file path");
        }

        File baseDir = new File(System.getProperty("user.dir"), "games");
        File targetDir = new File(baseDir, category);
        File scriptFile = new File(targetDir, scriptName);

        if (!scriptFile.exists()) {
            throw new IllegalArgumentException("File not found: " + scriptFile.getPath());
        }

        ProcessBuilder pb = new ProcessBuilder("python", scriptName);
        pb.directory(targetDir);
        pb.start();
    }
}