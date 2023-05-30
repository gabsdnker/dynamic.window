// Arquivo edit_table.js

// Espera que o documento HTML esteja completamente carregado antes de executar qualquer código JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Adiciona um ouvinte de evento para o botão de adicionar linha
    var addRowBtn = document.getElementById('add-row-btn');
    if (addRowBtn) {
      addRowBtn.addEventListener('click', function(event) {
        event.preventDefault(); // Impede o comportamento padrão do botão de envio do formulário
  
        // Obtém o formulário pai do botão
        var form = addRowBtn.closest('form');
        if (form) {
          form.submit(); // Submete o formulário para a rota 'add_row'
        }
      });
    }
  });
  