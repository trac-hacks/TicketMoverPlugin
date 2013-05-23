TicketMoverPlugin
=================

Allows copying or moving a ticket from one trac to a sibling trac
(i.e. a trac-environment in the same parent folder as the current trac
environment).

The user will need the TICKET\_ADMIN privilege on the current trac and
TICKET\_CREATE privilege on the target trac.

This plugin adds a new `Action` (alongside "leave as new", "resolve as
__", "accept", etc) of "Move to <list> and Delete Ticket <check>"



Installation
------------

1. python install the plugin.
2. Ensure the component is active either through the web admin or by
   adding to trac.ini
	[components]
	ticketmoverplugin.ticketmover = enabled
3. In trac.ini enable this as a workflow provider. Under the
   `[ticket]` section add `TicketMover` to the `workflow` list (comma
   delimitted).
