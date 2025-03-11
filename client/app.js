document.addEventListener("DOMContentLoaded", function() {
    fetch("http://127.0.0.1:5000/get_brand_names")
    .then(response => response.json())
    .then(data => {
        let brandSelect = document.getElementById("brand");
        brandSelect.innerHTML = ""; // Clear existing options
        data.brands.forEach(brand => {
            let option = document.createElement("option");
            option.value = brand;
            option.textContent = brand;
            brandSelect.appendChild(option);
        });
    })
    .catch(error => {
        console.error("Error fetching brands:", error);
        let brandSelect = document.getElementById("brand");
        brandSelect.innerHTML = "<option value=''>Error loading brands</option>";
    });
});

document.getElementById("priceForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent form submission

    let formData = new FormData();
    formData.append("brand", document.getElementById("brand").value);
    formData.append("os", document.getElementById("os").value);
    formData.append("screen_size", document.getElementById("screen_size").value);
    formData.append("rear_camera_mp", document.getElementById("rear_camera_mp").value);
    formData.append("front_camera_mp", document.getElementById("front_camera_mp").value);
    formData.append("internal_memory", document.getElementById("internal_memory").value);
    formData.append("ram", document.getElementById("ram").value);
    formData.append("battery", document.getElementById("battery").value);
    formData.append("weight", document.getElementById("weight").value);
    formData.append("device_age", document.getElementById("device_age").value);
    formData.append("price_drop", document.getElementById("price_drop").value);
    formData.append("has_4g", document.getElementById("has_4g").value);
    formData.append("has_5g", document.getElementById("has_5g").value);

    fetch("http://127.0.0.1:5000/predict_device_price", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.estimated_price) {
            document.getElementById("result").innerHTML = `Estimated Price: $${data.estimated_price}`;
        } else {
            document.getElementById("result").innerHTML = `Error: ${data.error}`;
        }
    })
    .catch(error => {
        document.getElementById("result").innerHTML = `Error connecting to API`;
    });
});
