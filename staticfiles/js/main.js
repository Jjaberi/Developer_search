

let searchform = document.getElementById('searchform')
let pagelinks = document.getElementsByClassName('page-link')

if(searchform){
    for (let i=0; pagelinks.length > i; i++){
        pagelinks[i].addEventListener('click',function (e) {
            e.preventDefault()
            let page = this.dataset.page
            searchform.innerHTML+=`<input value=${page} name="page" hidden/>`
            searchform.submit()
        } )
    }
}

