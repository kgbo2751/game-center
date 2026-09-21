import glob
import os

translations = {
    " - 당신의 선택은 틀렸습니다.": " - Your choice was wrong.",
    " - 당신의 선택이 맞았습니다!": " - Your choice was correct!",
    "1~100 사이 숫자를 입력하세요": "Enter a number between 1 and 100",
    "1대1 포커 (카드 교환 가능)": "1v1 Poker (Cards Exchangeable)",
    "2048 게임": "2048 Game",
    "3자리 룰렛 머신": "3-Slot Roulette Machine",
    "4x4 퍼즐 맞추기": "4x4 Puzzle",
    "4자리 숫자 야구 맞추기": "Bulls and Cows",
    "4자리 숫자를 입력하세요!": "Enter 4 digits!",
    "5레인 경마 게임": "5-Lane Horse Racing",
    "가위": "Scissors",
    "가위 바위 보": "Rock Paper Scissors",
    "게임 오버!": "Game Over!",
    "게임 종료! 모든 카드를 맞추셨습니다.": "Game Over! You matched all cards.",
    "게임 종료! 우승자: {winner}": "Game Over! Winner: {winner}",
    "게임 종료! 총 {self.kick_count}번 중 {self.score}골 성공했습니다.": "Game Over! {self.score} goals out of {self.kick_count} kicks.",
    "게임 클리어! 🎉": "Game Cleared! 🎉",
    "결과: {numbers[selected_number_on_wheel]}": "Result: {numbers[selected_number_on_wheel]}",
    "결과: {random.choice(possible_values)}": "Result: {random.choice(possible_values)}",
    "결과: {result}": "Result: {result}",
    "골! 성공입니다.": "Goal! Success.",
    "골: 0 / 5": "Goal: 0 / 5",
    "골: {self.score} / {self.kick_count}": "Goal: {self.score} / {self.kick_count}",
    "내 선택: {user_choice}": "My Choice: {user_choice}",
    "다운!": "Down!",
    "당신: {self.kicker_choice}  키퍼: {self.goalkeeper_choice}  -  {result}": "You: {self.kicker_choice} Keeper: {self.goalkeeper_choice} - {result}",
    "당신이 이겼습니다!": "You Win!",
    "돌리기": "Spin",
    "두더지 잡기": "Whack-a-Mole",
    "러시아워": "Rush Hour",
    "레이저 피하기 게임": "Dodge Laser",
    "룰렛 머신": "Roulette Machine",
    "리듬 게임": "Rhythm Game",
    "마우스로 좌/중앙/우로 드래그해서 차세요": "Drag Left/Center/Right to Kick",
    "말을 선택하세요": "Select your horse",
    "메모리 카드 게임": "Memory Card Game",
    "바위": "Rock",
    "발판 점프 게임": "Platform Jump",
    "벽돌깨기 게임": "Breakout",
    "보": "Paper",
    "블랙잭 게임": "Blackjack",
    "비겼습니다!": "It's a Tie!",
    "비김": "Tie",
    "선택한 번호: {selected_number}": "Selected Number: {selected_number}",
    "시도 횟수: {attempts}": "Attempts: {attempts}",
    "실패! 키퍼가 막았습니다.": "Miss! Keeper blocked it.",
    "업!": "Up!",
    "업다운 게임": "Up Down Game",
    "와 ": " and ",
    "우승: 말 {winner + 1}": "Winner: Horse {winner + 1}",
    "이김": "Win",
    "입력: {input_number}": "Input: {input_number}",
    "정답! {attempts}번 만에 성공!": "Correct! Success in {attempts} tries!",
    "정답을 맞췄습니다! {attempts}번째 시도": "Correct answer! Attempt: {attempts}",
    "지뢰찾기": "Minesweeper",
    "짐": "Lose",
    "총 쏘기 게임": "Shooting Game",
    "최대 시도 횟수를 초과했습니다! 정답은 {target_number}였습니다.": "Max attempts exceeded! Answer was {target_number}.",
    "축하합니다! {self.kick_count}번째 슛에 3골 이상 성공해 승리했습니다!": "Congratulations! Won with 3+ goals on kick {self.kick_count}!",
    "컴퓨터 선택: {computer_choice}": "Computer Choice: {computer_choice}",
    "컴퓨터가 이겼습니다!": "Computer Wins!",
    "클리어!": "Clear!",
    "테트리스": "Tetris",
    "틱택토 - 컴퓨터 대결": "TicTacToe vs Computer",
    "퍼즐 맞추기 성공!": "Puzzle completed!",
    "페널티킥 게임": "Penalty Kick Game",
    "폰트를 찾을 수 없습니다. NotoSansKR-Regular.ttf 파일이 같은 폴더에 있어야 합니다.": "Font not found",
    "피하기 게임": "Dodge Game",
    "🏆 우승자: {winner} 🏆": "🏆 Winner: {winner} 🏆"
}

files = glob.glob('games/**/*.py', recursive=True)
count = 0
for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    original = content
    for kr, en in translations.items():
        content = content.replace(kr, en)
        
    if content != original:
        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
        count += 1
        print(f"Translated: {f}")

print(f"Total files translated: {count}")
