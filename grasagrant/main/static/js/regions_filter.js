const input = document.getElementById('user_input')
const regions = document.getElementsByClassName('info-card')

input.oninput = (event) => {
    let user_input = event.target.value
    let regions_list = [...regions].map(item => item.id)
    let mask = regions_list.map(region => {
        let splitted_region = region.split(' ')
        let presence = splitted_region.map(str => str.startsWith(user_input.toLowerCase()) ? true: false)
        return presence.includes(true)
    })
    mask.findIndex((item, idx) => {item ? regions[idx].style.display='block': regions[idx].style.display='none'});
}