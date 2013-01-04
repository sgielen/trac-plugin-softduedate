# Soft Due Date plugin

This is the Soft Due Date plugin for Trac. It implements automatic setting of
a soft due-date field for every ticket based on its Priority.

## Known issues
* The soft due date is only set when a ticket is created/modified, so making
  this plugin useful after installing it on an active Trac installation
  requires a trivial change to all tickets.
* The soft due date ticket field can be set when creating/modifying a ticket,
  but the value to which it will be set is ignored.
* The soft due date can only be based on the priority at the moment.
* The priority-to-time-offset is currently hard-coded in the source, while it
  should be changeable using the administrator interface.

## Installation
Before you can use this module, you need to install the [DateFieldPlugin
module](http://trac-hacks.org/wiki/DateFieldPlugin). Then, add a
`soft_due_date` field to the configuration file:

    [ticket-custom]
    soft_due_date = text
    soft_due_date.date = true
    soft_due_date.date_empty = true
    soft_due_date.label = Soft Due Date
    soft_due_date.value =

In order to add the new soft due-date field to a Trac ticket report, change
your report query to something like this:

    SELECT id AS ticket, summary, [...],
      c.value AS soft_due_date
    FROM ticket t
    LEFT JOIN ticket_custom c ON t.id = c.ticket AND c.name = 'soft_due_date'

To sort the table by soft due date:

    ORDER BY date(c.value) ASC

Or, to sort the table keeping every unset `soft_due_date` at the bottom:

    ORDER BY case when date(c.value) then date(c.value)
      else date("9999-12-31") end ASC, created, [...]

It can also be used next to a configurable `due_date` field, after you added it
to the configuration file just like the `soft_due_date` field:

    SELECT id AS ticket, summary, [...],
      c.value AS soft_due_date,
      d.value AS due_date
    FROM ticket t
    LEFT JOIN ticket_custom c ON t.id = c.ticket AND c.name = 'soft_due_date'
    LEFT JOIN ticket_custom d ON t.id = d.ticket AND d.name = 'due_date'
    ORDER BY min(
      case when date(c.value) then date(c.value) else date("9999-12-31") end,
      case when date(d.value) then date(d.value) else date("9999-12-31") end
    ) ASC, created, [...]

## Author and license

This plugin was tested against Trac 0.12.3 using an SQLite database. Your
mileage may vary, I'm interested in hearing from you!

Copyright (c) 2013, Sjors Gielen
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met: 

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer. 
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution. 

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
