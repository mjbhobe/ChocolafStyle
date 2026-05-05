// FileContentPanel.cpp

#include "FileContentPanel.h"

#include <QVBoxLayout>
#include <QHeaderView>
#include <QDir>
#include <QFile>
#include <QFileInfo>
#include <QMenu>
#include <QAction>
#include <QMessageBox>
#include <QTimer>

// ─── FolderFirstProxyModel ────────────────────────────────────────────────────
//
// Qt applies the sort order by negating lessThan's result for descending sorts.
// So to keep directories first in both directions we must flip our tie-break
// result when sortOrder() == Qt::DescendingOrder.
//
bool FolderFirstProxyModel::lessThan(const QModelIndex& left,
                                      const QModelIndex& right) const
{
    auto* fs = qobject_cast<QFileSystemModel*>(sourceModel());
    if (fs) {
        const bool ld = fs->isDir(left);
        const bool rd = fs->isDir(right);
        if (ld != rd) {
            // Ascending:  dir is "less" → return ld (true when left is dir).
            // Descending: Qt negates the result, so return !ld to compensate
            //             and still get dirs first.
            return sortOrder() == Qt::AscendingOrder ? ld : !ld;
        }
    }
    return QSortFilterProxyModel::lessThan(left, right);
}

// ─────────────────────────────────────────────────────────────────────────────
FileContentPanel::FileContentPanel(QFileSystemModel* model, QWidget* parent)
    : QWidget(parent)
    , m_model(model)
{
    buildUI();
}

// ─────────────────────────────────────────────────────────────────────────────
void FileContentPanel::buildUI()
{
    m_stack = new QStackedWidget(this);

    // Proxy model for the detail view (sorts dirs first on any column).
    m_proxyModel = new FolderFirstProxyModel(this);
    m_proxyModel->setSourceModel(m_model);
    m_proxyModel->setSortCaseSensitivity(Qt::CaseInsensitive);
    m_proxyModel->setDynamicSortFilter(true);

    // ── Icon view ─────────────────────────────────────────────────────────────
    m_iconView = new QListView(this);
    m_iconView->setModel(m_model);
    applyIconMode();
    m_iconView->setContextMenuPolicy(Qt::CustomContextMenu);
    m_stack->addWidget(m_iconView);

    // ── Tile view ─────────────────────────────────────────────────────────────
    m_tileView = new QListView(this);
    m_tileView->setModel(m_model);
    applyTileMode();
    m_tileView->setContextMenuPolicy(Qt::CustomContextMenu);
    m_stack->addWidget(m_tileView);

    // ── Detail view (uses proxy model so dirs always sort first) ──────────────
    m_detailView = new QTreeView(this);
    m_detailView->setModel(m_proxyModel);
    applyDetailsMode();
    m_detailView->setContextMenuPolicy(Qt::CustomContextMenu);
    m_stack->addWidget(m_detailView);

    // Wire context menus for all three views to the same slot.
    auto wireCtx = [this](QAbstractItemView* view) {
        connect(view, &QAbstractItemView::customContextMenuRequested,
                this, &FileContentPanel::onContextMenu);
    };
    wireCtx(m_iconView);
    wireCtx(m_tileView);
    wireCtx(m_detailView);

    auto* layout = new QVBoxLayout(this);
    layout->setContentsMargins(0, 0, 0, 0);
    layout->addWidget(m_stack);
    setLayout(layout);

    m_stack->setCurrentIndex(0);
}

// ─────────────────────────────────────────────────────────────────────────────
void FileContentPanel::applyIconMode()
{
    m_iconView->setViewMode(QListView::IconMode);
    m_iconView->setIconSize(QSize(48, 48));   // Medium — matches toolbar default
    m_iconView->setGridSize(QSize(90, 90));
    m_iconView->setWordWrap(true);
    m_iconView->setResizeMode(QListView::Adjust);
    m_iconView->setUniformItemSizes(true);
    m_iconView->setSpacing(4);
    m_iconView->setSelectionMode(QAbstractItemView::ExtendedSelection);
    m_iconView->setEditTriggers(QAbstractItemView::EditKeyPressed
                              | QAbstractItemView::SelectedClicked);
}

void FileContentPanel::applyTileMode()
{
    m_tileView->setViewMode(QListView::IconMode);
    m_tileView->setIconSize(QSize(32, 32));
    m_tileView->setGridSize(QSize(200, 48));
    m_tileView->setWordWrap(false);
    m_tileView->setResizeMode(QListView::Adjust);
    m_tileView->setUniformItemSizes(true);
    m_tileView->setSpacing(2);
    m_tileView->setFlow(QListView::LeftToRight);
    m_tileView->setWrapping(true);
    m_tileView->setSelectionMode(QAbstractItemView::ExtendedSelection);
    m_tileView->setEditTriggers(QAbstractItemView::EditKeyPressed
                              | QAbstractItemView::SelectedClicked);
}

void FileContentPanel::applyDetailsMode()
{
    m_detailView->setRootIsDecorated(false);
    m_detailView->setAlternatingRowColors(true);
    m_detailView->setSortingEnabled(true);
    m_detailView->sortByColumn(0, Qt::AscendingOrder);
    m_detailView->setSelectionMode(QAbstractItemView::ExtendedSelection);
    m_detailView->setIconSize(QSize(16, 16));
    m_detailView->setEditTriggers(QAbstractItemView::EditKeyPressed
                                | QAbstractItemView::SelectedClicked);

    // All columns are user-resizable (Interactive).
    // Column 0 (Name) gets the bulk of the space; the others have sane defaults.
    auto* hdr = m_detailView->header();
    hdr->setStretchLastSection(false);
    hdr->setSectionResizeMode(QHeaderView::Interactive);
    hdr->setMinimumSectionSize(50);
    hdr->resizeSection(0, 260);   // Name
    hdr->resizeSection(1,  80);   // Size
    hdr->resizeSection(2, 120);   // Type
    hdr->resizeSection(3, 150);   // Date Modified
}

// ─────────────────────────────────────────────────────────────────────────────
QAbstractItemView* FileContentPanel::activeView() const
{
    switch (m_viewMode) {
        case 1:  return m_tileView;
        case 2:  return m_detailView;
        default: return m_iconView;
    }
}

// ─────────────────────────────────────────────────────────────────────────────
void FileContentPanel::navigateTo(const QModelIndex& folderIndex)
{
    if (!folderIndex.isValid()) return;
    m_currentRoot = folderIndex;
    m_iconView->setRootIndex(folderIndex);
    m_tileView->setRootIndex(folderIndex);
    // Detail view is backed by the proxy model — map the source index.
    m_detailView->setRootIndex(m_proxyModel->mapFromSource(folderIndex));
}

void FileContentPanel::setViewMode(int mode)
{
    m_viewMode = mode;
    m_stack->setCurrentIndex(mode);
}

// ─────────────────────────────────────────────────────────────────────────────
// Icon sizes (icon view only):
//   0 = Small     32 × 32   grid 64 × 64
//   1 = Medium    48 × 48   grid 90 × 90   (default)
//   2 = Large     64 × 64   grid 110 × 110
//   3 = XLarge    96 × 96   grid 150 × 150
// ─────────────────────────────────────────────────────────────────────────────
void FileContentPanel::setIconSizePreset(int preset)
{
    struct Preset { QSize icon; QSize grid; };
    static const Preset presets[] = {
        { QSize(32, 32),  QSize(64,  64)  },
        { QSize(48, 48),  QSize(90,  90)  },
        { QSize(64, 64),  QSize(110, 110) },
        { QSize(96, 96),  QSize(150, 150) },
    };
    if (preset < 0 || preset > 3) return;
    m_iconView->setIconSize(presets[preset].icon);
    m_iconView->setGridSize(presets[preset].grid);
}

// ─────────────────────────────────────────────────────────────────────────────
// Context menu
// ─────────────────────────────────────────────────────────────────────────────
void FileContentPanel::onContextMenu(const QPoint& pos)
{
    QAbstractItemView* view = activeView();
    const QModelIndex viewIndex = view->indexAt(pos);

    // The detail view is backed by the proxy — map back to the source model.
    if (m_viewMode == 2 && viewIndex.isValid())
        m_contextIndex = m_proxyModel->mapToSource(viewIndex);
    else
        m_contextIndex = viewIndex;

    QMenu menu(this);
    auto* newFileAct   = menu.addAction(tr("New File"));
    auto* newFolderAct = menu.addAction(tr("New Folder"));
    menu.addSeparator();
    auto* renameAct = menu.addAction(tr("Rename"));
    auto* deleteAct = menu.addAction(tr("Delete"));

    renameAct->setEnabled(m_contextIndex.isValid());
    deleteAct->setEnabled(m_contextIndex.isValid());

    connect(newFileAct,   &QAction::triggered, this, &FileContentPanel::createNewFile);
    connect(newFolderAct, &QAction::triggered, this, &FileContentPanel::createNewFolder);
    connect(renameAct,    &QAction::triggered, this, &FileContentPanel::renameSelected);
    connect(deleteAct,    &QAction::triggered, this, &FileContentPanel::deleteSelected);

    menu.exec(view->viewport()->mapToGlobal(pos));
}

// ─────────────────────────────────────────────────────────────────────────────
void FileContentPanel::createNewFile()
{
    if (!m_currentRoot.isValid()) return;

    const QString parentPath = m_model->filePath(m_currentRoot);
    QDir dir(parentPath);

    QString name  = QStringLiteral("New File");
    int     count = 1;
    while (dir.exists(name))
        name = QStringLiteral("New File (%1)").arg(count++);

    QFile file(dir.filePath(name));
    if (!file.open(QIODevice::WriteOnly)) return;
    file.close();

    QTimer::singleShot(100, this, [this, parentPath, name]() {
        const QModelIndex idx = m_model->index(QDir(parentPath).filePath(name));
        if (idx.isValid())
            startInlineEdit(idx);
    });
}

// ─────────────────────────────────────────────────────────────────────────────
void FileContentPanel::createNewFolder()
{
    if (!m_currentRoot.isValid()) return;

    const QString parentPath = m_model->filePath(m_currentRoot);
    QDir dir(parentPath);

    QString name  = QStringLiteral("New Folder");
    int     count = 1;
    while (dir.exists(name))
        name = QStringLiteral("New Folder (%1)").arg(count++);

    if (!dir.mkdir(name)) return;

    QTimer::singleShot(100, this, [this, parentPath, name]() {
        const QModelIndex idx = m_model->index(QDir(parentPath).filePath(name));
        if (idx.isValid())
            startInlineEdit(idx);
    });
}

// ─────────────────────────────────────────────────────────────────────────────
void FileContentPanel::renameSelected()
{
    if (m_contextIndex.isValid())
        startInlineEdit(m_contextIndex);
}

// ─────────────────────────────────────────────────────────────────────────────
void FileContentPanel::deleteSelected()
{
    if (!m_contextIndex.isValid()) return;

    const QFileInfo fi   = m_model->fileInfo(m_contextIndex);
    const QString   name = fi.fileName();

    const auto reply = QMessageBox::question(
        this,
        tr("Confirm Delete"),
        tr("Are you sure you want to delete \"%1\"?\nThis cannot be undone.").arg(name),
        QMessageBox::Yes | QMessageBox::No,
        QMessageBox::No);

    if (reply != QMessageBox::Yes) return;

    if (fi.isDir())
        QDir(fi.absoluteFilePath()).removeRecursively();
    else
        QFile::remove(fi.absoluteFilePath());
}

// ─────────────────────────────────────────────────────────────────────────────
// sourceIndex is always an index into m_model (never a proxy index).
// The method maps it to the appropriate view index before editing.
// ─────────────────────────────────────────────────────────────────────────────
void FileContentPanel::startInlineEdit(const QModelIndex& sourceIndex)
{
    if (!sourceIndex.isValid()) return;

    QAbstractItemView* view = activeView();

    // Map to the view's own model index (proxy for detail view, direct otherwise).
    const QModelIndex viewIndex = (m_viewMode == 2)
        ? m_proxyModel->mapFromSource(sourceIndex)
        : sourceIndex;

    if (!viewIndex.isValid()) return;
    view->setCurrentIndex(viewIndex);
    view->scrollTo(viewIndex);
    view->edit(viewIndex);
}