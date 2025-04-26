// En tu archivo JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // URL de la vista de proxy en tu aplicación Django
    var proxyUrl = '/proxy-api/';

    // Hacer una solicitud GET a la vista de proxy
    fetch(proxyUrl)
        .then(function(response) {
            return response.json();
        })
        .then(function(data) {
            // Procesar los datos recibidos y mostrarlos en tu página web
            console.log(data);
        })
        .catch(function(error) {
            console.error('Error al obtener datos del servidor:', error);
        });
});
