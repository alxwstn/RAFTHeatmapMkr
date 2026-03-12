#! python3

"""Manager for heatmap layers and styles."""

import os
import pathlib

# standard
from datetime import datetime

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

# project
from raft_heatmap.category_enum import PinCategories
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
        self.base_layer = None

    def run(self):
        try:
            self.log(
                message="Initializing RAFT heatmap dockwidget...",
                log_level=Qgis.MessageLevel.Success,
                push=False,
            )

            # show the dockwidget
            if not self.widget_added:
                self.iface.addDockWidget(
                    Qt.DockWidgetArea.RightDockWidgetArea, self.dockwidget
                )
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
        """Add the map baselayer"""
        uri = "type=xyz&url=http://services.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/%7Bz%7D/%7By%7D/%7Bx%7D&zmax=16&zmin=0&http-header:referer="
        self.base_layer = QgsRasterLayer(uri, "ESRI dark", "wms")
        QgsProject.instance().addMapLayer(self.base_layer)

    def add_parcels(self):
        """Add the parcel shapefile layer"""
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
        """Load Mappler CSV pins into a QgsVectorLayer

        :param csv_f_path: path to the csv file in the user's filesystem
        :type csv_f_path: str
        """
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
        """_summary_

        :param layer: layer to be styled
        :type layer: QgsVectorLayer
        :param style_fname: filename of named style to be applied to the layer
        :type style_fname: string
        """
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

    def reset_layers(self):
        """_summary_ rename the existing pin layer, hide it,
        and manage base_layer and parcel layers
        """
        try:
            displayedMapLayers = QgsProject.instance().mapLayers()
            # remove references to the basemap and parcels layers, if they are no longer
            # visible in the interface. They will be reloaded the next time a file is selected
            if self.base_layer is not None:
                if self.base_layer.id() not in displayedMapLayers:
                    self.base_layer = None

            if (
                self.parcel_layer is not None
                and self.parcel_layer.id() not in displayedMapLayers
            ):
                self.parcel_layer = None

            # rename the old pin layer and change its visibility, if it is still loaded in the map
            if self.pin_layer is not None and self.pin_layer.id() in displayedMapLayers:
                layer_name = "{}_{}".format(
                    self.pin_layer.name(), datetime.now().isoformat()
                )
                self.pin_layer.setName(layer_name)
                node = QgsProject.instance().layerTreeRoot().findLayer(self.pin_layer)
                self.pin_layer = None
                if node:
                    node.setItemVisibilityChecked(False)
                    self.log(
                        message="CSV file changed or removed. Previous pin layer saved as {} and visibility changed to hidden".format(
                            layer_name
                        ),
                        log_level=Qgis.MessageLevel.Warning,
                        push=True,
                    )
        except Exception as err:
            self.log(
                message="Layer cleanup error: {}".format(err),
                log_level=Qgis.MessageLevel.Warning,
                push=False,
            )
            print(err)

        self.pin_layer = None
        self.iface.mapCanvas().refresh()

    # --------------Handlers for signals emitted by dockwidget------------------

    def configure_signal_handlers(self):
        """connect signals from the dockwidget UI to handlers in the heatmap_manager"""
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
        """signal handler that is triggered when the dockwidget csvSelected signal fires

        :param csv_f_path: path to the csv file in the user's filesystem
        :type csv_f_path: str
        """
        self.reset_layers()

        if csv_f_path:
            if self.base_layer is None:
                self.add_basemap()
            if self.parcel_layer is None:
                self.add_parcels()
            self.add_trashpins(csv_f_path)

    def onHeatMapDisplaySelected(self):
        """signal handler that is triggered when the dockwidget onHeatMapDisplaySelected
        signal fires
        """
        if self.pin_layer is not None:
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
        """signal handler that is triggered when the dockwidget onPinDisplaySelected signal
        fires.
        """
        if self.pin_layer is not None:
            self.load_style(self.pin_layer, self.fname_pin_style)
            self.pin_layer.triggerRepaint()

    def onPinsFiltered(self, selected_categories):
        """signal handler that is triggered when the dockwidget pinsFiltered
        fires. This signal fires when the UI checkbox states are changed.
        :param selected_categories: array representing the selected pin categories
        :type selected_categories: list[PinCategory enum key]
        """
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
