const p = document.createElement('p');
p.innerText = 'You have some questions unanswered';
const input = document.querySelector('input[type="radio"]');
const formObj = document.querySelector('form');
console.log("loaded...", formObj)
input.addEventListener('submit', function(e){

    if(!input.checked){
        console.log('Please select all queries');
        formObj.prepend(p)
        e.preventDefault()
    }

})