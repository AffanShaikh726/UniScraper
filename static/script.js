fetch("/api/data")
    .then((response) => response.json())
    .then((data) => {
        console.log(data);
        const tableBody = document.getElementById("tableBody");
        if (data && data.courses) {
            data.courses.forEach((course) => {
                const row = document.createElement("tr");
                const attendancePercent =
                    parseFloat(course.attendance_percent) || 0;
                const attendanceClass =
                    attendancePercent < 75
                        ? "low-attendance"
                        : "good-attendance";
                const attendanceStatus =
                    attendancePercent < 75 ? "⚠️ Low" : "✅ Good";

                row.innerHTML = `
                    <td data-label="Course Code">${
                        course.course_code || "-"
                    }</td>
                    <td data-label="Course Title">${
                        course.course_title || "-"
                    }</td>
                    <td data-label="Category">${course.category || "-"}</td>
                    <td data-label="Faculty Name">${
                        course.faculty_name || "-"
                    }</td>
                    <td data-label="Slot">${course.slot || "-"}</td>
                    <td data-label="Hours Conducted">${
                        course.hours_conducted || "-"
                    }</td>
                    <td data-label="Hours Absent">${course.absent || "0"}</td>
                    <td data-label="Attendance %" class="${attendanceClass}">
                        ${course.attendance_percent || "0"}% ${attendanceStatus}
                    </td>
                `;
                tableBody.appendChild(row);
            });
        } else {
            console.error("Invalid data format");
        }
    });
