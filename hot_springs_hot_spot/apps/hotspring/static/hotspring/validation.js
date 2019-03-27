$(document).ready(function(){
    $('#email').keyup(function(){
        console.log("KeyUP**********")
        $.ajax({
            method:"GET",
            url: "/username",
            data : {'email': $("#email").val()}
            
        })
        .done(function(res){
            $('#usernameMsg').html(res)
            console.log(res)
        })
    })
})