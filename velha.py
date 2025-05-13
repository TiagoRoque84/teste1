import tkinter as tk
from tkinter import messagebox
import random

class TicTacToe:
    def __init__(self, master):
        self.master = master
        master.title("Jogo da Velha - Corporate Edition")
        self.vs_computer = None  # True: vs computador; False: vs jogador
        self.current_player = "X"
        self.board = [""] * 9

        # Cria frame para seleção do modo de jogo
        self.menu_frame = tk.Frame(master)
        self.menu_frame.pack(padx=20, pady=20)
        self.create_menu()

        # Frame do jogo (será exibido após escolher o modo)
        self.game_frame = tk.Frame(master)

    def create_menu(self):
        tk.Label(self.menu_frame, text="Escolha o modo de jogo", font=("Helvetica", 16)).pack(pady=10)
        tk.Button(self.menu_frame, text="Jogador vs Computador", font=("Helvetica", 14),
                  command=lambda: self.start_game(True)).pack(pady=5)
        tk.Button(self.menu_frame, text="Jogador vs Jogador", font=("Helvetica", 14),
                  command=lambda: self.start_game(False)).pack(pady=5)

    def start_game(self, vs_computer):
        self.vs_computer = vs_computer
        self.menu_frame.pack_forget()  # Remove o menu
        self.game_frame.pack(padx=20, pady=20)
        self.create_game_board()

    def create_game_board(self):
        # Status da partida
        self.status_label = tk.Label(self.game_frame, text=f"Vez do {self.current_player}", font=("Helvetica", 16))
        self.status_label.grid(row=0, column=0, columnspan=3, pady=10)

        # Cria os botões do tabuleiro 3x3
        self.buttons = []
        for i in range(9):
            btn = tk.Button(self.game_frame, text="", font=("Helvetica", 20), width=5, height=2,
                            command=lambda i=i: self.button_click(i))
            btn.grid(row=(i // 3) + 1, column=i % 3, padx=5, pady=5)
            self.buttons.append(btn)

        # Botões de reiniciar e sair
        tk.Button(self.game_frame, text="Reiniciar", font=("Helvetica", 14),
                  command=self.restart_game).grid(row=4, column=0, pady=10)
        tk.Button(self.game_frame, text="Sair", font=("Helvetica", 14),
                  command=self.master.quit).grid(row=4, column=2, pady=10)

    def button_click(self, index):
        if self.buttons[index]["text"] != "" or self.check_winner():
            return

        self.buttons[index]["text"] = self.current_player
        self.board[index] = self.current_player

        if self.check_winner():
            self.status_label.config(text=f"{self.current_player} venceu!")
            messagebox.showinfo("Fim de jogo", f"Parabéns! {self.current_player} venceu!")
            self.disable_buttons()
            return
        elif "" not in self.board:
            self.status_label.config(text="Empate!")
            messagebox.showinfo("Fim de jogo", "Empate!")
            return

        # Troca de jogador
        self.current_player = "O" if self.current_player == "X" else "X"
        self.status_label.config(text=f"Vez do {self.current_player}")

        # Se for vs Computador e a vez do computador, processa o movimento
        if self.vs_computer and self.current_player == "O":
            self.master.after(500, self.computer_move)

    def computer_move(self):
        available_moves = [i for i, v in enumerate(self.board) if v == ""]
        if not available_moves or self.check_winner():
            return

        move = random.choice(available_moves)
        self.buttons[move]["text"] = self.current_player
        self.board[move] = self.current_player

        if self.check_winner():
            self.status_label.config(text=f"{self.current_player} venceu!")
            messagebox.showinfo("Fim de jogo", f"Parabéns! {self.current_player} venceu!")
            self.disable_buttons()
            return
        elif "" not in self.board:
            self.status_label.config(text="Empate!")
            messagebox.showinfo("Fim de jogo", "Empate!")
            return

        # Volta a vez para o jogador
        self.current_player = "X"
        self.status_label.config(text=f"Vez do {self.current_player}")

    def check_winner(self):
        win_conditions = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Linhas
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Colunas
            (0, 4, 8), (2, 4, 6)              # Diagonais
        ]
        for a, b, c in win_conditions:
            if self.board[a] == self.board[b] == self.board[c] != "":
                return True
        return False

    def disable_buttons(self):
        for btn in self.buttons:
            btn.config(state="disabled")

    def restart_game(self):
        self.current_player = "X"
        self.board = [""] * 9
        self.status_label.config(text=f"Vez do {self.current_player}")
        for btn in self.buttons:
            btn.config(text="", state="normal")

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToe(root)
    root.mainloop()
