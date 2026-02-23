# standard

# PyQGIS
from qgis.core import Qgis
from qgis.gui import QgisInterface
from qgis.PyQt.QtCore import Qt

# project
from raft_heatmap.gui.dockwidget import RaftDockWidget
from raft_heatmap.toolbelt import PlgLogger


class HeatmapManager:
    def __init__(self, logger: PlgLogger, iface: QgisInterface):
        self.log = logger.log
        self.iface = iface
        self.dockwidget = None

    def run(self):
        try:
            self.log(
                message="Initializing RAFT heatmap dockwidget...",
                log_level=Qgis.MessageLevel.Success,
                push=False,
            )
            if self.dockwidget is None:
                # Create the dockwidget (after translation) and keep reference
                self.dockwidget = RaftDockWidget()
                # show the dockwidget
                self.iface.addDockWidget(Qt.RightDockWidgetArea, self.dockwidget)
                self.log(
                    message="Dockwidget initialized.",
                    log_level=Qgis.MessageLevel.Success,
                    push=False,
                )
            self.dockwidget.show()

        except Exception as err:
            self.log(
                message="Something went wrong with RAFT heatmap widget initialization: {}".format(
                    err
                ),
                log_level=Qgis.MessageLevel.Critical,
                push=True,
            )
