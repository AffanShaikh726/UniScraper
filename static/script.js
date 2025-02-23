fetch("/api/data")
    .then((response) => response.json())
    .then((data) => {
        console.log(data);
        const tableBody = document.getElementById("tableBody");
        if (data && data.courses) {
            data.courses.forEach((course) => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td data-label="Course Code">${
                        course.course_code || ""
                    }</td>
                    <td data-label="Course Title">${
                        course.course_title || ""
                    }</td>
                    <td data-label="Category">${course.category || ""}</td>
                    <td data-label="Faculty Name">${
                        course.faculty_name || ""
                    }</td>
                    <td data-label="Slot">${course.slot || ""}</td>
                    <td data-label="Hours Conducted">${
                        course.hours_conducted || ""
                    }</td>
                    <td data-label="Hours Absent">${
                        course.absent || "None"
                    }</td>
                    <td data-label="Attendance %">${
                        course.attendance_percent || ""
                    }</td>
                `;
                tableBody.appendChild(row);
            });
        } else {
            console.error("Invalid data format:");
        }
    });
