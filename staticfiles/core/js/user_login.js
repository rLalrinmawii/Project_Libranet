$(document).ready(function() {
    // Web app's Firebase configuration
    var firebaseConfig = {
        apiKey: "AIzaSyBin1evT-H6jfR49WIhtVPsGMLzbEklIQY",
        authDomain: "library-management-syste-f2a85.firebaseapp.com",
        databaseURL: "https://library-management-syste-f2a85.firebaseio.com",
        projectId: "library-management-syste-f2a85",
        storageBucket: "library-management-syste-f2a85.appspot.com",
        messagingSenderId: "914416876417",
        appId: "1:914416876417:web:bf9e7762c1c283ba"
    };

    // Initialize Firebase
    firebase.initializeApp(firebaseConfig);
    const db = firebase.firestore();
    const auth = firebase.auth();

    // Prevent default refresh of form 
    $("#login-form").submit(function(e) {
        e.preventDefault();
    });

    $("#register-form").submit(function(e) {
        e.preventDefault();
    });

    // Check if user is logged in
    auth.onAuthStateChanged(user => {
        if (user) {
            // If the user is logged in, redirect to the user portal (if needed)
            // Commenting out if you don't want to redirect to user portal at login
            // window.location = '/user-portal/'; // Uncomment if needed
        }
    });

    $('#log_me_in').click(function() {
        login();
    });

    $('#register_new').click(function() {
        register_me();
    });

    $('#log_button').click(function() {
        logout();
    });
});

function logout() {
    const auth = firebase.auth();
    
    auth.signOut().then(function() {
        console.log("Logout successful");
        window.location.href = '/user-login/'; // Redirect to login page
    }).catch(function(error) {
        console.error("Error during logout:", error);
    });
}

function register_me() {
    // Get input data
    var name = document.getElementById("usr_name").value;
    var password = document.getElementById("usr_pass").value;
    var email = document.getElementById("usr_email").value;
    var rollNumber = document.getElementById("usr_roll").value;
    var dateOfBirth = document.getElementById("usr_dob").value;
    var books = [];

    // Check if user already exists
    firebase.auth().fetchSignInMethodsForEmail(email)
        .then((signInMethods) => {
            if (signInMethods.length > 0) {
                alert("User already exists!");
            } else {
                // Firebase registration
                firebase.auth().createUserWithEmailAndPassword(email, password)
                    .then((userCredential) => {
                        // Registration successful, now write to Firestore
                        var user = userCredential.user;
                        return db.collection("users").doc(user.uid).set({
                            name: name,
                            Email: email,
                            Roll_Number: rollNumber,
                            DOB: dateOfBirth,
                            books: books
                        });
                    })
                    .then(() => {
                        console.log("User data successfully written to Firestore!");
                        // Redirect to user login page after successful registration
                        window.location.href = '/user-login/'; // Adjust URL as needed
                    })
                    .catch((error) => {
                        console.error("Error during registration:", error);
                        alert("Error: " + error.message);
                    });
            }
        })
        .catch((error) => {
            console.error("Error fetching sign-in methods:", error);
        });
}

function login() {
    var email = document.getElementById("username").value;
    var password = document.getElementById("password").value;

    // Use email instead of username to login
    firebase.auth().signInWithEmailAndPassword(email, password)
        .then((userCredential) => {
            // Successfully logged in
            console.log("User logged in:", userCredential.user);
            window.location.href = '/user-login/'; // Redirect to user login page
        })
        .catch((error) => {
            // Handle Errors here.
            var errorCode = error.code;
            var errorMessage = error.message;
            alert(errorMessage); // Show error message to the user
            console.error("Error during login:", errorMessage);
        });
}