document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.edit').forEach(button => {
        button.onclick = function() {
            editpost(this);
        }
    });

    document.querySelectorAll('.post').forEach(post => {
        let likebtn = post.querySelector('img');
        if (likebtn.getAttribute("name") == '') {
            return false
        }
        likebtn.style.cursor = 'pointer';
        likebtn.onclick = function() {
            if (likebtn.getAttribute("name") == 'like') {
                like(post)
            }
            else if (likebtn.getAttribute("name") == 'unlike') {
                unlike(post)
            }
        }
    });
});


function editpost(button) {
    let x = button.parentElement;
    button.style.display = 'none';
    content = x.querySelector('.content').innerHTML;
    x.querySelector('.content').style.display = 'none';

    x.querySelector('textarea').innerHTML = content;
    x.querySelector('.editform').style.display = 'block';
}


function like(post) {
    fetch('/like_fun', {
        method: 'POST',
        body: JSON.stringify({
            post_id: post.id,
            reason: 'like'
        })
    })
    .then(response => response.json());

    let count = parseInt(post.querySelector('.counter').innerHTML);
    count += 1;
    post.querySelector('.counter').innerHTML = count
    const img = post.querySelector('img');
    img.setAttribute('name', 'unlike');
    img.setAttribute('src', 'https://www.freeiconspng.com/uploads/like-heart-icon--16.png');
}

function unlike(post) {
    fetch('/like_fun', {
        method: 'POST',
        body: JSON.stringify({
            post_id: post.id,
            reason: 'unlike'
        })
    })
    .then(response => response.json());

    let count = parseInt(post.querySelector('.counter').innerHTML);
    count -= 1;
    post.querySelector('.counter').innerHTML = count
    const img = post.querySelector('img');
    img.setAttribute('name', 'like');
    img.setAttribute('src', 'https://cdn.icon-icons.com/icons2/1812/PNG/512/4213423-active-favorite-heart-like-love-romantic_115369.png');
}


// FUTURE ME I MANAGED TO MAKE THE COUNTER GO UP WHEN LIKING
// NEXT I WANNA MAKE THE HEART BECOME BLACKED OUT WHEN CLICKING
// THEN MAKE THE UNLIKE FEATUREr