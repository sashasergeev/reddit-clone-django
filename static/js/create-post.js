let image = document.querySelector('#id_image');
let text = document.querySelector('#id_text');

image.style.display = 'none';

document.querySelector('#id_post_type').addEventListener('change', (e) => {
    if (e.target.value === 'IP') {
        text.style.display = 'none';
        image.style.display = 'block';
        text.value = '';
    } else {
        text.style.display = 'block';
        image.style.display = 'none';
        image.value = '';
    };
})
