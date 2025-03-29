from fleet_management_system.src import DATA_PATH
from gui.fleet_gui import FleetGUI

if __name__ == "__main__":
    app = FleetGUI(DATA_PATH / "nav_graph_1.json")
    app.run()
