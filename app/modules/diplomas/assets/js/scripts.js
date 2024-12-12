// Función para obtener los IDs de los diplomas seleccionados
function getSelectedDiplomas() {
    const selectedDiplomas = [];
    document.querySelectorAll('.send-checkbox:checked').forEach(checkbox => {
        // Obtener el ID desde la primera columna de la fila
        selectedDiplomas.push(checkbox.closest('tr').querySelector('td:first-child').textContent.trim());
    });
    return selectedDiplomas;
}


// Función para enviar los diplomas seleccionados
function sendSelectedDiplomas() {
    const selectedDiplomas = getSelectedDiplomas();

    if (selectedDiplomas.length === 0) {
        alert("Please select at least one diploma.");
        return;
    }

    if (!confirm(`Are you sure you want to send ${selectedDiplomas.length} diplomas?`)) {
        return;
    }

    // Mostrar en consola los diplomas seleccionados para debug
    console.log("Selected diplomas: ", selectedDiplomas);

    fetch('/send_diplomas', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token() }}'
        },
        body: JSON.stringify({ diploma_ids: selectedDiplomas })
    })
    .then(response => response.text())  // Cambiar a `response.text()` ya que el backend usa `flash`
    .then(data => {
        // Aquí gestionamos la respuesta
        alert(data);  // Se asume que el servidor enviará un mensaje de éxito o error con `flash`
        location.reload(); // Recargamos la página para reflejar los cambios
    })
    .catch(error => {
        console.error('Error:', error);
        alert("There was an error sending diplomas.");
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


// Manejo de eliminación de múltiples diplomas
function handleDeleteSelected(event) {
    if (confirm('Are you sure you want to delete the selected diplomas?')) {
        const selectedDiplomas = [];
        document.querySelectorAll('.send-checkbox:checked').forEach(checkbox => {
            const diplomaIdCell = checkbox.closest('tr').querySelector('td:first-child');
            if (diplomaIdCell) {
                selectedDiplomas.push(diplomaIdCell.textContent.trim());
            }
        });

        if (selectedDiplomas.length === 0) {
            event.preventDefault(); // Detener envío del formulario
            alert("Please select at least one diploma to delete.");
            return false;
        }

        // Colocar los IDs en el campo oculto
        document.getElementById('diplomaIdsInput').value = JSON.stringify(selectedDiplomas);
        return true; // Permitir el envío del formulario
    }
}