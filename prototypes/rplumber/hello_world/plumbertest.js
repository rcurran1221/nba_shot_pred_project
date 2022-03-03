var xhr = new XMLHttpRequest()

xhr.onload = function () {
    console.log(xhr.response)
    alert(xhr.response)
}
xhr.open('GET', 'http://localhost:8208/state', true)
xhr.send()

var xhr2 = new XMLHttpRequest()
xhr2.onload = function () {
    console.log(xhr2.response)
    alert(xhr2.response)
}

xhr2.open('POST', 'http://localhost:8208/sum?b=10&a=12', true)
xhr2.send()
