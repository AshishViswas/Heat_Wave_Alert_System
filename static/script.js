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
