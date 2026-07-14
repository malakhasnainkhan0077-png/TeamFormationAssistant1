# Team Formation Assistant

A desktop GUI application that creates balanced sports teams from a list of players using a game theory–based fair division algorithm (snake draft).

## What It Does

- Add players with a name and a skill rating (1–10)
- View and manage the full player list in a table
- Choose how many teams to split players into
- Generate balanced teams with one click
- View each team's roster and total skill score in separate tabs
- See a summary comparing skill totals across teams to confirm balance

## How It Works

Players are sorted by skill rating (highest to lowest) and distributed across teams using a **snake draft**: team 1 picks first, then team 2, team 3, ... up to the last team, then the order reverses (last team picks again, then second-to-last, and so on back to team 1). This repeats until all players are assigned.

This approach is rooted in fair division / game theory, since it prevents any single team from ending up with all the top-rated players and keeps total skill levels close across teams.

## Requirements

- Python 3.8+
- PyQt6

## Installation

```bash
pip install -r requirements.txt
```

## How to Run

```bash
python team_formation_assistant.py
```

## Usage

1. Enter a player's name and skill rating, then click **Add Player**.
2. Repeat for all players. Use **Remove Selected** or **Clear All** to edit the list.
3. Set the **Number of Teams**.
4. Click **Generate Teams**.
5. Browse the generated teams and the **Summary** tab to see the skill balance.

## Screenshots

*(Add 2–3 screenshots here after running the app, e.g.:)*

`![Player List](screenshots/player-list.png)`

`![Generated Teams](screenshots/generated-teams.png)`

`![Summary Tab](screenshots/summary.png)`

## Note on AI Usage

AI (Claude) was used to help design and generate the initial version of the code, including the PyQt GUI layout and the snake draft balancing algorithm. The code was reviewed, tested, and run locally to confirm it meets the assignment requirements before submission. AI was also used to troubleshoot a PyQt5/Python 3.13 compatibility issue, which led to switching to PyQt6.

## Author

Malak Hasnain Khan
