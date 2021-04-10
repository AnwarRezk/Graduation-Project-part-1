window.addEventListener("DOMContentLoaded", () => {
    const ranges = document.getElementsByClassName("range_star");
    const changedMovies = {};

    for (let range of ranges) {
        range.oldvalue = range.value;

        range.addEventListener("change", (event) => {
            if (parseFloat(event.target.value) !== parseFloat(event.target.oldvalue)) {
                changedMovies[event.target.name] = event.target.name;
                console.dir(changedMovies);
            }
            else if (changedMovies[event.target.name]) {
                delete changedMovies[event.target.name];
                console.dir(changedMovies);
            }
        });
    }

    document.getElementById("form").addEventListener("submit", () => {
        for (let movie of Object.keys(changedMovies)) {
            if (sessionStorage.getItem(movie)) {
                sessionStorage.removeItem(movie);
            }
        }
    });
});