function validateForm() {
    //collect form data in JavaScript variables
    var pw1 = document.getElementById("pswd1").value;
    var upperCaseLetters = /[A-Z]/g;
    var lowerCaseLetters = /[a-z]/g;
    var numbers = /[0-9]/g;

    //check empty password field
    if(pw1 != "") {
        //minimum password length validation
        if (pw1.length < 8) {
            document.getElementById("message1").innerHTML = "**Password length must be atleast 8 characters";
            return false;
        }
        else{

            if(lowerCaseLetters.test(pw1) === false){
                document.getElementById("message1").innerHTML = "**Password must contain atleast one lowercase character";
                return false;

            }
            if(upperCaseLetters.test(pw1) === false){
                document.getElementById("message1").innerHTML = "**Password must contain atleast one uppercase character";
                return false;

            }
            if(numbers.test(pw1) === false){
                document.getElementById("message1").innerHTML = "**Password must contain atleast one number";
                return false;

            }
        }

        //maximum length of password validation
        if (pw1.length > 15) {
            document.getElementById("message1").innerHTML = "**Password length must not exceed 15 characters";
            return false;
        }
    }
}