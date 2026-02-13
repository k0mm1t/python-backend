let send_btn = document.getElementById('send_btn')
let inp_name = document.getElementById('inp_name')
let inp_pass_id = document.getElementById('inp_pass_id')

send_btn.addEventListener('click', function(event) {
    let password_1 = inp_pass_id.value
    let user_name = inp_name.value
    // console.log(password_1, user_name)

    let data = {"username": user_name, "password": password_1};

    fetch("/", {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    }).then(res => {
        console.log("resonse ", res);
    });
})