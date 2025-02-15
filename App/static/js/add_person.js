// document.addEventListener("DOMContentLoaded", function() {
//     const roleField = document.querySelector('select[name="role"]');
//     const studentFields = document.getElementById("student-fields");
//     const teacherFields = document.getElementById("teacher-fields");
//     const staffFields = document.getElementById("staff-fields");

//     function toggleFields() {
//         const role = roleField.value;
//         studentFields.classList.toggle("hidden", role !== "student");
//         teacherFields.classList.toggle("hidden", role !== "teacher");
//         staffFields.classList.toggle("hidden", role !== "staff");
//     }

//     roleField.addEventListener("change", toggleFields);
//     toggleFields(); // Initialize on page load
// });

document.addEventListener("DOMContentLoaded", function () {
    const roleField = document.querySelector("#id_role"); // Role selection
    const studentFields = document.getElementById("student-fields");
    const teacherFields = document.getElementById("teacher-fields");
    const staffFields = document.getElementById("staff-fields");
    const roleSections = document.querySelectorAll(".role-section");

    const step1 = document.getElementById("step-1");
    const step2 = document.getElementById("step-2");
    const nextBtn = document.getElementById("next-btn");
    const prevBtn = document.getElementById("prev-btn");

    // Hide all role fields initially
    function hideAllRoleFields() {
        roleSections.forEach(section => section.classList.add("hidden"));
    }

    // Show the correct role fields based on selection
    function showRoleFields() {
        hideAllRoleFields(); // Hide all fields first
        const selectedRole = roleField.value.trim().toLowerCase(); // Convert to lowercase for consistency

        if (selectedRole === "student") {
            studentFields.classList.remove("hidden");
        } else if (selectedRole === "teacher") {
            teacherFields.classList.remove("hidden");
        } else if (selectedRole === "staff") {
            staffFields.classList.remove("hidden");
        }
    }

    // Ensure correct role fields are shown when role is selected
    roleField.addEventListener("change", showRoleFields);

    // Step Navigation: Move to Step 2
    nextBtn.addEventListener("click", function () {
        if (roleField.value) {
            showRoleFields(); // Ensure correct fields show
            step1.classList.add("hidden");
            step2.classList.remove("hidden");
        } else {
            alert("Please select a role before proceeding.");
        }
    });

    // Step Navigation: Move back to Step 1
    prevBtn.addEventListener("click", function () {
        step2.classList.add("hidden");
        step1.classList.remove("hidden");
    });

    // Ensure correct fields are visible when the page loads
    showRoleFields();
});

