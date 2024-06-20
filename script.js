document.addEventListener('DOMContentLoaded', function() {
    fetch('/movies')
        .then(response => response.json())
        .then(movies => {
            const moviesList = document.getElementById('movies-list');
            movies.forEach(movie => {
                const movieElement = document.createElement('div');
                movieElement.className = 'movie';
                movieElement.innerHTML = `<a href="/movies/${movie}" target="_blank">${movie}</a>`;
                moviesList.appendChild(movieElement);
            });
        });
});
