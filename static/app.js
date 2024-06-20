document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/movies')
        .then(response => response.json())
        .then(movies => {
            const moviesList = document.getElementById('movies-list');
            movies.forEach(movie => {
                const movieElement = document.createElement('div');
                movieElement.className = 'movie';

                // Assuming the thumbnail image has the same name as the movie file but with .jpg extension
                const thumbnailPath = `/thumbnails/${movie}.jpg`;

                movieElement.innerHTML = `
                    <img src="${thumbnailPath}" alt="${movie}">
                    <a href="/movies/${movie}" target="_blank">${movie}</a>
                `;

                moviesList.appendChild(movieElement);
            });
        });
});
