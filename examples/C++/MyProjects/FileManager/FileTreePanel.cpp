// FileTreePanel.cpp  (Part 2)

#include "FileTreePanel.h"

#include <QVBoxLayout>
#include <QHeaderView>
#include <QItemSelectionModel>
#include <QMenu>
#include <QAction>
#include <QMessageBox>
#include <QDir>
#include <QFile>
#include <QTimer>

FileTreePanel::FileTreePanel(QFileSystemModel* model, QWidget* parent)
    : QWidget(parent)
    , m_model(model)
{
    buildUI();
}

void FileTreePanel::buildUI()
{
    m_treeView = new QTreeView(this);
    m_treeView->setModel(m_model);

    m_treeView->hideColumn(1);
    m_treeView->hideColumn(2);
    m_treeView->hideColumn(3);
    m_treeView->header()->hide();
    m_treeView->setAnimated(true);
    m_treeView->setIndentation(16);
    m_treeView->setSortingEnabled(false);
    m_treeView->setUniformRowHeights(true);

    // Enable inline editing (Qt's built-in delegate)
    m_treeView->setEditTriggers(QAbstractItemView::EditKeyPressed);

    // Context menu
    m_treeView->setContextMenuPolicy(Qt::CustomContextMenu);
    connect(m_treeView, &QTreeView::customContextMenuRequested,
            this, &FileTreePanel::onContextMenu);

    const QModelIndex rootIndex = m_model->index(m_model->rootPath());
    m_treeView->setRootIndex(rootIndex);

    const QString homePath = QDir::homePath();
    const QModelIndex homeIndex = m_model->index(homePath);
    if (homeIndex.isValid()) {
        m_treeView->expand(homeIndex);
        m_treeView->setCurrentIndex(homeIndex);
        m_treeView->scrollTo(homeIndex);
    }

    connect(m_treeView->selectionModel(),
            &QItemSelectionModel::currentChanged,
            this, &FileTreePanel::onSelectionChanged);

    auto* layout = new QVBoxLayout(this);
    layout->setContentsMargins(0, 0, 0, 0);
    layout->addWidget(m_treeView);
    setLayout(layout);
}

// ─────────────────────────────────────────────────────────────────────────────
void FileTreePanel::onSelectionChanged(const QModelIndex& current,
                                       const QModelIndex& /*previous*/)
{
    if (!current.isValid()) return;
    if (m_model->fileInfo(current).isDir()) {
        emit folderSelected(current);
    }
}

// ─────────────────────────────────────────────────────────────────────────────
// Context menu
// ─────────────────────────────────────────────────────────────────────────────
void FileTreePanel::onContextMenu(const QPoint& pos)
{
    m_contextIndex = m_treeView->indexAt(pos);

    QMenu menu(this);

    auto* newFileAct   = menu.addAction(tr("New File"));
    auto* newFolderAct = menu.addAction(tr("New Folder"));
    menu.addSeparator();
    auto* renameAct    = menu.addAction(tr("Rename"));
    auto* deleteAct    = menu.addAction(tr("Delete"));

    // Rename/Delete only make sense on a real item
    renameAct->setEnabled(m_contextIndex.isValid());
    deleteAct->setEnabled(m_contextIndex.isValid());

    connect(newFileAct,   &QAction::triggered, this, &FileTreePanel::createNewFile);
    connect(newFolderAct, &QAction::triggered, this, &FileTreePanel::createNewFolder);
    connect(renameAct,    &QAction::triggered, this, &FileTreePanel::renameSelected);
    connect(deleteAct,    &QAction::triggered, this, &FileTreePanel::deleteSelected);

    menu.exec(m_treeView->viewport()->mapToGlobal(pos));
}

// ─────────────────────────────────────────────────────────────────────────────
// Create new file — puts a placeholder file in the target dir then
// triggers inline rename so the user can type the real name.
// ─────────────────────────────────────────────────────────────────────────────
void FileTreePanel::createNewFile()
{
    // Determine parent directory: if context was on a dir, use it; else use its parent
    QString parentPath;
    if (m_contextIndex.isValid()) {
        const QFileInfo fi = m_model->fileInfo(m_contextIndex);
        parentPath = fi.isDir() ? fi.absoluteFilePath()
                                : fi.absolutePath();
    } else {
        // Fall back to home
        parentPath = QDir::homePath();
    }

    // Create a unique placeholder name
    QDir dir(parentPath);
    QString name = QStringLiteral("New File");
    int counter  = 1;
    while (dir.exists(name)) {
        name = QStringLiteral("New File (%1)").arg(counter++);
    }

    QFile file(dir.filePath(name));
    if (!file.open(QIODevice::WriteOnly)) return;
    file.close();

    // Qt's model will pick up the new file via the filesystem watcher.
    // Give it a tick to populate, then start inline edit.
    QTimer::singleShot(100, this, [this, parentPath, name]() {
        const QModelIndex newIndex = m_model->index(QDir(parentPath).filePath(name));
        if (newIndex.isValid()) {
            m_treeView->setCurrentIndex(newIndex);
            startInlineEdit(newIndex);
        }
    });
}

// ─────────────────────────────────────────────────────────────────────────────
void FileTreePanel::createNewFolder()
{
    QString parentPath;
    if (m_contextIndex.isValid()) {
        const QFileInfo fi = m_model->fileInfo(m_contextIndex);
        parentPath = fi.isDir() ? fi.absoluteFilePath()
                                : fi.absolutePath();
    } else {
        parentPath = QDir::homePath();
    }

    QDir dir(parentPath);
    QString name   = QStringLiteral("New Folder");
    int counter    = 1;
    while (dir.exists(name)) {
        name = QStringLiteral("New Folder (%1)").arg(counter++);
    }

    if (!dir.mkdir(name)) return;

    QTimer::singleShot(100, this, [this, parentPath, name]() {
        const QModelIndex newIndex = m_model->index(QDir(parentPath).filePath(name));
        if (newIndex.isValid()) {
            m_treeView->expand(m_model->index(parentPath));
            m_treeView->setCurrentIndex(newIndex);
            startInlineEdit(newIndex);
        }
    });
}

// ─────────────────────────────────────────────────────────────────────────────
void FileTreePanel::renameSelected()
{
    if (m_contextIndex.isValid()) {
        startInlineEdit(m_contextIndex);
    }
}

// ─────────────────────────────────────────────────────────────────────────────
void FileTreePanel::deleteSelected()
{
    if (!m_contextIndex.isValid()) return;

    const QFileInfo fi = m_model->fileInfo(m_contextIndex);
    const QString   name = fi.fileName();

    const auto reply = QMessageBox::question(
        this,
        tr("Confirm Delete"),
        tr("Are you sure you want to delete \"%1\"?\nThis cannot be undone.").arg(name),
        QMessageBox::Yes | QMessageBox::No,
        QMessageBox::No);

    if (reply != QMessageBox::Yes) return;

    if (fi.isDir()) {
        QDir(fi.absoluteFilePath()).removeRecursively();
    } else {
        QFile::remove(fi.absoluteFilePath());
    }
}

// ─────────────────────────────────────────────────────────────────────────────
// Triggers Qt's built-in inline delegate editor on the given index.
// QFileSystemModel's flags() returns Qt::ItemIsEditable for the name column,
// so the default QStyledItemDelegate provides a QLineEdit inline edit.
// ─────────────────────────────────────────────────────────────────────────────
void FileTreePanel::startInlineEdit(const QModelIndex& index)
{
    if (!index.isValid()) return;
    m_treeView->setCurrentIndex(index);
    m_treeView->scrollTo(index);
    m_treeView->edit(index);
}
