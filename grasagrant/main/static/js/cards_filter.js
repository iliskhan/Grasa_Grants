const input = document.getElementById('user_input')
const cards = document.getElementsByClassName('info-card')

input.oninput = (event) => {
    let user_input = event.target.value
    let cards_list = [...cards].map(item => item.innerText)
    let mask = cards_list.map(string => string.toLowerCase().includes(user_input.toLowerCase())) 
    mask.findIndex((item, idx) => {item ? cards[idx].style.display='block': cards[idx].style.display='none'});
}