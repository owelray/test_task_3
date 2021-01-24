var tables = []

const arrClass = document.querySelectorAll(".table");
for (let i of arrClass) {
  i.addEventListener("click", (e) => {
    if (e.target.classList.contains("table")) {
        if (e.target.style.backgroundColor == 'red'){

        } else if (e.target.style.backgroundColor == 'yellow') {
          tables.splice(tables.indexOf(e.target.getAttribute('value')), 1)
          e.target.style.backgroundColor = null
        } else {
          tables.push(e.target.getAttribute('value'))
          e.target.style.backgroundColor = 'yellow'
        }
    }
    document.getElementById('tables').value = tables
    console.log(document.getElementById('tables').value)
    if (tables.length > 0) {
        document.getElementById('book-form').style.display = 'block'
    } else {
        document.getElementById('book-form').style.display = 'none'
    }
  })
}