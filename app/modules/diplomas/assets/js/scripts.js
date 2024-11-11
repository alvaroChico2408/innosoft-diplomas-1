// Obtener los IDs de los diplomas seleccionados
function getSelectedDiplomaIds() {
    const checkboxes = document.querySelectorAll('.send-checkbox:checked');
    const selectedIds = Array.from(checkboxes).map(checkbox => checkbox.getAttribute('data-id'));
    return selectedIds;
}

// Enviar diplomas seleccionados al backend
function sendSelectedDiplomas() {
    const selectedIds = getSelectedDiplomaIds();

    if (selectedIds.length === 0) {
        alert("Please select at least one diploma to send.");
        return;
    }

    fetch('/diplomas/send_diplomas', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ diploma_ids: selectedIds })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message);
            location.reload(); // Recargar la página para actualizar el estado de los diplomas
        } else {
            alert(data.message);
        }
    })
    .catch(error => {
        console.error("Error sending diplomas:", error);
        alert("An error occurred while sending diplomas.");
    });
}

// Seleccionar todos los checkboxes
function selectAll() {
    const checkboxes = document.querySelectorAll('.send-checkbox');
    checkboxes.forEach(checkbox => checkbox.checked = true);
}

// Deseleccionar todos los checkboxes
function deselectAll() {
    const checkboxes = document.querySelectorAll('.send-checkbox');
    checkboxes.forEach(checkbox => checkbox.checked = false);
}

// Filtro por UVUS
function filterByUVUS() {
    const filterValue = document.getElementById('uvusFilter').value.toLowerCase().trim();
    const rows = document.querySelectorAll('#diplomaTableBody tr');
    
    rows.forEach(row => {
        const uvusCell = row.cells[4]; // Columna de UVUS
        if (uvusCell) {
            const uvusText = uvusCell.textContent.toLowerCase().trim();
            // Mostrar solo las filas que coinciden con el filtro de UVUS
            row.style.display = uvusText.includes(filterValue) ? '' : 'none';
        }
    });
}

// Restablecer filtro por UVUS
function resetFilters() {
    document.getElementById('uvusFilter').value = ''; 
    const rows = document.querySelectorAll('#diplomaTableBody tr');
    rows.forEach(row => {
        row.style.display = ''; // Mostrar todas las filas
    });
}

// Filtro por Participación
function filterByParticipation(participation) {
    const rows = document.querySelectorAll('#diplomaTableBody tr');
    rows.forEach(row => {
        const participationCell = row.cells[5]; // Columna de Participación
        if (participationCell) {
            const participationText = participationCell.textContent.trim();
            // Mostrar solo las filas que coinciden con la participación seleccionada
            row.style.display = participationText === participation ? '' : 'none';
        }
    });
}

// Restablecer filtro por Participación
function resetParticipationFilter() {
    const rows = document.querySelectorAll('#diplomaTableBody tr');
    rows.forEach(row => {
        row.style.display = '';   // Mostrar todas las filas
    });
}
