document.addEventListener('DOMContentLoaded', function () {

  // For creating new client
  const add_new_client = document.querySelector("#add_new_client");
  add_new_client.addEventListener('submit', (event) => {
    event.preventDefault();

    const name = add_new_client.name.value;
    const address = add_new_client.address.value;
    const image = add_new_client.image.files[0];

    const formData = new FormData();
    formData.append('name', name);
    formData.append('address', address);
    formData.append('image', image);

    fetch('/estimate/add_new_client', {
      method: "POST",
      body: formData
    })
      .then(response => response.json())
      .then(result => {
        console.log(result);
        location.reload();
      })
      .catch(error => {
        console.error(error);
      });

    return false;
  });


  // To display create new client form as a pop-up
  const modal = document.querySelector("#add_new_client_modal");
  const add_new_client_btn = document.querySelector("#add_new_client_btn");

  add_new_client_btn.addEventListener('click', () => {
    modal.style.display = "block";
  })

  window.addEventListener('click', (event) => {
    if (event.target == modal) {
      modal.style.display = "none";
    }
  })


});


function showScopeItems(scopeId) {
  fetch('/estimate/get_scope_items/' + scopeId)
      .then(response => response.json())
      .then(data => {
          console.log(data)
          let html = '<h2 class="second-header">' + data[0].scope_name + '</h2><table class="scope_table">';
          html += '<thead>';
          html += ' <tr>';
          html += '  <th colspan="2" style="width: 20rem;">Description</th>';
          html += '  <th style="width: 7rem;">Quantity</th>';
          html += '  <th style="width: 7rem;">Unit</th>';
          html += '  <th>Unit Price</th>';
          html += '  <th>Amount</th>';
          html += ' </tr>';
          html += '</thead>';
          html += '<tbody>';
          html += ' <tr><td colspan="6"><b>Material</b></td><td></td><td></td><td></td>';
          for (let i = 0; i < data.length; i++) {
            if (data[i].type === "material") {
              html += '<tr>';
              html += ' <td style="border-right: 0;">' + data[i].name + '</td>';
              html += ' <td style="border-left: 0;"><form action="/estimate/remove_item/' + data[i].project_id + '" method="post"><input type="hidden" name="item_id" value="' + data[i].id + '"><input type="submit" value="Delete"></form></td>';
              html += ' <td>' + data[i].quantity + '</td>';
              html += ' <td>' + data[i].unit + '</td>';
              html += ' <td>' + data[i].unit_price + '</td>';
              html += ' <td>' + data[i].amount + '</td>';
              html += '</tr>';
            }   
          }
          html += ' <tr><td colspan="6"><b>Labor</b></td><td></td><td></td><td></td>';
          for (let i = 0; i < data.length; i++) {
            if (data[i].type === "labor") {
              html += '<tr>';
              html += ' <td style="border-right: 0;">' + data[i].name + '</td>';
              html += ' <td style="border-left: 0;"><form action="/estimate/remove_item/' + data[i].project_id + '" method="post"><input type="hidden" name="item_id" value="' + data[i].id + '"><input type="submit" value="Delete"></form></td>';
              html += ' <td>' + data[i].quantity + '</td>';
              html += ' <td>' + data[i].unit + '</td>';
              html += ' <td>' + data[i].unit_price + '</td>';
              html += ' <td>' + data[i].amount + '</td>';
              html += '</tr>';
            }   
          }
          html += ' <tr><td colspan="6"><b>Equipment</b></td><td></td><td></td><td></td>';
          for (let i = 0; i < data.length; i++) {
            if (data[i].type === "equipment") {
              html += '<tr>';
              html += ' <td style="border-right: 0;">' + data[i].name + '</td>';
              html += ' <td style="border-left: 0;"><form action="/estimate/remove_item/' + data[i].project_id + '" method="post"><input type="hidden" name="item_id" value="' + data[i].id + '"><input type="submit" value="Delete"></form></td>';
              html += ' <td>' + data[i].quantity + '</td>';
              html += ' <td>' + data[i].unit + '</td>';
              html += ' <td>' + data[i].unit_price + '</td>';
              html += ' <td>' + data[i].amount + '</td>';
              html += '</tr>';
            }   
          }
          html += '</tbody>';
          html += '</table>';

          document.querySelector("#scope_items").innerHTML = html;
      });
}
