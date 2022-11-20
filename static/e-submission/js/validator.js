const p = document.createElement('p');
p.innerText = 'You have some questions unanswered'
const input = document.querySelector('input[type="radio"]')
const formObj = document.querySelector('form#formEval')
formObj.addEventListener('submit', function(e){
    if(!input.checked){
    formObj.prepend(p)
    e.preventDefault()

    }

})