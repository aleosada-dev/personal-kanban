// Authentication Helper Functions

// Get authentication token from localStorage
function getAuthToken() {
    return localStorage.getItem('access_token');
}

// Get authorization headers
function getAuthHeaders() {
    const token = getAuthToken();
    return {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
    };
}

// Check if user is authenticated and redirect if not
function checkAuth() {
    const token = getAuthToken();
    if (!token) {
        window.location.href = '/';
        return false;
    }
    return true;
}

// Logout function
function logout() {
    localStorage.removeItem('access_token');
    window.location.href = '/';
}

// Check authentication on page load
if (!checkAuth()) {
    // Will redirect if not authenticated
}

// Card Management Functions

// Edit a card
async function editCard(cardId) {
    if (!currentBoardId) {
        alert('No board selected');
        return;
    }

    try {
        const response = await fetch(`/api/boards/${currentBoardId}/cards`, {
            headers: getAuthHeaders()
        });
        const cards = await response.json();
        const card = cards.find(c => c.id === cardId);

        if (!card) {
            alert('Card not found');
            return;
        }

        // Populate edit form
        document.getElementById('editCardId').value = card.id;
        document.getElementById('editCardTitle').value = card.title;
        document.getElementById('editCardDescription').value = card.description || '';
        document.getElementById('editCardStatus').value = card.status;
        document.getElementById('editCardPriority').value = card.priority;

        // Show modal
        const modal = new bootstrap.Modal(document.getElementById('editCardModal'));
        modal.show();
    } catch (error) {
        console.error('Error fetching card:', error);
        alert('Failed to load card details');
    }
}

// Delete a card
async function deleteCard(cardId) {
    if (!confirm('Are you sure you want to delete this card?')) {
        return;
    }

    try {
        const response = await fetch(`/api/cards/${cardId}`, {
            method: 'DELETE',
            headers: getAuthHeaders()
        });

        if (response.ok) {
            await loadCardsForCurrentBoard();
        } else {
            alert('Failed to delete card');
        }
    } catch (error) {
        console.error('Error deleting card:', error);
        alert('Failed to delete card');
    }
}

// Handle add card form submission
document.addEventListener('DOMContentLoaded', () => {
    const addForm = document.getElementById('addCardForm');
    if (addForm) {
        addForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            if (!currentBoardId) {
                alert('No board selected');
                return;
            }

            const formData = {
                title: document.getElementById('cardTitle').value,
                description: document.getElementById('cardDescription').value,
                status: 'todo',  // Default to "To Do" status
                priority: parseInt(document.getElementById('cardPriority').value),
            };

            try {
                const response = await fetch(`/api/boards/${currentBoardId}/cards`, {
                    method: 'POST',
                    headers: getAuthHeaders(),
                    body: JSON.stringify(formData),
                });

                if (response.ok) {
                    bootstrap.Modal.getInstance(document.getElementById('addCardModal')).hide();
                    document.getElementById('addCardForm').reset();
                    await loadCardsForCurrentBoard();
                } else {
                    alert('Failed to create card');
                }
            } catch (error) {
                console.error('Error creating card:', error);
                alert('Failed to create card');
            }
        });
    }

    // Handle edit card form submission
    const editForm = document.getElementById('editCardForm');
    if (editForm) {
        editForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const cardId = document.getElementById('editCardId').value;
            const formData = {
                title: document.getElementById('editCardTitle').value,
                description: document.getElementById('editCardDescription').value,
                status: document.getElementById('editCardStatus').value,
                priority: parseInt(document.getElementById('editCardPriority').value),
            };

            try {
                const response = await fetch(`/api/cards/${cardId}`, {
                    method: 'PUT',
                    headers: getAuthHeaders(),
                    body: JSON.stringify(formData),
                });

                if (response.ok) {
                    bootstrap.Modal.getInstance(document.getElementById('editCardModal')).hide();
                    await loadCardsForCurrentBoard();
                } else {
                    alert('Failed to update card');
                }
            } catch (error) {
                console.error('Error updating card:', error);
                alert('Failed to update card');
            }
        });
    }
});

// Drag and drop functionality (optional enhancement)
let draggedCard = null;

document.addEventListener('dragstart', (e) => {
    if (e.target.classList.contains('kanban-card')) {
        draggedCard = e.target;
        e.target.style.opacity = '0.5';
    }
});

document.addEventListener('dragend', (e) => {
    if (e.target.classList.contains('kanban-card')) {
        e.target.style.opacity = '1';
    }
});

document.addEventListener('dragover', (e) => {
    e.preventDefault();
});

document.addEventListener('drop', async (e) => {
    e.preventDefault();

    if (!draggedCard) return;

    const dropZone = e.target.closest('.kanban-cards');
    if (!dropZone) return;

    const columnId = dropZone.id;
    const newStatus = columnId.replace('column-', '');
    const cardId = draggedCard.dataset.cardId;

    try {
        const response = await fetch(`/api/cards/${cardId}`, {
            method: 'PUT',
            headers: getAuthHeaders(),
            body: JSON.stringify({ status: newStatus }),
        });

        if (response.ok) {
            await loadCardsForCurrentBoard();
        }
    } catch (error) {
        console.error('Error updating card status:', error);
    }

    draggedCard = null;
});
