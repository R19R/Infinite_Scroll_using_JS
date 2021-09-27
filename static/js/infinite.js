/* 
'Function to fetch data from csv file and post it to Databae'

document
.getElementById('btn')
.addEventListener("click", readDetails);

async function readDetails(){
    let req = await fetch('/list');
    let res = await req.json();
    console.log(res);
    res.forEach(element => {
        postDetails(element.Employee_ID,
            element.First_Name,
            element.Last_name,
            element.Department)
    });
}

async function postDetails(id, firstname, lastname, dept){
    let details = JSON.stringify({
    id:id,
    firstName : firstname,
    lastName : lastname,
    department : dept })

    let request_settings = {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: details
    }

    let req = await fetch("/employee", request_settings);
    let res = await req.text()
    console.log(res);
} */

document.addEventListener('DOMContentLoaded', employeeDetails);

var cursor = null; 
var offset = null; 

async function employeeDetails(){
    let req = await fetch('/showdetails');
    let res = await req.json();

    if (res.details_list){
        let det = res.details_list;
        console.log("First", det);
        det.forEach(element => {
            table(element.id,
                element.fname,
                element.lname,
                element.dept)      
        });
    } 
    cursor = res.cursor;
}

async function cursorFunc(){
    let req = await fetch('/otherdetails?cursor='+cursor+"&offset="+offset);
    let res = await req.json();

    req_test = false;
    
    if (res.cursor){
        console.log("cursorFunc", res.details_list);
        let det = res.details_list;
        det.forEach(element => {
            table(element.id,
                element.fname,
                element.lname,
                element.dept)      
        });
    } else {
        req_test = true;
        console.log(res.info);
    }
    cursor = res.cursor;
    offset = res.offset;
}

var row = 0;
function table(t1,t2,t3,t4){
    var table = document.getElementById("listSongs-table-tbody");
    var newRow = table.insertRow(row);

    var cell_id = newRow.insertCell(0);
    var cell_firstName = newRow.insertCell(1);
    var cell_LastName = newRow.insertCell(2);
    var cell_department = newRow.insertCell(3);

    cell_id.style.width = '125px';
    cell_firstName.style.width = '125px';
    cell_LastName.style.width = '125px';
    cell_department.style.width = '125px';


    cell_id.innerHTML = t1;
    cell_firstName.innerHTML = t2;
    cell_LastName.innerHTML = t3;
    cell_department.innerHTML = t4;
    
    row++;
}

// infinte scroll

var infinte = document.getElementById("sample");
infinte.addEventListener("scroll", scrollTable);

var req_test = false;

function scrollTable() {
  var table1 = document.getElementById("listSongs-table");

  var scrollHeight = table1.scrollHeight;
  var scrollTop = table1.scrollTop;
  var clientHeight = table1.clientHeight;


if (scrollTop + clientHeight >= scrollHeight){
    if(!req_test){
        req_test = true;
        cursorFunc();
  }
}
}