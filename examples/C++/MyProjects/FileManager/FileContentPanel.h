// FileContentPanel.h
// Right panel: shows folder contents in three switchable view modes.
// Right-click: New File | New Folder | Rename | Delete
//
// Details view uses FolderFirstProxyModel so that directories always sort
// before files regardless of which column header the user clicks.

#pragma once

#include <QWidget>
#include <QStackedWidget>
#include <QListView>
#include <QTreeView>
#include <QFileSystemModel>
#include <QPoint>
#include <QSortFilterProxyModel>

// ─── Proxy model: directories always appear before files ──────────────────────
class FolderFirstProxyModel final : public QSortFilterProxyModel
{
    Q_OBJECT
public:
    explicit FolderFirstProxyModel(QObject* parent = nullptr)
        : QSortFilterProxyModel(parent) {}

protected:
    // Overridden so that directories sort before regular files for both
    // ascending and descending column-header clicks.
    bool lessThan(const QModelIndex& left, const QModelIndex& right) const override;
};

// ─────────────────────────────────────────────────────────────────────────────
class FileContentPanel final : public QWidget
{
    Q_OBJECT

public:
    explicit FileContentPanel(QFileSystemModel* model, QWidget* parent = nullptr);

    void navigateTo(const QModelIndex& folderIndex);
    void setViewMode(int mode);

    // Slot: change icon size in the Icon view.
    // preset: 0=Small(32px), 1=Medium(48px), 2=Large(64px), 3=XLarge(96px)
    void setIconSizePreset(int preset);

private slots:
    void onContextMenu(const QPoint& pos);
    void createNewFile();
    void createNewFolder();
    void renameSelected();
    void deleteSelected();

private:
    void buildUI();
    void applyIconMode();
    void applyTileMode();
    void applyDetailsMode();

    // sourceIndex is always an index into m_model (never proxy).
    void startInlineEdit(const QModelIndex& sourceIndex);

    // Returns the currently visible view widget.
    QAbstractItemView* activeView() const;

    QFileSystemModel*      m_model{nullptr};
    FolderFirstProxyModel* m_proxyModel{nullptr};  // wraps m_model for detail view
    QStackedWidget*        m_stack{nullptr};
    QListView*             m_iconView{nullptr};
    QListView*             m_tileView{nullptr};
    QTreeView*             m_detailView{nullptr};
    QModelIndex            m_currentRoot{};
    QModelIndex            m_contextIndex{};  // always a source-model index
    int                    m_viewMode{0};
};