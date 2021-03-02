

const updateData = async() => {


    const data = await fetch("http://localhost:8080/data",
        {
            method: 'GET', // *GET, POST, PUT, DELETE, etc.
            mode: '*cors', // no-cors, *cors, same-origin
            cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
            credentials: 'same-origin', // include, *same-origin, omit
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(function (response) {
            console.log(response);
            return response.json();
        })
        .then(function (myJson) {
            console.log(myJson.ip);
        })
        .catch(function (error) {
            console.log("Error: " + error);
        });

    return data;
}


function main(){
    updateData();
    return;
}

main()