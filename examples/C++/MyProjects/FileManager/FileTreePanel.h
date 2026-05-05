// FileTreePanel.h  (Part 2 — context menus + inline editing)
// Left panel: QTreeView showing the full folder hierarchy.
// Emits folderSelected(QModelIndex) when the user clicks a directory.
// Right-click menu: New File | New Folder | Rename | Delete

#pragma once

#include <QWidget>
#include <QTreeView>
#include <QFileSystemModel>
#include <QPoint>

class FileTreePanel final : public QWidget
{
    Q_OBJECT

public:
    explicit FileTreePanel(QFileSystemModel* model, QWidget* parent = nullptr);

signals:
    void folderSelected(const QModelIndex& index);

private slots:
    void onSelectionChanged(const QModelIndex& current, const QModelIndex& previous);
    void onContextMenu(const QPoint& pos);

    void createNewFile();
    void createNewFolder();
    void renameSelected();
    void deleteSelected();

private:
    void buildUI();
    void startInlineEdit(const QModelIndex& index);

    QFileSystemModel* m_model{nullptr};
    QTreeView*        m_treeView{nullptr};
    QModelIndex       m_contextIndex{};
};
