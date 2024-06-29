// document.addEventListener('DOMContentLoaded', function() {
//     const form = document.getElementById('registrationForm');

//     form.addEventListener('submit', function(event) {
//         event.preventDefault(); // Prevent the form from submitting normally

//         // Get form data
//         const mailId = document.getElementById('mail_id').value;
//         const firstName = document.getElementById('first_name').value;
//         const lastName = document.getElementById('last_name').value;

//         // Create URL-encoded form data
//         const formData = new URLSearchParams();
//         formData.append('mail_id', mailId);
//         formData.append('first_name', firstName);
//         formData.append('last_name', lastName);

//         // Send URL-encoded data to backend endpoint
//         fetch('/Register', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/x-www-form-urlencoded'
//             },
//             body: formData.toString()
//         })
//         .then(response => {
//             if (!response.ok) {
//                 throw new Error('Network response was not ok');
//             }
//             return response.json();
//         })
//         .then(data => {
//             console.log('Registration successful', data);
//             alert('Registration successful!');
//             // Optionally, redirect to a success page
//             window.location.href = '/home';
//         })
//         .catch(error => {
//             console.error('Error during registration:', error);
//             alert('Registration failed. Please try again.');
//         });
//     });
// });

// document.getElementById('subscriptionForm').addEventListener('submit', function(event) {
//     event.preventDefault();  // Prevent the default form submission behavior (which would reload the page)

//     var formData = new FormData();  // Create a new FormData object to collect form data
//     formData.append('email', document.getElementById('email').value);  // Get the email input value and add it to the FormData object

//     fetch('/subscribe', {
//         method: 'POST',
//         headers: {
//                             'Content-Type': 'application/x-www-form-urlencoded'
//                         },
//         body: formData
//     })
//     .then(response => {
//                     if (!response.ok) {
//                         throw new Error('Network response was not ok');
//                     }
//                     return response.json();
//                 })
//                 .then(data => {
//                     console.log('Registration successful', data);
//                     alert('Registration successful!');
//                     // Optionally, redirect to a success page
//                     window.location.href = '/home';
//                 })
//                 .catch(error => {
//                     console.error('Error during registration:', error);
//                     alert('Registration failed. Please try again.');
//                });
//             });
      
document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector('form');

    form.addEventListener('submit', function(event) {
        const phoneNumberInput = document.getElementById('phone_number');
        const phoneNumber = phoneNumberInput.value.trim();

        if (!isValidPhoneNumber(phoneNumber)) {
            alert('Please enter a valid phone number.');
            event.preventDefault();
            return; // Stop further processing if phone number is invalid
        }

        // Send the phone number to the Flask backend using AJAX
        sendPhoneNumberToBackend(phoneNumber);
        event.preventDefault(); // Prevent the default form submission
    });

    function isValidPhoneNumber(phoneNumber) {
        // You can add your phone number validation logic here
        // For example, you might check for a specific format or length
        return true;
    }

    function sendPhoneNumberToBackend(phoneNumber) {
        const xhr = new XMLHttpRequest();
        const url = '/Register'; // Replace with your Flask route URL

        xhr.open('POST', url, true);
        xhr.setRequestHeader('Content-Type', 'application/json');

        xhr.onreadystatechange = function() {
            if (xhr.readyState === XMLHttpRequest.DONE) {
                if (xhr.status === 200) {
                    const response = JSON.parse(xhr.responseText);
                    console.log(response.message); // Log the response from Flask
                    // You can update the UI or perform further actions based on the response
                } else {
                    console.error('Error:', xhr.status);
                    // Handle error response from Flask if needed
                }
            }
        };

        const data = JSON.stringify({ phone_number: phoneNumber });
        xhr.send(data);
    }
});
