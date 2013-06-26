TicketMoverPlugin
=================

Allows copying or moving a ticket from one trac to a sibling trac
(i.e. a trac-environment in the same parent folder as the current trac
environment).

The user will need the TICKET\_ADMIN privilege on the current trac and
TICKET\_CREATE privilege on the target trac.

This plugin adds a new `Action` (alongside "leave as new", "resolve as
__", "accept", etc) of "Move to DROPDOWNLIST and Delete Ticket CHECKBOX"
I.e. you can move the ticket somewhere else and optionally delete it
from here (if you click the checkbox).

The DROPDOWNLIST is populated with all trac environments that are
siblings to the current one. Permissions are checked on the target
trac when you actually attempt to move a ticket to there.

Requirements
------------

This plugin requires
[TracSqlHelperScript](http://trac-hacks.org/wiki/TracSqlHelperScript),
though installing with pip handles this automatically.

Installation
------------

1. python install the plugin. If you install with pip (e.g. `pip
   install .`) it will handle the TracSqlHelperScript dependency for
   you.

2. Ensure the component is active either through the web admin or by
   adding to trac.ini
```ini
    [components]
    ticketmoverplugin.ticketmover = enabled
```    

3. In trac.ini enable this as a workflow provider. Under the
   `[ticket]` section add `TicketMover` to the `workflow` list (comma
   delimitted). e.g.
```ini
    [ticket]
    workflow = ConfigurableTicketWorkflow,TicketMover
```
