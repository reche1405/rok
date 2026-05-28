const form = document.querySelector('form');
let inputs;
let submit; 
let spinner;
const handlePost = (e) => {
    e.preventDefault();
    inputs.forEach(input => {
        input.classList.add('disabled');
    });
    submit.disabled = true;

    spinner.removeAttribute("hidden");
    spinner.classList.add("spin");
    setTimeout(() => {

        e.target.submit();
    }, 1000)
}

if(form) {
    inputs = form.querySelectorAll("input, textarea");
    submit = form.querySelector("button");
    spinner = form.nextElementSibling;
    form.addEventListener('submit', handlePost)
}

