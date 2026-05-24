const form = document.querySelector('form');
const inputs = form.querySelectorAll("input, textarea");
const submit = form.querySelector("button");
const spinner = form.nextElementSibling;
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
    form.addEventListener('submit', handlePost)
}

