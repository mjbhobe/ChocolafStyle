import QtQuick 2.3
import QtQuick.Window 2.3
import QtQuick.Controls 2.5

ApplicationWindow {
    width: 360
    height: 720
    visible: true
    title: qsTr("Task-Master")

    StackView {
        id: contentFrame
        anchors.fill: parent
        initialItem: Qt.resolvedUrl("LoadPage.qml")
    }
}
