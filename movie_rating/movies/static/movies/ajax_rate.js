document.addEventListener("DOMContentLoaded", () => {
    const rating = document.getElementById('rating');
    const csrftoken = getCookie('csrftoken');

    rating.addEventListener("change", () => {
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
            if (res.status == "OK") {
                window.location.reload();
            }
        })
        .catch(err => console.error(err));
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