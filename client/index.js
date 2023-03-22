/*function getPeople(done) {

    const results = fetch("http://127.0.0.1:8000/people/", {
        'mode': 'cors',
        'headers': {
            'Access-Control-Allow-Origin': '*',
        }
    });

    results
        .then(response => response.json())
        .then(data => {
            done(data)
        });

}

getPeople(data => {

    data.results.forEach(person => {
        const article = document.createRange().createContextualFragment(`
        <td>${person.name}</td>
        <td>${person.email}</td>
        <td>
            <button type="button" class="btn btn-sm btn-info">Editar</button>
            <button type="button" class="btn btn-sm btn-danger">Borrar</button>
        </td>

        `);

    const main = document.querySelector("#people_table");
    main.append(article);

    });
})*/

const API_URL = "http://127.0.0.1:8000";

const HTMLResponse = document.querySelector("#people_table");

fetch(`${API_URL}/people/`)
    .then((response)=> response.json())
    .then((users)=>{
        const tpl = users.map(user => `
        <tr>
        <td>${user.name}</td>
        <td>${user.email}</td>
        <td>
            ${user.id}
        </td>
        </tr>`);
        HTMLResponse.innerHTML = `
                ${tpl}
            `;
})
/////////////////////////////////////////////////////////
const input_mail = document.querySelector("#correo_persona")
const input_name = document.querySelector("#nombre_persona")
const button_person = document.querySelector("#person_button")

button_person.addEventListener('click', (e)=> {
    e.preventDefault();
    create_person(input_name.value, input_mail.value);
})
function create_person(person_name,mail){
    fetch(`${API_URL}/people/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            name: person_name,
            email: mail
        })
    })
    .then((response) => response.json())
    .then((data) => {
        console.log(data);
    });
}

//////////////////////////////////////////////////////////
const HTMLResponse2 = document.querySelector("#vehicle_table");

fetch(`${API_URL}/vehicles/`)
    .then((response)=> response.json())
    .then((users)=>{
        const tpl = users.map(user => `
        <tr>
        <td>${user.plate}</td>
        <td>${user.car_brand}</td>
        <td>${user.color}</td>
        </tr>`);
        HTMLResponse2.innerHTML = `
                ${tpl}
            `;
})
/////////////////////////////////////////////////////////
const input_placa = document.querySelector("#placa_vehiculo")
const input_marca = document.querySelector("#marca_carro")
const input_color = document.querySelector("#color_carro")
const input_id = document.querySelector("#person_id")
const button_vehicle = document.querySelector("#button_vehicle")

button_vehicle.addEventListener('click', (e)=> {
    e.preventDefault();
    create_vehicle(input_id.value,input_placa.value, input_marca.value,input_color.value);
})
function create_vehicle(person_id,plate,brand,color){
    fetch(`${API_URL}/people/${person_id}/vehicles/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            plate: plate,
            car_brand: brand,
            color: color
        })
    })
    .then((response) => response.json())
    .then((data) => {
        console.log(data);
    });
}

//////////////////////////////////////////////////////////
const HTMLResponse3 = document.querySelector("#agent_table");

fetch(`${API_URL}/agents/`)
    .then((response)=> response.json())
    .then((users)=>{
        const tpl = users.map(user => `
        <tr>
        <td>${user.name}</td>
        <td>${user.agent_identifier}</td>
        <td>
            <button type="button" class="btn btn-sm btn-info">Editar</button>
            <button type="button" class="btn btn-sm btn-danger">Borrar</button>
        </td>
        </tr>`);
        HTMLResponse3.innerHTML = `
                ${tpl}
            `;
})
/////////////////////////////////////////////////////////
const input_agente = document.querySelector("#nombre_agente")
const input_agente_id = document.querySelector("#id_agente")
const input_password = document.querySelector("#agent_password")
const button_agent = document.querySelector("#button_agent")

button_agent.addEventListener('click', (e)=> {
    e.preventDefault();
    create_agent(input_agente.value, input_agente_id.value, input_password.value);
})
function create_agent(agent_name,agent_id,password){
    fetch(`${API_URL}/agents/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            name: agent_name,
            agent_identifier: agent_id,
            password: password
        })
    })
    .then((response) => response.json())
    .then((data) => {
        console.log(data);
    });
}

//////////////////////////////////////////////////////////

/////////////////////////////////////////////////////////
const input_agente_id_borrar = document.querySelector("#id_agente_borrar")
const button_agent_borrar = document.querySelector("#agente_button_borrar")

button_agent_borrar.addEventListener('click', (e)=> {
    e.preventDefault();
    delete_agent(input_agente_id_borrar.value);
})
function delete_agent(agent_id){
    fetch(`${API_URL}/agents/${agent_id}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
        })
    })
    .then((response) => response.json())
    .then((data) => {
        console.log(data);
    });
}

//////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////
const input_plate_borrar = document.querySelector("#plate_vehiculo_borrar")
const button_vehicle_borrar = document.querySelector("#vehiculo_button_borrar")

button_vehicle_borrar.addEventListener('click', (e)=> {
    e.preventDefault();
    delete_vehicle(input_plate_borrar.value);
})
function delete_vehicle(plate){
    fetch(`${API_URL}/vehicles/${plate}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
        })
    })
    .then((response) => response.json())
    .then((data) => {
        console.log(data);
    });
}

//////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////
const input_person_borrar = document.querySelector("#id_persona_borrar")
const button_person_borrar = document.querySelector("#persona_button_borrar")

button_person_borrar.addEventListener('click', (e)=> {
    e.preventDefault();
    delete_person(input_person_borrar.value);
})
function delete_person(id){
    fetch(`${API_URL}/people/${id}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
        })
    })
    .then((response) => response.json())
    .then((data) => {
        console.log(data);
    });
}

//////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////
const input_person_cambiar = document.querySelector("#id_persona_cambiar")
const input_name_person_cambiar = document.querySelector("#nombre_persona_cambiar")
const button_person_cambiar = document.querySelector("#persona_button_modificar")

button_person_cambiar.addEventListener('click', (e)=> {
    e.preventDefault();
    update_person(input_person_cambiar.value,input_name_person_cambiar.value);
})
function update_person(id,person_name){
    const url = new URL(`${API_URL}/people/${id}`);
    url.searchParams.append('name', person_name);
    fetch(url, {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then((response) => response.json())
    .then((data) => {
        console.log(data);
    });
}
//////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////
const placa_vehiculo_cambiar = document.querySelector("#placa_vehiculo_cambiar")
const marca_cambiar = document.querySelector("#marca_cambiar")
const vehiculo_button_modificar = document.querySelector("#vehiculo_button_modificar")

vehiculo_button_modificar.addEventListener('click', (e)=> {
    e.preventDefault();
    update_vehicle(placa_vehiculo_cambiar.value,marca_cambiar.value);
})
function update_vehicle(placa,marca){
    const url = new URL(`${API_URL}/vehicles/${placa}`);
    url.searchParams.append('brand', marca);
    fetch(url, {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then((response) => response.json())
    .then((data) => {
        console.log(data);
    });
}
//////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////
const id_agente_cambiar = document.querySelector("#id_agente_cambiar")
const nombre_agente_cambiar = document.querySelector("#nombre_agente_cambiar")
const agente_button_modificar = document.querySelector("#agente_button_modificar")

agente_button_modificar.addEventListener('click', (e)=> {
    e.preventDefault();
    update_agent(id_agente_cambiar.value,nombre_agente_cambiar.value);
})
function update_agent(id,nombre){
    const url = new URL(`${API_URL}/agents/${id}`);
    url.searchParams.append('name', nombre);
    fetch(url, {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then((response) => response.json())
    .then((data) => {
        console.log(data);
    });
}
//////////////////////////////////////////////////////////