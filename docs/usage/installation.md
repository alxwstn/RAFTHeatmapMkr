# Installation

## Latest released version

The plugin is automatically packaged for each commit to main, so you can use this address as repository URL in your QGIS extensions manager settings:

```url
https://alxwstn.github.io/RAFTHeatmapMkr/plugins.xml
```

## Installation Steps:

1. Launch QGIS and open the Plugin Manager: Select `Plugins` from the menu toolbar, then `Manage and Install Plugins`
2. Select `Settings`. In the Plugin Repositories, select `Add`. Set the `Name` field to `RAFT heatmap Repository`, and the url field to `https://alxwstn.github.io/RAFTHeatmapMkr/plugins.xml`. Select `OK`.

    ![QGIS - Add Custom Plugin Repository](../static/install_plugin_repository.png)

3. Select `All` on the left hand menu, then filter to `raft`
4. Select `raft_heatmap` and install

## Target a specific version

You can install a specific version of the plugin by downloading the zipped release [here](https://github.com/alxwstn/RAFTHeatmapMkr/releases) and install it as described [here](https://docs.qgis.org/3.40/en/docs/user_manual/plugins/plugins.html#the-install-from-zip-tab).
