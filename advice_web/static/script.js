function refreshDiv() {
    $.ajax({
        url: '/get_new_advice',
        type: 'POST',
        success: function (data) {
            try {
                // Atualize o conteúdo da div com o novo conteúdo do servidor
                console.log(data.advice)
                $('.advice-details').html(data.advice['advice']);
                $('.id__advice').html(data.advice['id']);

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

var loader = document.querySelector(".spinner__load");

$(document).ready(function () {
    // Adiciona o evento de clique ao ícone de fechar
    $(".msg__close").click(function () {
        // Esconde o elemento .error quando o ícone de fechar é clicado
        $("#message-all").hide();
    });
});

$(window).on("beforeunload", function() {
    $(".spinner__load").fadeIn("slow");
});

$(window).on("load", function() {
    $(".spinner__load").fadeOut("slow");
});