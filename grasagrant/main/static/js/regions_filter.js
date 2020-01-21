const input = document.getElementById('user_input')
const regions = document.getElementsByClassName('info-card')

input.oninput = (event) => {
    let user_input = event.target.value
    let regions_list = [...regions].map(item => item.id)
    console.log(regions_list)

}