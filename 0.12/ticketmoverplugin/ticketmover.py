"""
TicketMoverPlugin:
a plugin for Trac to move tickets from one Trac instance to another
See:
 * http://trac-hacks.org/wiki/DataMoverPlugin
 * http://trac.edgewall.org
"""

import os
import shutil

from trac.config import ListOption
from trac.config import Option
from trac.core import *
from trac.env import open_environment
from trac.perm import PermissionCache
from trac.web.api import ITemplateStreamFilter
from trac.ticket import Ticket
from trac.ticket.api import ITicketActionController
from tracsqlhelper import get_all_dict
from tracsqlhelper import insert_row_from_dict

class TicketMover(Component):
    ### methods for ITemplateStreamFilter

    """Filter a Genshi event stream prior to rendering."""

    def filter_stream(self, req, method, filename, stream, data):
        """Return a filtered Genshi event stream, or the original unfiltered
        stream if no match.

        `req` is the current request object, `method` is the Genshi render
        method (xml, xhtml or text), `filename` is the filename of the template
        to be rendered, `stream` is the event stream and `data` is the data for
        the current template.

        See the Genshi documentation for more information.
        """

    ### methods for ITicketActionController

    """Extension point interface for components willing to participate
    in the ticket workflow.

    This is mainly about controlling the changes to the ticket ''status'',
    though not restricted to it.
    """

    def apply_action_side_effects(self, req, ticket, action):
        """Perform side effects once all changes have been made to the ticket.

        Multiple controllers might be involved, so the apply side-effects
        offers a chance to trigger a side-effect based on the given `action`
        after the new state of the ticket has been saved.

        This method will only be called if the controller claimed to handle
        the given `action` in the call to `get_ticket_actions`.
        """

    def get_all_status(self):
        """Returns an iterable of all the possible values for the ''status''
        field this action controller knows about.

        This will be used to populate the query options and the like.
        It is assumed that the initial status of a ticket is 'new' and
        the terminal status of a ticket is 'closed'.
        """

    def get_ticket_actions(self, req, ticket):
        """Return an iterable of `(weight, action)` tuples corresponding to
        the actions that are contributed by this component.
        That list may vary given the current state of the ticket and the
        actual request parameter.

        `action` is a key used to identify that particular action.
        (note that 'history' and 'diff' are reserved and should not be used
        by plugins)
        
        The actions will be presented on the page in descending order of the
        integer weight. The first action in the list is used as the default
        action.

        When in doubt, use a weight of 0."""

    def get_ticket_changes(self, req, ticket, action):
        """Return a dictionary of ticket field changes.

        This method must not have any side-effects because it will also
        be called in preview mode (`req.args['preview']` will be set, then).
        See `apply_action_side_effects` for that. If the latter indeed triggers
        some side-effects, it is advised to emit a warning
        (`trac.web.chrome.add_warning(req, reason)`) when this method is called
        in preview mode.

        This method will only be called if the controller claimed to handle
        the given `action` in the call to `get_ticket_actions`.
        """

    def render_ticket_action_control(self, req, ticket, action):
        """Return a tuple in the form of `(label, control, hint)`

        `label` is a short text that will be used when listing the action,
        `control` is the markup for the action control and `hint` should
        explain what will happen if this action is taken.
        
        This method will only be called if the controller claimed to handle
        the given `action` in the call to `get_ticket_actions`.

        Note that the radio button for the action has an `id` of
        `"action_%s" % action`.  Any `id`s used in `control` need to be made
        unique.  The method used in the default ITicketActionController is to
        use `"action_%s_something" % action`.
        """

    ### internal methods

    def projects(self):
        self.env.log.debug("Building list of peer environments")
        base_path, _project = os.path.split(self.env.path)
        return [i for i in os.listdir(base_path)
                if i != _project
                and os.path.exists(os.path.join(base_path, i,"conf","trac.ini"))]

    def move(self, ticket_id, author, env, delete=False):
        """
        move a ticket to another environment
        
        env: environment to move to
        """
        tables = { 'attachment': 'id',
                   'ticket_change': 'ticket', }

        # open the environment if it is a string
        if isinstance(env, basestring):
            base_path, _project = os.path.split(self.env.path)
            env = open_environment(os.path.join(base_path, env))
            PermissionCache(env,author).require('TICKET_CREATE')

        # get the old ticket
        old_ticket = Ticket(self.env, ticket_id)

        # make a new ticket from the old ticket values
        new_ticket = Ticket(env)
        new_ticket.values = old_ticket.values.copy()
        new_ticket.insert(when=old_ticket.time_created)

        # copy the changelog and attachment DBs
        for table, _id in tables.items():
            for row in get_all_dict(self.env, "SELECT * FROM %s WHERE %s = '%s'" % (table, _id, ticket_id)):
                row[_id] = new_ticket.id
                insert_row_from_dict(env, table, row)

        # copy the attachments
        src_attachment_dir = os.path.join(self.env.path, 'attachments', 'ticket', str(ticket_id))
        if os.path.exists(src_attachment_dir):
            dest_attachment_dir = os.path.join(env.path, 'attachments', 'ticket')
            if not os.path.exists(dest_attachment_dir):
                os.makedirs(dest_attachment_dir)
            dest_attachment_dir = os.path.join(dest_attachment_dir, str(new_ticket.id))
            shutil.copytree(src_attachment_dir, dest_attachment_dir)

        # note the previous location on the new ticket
        new_ticket.save_changes(author, 'moved from %s' % self.env.abs_href('ticket', ticket_id))

        # location of new ticket
        new_location = env.abs_href('ticket', new_ticket.id)

        if delete:
            old_ticket.delete()
        else:
            # close old ticket and point to new one
            old_ticket['status'] = u'closed'
            old_ticket['resolution'] = u'moved'
            old_ticket.save_changes(author, u'moved to %s' % new_location)

        # return the new location
        return new_location
