// MainWindow.cpp

#include "MainWindow.h"

#include <QApplication>
#include <QMenuBar>
#include <QStatusBar>
#include <QVBoxLayout>
#include <QWidget>
#include <QDir>
#include <QStorageInfo>

MainWindow::MainWindow(QWidget* parent)
    : QMainWindow(parent)
{
    setWindowTitle(tr("Qt File Manager"));
    resize(1100, 680);

    buildUI();
    buildMenuBar();
    buildStatusBar();
}

// ─────────────────────────────────────────────────────────────────────────────
// buildUI
// Creates the central widget: [ViewToolBar on top] + [splitter below].
// Splitter ratio ≈ 1/3 : 2/3 set via initial sizes after show().
// ─────────────────────────────────────────────────────────────────────────────
void MainWindow::buildUI()
{
    // ── Shared filesystem model ───────────────────────────────────────────────
    m_fsModel = new QFileSystemModel(this);
    m_fsModel->setRootPath(QString{}); // Load entire filesystem lazily
    // Show hidden files: off by default (toggle later via menu)
    m_fsModel->setFilter(QDir::AllDirs | QDir::Files | QDir::NoDotAndDotDot);

    // ── Panels ────────────────────────────────────────────────────────────────
    m_treePanel    = new FileTreePanel(m_fsModel, this);
    m_contentPanel = new FileContentPanel(m_fsModel, this);

    // ── ViewToolBar ───────────────────────────────────────────────────────────
    m_viewToolBar = new ViewToolBar(this);
    addToolBar(Qt::TopToolBarArea, m_viewToolBar);

    // ── Splitter ──────────────────────────────────────────────────────────────
    m_splitter = new QSplitter(Qt::Horizontal, this);
    m_splitter->addWidget(m_treePanel);
    m_splitter->addWidget(m_contentPanel);
    // 1:2 ratio approximation — refined in showEvent via actual width
    m_splitter->setSizes({300, 700});
    m_splitter->setChildrenCollapsible(false);

    setCentralWidget(m_splitter);

    // ── Wire signals ──────────────────────────────────────────────────────────
    connect(m_treePanel, &FileTreePanel::folderSelected,
            this, &MainWindow::onTreeFolderSelected);

    connect(m_viewToolBar, &ViewToolBar::viewModeChanged,
            this, &MainWindow::onViewModeChanged);

    connect(m_viewToolBar, &ViewToolBar::iconSizePresetChanged,
            m_contentPanel, &FileContentPanel::setIconSizePreset);
}

// ─────────────────────────────────────────────────────────────────────────────
void MainWindow::buildMenuBar()
{
    auto* fileMenu = menuBar()->addMenu(tr("&File"));
    fileMenu->addAction(tr("&Quit"), qApp, &QApplication::quit, QKeySequence::Quit);

    auto* viewMenu = menuBar()->addMenu(tr("&View"));
    auto* showHiddenAct = viewMenu->addAction(tr("Show &Hidden Files"));
    showHiddenAct->setCheckable(true);
    connect(showHiddenAct, &QAction::toggled, this, [this](bool checked) {
        auto flags = QDir::AllDirs | QDir::Files | QDir::NoDotAndDotDot;
        if (checked) flags |= QDir::Hidden;
        m_fsModel->setFilter(flags);
    });
}

// ─────────────────────────────────────────────────────────────────────────────
void MainWindow::buildStatusBar()
{
    m_statusLabel = new QLabel(tr("Ready"), this);
    statusBar()->addWidget(m_statusLabel, 1);
}

// ─────────────────────────────────────────────────────────────────────────────
// Slots
// ─────────────────────────────────────────────────────────────────────────────
void MainWindow::onTreeFolderSelected(const QModelIndex& index)
{
    m_contentPanel->navigateTo(index);

    const QString path = m_fsModel->filePath(index);
    m_statusLabel->setText(path);
}

void MainWindow::onViewModeChanged(int mode)
{
    m_contentPanel->setViewMode(mode);
}
