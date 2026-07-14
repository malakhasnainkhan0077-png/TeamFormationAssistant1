import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QSpinBox,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, QGroupBox,
    QMessageBox, QHeaderView, QTabWidget, QTextEdit
)
from PyQt6.QtCore import Qt


class TeamFormationAssistant(QWidget):
    def __init__(self):
        super().__init__()
        self.players = []
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Team Formation Assistant - Game Theory Based")
        self.resize(800, 600)

        main_layout = QVBoxLayout()

        input_group = QGroupBox("Add Player")
        input_layout = QHBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Player Name")

        self.skill_input = QSpinBox()
        self.skill_input.setRange(1, 10)
        self.skill_input.setValue(5)

        add_button = QPushButton("Add Player")
        add_button.clicked.connect(self.add_player)

        remove_button = QPushButton("Remove Selected")
        remove_button.clicked.connect(self.remove_player)

        clear_button = QPushButton("Clear All")
        clear_button.clicked.connect(self.clear_players)

        input_layout.addWidget(QLabel("Name:"))
        input_layout.addWidget(self.name_input)
        input_layout.addWidget(QLabel("Skill (1-10):"))
        input_layout.addWidget(self.skill_input)
        input_layout.addWidget(add_button)
        input_layout.addWidget(remove_button)
        input_layout.addWidget(clear_button)

        input_group.setLayout(input_layout)
        main_layout.addWidget(input_group)

        self.player_table = QTableWidget()
        self.player_table.setColumnCount(2)
        self.player_table.setHorizontalHeaderLabels(["Player Name", "Skill Rating"])
        self.player_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.player_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        main_layout.addWidget(self.player_table)

        team_group = QGroupBox("Generate Balanced Teams")
        team_layout = QHBoxLayout()

        self.team_count_input = QSpinBox()
        self.team_count_input.setRange(2, 10)
        self.team_count_input.setValue(2)

        generate_button = QPushButton("Generate Teams")
        generate_button.clicked.connect(self.generate_teams)

        team_layout.addWidget(QLabel("Number of Teams:"))
        team_layout.addWidget(self.team_count_input)
        team_layout.addWidget(generate_button)

        team_group.setLayout(team_layout)
        main_layout.addWidget(team_group)

        self.result_tabs = QTabWidget()
        main_layout.addWidget(self.result_tabs)

        self.setLayout(main_layout)

    def add_player(self):
        name = self.name_input.text().strip()
        skill = self.skill_input.value()

        if not name:
            QMessageBox.warning(self, "Input Error", "Player name cannot be empty.")
            return

        for player in self.players:
            if player["name"].lower() == name.lower():
                QMessageBox.warning(self, "Duplicate Player", "A player with this name already exists.")
                return

        self.players.append({"name": name, "skill": skill})
        self.refresh_player_table()
        self.name_input.clear()
        self.skill_input.setValue(5)

    def remove_player(self):
        selected_rows = sorted(set(index.row() for index in self.player_table.selectedIndexes()), reverse=True)
        if not selected_rows:
            QMessageBox.warning(self, "Selection Error", "Select a player row to remove.")
            return

        for row in selected_rows:
            del self.players[row]

        self.refresh_player_table()

    def clear_players(self):
        if not self.players:
            return

        confirm = QMessageBox.question(
            self, "Confirm Clear", "Remove all players?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm == QMessageBox.StandardButton.Yes:
            self.players.clear()
            self.refresh_player_table()
            self.result_tabs.clear()

    def refresh_player_table(self):
        self.player_table.setRowCount(len(self.players))
        for row, player in enumerate(self.players):
            self.player_table.setItem(row, 0, QTableWidgetItem(player["name"]))
            self.player_table.setItem(row, 1, QTableWidgetItem(str(player["skill"])))

    def generate_teams(self):
        team_count = self.team_count_input.value()

        if len(self.players) < team_count:
            QMessageBox.warning(self, "Not Enough Players", "You need at least as many players as teams.")
            return

        sorted_players = sorted(self.players, key=lambda p: p["skill"], reverse=True)
        teams = [[] for _ in range(team_count)]
        team_totals = [0] * team_count

        direction = 1
        team_index = 0

        for player in sorted_players:
            teams[team_index].append(player)
            team_totals[team_index] += player["skill"]

            if direction == 1:
                team_index += 1
                if team_index == team_count:
                    team_index -= 1
                    direction = -1
            else:
                team_index -= 1
                if team_index < 0:
                    team_index += 1
                    direction = 1

        self.display_teams(teams, team_totals)

    def display_teams(self, teams, team_totals):
        self.result_tabs.clear()

        for i, team in enumerate(teams):
            team_widget = QTextEdit()
            team_widget.setReadOnly(True)

            content = f"Team {i + 1} - Total Skill: {team_totals[i]}\n"
            content += "-" * 40 + "\n"
            for player in team:
                content += f"{player['name']} (Skill: {player['skill']})\n"

            team_widget.setText(content)
            self.result_tabs.addTab(team_widget, f"Team {i + 1}")

        summary_widget = QTextEdit()
        summary_widget.setReadOnly(True)
        summary_content = "Balance Summary\n" + "-" * 40 + "\n"
        max_diff = max(team_totals) - min(team_totals)
        for i, total in enumerate(team_totals):
            summary_content += f"Team {i + 1} Total Skill: {total}\n"
        summary_content += f"\nMax Skill Difference Between Teams: {max_diff}\n"
        summary_widget.setText(summary_content)
        self.result_tabs.addTab(summary_widget, "Summary")


def main():
    app = QApplication(sys.argv)
    window = TeamFormationAssistant()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
