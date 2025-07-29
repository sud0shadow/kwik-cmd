#!/bin/bash

WIDGET_NAME="kwik-cmd"
BUILD_DIR="build"

echo "Building KDE Plasma Widget: $WIDGET_NAME"

# Clean previous build
rm -rf $BUILD_DIR
mkdir -p $BUILD_DIR/$WIDGET_NAME/contents/{ui,code}

# Copy metadata
cp metadata.desktop $BUILD_DIR/$WIDGET_NAME/

# Copy QML files
cp contents/ui/main.qml $BUILD_DIR/$WIDGET_NAME/contents/ui/

# Copy JavaScript files
cp contents/code/config_manager.js $BUILD_DIR/$WIDGET_NAME/contents/code/
cp contents/code/command_executor.js $BUILD_DIR/$WIDGET_NAME/contents/code/

# Copy config file template if it exists
if [ -f commands_config.json ]; then
    cp commands_config.json $BUILD_DIR/$WIDGET_NAME/
fi

# Create plasmoid package
cd $BUILD_DIR
zip -r ../$WIDGET_NAME.plasmoid $WIDGET_NAME/
cd ..

echo "Widget package created: $WIDGET_NAME.plasmoid"
echo ""
echo "To install:"
echo "  plasmapkg2 -i $WIDGET_NAME.plasmoid"
echo ""
echo "To uninstall previous version:"
echo "  plasmapkg2 -r kwik-cmd"
echo ""
echo "To install/upgrade:"
echo "  plasmapkg2 -u $WIDGET_NAME.plasmoid"