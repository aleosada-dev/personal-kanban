// Card Management Functions

// Edit a card
async function editCard(cardId) {
    try {
        const response = await fetch(`/api/cards`);
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
        });

        if (response.ok) {
            htmx.trigger('#kanban-board', 'cardUpdated');
        } else {
            alert('Failed to delete card');
        }
    } catch (error) {
        console.error('Error deleting card:', error);
        alert('Failed to delete card');
    }
}

// Handle edit form submission
document.getElementById('editCardForm').addEventListener('submit', async (e) => {
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
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData),
        });

        if (response.ok) {
            bootstrap.Modal.getInstance(document.getElementById('editCardModal')).hide();
            htmx.trigger('#kanban-board', 'cardUpdated');
        } else {
            alert('Failed to update card');
        }
    } catch (error) {
        console.error('Error updating card:', error);
        alert('Failed to update card');
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
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ status: newStatus }),
        });

        if (response.ok) {
            htmx.trigger('#kanban-board', 'cardUpdated');
        }
    } catch (error) {
        console.error('Error updating card status:', error);
    }

    draggedCard = null;
});

// Make cards draggable
document.addEventListener('htmx:afterSwap', () => {
    document.querySelectorAll('.kanban-card').forEach(card => {
        card.setAttribute('draggable', 'true');
    });
});

// Handle htmx form submission with JSON encoding
htmx.defineExtension('json-enc', {
    onEvent: function (name, evt) {
        if (name === "htmx:configRequest") {
            evt.detail.headers['Content-Type'] = "application/json";
        }
    },
    encodeParameters: function (xhr, parameters, elt) {
        xhr.overrideMimeType('application/json');
        const formData = {};
        for (const [key, value] of Object.entries(parameters)) {
            formData[key] = value;
        }
        return JSON.stringify(formData);
    }
});
