#! python3

"""Manager for heatmap layers and styles."""

# standard
import os
import pathlib

# PyQGIS
from qgis.core import (
    Qgis,
    QgsCoordinateReferenceSystem,
    QgsProject,
    QgsRasterLayer,
    QgsVectorLayer,
)
from qgis.gui import QgisInterface
from qgis.PyQt.QtCore import Qt

from raft_heatmap.category_enum import PinCategories

# project
from raft_heatmap.gui.dockwidget import RaftDockWidget
from raft_heatmap.toolbelt import PlgLogger


class HeatmapManager:
    # @TODO: fix hardcoded style file names
    fname_parcel_style = "parcel_styles.qml"
    fname_pin_style = "pin_styles.qml"
    fname_heatmap_style = "heatmap_styles.qml"

    def __init__(self, logger: PlgLogger, iface: QgisInterface):
        self.log = logger.log
        self.iface = iface
        # Create the dockwidget and keep reference
        self.dockwidget = RaftDockWidget()
        self.configure_signal_handlers()
        self.widget_added = False
        self.parcel_layer = None
        self.pin_layer = None

    def run(self):
        try:
            self.log(
                message="Initializing RAFT heatmap dockwidget...",
                log_level=Qgis.MessageLevel.Success,
                push=False,
            )

            # show the dockwidget
            if not self.widget_added:
                self.iface.addDockWidget(Qt.RightDockWidgetArea, self.dockwidget)
                self.widget_added = True

            self.dockwidget.show()
            self.log(
                message="Dockwidget initialized.",
                log_level=Qgis.MessageLevel.Success,
                push=False,
            )

        except Exception as err:
            self.log(
                message="Something went wrong with RAFT heatmap widget initialization: {}".format(
                    err
                ),
                log_level=Qgis.MessageLevel.Critical,
                push=True,
            )

    def unload(self):
        self.dockwidget.close()

    def add_basemap(self):
        uri = "type=xyz&url=http://services.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/%7Bz%7D/%7By%7D/%7Bx%7D&zmax=16&zmin=0&http-header:referer="
        layer = QgsRasterLayer(uri, "ESRI dark", "wms")
        QgsProject.instance().addMapLayer(layer)

    def add_parcels(self):
        # loading parcels
        # @TODO: fix hardcoded path to parcel shapefile
        project_uri = pathlib.Path(__file__).parent.resolve()
        parcel_uri = os.path.join(
            project_uri, "resources", "river_parcels", "ParcelUpdate1124.shp"
        )
        if os.path.exists(parcel_uri):
            self.parcel_layer = QgsVectorLayer(parcel_uri, "SDRPF_Parcels", "ogr")
            self.load_style(self.parcel_layer, self.fname_parcel_style)
            QgsProject.instance().addMapLayer(self.parcel_layer)
        else:
            self.log(
                message="Parcel file path invalid. Please recheck and try again: {}".format(
                    parcel_uri
                ),
                log_level=Qgis.MessageLevel.Critical,
                push=True,
            )

    def add_trashpins(self, csv_f_path: str):
        try:
            mappler_csv_uri = (
                "file:///"
                + csv_f_path
                + "?delimiter=%s&crs=epsg:4326&xField=%s&yField=%s"
                % (",", "Longitude", "Latitude")
            )
            self.pin_layer = QgsVectorLayer(
                mappler_csv_uri, "Trash_Pins", "delimitedtext"
            )
            self.load_style(self.pin_layer, self.fname_pin_style)
            QgsProject.instance().addMapLayer(self.pin_layer)
        except Exception as err:
            self.log(
                message="Unable to load Mappler CSV file. Please inspect your file and try again: {}".format(
                    err
                ),
                log_level=Qgis.MessageLevel.Critical,
                push=True,
            )
            return

    def load_style(self, layer, style_fname):
        # @TODO: fix hardcoded path to styles
        project_uri = pathlib.Path(__file__).parent.resolve()
        style_uri = os.path.join(project_uri, "resources", "styles", style_fname)
        try:
            layer.loadNamedStyle(style_uri)
        except Exception as err:
            self.log(
                message="Unable to layer style: {}".format(err),
                log_level=Qgis.MessageLevel.Critical,
                push=True,
            )

    # --------------Handlers for signals emitted by dockwidget------------------

    def configure_signal_handlers(self):
        try:
            self.dockwidget.csvSelected.connect(self.onMapplerCSVSelected)
            self.dockwidget.heatMapDisplaySelected.connect(
                self.onHeatMapDisplaySelected
            )
            self.dockwidget.pinDisplaySelected.connect(self.onPinDisplaySelected)
            self.dockwidget.pinsFiltered.connect(self.onPinsFiltered)
        except Exception as err:
            self.log(
                message="Something went wrong with signal handler configuration: {}".format(
                    err
                ),
                log_level=Qgis.MessageLevel.Critical,
                push=True,
            )

    def onMapplerCSVSelected(self, csv_f_path: str):
        self.add_basemap()
        self.add_parcels()
        self.add_trashpins(csv_f_path)

    def onHeatMapDisplaySelected(self):
        self.load_style(self.pin_layer, self.fname_heatmap_style)
        self.log(
            message="Updating project CRS to EPSG:3857",
            log_level=Qgis.MessageLevel.Info,
            push=False,
        )
        # heatmap style requires EPSG:3857
        QgsProject.instance().setCrs(QgsCoordinateReferenceSystem("EPSG:3857"))

        self.pin_layer.triggerRepaint()

    def onPinDisplaySelected(self):
        self.load_style(self.pin_layer, self.fname_pin_style)
        self.pin_layer.triggerRepaint()

    def onPinsFiltered(self, selected_categories):
        if self.pin_layer is not None:
            serialized_categories = "','".join(
                [PinCategories[c].value for c in selected_categories]
            )
            self.pin_layer.setSubsetString(
                "\"Category\" IN ('{}')".format(serialized_categories)
            )
            self.log(
                message="Filtered to {} features".format(self.pin_layer.featureCount()),
                log_level=Qgis.MessageLevel.Info,
                push=False,
            )
