document.getElementById('back').onclick = function() {
    window.location.replace('/account')
}

function styleForm() {
    let currentDate = new Date();
    let currentYear = currentDate.getFullYear(); let currentMonth = (currentDate.getMonth()+1) < 10 ? '0' + (currentDate.getMonth() + 1) : (currentDate.getMonth() + 1); let currentDay = currentDate.getDate() < 10 ? '0' + currentDate.getDate() : currentDate.getDate();
    document.getElementById('bornDate').max = (currentYear - 18) + '-' + currentMonth + '-' + currentDay;
    if (document.getElementById('bornDate').value == '1900-01-01') {
        document.getElementById('bornDate').style.color = '#808080';
        document.getElementById('bornDate').onchange = function(){
            document.getElementById('bornDate').style.color = '#000';
        };
    }

    if ( (document.getElementById('male').checked || document.getElementById('female').checked || document.getElementById('other').checked) == false) {
        document.getElementById('options').style.color = '#808080';
        document.getElementById('options').onchange = function() {
            document.getElementById('options').style.color = '#000';
        }
    }
}

styleForm();