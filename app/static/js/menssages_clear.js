// Script para remover automaticamente as mensagens flash após 3 segundos
setTimeout(function() {
    var alert = document.querySelector('.alert');
    if (alert) {
        alert.classList.remove('show');
        alert.classList.add('fade');
        setTimeout(function() {
            alert.remove();
        }, 150); // Tempo para a transição de fade out
    }
}, 3000); // 3000 milissegundos = 3 segundos