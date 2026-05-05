// MainWindow.h
// Top-level application window — owns the splitter, toolbar, and both panels.

#pragma once

#include <QMainWindow>
#include <QSplitter>
#include <QFileSystemModel>
#include <QLabel>

#include "FileTreePanel.h"
#include "FileContentPanel.h"
#include "ViewToolBar.h"

class MainWindow final : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget* parent = nullptr);
    ~MainWindow() override = default;

private slots:
    // Called when the user selects a folder in the left tree
    void onTreeFolderSelected(const QModelIndex& index);

    // Called when the view-mode toolbar buttons are clicked
    void onViewModeChanged(int mode);

private:
    void buildUI();
    void buildMenuBar();
    void buildStatusBar();

    // ── Shared model ─────────────────────────────────────────────────────────
    // Both panels use the same QFileSystemModel so the OS does one stat pass.
    QFileSystemModel* m_fsModel{nullptr};

    // ── Layout ───────────────────────────────────────────────────────────────
    QSplitter*        m_splitter{nullptr};
    FileTreePanel*    m_treePanel{nullptr};
    FileContentPanel* m_contentPanel{nullptr};
    ViewToolBar*      m_viewToolBar{nullptr};

    // ── Status bar helpers ───────────────────────────────────────────────────
    QLabel*           m_statusLabel{nullptr};
};
