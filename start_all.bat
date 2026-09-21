@echo off
echo ==================================================
echo  MSA Servers Starting...
echo ==================================================

echo 1. Starting Wallet Service (Port 8081)
start "Wallet Service (8081)" cmd /k "cd wallet-service && gradlew bootRun"

echo 2. Starting API Gateway (Port 9000)
start "API Gateway (9000)" cmd /k "cd api-gateway && gradlew bootRun"

echo 3. Starting Game Center (Port 8080)
start "Game Center (8080)" cmd /k "cd game-center && gradlew bootRun"

echo 4. Starting Python Frontend (Port 8000)
start "Python Web (8000)" cmd /k "cd game-center\python-web && uvicorn main:app --reload"

echo ==================================================
echo [IMPORTANT] 4 servers are booting up! (Takes ~20 seconds)
echo Please wait until the scrolling text stops in all 4 windows.
echo Once you see "Started Application in ...", open your browser!
echo ==================================================
pause
