function addCampo() {
    var form = document.querySelector('form[action="/cadastrar"]');
    var campo = document.createElement('input');
    campo.type = 'text';
    campo.name = 'campo';
    campo.placeholder = 'Nome do campo';
    var valor = document.createElement('input');
    valor.type = 'text';
    valor.name = 'valor';
    valor.placeholder = 'Valor do campo';
    var botao = document.createElement('button');
    botao.type = 'button';
    botao.innerText = '-';
    botao.onclick = function() {
        form.removeChild(campo);
        form.removeChild(valor);
        form.removeChild(botao);
    }
    form.insertBefore(campo, form.lastElementChild);
    form.insertBefore(valor, form.lastElementChild);
    form.insertBefore(botao, form.lastElementChild);
}

