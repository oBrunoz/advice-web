function refreshDiv() {
    $.ajax({
        url: '/get_new_advice',
        type: 'POST',
        success: function(data) {
            try {
            // Atualize o conteúdo da div com o novo conteúdo do servidor
            console.log(data.advice)
            $('#advice__response').html(data.advice);
            } catch(err) {
                console.log(err)
            }
        },
        error: function(xhr, status, error) {
            console.error(error);
        }
    });
}

$(document).ready(function() {
    // Adiciona o evento de clique ao ícone de fechar
    $(".error__close, .success__close").click(function() {
        // Esconde o elemento .error quando o ícone de fechar é clicado
        $("#message-all").hide();
    });
});