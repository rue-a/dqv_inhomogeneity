const editor = CodeMirror.fromTextArea(document.getElementById("code"), {
    mode: "application/sparql-query",
    matchBrackets: true,
})

document.getElementById("execute").addEventListener('click', sparql)

async function sparql() {
    // console.log(editor.getValue())
    let endpoint = document.getElementById("endpoint").value;
    let query = editor.getValue();
    console.log(query)
    const url = endpoint +
        '?query=' + encodeURIComponent(query) +
        '&format=json';
    console.log(url)

    document.getElementById("query_url").innerText = "\nQuery URL"
    document.getElementById("query_url").href = url
    const response = await fetch(url);




    if (response.ok) {
        const json = await response.json();

        sparql_json_response_2_html_table(json, document.getElementById("response"));
    } else {
        const error = await response.text()
        document.getElementById("response").innerText = "\n" + error
    }
}

function sparql_json_response_2_html_table(json_response, div) {
    div.innerText = "\n";
    const table = document.createElement("table");

    const table_head = document.createElement("thead");
    const head_row = document.createElement("tr");
    for (let variable of json_response.head.vars) {
        const head_col = document.createElement("th");
        head_col.innerText = variable;
        head_row.appendChild(head_col);
    }
    table_head.appendChild(head_row);
    table.appendChild(table_head);

    const table_body = document.createElement("tbody");
    for (let binding of json_response.results.bindings) {
        const row = document.createElement("tr");
        for (let variable of json_response.head.vars) {
            const cell = document.createElement("td");
            if (binding[variable]) {
                cell.innerText = binding[variable].type + ": " + binding[variable].value;
            }
            row.appendChild(cell)
        }
        table_body.appendChild(row)
        table.appendChild(table_body)
        div.appendChild(table);
    }
}