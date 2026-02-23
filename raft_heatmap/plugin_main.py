#! python3  # noqa: E265

"""Main plugin module."""

# standard
from functools import partial
from pathlib import Path

# PyQGIS
from qgis.core import Qgis, QgsApplication, QgsSettings
from qgis.gui import QgisInterface
from qgis.PyQt.QtCore import QCoreApplication, QLocale, QTranslator, QUrl
from qgis.PyQt.QtGui import QDesktopServices, QIcon
from qgis.PyQt.QtWidgets import QAction

# project
from raft_heatmap.__about__ import (
    DIR_PLUGIN_ROOT,
    __icon_path__,
    __title__,
    __uri_homepage__,
)
from raft_heatmap.gui.dlg_settings import PlgOptionsFactory
from raft_heatmap.heatmap_manager import HeatmapManager
from raft_heatmap.toolbelt import PlgLogger

# ############################################################################
# ########## Classes ###############
# ##################################


class RaftHeatmapPlugin:
    def __init__(self, iface: QgisInterface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class which \
        provides the hook by which you can manipulate the QGIS application at run time.
        :type iface: QgsInterface
        """
        self.iface = iface
        logger = PlgLogger()
        self.log = logger.log
        self.heatmap_manager = HeatmapManager(logger=logger, iface=iface)

        # translation
        # initialize the locale
        self.locale: str = QgsSettings().value("locale/userLocale", QLocale().name())[
            0:2
        ]
        locale_path: Path = (
            DIR_PLUGIN_ROOT
            / "resources"
            / "i18n"
            / f"{__title__.lower()}_{self.locale}.qm"
        )
        self.log(
            message=f"Translation: {self.locale}, {locale_path}",
            log_level=Qgis.MessageLevel.NoLevel,
        )
        if locale_path.exists():
            self.translator = QTranslator()
            self.translator.load(str(locale_path.resolve()))
            QCoreApplication.installTranslator(self.translator)

    def initGui(self):
        """Set up plugin UI elements."""

        # settings page within the QGIS preferences menu
        self.options_factory = PlgOptionsFactory()
        self.iface.registerOptionsWidgetFactory(self.options_factory)

        # -- Actions
        self.action_help = QAction(
            QgsApplication.getThemeIcon("mActionHelpContents.svg"),
            self.tr("Help"),
            self.iface.mainWindow(),
        )
        self.action_help.triggered.connect(
            partial(QDesktopServices.openUrl, QUrl(__uri_homepage__))
        )

        self.action_settings = QAction(
            QgsApplication.getThemeIcon("console/iconSettingsConsole.svg"),
            self.tr("Setting"),
            self.iface.mainWindow(),
        )
        self.action_settings.triggered.connect(
            lambda: self.iface.showOptionsDialog(
                currentPage="mOptionsPage{}".format(__title__)
            )
        )

        self.action_heatmap = QAction(
            QgsApplication.getThemeIcon("console/iconSettingsConsole.svg"),
            self.tr("Generate Heatmap"),
            self.iface.mainWindow(),
        )
        self.action_heatmap.triggered.connect(lambda: self.heatmap_manager.run())

        # -- Menu
        self.iface.addPluginToMenu(__title__, self.action_heatmap)
        self.iface.addPluginToMenu(__title__, self.action_settings)
        self.iface.addPluginToMenu(__title__, self.action_help)

        # -- Help menu

        # documentation
        self.iface.pluginHelpMenu().addSeparator()
        self.action_help_plugin_menu_documentation = QAction(
            QIcon(str(__icon_path__)),
            f"{__title__} - Documentation",
            self.iface.mainWindow(),
        )
        self.action_help_plugin_menu_documentation.triggered.connect(
            partial(QDesktopServices.openUrl, QUrl(__uri_homepage__))
        )

        self.iface.pluginHelpMenu().addAction(
            self.action_help_plugin_menu_documentation
        )

    def tr(self, message: str) -> str:
        """Get the translation for a string using Qt translation API.

        :param message: string to be translated.
        :type message: str

        :returns: Translated version of message.
        :rtype: str
        """
        return QCoreApplication.translate(self.__class__.__name__, message)

    def unload(self):
        """Cleans up when plugin is disabled/uninstalled."""
        # -- Clean up menu
        self.iface.removePluginMenu(__title__, self.action_help)
        self.iface.removePluginMenu(__title__, self.action_settings)
        self.iface.removePluginMenu(__title__, self.action_heatmap)

        # -- Clean up preferences panel in QGIS settings
        self.iface.unregisterOptionsWidgetFactory(self.options_factory)

        # remove from QGIS help/extensions menu
        if self.action_help_plugin_menu_documentation:
            self.iface.pluginHelpMenu().removeAction(
                self.action_help_plugin_menu_documentation
            )

        # remove actions
        del self.action_settings
        del self.action_help

    def run(self):
        """Main process.

        :raises Exception: if there is no item in the feed
        """
        try:
            self.log(
                message=self.tr("Everything ran OK with plugin."),
                log_level=Qgis.MessageLevel.Success,
                push=False,
            )

        except Exception as err:
            self.log(
                message=self.tr(
                    "Something went wrong with RAFT heatmap plugin initialization: {}".format(
                        err
                    )
                ),
                log_level=Qgis.MessageLevel.Critical,
                push=True,
            )
