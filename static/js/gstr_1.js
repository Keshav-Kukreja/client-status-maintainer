let th =  `<th> </th><th>S. No.</th><th>Code</th><th>Name</th><th>GST No.</th>
<th>Working Hand</th><th>R_Type</th><th>D_Type</th><th>Apr</th><th>May</th><th>Jun</th><th>Jul</th>
<th>Aug</th><th>Sep</th><th>Oct</th><th>Nov</th><th>Dec</th><th>Jan</th><th>Feb</th>
<th>Mar</th>`

// checkboxes state is saved in this object
let obj = {}

$(document).ready(function(){
    $('#search').keyup(function(){
            $.ajax({
                type: "POST",
                url: "/search",
                data:{
                    searchTerm: $('#search').val(),
                    col: $('#search-by').val(),
                    table: $('#return').val(),
                    filter: $('#filter').val(),
                    month: $('#month-by').val(),
                },
                success: get_result}
                )})
            })
// on page load request is sent to the server
window.addEventListener("load", post_data);

// on id = return change request is sent to the server
$('#return').change(post_data)
$('#filter').change(post_data)
$('#month-by').change(post_data)
document.getElementById('return').onchange=$.cookie('table', $('#return').val());


// function to get result or response of the request from the server
function get_result(result){
                /*var resultsHtml = '';
                for (var i = 0; i < result.results.length; i++) {
                    resultsHtml += '<tr><td>''</td></tr>'}
                $('#searchResults').html(resultsHtml);*/
        var resultsHtml = ''
        result.forEach(result=>{
          if ($("#return").val()=="r9"){
                head=`<th> </th><th>S. No.</th><th>Code</th><th>Name</th><th>GST No.</th>
                <th>Working Hand</th><th>Status</th>`
                resultsHtml+=`<tr>
                <td><input type="checkbox" value=${result["code_no"]} name="code"></td>
                <td>${result["S_No"]}</td>
                <td>${result["code_no"]}</td>
                <td>${result["name"]}</td>
                <td>${result["gst_no"]}</td>
                <td>${result["working_hand"]}</td>
                <td>${result["Status"]}</td>
                </tr>`
                document.getElementById("table").innerHTML=head+resultsHtml
            }
          else{
           resultsHtml += `<tr>
                        <td><input type="checkbox" value=${result["code_no"]} name="code"></td>
                        <td>${result["S_No"]}</td>
                        <td>${result["code_no"]}</td>
                        <td>${result["name"]}</td>
                        <td>${result["gst_no"]}</td>
                        <td>${result["working_hand"]}</td>
                        <td>${result["r_type"]}</td>
                        <td>${result["d_type"]}</td>
                        <td>${result["Apr"]}</td>
                        <td>${result["May"]}</td>
                        <td>${result["Jun"]}</td>
                        <td>${result["Jul"]}</td>
                        <td>${result["Aug"]}</td>
                        <td>${result["Sep"]}</td>
                        <td>${result["Oct"]}</td>
                        <td>${result["Nov"]}</td>
                        <td>${result["Dec"]}</td>
                        <td>${result["Jan"]}</td>
                        <td>${result["Feb"]}</td>
                        <td>${result["Mar"]}</td>
                        </tr>`
                        document.getElementById("table").innerHTML=th+resultsHtml
                    }})
                    Colorchange()
                    checkbox()
                    change_check_state()
                    document.getElementById('return').onchange=$.cookie('table', $('#return').val());
                    if ($('#filter').val()=="F" || $('#filter').val()=="P"){
                       $('#month-by').prop('disabled', false)
                      }
                    else { $('#month-by').prop('disabled', true) }
            }

// function to post  request to the server
function post_data() {
    $.ajax({
        type: "POST",
        url: "/search",
        data:{
            searchTerm: $('#search').val(),
            col: $('#search-by').val(),
            table: $('#return').val(),
            filter: $('#filter').val(),
            month: $('#month-by').val(),
        },
        success: get_result}
        )}
// ***************  function to post  request to the server ***********************
// **************** change it in the future to make code clean ********************
function Colorchange(){
        let td = document.getElementsByTagName("td")
        td=Array.from(td)
        td.forEach(td=>{
            if (td.innerHTML=="N"){
                td.style.background="lightgrey"
            }
            else if (td.innerHTML=="N/A"){
                td.style.background="white"
            }
            else if (td.innerHTML=="P"){
                td.style.background="red"
            }
            else if (td.innerHTML=="F"){
                td.style.background="lightgreen"
            }
        })
}

// **************** function to add eventlistner to checkboxes ********************
// it also stores the state of the checkboxes
// **************** change it in the future to make code clean ********************
function checkbox() {
    let isCheckbox = document.querySelectorAll('input[type=checkbox]')
    isCheckbox = Array.from(isCheckbox)
    isCheckbox.forEach(checkbox=>{
        checkbox.addEventListener('change', function(e) {
             if (e.target.checked){
                obj[e.target.value] = true    
             }
             else {
                obj[e.target.value] = false    
             }
          });
    })
}

/***************** func to change the state   *********************
********  of the checkboxes saved by previous funcinon  *********************/
function change_check_state(element){
    let checkbox = document.querySelectorAll('input[type=checkbox]')
    checkbox = Array.from(checkbox)
    checkbox.forEach(checkbox=>{
        for (let val in obj){
            if (checkbox.value==val && obj[val]){
                checkbox.checked=true
            }
        }
    })
}

//************ code to redirect on change event   *******************
// var r_type = document.getElementById('return');
// r_type.onchange = function() {
// //   window.open(e.target.value);
// if (this.selectedIndex!=0){
//   window.open(this.options[this.selectedIndex].value)
// }
// };


//************ code to redirect on change event   *******************
var fy = document.getElementById('fy');
fy.onchange = function() {
//   window.open(e.target.value);
if (this.selectedIndex!=0){
  window.open(this.options[this.selectedIndex].value)
}
};


