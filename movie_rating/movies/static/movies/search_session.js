window.addEventListener("DOMContentLoaded", () => {
    let ranges = document.getElementsByClassName("range_star");

    for(let range of ranges) {
        let value = sessionStorage.getItem(range.getAttribute("name"));

        if (value) {
            range.setAttribute("value", value);
        }

        let textInput = document.getElementById(`${range.getAttribute("name")} textInput`);
        let ratingValue = document.getElementById(`${range.getAttribute("name")} rating-value`);
        textInput.innerHTML = range.getAttribute("value");
        ratingValue.innerHTML = range.getAttribute("value");

        range.addEventListener("change", (event) => {
            sessionStorage.setItem(range.getAttribute("name"), event.target.value);
        });

        range.addEventListener('input', function (event) {
            textInput.innerHTML = event.target.value;
            ratingValue.innerHTML = event.target.value;
        });
    }
});