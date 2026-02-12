let sebd_btn = document.getElementById('sebd_btn')
let inp_name = document.getElementById('inp_name')
let inp_pass_id = document.getElementById('inp_pass_id')

sebd_btn.addEventListener('click', function(event) {
    let password_1 = inp_pass_id.value
    let user_name = inp_name.value
    console.log(password_1, user_name)

    let data = {"f_name": user_name, "pass": password_1};

    fetch("/", {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    }).then(res => {
        console.log("Request complete! response:", res);
    });
})