/**
 * Board management JavaScript
 */

// Current board state
let currentBoardId = null;
let allBoards = [];

// Initialize boards on page load
async function initializeBoards() {
    await loadBoards();

    // Check if board ID is specified in URL query parameter
    const urlParams = new URLSearchParams(window.location.search);
    const urlBoardId = urlParams.get('id');

    if (urlBoardId && allBoards.find(b => b.id == urlBoardId)) {
        await switchToBoard(parseInt(urlBoardId));
    } else {
        // Load the current board (from localStorage or default)
        const savedBoardId = localStorage.getItem('current_board_id');
        if (savedBoardId && allBoards.find(b => b.id == savedBoardId)) {
            await switchToBoard(parseInt(savedBoardId));
        } else if (allBoards.length > 0) {
            // Switch to the first board (or default board)
            const defaultBoard = allBoards.find(b => b.is_default) || allBoards[0];
            await switchToBoard(defaultBoard.id);
        }
    }
}

// Load all boards for the current user
async function loadBoards() {
    try {
        const response = await fetch('/api/boards', {
            headers: getAuthHeaders()
        });

        if (response.ok) {
            allBoards = await response.json();
            renderBoardSelector();
        } else if (response.status === 401) {
            // Unauthorized - redirect to login
            window.location.href = '/';
        }
    } catch (error) {
        console.error('Error loading boards:', error);
    }
}

// Render the board selector dropdown
function renderBoardSelector() {
    const selector = document.getElementById('board-selector');
    if (!selector) return;

    selector.innerHTML = allBoards.map(board => `
        <option value="${board.id}" ${board.id === currentBoardId ? 'selected' : ''}>
            ${escapeHtml(board.name)} ${board.is_default ? '⭐' : ''}
        </option>
    `).join('');
}

// Switch to a different board
async function switchToBoard(boardId) {
    currentBoardId = boardId;
    localStorage.setItem('current_board_id', boardId);

    // Update the selector
    const selector = document.getElementById('board-selector');
    if (selector) {
        selector.value = boardId;
    }

    // Update the board name display
    const board = allBoards.find(b => b.id === boardId);
    if (board) {
        const boardNameDisplay = document.getElementById('current-board-name');
        if (boardNameDisplay) {
            boardNameDisplay.textContent = board.name;
        }
    }

    // Load cards for this board
    await loadCardsForCurrentBoard();
}

// Load cards for the current board
async function loadCardsForCurrentBoard() {
    if (!currentBoardId) return;

    htmx.trigger('#kanban-board', 'loadBoard');
}

// Handle board selector change
document.addEventListener('DOMContentLoaded', () => {
    const selector = document.getElementById('board-selector');
    if (selector) {
        selector.addEventListener('change', (e) => {
            switchToBoard(parseInt(e.target.value));
        });
    }
});

// Create a new board
async function createNewBoard() {
    const name = document.getElementById('newBoardName').value;
    const description = document.getElementById('newBoardDescription').value;
    const color = document.getElementById('newBoardColor').value;

    if (!name || name.trim().length === 0) {
        alert('Please enter a board name');
        return;
    }

    try {
        const response = await fetch('/api/boards', {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify({
                name: name.trim(),
                description: description.trim() || null,
                color: color,
                is_default: false
            })
        });

        if (response.ok) {
            const newBoard = await response.json();

            // Close modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('createBoardModal'));
            if (modal) modal.hide();

            // Clear form
            document.getElementById('createBoardForm').reset();

            // Reload boards and switch to the new board
            await loadBoards();
            await switchToBoard(newBoard.id);
        } else {
            const error = await response.json();
            alert('Failed to create board: ' + (error.detail || 'Unknown error'));
        }
    } catch (error) {
        console.error('Error creating board:', error);
        alert('Failed to create board');
    }
}

// Edit current board
async function editCurrentBoard() {
    if (!currentBoardId) return;

    const board = allBoards.find(b => b.id === currentBoardId);
    if (!board) return;

    // Populate edit form
    document.getElementById('editBoardId').value = board.id;
    document.getElementById('editBoardName').value = board.name;
    document.getElementById('editBoardDescription').value = board.description || '';
    document.getElementById('editBoardColor').value = board.color;
    document.getElementById('editBoardDefault').checked = board.is_default;

    // Show modal
    const modal = new bootstrap.Modal(document.getElementById('editBoardModal'));
    modal.show();
}

// Save board edits
async function saveBoard Edits() {
    const boardId = parseInt(document.getElementById('editBoardId').value);
    const name = document.getElementById('editBoardName').value;
    const description = document.getElementById('editBoardDescription').value;
    const color = document.getElementById('editBoardColor').value;
    const isDefault = document.getElementById('editBoardDefault').checked;

    if (!name || name.trim().length === 0) {
        alert('Please enter a board name');
        return;
    }

    try {
        const response = await fetch(`/api/boards/${boardId}`, {
            method: 'PUT',
            headers: getAuthHeaders(),
            body: JSON.stringify({
                name: name.trim(),
                description: description.trim() || null,
                color: color,
                is_default: isDefault
            })
        });

        if (response.ok) {
            // Close modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('editBoardModal'));
            if (modal) modal.hide();

            // Reload boards
            await loadBoards();
            await switchToBoard(boardId);
        } else {
            const error = await response.json();
            alert('Failed to update board: ' + (error.detail || 'Unknown error'));
        }
    } catch (error) {
        console.error('Error updating board:', error);
        alert('Failed to update board');
    }
}

// Delete current board
async function deleteCurrentBoard() {
    if (!currentBoardId) return;

    const board = allBoards.find(b => b.id === currentBoardId);
    if (!board) return;

    if (!confirm(`Are you sure you want to delete "${board.name}"? All cards in this board will be deleted.`)) {
        return;
    }

    try {
        const response = await fetch(`/api/boards/${currentBoardId}`, {
            method: 'DELETE',
            headers: getAuthHeaders()
        });

        if (response.ok) {
            // Close edit modal if open
            const modal = bootstrap.Modal.getInstance(document.getElementById('editBoardModal'));
            if (modal) modal.hide();

            // Reload boards and switch to first available
            await loadBoards();
            if (allBoards.length > 0) {
                const defaultBoard = allBoards.find(b => b.is_default) || allBoards[0];
                await switchToBoard(defaultBoard.id);
            }
        } else {
            const error = await response.json();
            alert('Failed to delete board: ' + (error.detail || 'Cannot delete last board'));
        }
    } catch (error) {
        console.error('Error deleting board:', error);
        alert('Failed to delete board');
    }
}

// Handle create board form submission
document.addEventListener('DOMContentLoaded', () => {
    const createForm = document.getElementById('createBoardForm');
    if (createForm) {
        createForm.addEventListener('submit', (e) => {
            e.preventDefault();
            createNewBoard();
        });
    }

    const editForm = document.getElementById('editBoardForm');
    if (editForm) {
        editForm.addEventListener('submit', (e) => {
            e.preventDefault();
            saveBoardEdits();
        });
    }
});
