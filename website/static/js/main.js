function cookieToJson() {
    var cookie = document.cookie;
    console.log(cookie)
    var output = {};
    cookie.split(/\s*;\s*/).forEach(function(pair) {
      pair = pair.split(/\s*=\s*/);
      output[pair[0]] = pair.splice(1).join('=');
    });
    return output;
}

function userFromCookie() {
    var cookieJson = cookieToJson();
    console.log(cookieJson)

    var user = {
        'id': cookieJson.patient_id,
        'username': (cookieJson.patient_username).replaceAll('"', '').replaceAll("'", ''),
        'email': (cookieJson.patient_email).replaceAll('"', '').replaceAll("'", ''),
        'name': (cookieJson.patient_name).replaceAll('"', '').replaceAll("'", ''),
        'phoneNumber': cookieJson.patient_phoneNumber,
        'bornDate': cookieJson.patient_bornDate,
        'gender': cookieJson.patient_gender,
        'patientNumber': cookieJson.patient_patientNumber,
        'alzheimer': (cookieJson.patient_alzheimer.toLowerCase() === "true"),
        'parkinson': (cookieJson.patient_parkinson.toLowerCase() === "true"),
        'observations': cookieJson.patient_observations.replaceAll('"', '').replaceAll("'", ''),
        'doctor_id': cookieJson.patient_doctor_id,
    }

    return user;
}

function setForm() {
    let user = userFromCookie();
    document.getElementById('title').textContent = 'Olá ' + user.username + ',';
    
    document.getElementById('username').value = user.username;
    document.getElementById('email').value = user.email;
    if (user.name !== '') { document.getElementById('name').value = user.name; }
    if (user.phoneNumber !== '') { document.getElementById('phoneNumber').value = user.phoneNumber; }
    let currentDate = new Date();
    let currentYear = currentDate.getFullYear(); let currentMonth = (currentDate.getMonth()+1) < 10 ? '0' + (currentDate.getMonth() + 1) : (currentDate.getMonth() + 1); let currentDay = currentDate.getDate() < 10 ? '0' + currentDate.getDate() : currentDate.getDate();
    if (user.bornDate === '1900-01-01') {
        document.getElementById('bornDate').value = currentYear + '-' + currentMonth + '-' + currentDay;
        document.getElementById('bornDate').style.color = '#808080';
        document.getElementById('bornDate').onchange = function(){
            document.getElementById('bornDate').style.color = '#000';
        };
    } else {
        document.getElementById('bornDate').value = user.bornDate;
    }
    let genderIndex = {'M': 0, 'F': 1, 'O': 2};
    if (user.gender === '') {
        document.getElementById('options').style.color = '#808080';
        document.getElementById('options').onchange = function() {
            document.getElementById('options').style.color = '#000';
        }
    } else {
        document.getElementsByClassName('genderOption')[genderIndex[user.gender]].checked = true;
        document.getElementById('options').style.color = '#000';
    }
    for (let i = 0; i < Object.keys(genderIndex).length; i++) {
        document.getElementsByClassName('genderOption')[i].onchange = function(){
            document.getElementById('options').style.color = '#000';
        };
    }
    if (user.patientNumber !== '') { document.getElementById('patientNumber').value = user.patientNumber; }
    if (user.alzheimer === false) {
        console.log('1')
        document.getElementsByClassName('alzheimerOption')[0].checked = true;
    } else {
        console.log('2')
        document.getElementsByClassName('alzheimerOption')[1].checked = true;
    }
    if (user.parkinson === false) {
        document.getElementsByClassName('parkinsonOption')[0].checked = true;
    } else {
        document.getElementsByClassName('parkinsonOption')[1].checked = true;
    }
    
}

setForm();