// ViewToolBar.h
// Toolbar with three mutually-exclusive view-mode buttons: Icons | Tiles | Details
// plus an Icon Size combo box (visible only in Icons mode).
//
// Signals:
//   viewModeChanged(int mode)       — 0=Icons, 1=Tiles, 2=Details
//   iconSizePresetChanged(int preset) — 0=Small, 1=Medium, 2=Large, 3=XLarge

#pragma once

#include <QToolBar>
#include <QActionGroup>
#include <QComboBox>

class ViewToolBar final : public QToolBar
{
    Q_OBJECT

public:
    explicit ViewToolBar(QWidget* parent = nullptr);

    // Synchronises toolbar state (hides/shows icon-size widget) with the
    // current view mode.  Called automatically on user interaction; call
    // manually if the mode is changed from outside.
    void setActiveMode(int mode);

signals:
    void viewModeChanged(int mode);
    void iconSizePresetChanged(int preset); // 0=Small,1=Medium,2=Large,3=XLarge

private:
    void buildActions();

    QActionGroup* m_modeGroup{nullptr};
    QAction*      m_iconSizeSep{nullptr};          // separator before icon-size widget
    QAction*      m_iconSizeWidgetAction{nullptr};  // wrapper action for the widget
    QComboBox*    m_iconSizeCombo{nullptr};
};