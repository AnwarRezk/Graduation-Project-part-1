window.addEventListener("DOMContentLoaded", () => {
    const ranges = document.getElementsByClassName("range_star");

    for(let range of ranges) {
        range.oldvalue = range.value;
        let value = sessionStorage.getItem(range.getAttribute("name"));

        if (value) {
            range.setAttribute("value", value);
        }

        let textInput = document.getElementById(`${range.getAttribute("name")} textInput`);
        textInput.innerHTML = range.getAttribute("value");

        range.addEventListener("change", (event) => {
            if (parseFloat(event.target.value) !== parseFloat(event.target.oldvalue)) {
                sessionStorage.setItem(range.getAttribute("name"), event.target.value);
            }
            else if (sessionStorage.getItem(range.getAttribute("name"))) {
                sessionStorage.removeItem(range.getAttribute("name"));
            }
        });

        range.addEventListener('input', function (event) {
            textInput.innerHTML = event.target.value;
        });
    }

    document.getElementById("form").addEventListener("submit", (event) => {
        let form = event.target;

        for(let el of form) {
            if(el.className == "range_star") {
                el.remove();
            }
        }

        for(let i = 0; i < sessionStorage.length; i++) {
            let input = document.createElement('input');
            input.type = 'hidden';
            input.name = sessionStorage.key(i);
            input.value = sessionStorage.getItem(sessionStorage.key(i));

            form.appendChild(input);
        }

        form.submit();
    });

});