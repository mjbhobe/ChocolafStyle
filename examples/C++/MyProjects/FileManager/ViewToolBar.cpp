// ViewToolBar.cpp

#include "ViewToolBar.h"

#include <QAction>
#include <QIcon>
#include <QStyle>
#include <QApplication>
#include <QWidget>
#include <QHBoxLayout>
#include <QLabel>

ViewToolBar::ViewToolBar(QWidget* parent)
    : QToolBar(tr("View"), parent)
{
    setMovable(false);
    setFloatable(false);
    // Text-under-icon with 22 px icons gives a clean, Windows-toolbar look
    // (much less button-like than TextBesideIcon).
    setIconSize(QSize(22, 22));
    setToolButtonStyle(Qt::ToolButtonTextUnderIcon);
    buildActions();
}

void ViewToolBar::buildActions()
{
    m_modeGroup = new QActionGroup(this);
    m_modeGroup->setExclusive(true);

    auto* style = QApplication::style();

    // ── Icons mode ────────────────────────────────────────────────────────────
    auto* iconAct = new QAction(
        style->standardIcon(QStyle::SP_FileDialogListView),
        tr("Icons"), this);
    iconAct->setCheckable(true);
    iconAct->setChecked(true);
    iconAct->setData(0);
    iconAct->setToolTip(tr("Show items as icons (Ctrl+1)"));
    m_modeGroup->addAction(iconAct);
    addAction(iconAct);

    // ── Tiles mode ────────────────────────────────────────────────────────────
    auto* tileAct = new QAction(
        style->standardIcon(QStyle::SP_FileDialogContentsView),
        tr("Tiles"), this);
    tileAct->setCheckable(true);
    tileAct->setData(1);
    tileAct->setToolTip(tr("Show items as tiles (Ctrl+2)"));
    m_modeGroup->addAction(tileAct);
    addAction(tileAct);

    // ── Details mode ──────────────────────────────────────────────────────────
    auto* detailAct = new QAction(
        style->standardIcon(QStyle::SP_FileDialogDetailedView),
        tr("Details"), this);
    detailAct->setCheckable(true);
    detailAct->setData(2);
    detailAct->setToolTip(tr("Show detailed file information (Ctrl+3)"));
    m_modeGroup->addAction(detailAct);
    addAction(detailAct);

    // ── Emit on toggle, and keep icon-size widget in sync ─────────────────────
    connect(m_modeGroup, &QActionGroup::triggered, this, [this](QAction* act) {
        const int mode = act->data().toInt();
        setActiveMode(mode);
        emit viewModeChanged(mode);
    });

    // ── Icon-size controls (separator + label + combo) ────────────────────────
    // Visible only when Icons mode is active.
    m_iconSizeSep = addSeparator();

    auto* container = new QWidget(this);
    auto* hlay      = new QHBoxLayout(container);
    hlay->setContentsMargins(6, 0, 6, 0);
    hlay->setSpacing(4);

    hlay->addWidget(new QLabel(tr("Icon size:"), container));

    m_iconSizeCombo = new QComboBox(container);
    m_iconSizeCombo->addItem(tr("Small"));
    m_iconSizeCombo->addItem(tr("Medium"));
    m_iconSizeCombo->addItem(tr("Large"));
    m_iconSizeCombo->addItem(tr("Extra Large"));
    m_iconSizeCombo->setCurrentIndex(1);   // Medium by default
    m_iconSizeCombo->setToolTip(tr("Change icon size in Icon view"));
    hlay->addWidget(m_iconSizeCombo);

    m_iconSizeWidgetAction = addWidget(container);

    connect(m_iconSizeCombo, &QComboBox::currentIndexChanged,
            this, [this](int idx) { emit iconSizePresetChanged(idx); });

    // Initial state: Icons mode is active, so icon-size controls are visible.
    setActiveMode(0);
}

// ─────────────────────────────────────────────────────────────────────────────
void ViewToolBar::setActiveMode(int mode)
{
    const bool show = (mode == 0);   // icon-size only makes sense for Icon view
    if (m_iconSizeSep)          m_iconSizeSep->setVisible(show);
    if (m_iconSizeWidgetAction) m_iconSizeWidgetAction->setVisible(show);
}