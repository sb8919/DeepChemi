
var limit = 3;
var count = 0;
var www = []


function delete_value(){
    document.getElementsByClassName("back_space")[0].style.display='none';
    document.getElementById("searchid").value = '';
    const checkboxes = document.getElementsByName('chk');
    count -= document.querySelectorAll('.element:checked').length;
    checkboxes.forEach((checkbox) => {
        checkbox.checked = false;
        www.pop();
    })
}
function count_check(obj) {
    if (obj.checked == false) {
        count -= 1;
        www.splice((www.indexOf(obj.value)), 1);
        document.getElementById("searchid").value = www;
        document.getElementsByClassName("back_space")[0].style.display='none';
    }
    if (count > limit) {
        alert("최대 4개만 선택해주세요!");
        obj.checked = false;
        
    }
    else {
        if (obj.checked == true) {
            count += 1;
            www.push(obj.value);
            document.getElementsByClassName("back_space")[0].style.display='inline-block';
            document.getElementById("searchid").value = www;
        }

    }


}

function check_value() {

    const element = document.getElementById("searchid").value;

    if (element == '') {
        alert("원소를 선택해주세요!")
    }
    else {
        if (condition.checked == false) {
            ele_condition = 2;
        }
        else {
            ele_condition = 4;
        }

        link = 'http://orion.mokpo.ac.kr:8490/';
        location.href = link + element + ',' + ele_condition;
    }

}
