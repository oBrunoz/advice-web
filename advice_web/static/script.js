function refreshDiv() {
    $.ajax({
        url: '/get_new_advice',
        type: 'POST',
        success: function (data) {
            try {
                // Atualize o conteúdo da div com o novo conteúdo do servidor
                console.log(data.advice)
                $('#advice__response').html(data.advice['advice']);

                // Atualize o valor do input com o novo advice
                $('#btn__fav').val(data.advice);

                // Atualize o atributo "action" do formulário com o novo valor do "advice"
                var newAction = '/checkFav/' + data.advice['id'];
                $('#favoriteForm').attr('action', newAction);
                $('#btn__fav').submit();

                // $.ajax({
                //     url: '/',
                //     type: 'POST',
                //     data: { advice: data.advice['id'] },
                //     success: function (res) {
                //         console.log(res)
                //     },
                //     error: function (xhr, status, error) {
                //         console.error(error)
                //     }
                // })
            } catch (err) {
                console.log(err)
            }
        },
        error: function (xhr, status, error) {
            console.error(error);
        }
    });
}

$(document).ready(function () {
    // Adiciona o evento de clique ao ícone de fechar
    $(".error__close, .success__close, .info__close").click(function () {
        // Esconde o elemento .error quando o ícone de fechar é clicado
        $("#message-all").hide();
    });
});

$(function() {
    $(window).on("load", function() {
        appear('"spinner__load"')
        $(".spinner__load").fadeOut("slow");
        hide("spinner__load")
    });
});