function refreshDiv() {
    
    $.ajax({
        url: '/get_new_advice',
        type: 'POST',
        success: function(data) {
            // Atualize o conteúdo da div com o novo conteúdo do servidor
            console.log('Foi')
            $('#advice__response').html(data.advice);
        },
        error: function(xhr, status, error) {
            console.error(error);
        }
    });
}