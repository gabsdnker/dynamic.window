document.addEventListener('DOMContentLoaded', function() {
    const addRowBtn = document.getElementById('add-row-btn');
    addRowBtn.addEventListener('click', function() {
        const tableId = "{{ table.id }}";
        fetch(`/add_row/${tableId}`, {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            const tbody = document.querySelector('.edit-table tbody');
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${data.rowNumber}</td>
                ${data.columns.map(column => `
                    <td>
                        <form action="{{ url_for('edit_cell', table_id=table.id, column_id=column.id, row_id=data.rowId) }}" method="POST">
                            <input type="text" name="value" placeholder="Novo elemento" required>
                            <button type="submit">Salvar</button>
                        </form>
                    </td>
                `).join('')}
                <td>
                    <form action="{{ url_for('add_cell', table_id=table.id, row_id=data.rowId) }}" method="POST">
                        <input type="text" name="value" placeholder="Novo elemento" required>
                        <button type="submit">Adicionar</button>
                    </form>
                </td>
            `;
            tbody.appendChild(row);
        })
        .catch(error => console.log(error));
    });
});