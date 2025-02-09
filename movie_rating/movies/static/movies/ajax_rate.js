document.addEventListener("DOMContentLoaded", () => {
    const rating = document.getElementById('rating');
    const csrftoken = getCookie('csrftoken');
    rating.oldvalue = rating.value;

    rating.addEventListener("change", (event) => {
        if (parseFloat(event.target.value) !== parseFloat(event.target.oldvalue)) {
            fetch('#', {
                method: 'POST',
                mode: 'same-origin',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify({
                    rating: rating.value
                })
            })
                .then(res => res.json())
                .then(res => {
                    if (res.status === "OK") {
                        window.scrollTo(0, 0);
                        flashMessage(res.message);
                        
                        if (sessionStorage.getItem(rating.getAttribute("name"))) {
                            sessionStorage.removeItem(rating.getAttribute("name"));
                        }
                        event.target.oldvalue = event.target.value;
                    }
                })
                .catch(err => console.error(err));
        }
    });
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function flashMessage(message) {
    const messageElem = `<div class="row">
    <div class="alert ${message.tags} alert-dismissible fade show" id="msg" role="alert">
        ${message.data}
        <button type="button" class="close" data-dismiss="alert" aria-label="Close">
            <span aria-hidden="true">&times;</span>
        </button>
    </div>
</div>`;

    document.getElementById('messages').innerHTML += messageElem;
    document.getElementById('msg').style.marginTop = "20px";
    document.getElementById('msg').style.marginBottom = "5px";
    fadeMessage();
}

function fadeMessage() {
    setTimeout(function () {
        if ($('#msg').length > 0) {
            $('#msg').remove();
        }
    }, 2000);
}
