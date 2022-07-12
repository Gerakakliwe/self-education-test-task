/*
 * JavaScript file for the application to demonstrate
 * using the API
 */

// Create the namespace instance
let ns = {};

// Create the model instance
ns.model = (function() {
    'use strict';

    let $event_pump = $('body');

    // Return the API
    return {
        'read': function() {
            let ajax_options = {
                type: 'GET',
                url: 'api/employees',
                accepts: 'application/json',
                dataType: 'json'
            };
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('model_read_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
            })
        },
        create: function(employee) {
            let ajax_options = {
                type: 'POST',
                url: 'api/employees',
                accepts: 'application/json',
                contentType: 'application/json',
                dataType: 'json',
                data: JSON.stringify(employee)
            };
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('model_create_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
            })
        },
        update: function(employee) {
            let ajax_options = {
                type: 'PUT',
                url: `api/employees/${employee.employee_id}`,
                accepts: 'application/json',
                contentType: 'application/json',
                dataType: 'json',
                data: JSON.stringify(employee)
            };
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('model_update_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
            })
        },
        'delete': function(employee_id) {
            let ajax_options = {
                type: 'DELETE',
                url: `api/employees/${employee_id}`,
                accepts: 'application/json',
                contentType: 'plain/text'
            };
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('model_delete_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
            })
        }
    };
}());

// Create the view instance
ns.view = (function() {
    'use strict';

    let $employee_id = $('#employee_id'),
        $fname = $('#fname'),
        $lname = $('#lname'),
        $position = $('#position'),
        $computer_name = $('#computer_name');

    // return the API
    return {
        reset: function() {
            $employee_id.val('');
            $lname.val('');
            $position.val('');
            $computer_name.val('');
            $fname.val('').focus();
        },
        update_editor: function(employee) {
            $employee_id.val(employee.employee_id);
            $lname.val(employee.lname);
            $position.val(employee.position);
            $computer_name.val(employee.computer_name);
            $fname.val(employee.fname).focus();
        },
        build_table: function(employees) {
            let rows = ''

            // clear the table
            $('.employees table > tbody').empty();

            // did we get a employees array?
            if (employees) {
                for (let i=0, l=employees.length; i < l; i++) {
                    rows += `<tr data-employee-id="${employees[i].employee_id}">
                        <td class="fname">${employees[i].fname}</td>
                        <td class="lname">${employees[i].lname}</td>
                        <td class="position">${employees[i].position}</td>
                        <td class="computer_name">${employees[i].computer_name}</td>
                    </tr>`;
                }
                $('table > tbody').append(rows);
            }
        },
        error: function(error_msg) {
            $('.error')
                .text(error_msg)
                .css('visibility', 'visible');
            setTimeout(function() {
                $('.error').css('visibility', 'hidden');
            }, 3000)
        }
    };
}());

// Create the controller
ns.controller = (function(m, v) {
    'use strict';

    let model = m,
        view = v,
        $event_pump = $('body'),
        $employee_id = $('#employee_id'),
        $fname = $('#fname'),
        $lname = $('#lname'),
        $position = $('#position'),
        $computer_name = $('#computer_name');

    // Get the data from the model after the controller is done initializing
    setTimeout(function() {
        model.read();
    }, 100)

    // Validate input
    function validate(fname, lname, position, computer_name) {
        return fname !== "" && lname !== "" && position !== "" && computer_name !== "";
    }

    // Create our event handlers
    $('#create').click(function(e) {
        let fname = $fname.val(),
            lname = $lname.val(),
            position = $position.val(),
            computer_name = $computer_name.val();

        e.preventDefault();

        if (validate(fname, lname, position, computer_name)) {
            model.create({
                'fname': fname,
                'lname': lname,
                'position': position,
                'computer_name': computer_name,
            })
        } else {
            alert('Problem with first or last name input');
        }
    });

    $('#update').click(function(e) {
        let employee_id = $employee_id.val(),
            fname = $fname.val(),
            lname = $lname.val(),
            position = $position.val(),
            computer_name = $computer_name.val();

        e.preventDefault();

        if (validate(fname, lname, position, computer_name)) {
            model.update({
                employee_id: employee_id,
                fname: fname,
                lname: lname,
                position: position,
                computer_name: computer_name,
            })
        } else {
            alert('Problem with first or last name input');
        }
        e.preventDefault();
    });

    $('#delete').click(function(e) {
        let employee_id = $employee_id.val();

        e.preventDefault();

        if (validate('placeholder', lname)) {
            model.delete(employee_id)
        } else {
            alert('Problem with first or last name input');
        }
        e.preventDefault();
    });

    $('#reset').click(function() {
        view.reset();
    })

    $('table > tbody').on('dblclick', 'tr', function(e) {
        let $target = $(e.target),
            employee_id,
            fname,
            lname,
            position,
            computer_name;

        employee_id = $target
            .parent()
            .attr('data-employee-id');

        fname = $target
            .parent()
            .find('td.fname')
            .text();

        lname = $target
            .parent()
            .find('td.lname')
            .text();

        view.update_editor({
            employee_id: employee_id,
            fname: fname,
            lname: lname,
            position: position,
            computer_name: computer_name,
        });
    });

    // Handle the model events
    $event_pump.on('model_read_success', function(e, data) {
        view.build_table(data);
        view.reset();
    });

    $event_pump.on('model_create_success', function(e, data) {
        model.read();
    });

    $event_pump.on('model_update_success', function(e, data) {
        model.read();
    });

    $event_pump.on('model_delete_success', function(e, data) {
        model.read();
    });

    $event_pump.on('model_error', function(e, xhr, textStatus, errorThrown) {
        let error_msg = textStatus + ': ' + errorThrown + ' - ' + xhr.responseJSON.detail;
        view.error(error_msg);
        console.log(error_msg);
    })
}(ns.model, ns.view));
