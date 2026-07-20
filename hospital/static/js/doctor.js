const searchInput = document.getElementById("searchInput");
const rowsPerPage = document.getElementById("rowsPerPage");
const table = document.getElementById("doctorTable");
const tbody = table.querySelector("tbody");
const pageNumbers = document.getElementById("pageNumbers");
const prevBtn = document.getElementById("prevBtn");
const nextBtn = document.getElementById("nextBtn");
const tableInfo = document.getElementById("tableInfo");


let rows = Array.from(tbody.querySelectorAll("tr"));
let filteredRows = [...rows];
let currentPage = 1;
let rowsCount = parseInt(rowsPerPage.value);

function displayTable() {
    tbody.innerHTML = "";
    const start = (currentPage - 1) * rowsCount;
    const end = start + rowsCount;
    const pageRows = filteredRows.slice(start, end);
    pageRows.forEach(row => {
        tbody.appendChild(row);
    });
    updateTableInfo();
    createPagination();
}
searchInput.addEventListener("keyup", function () {
    const value = this.value.toLowerCase();
    filteredRows = rows.filter(row => {
        return row.innerText.toLowerCase().includes(value);
    });
    currentPage = 1;
    displayTable();
});
rowsPerPage.addEventListener("change", function () {
    rowsCount = parseInt(this.value);
    currentPage = 1;
    displayTable();
});
function createPagination() {
    pageNumbers.innerHTML = "";
    const totalPages = Math.ceil(filteredRows.length / rowsCount);
    for (let i = 1; i <= totalPages; i++) {
        const btn = document.createElement("button");
        btn.innerText = i;
        btn.style.margin = "2px";
        btn.style.padding = "8px 12px";
        btn.style.cursor = "pointer";
        if (i === currentPage) {
            btn.style.background = "#0d6efd";
            btn.style.color = "white";
        }
        btn.addEventListener("click", function () {
            currentPage = i;
            displayTable();
        });
        pageNumbers.appendChild(btn);
    }
}
prevBtn.addEventListener("click", function () {
    if (currentPage > 1) {
        currentPage--;
        displayTable();
    }
});
nextBtn.addEventListener("click", function () {
    const totalPages = Math.ceil(filteredRows.length / rowsCount);
    if (currentPage < totalPages) {
        currentPage++;
        displayTable();
    }
});
function updateTableInfo() {
    const start = filteredRows.length === 0 ? 0 : ((currentPage - 1) * rowsCount) + 1;
    const end = Math.min(currentPage * rowsCount, filteredRows.length);
    tableInfo.innerHTML =`Showing ${start} to ${end} of ${filteredRows.length} entries`;
}
displayTable();