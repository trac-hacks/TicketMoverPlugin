"""
Ticket sidebar for moving tickets
"""

from pkg_resources import resource_filename
from ticketmoverplugin.ticketmover import TicketMover
from ticketsidebarprovider import ITicketSidebarProvider
from trac.config import Option
from trac.core import *
from trac.web.api import IRequestHandler
from trac.web.chrome import Chrome
from trac.web.chrome import ITemplateProvider

class TicketMoverSidebar(Component):

    implements(ITicketSidebarProvider, ITemplateProvider)

    permission = Option('ticket', 'move_permission', 'TICKET_ADMIN',
                        "permission needed to move tickets between Trac projects")


    ### methods for ITicketSidebarProvider

    def enabled(self, req, ticket):
        if not self.permission in req.perm:
            return False
        tm = TicketMover(self.env)
        projects = tm.projects(req.authname)
        return bool(projects)

    def content(self, req, ticket):
        tm = TicketMover(self.env)
        projects = tm.projects(req.authname)
        chrome = Chrome(self.env)
        template = chrome.load_template('ticketmover-sidebar.html')
        data = { 'projects': projects,
                 'req': req,
                 'ticket': ticket }
        return template.generate(**data)
        

    ### methods for ITemplateProvider

    """Extension point interface for components that provide their own
    ClearSilver templates and accompanying static resources.
    """

    def get_htdocs_dirs(self):
        """Return a list of directories with static resources (such as style
        sheets, images, etc.)

        Each item in the list must be a `(prefix, abspath)` tuple. The
        `prefix` part defines the path in the URL that requests to these
        resources are prefixed with.
        
        The `abspath` is the absolute path to the directory containing the
        resources on the local file system.
        """
        return []

    def get_templates_dirs(self):
        """Return a list of directories containing the provided template
        files.
        """
        return [resource_filename(__name__, 'templates')]
        
class TicketMoverHandler(Component):

    permission = Option('ticket', 'move_permission', 'TICKET_ADMIN',
                        "permission needed to move tickets between Trac projects")
    
    implements(IRequestHandler)

    ### methods for IRequestHandler

    """Extension point interface for request handlers."""

    def match_request(self, req):
        """Return whether the handler wants to process the given request."""
        return req.method == 'POST' and req.path_info.rstrip('/') == '/ticket/move'

    def process_request(self, req):
        """Process the request. For ClearSilver, return a (template_name,
        content_type) tuple, where `template` is the ClearSilver template to use
        (either a `neo_cs.CS` object, or the file name of the template), and
        `content_type` is the MIME type of the content. For Genshi, return a
        (template_name, data, content_type) tuple, where `data` is a dictionary
        of substitutions for the template.

        For both templating systems, "text/html" is assumed if `content_type` is
        `None`.

        Note that if template processing should not occur, this method can
        simply send the response itself and not return anything.
        """
        
        assert self.permission in req.perm

        tm = TicketMover(self.env)
        new_location = tm.move(req.args['ticket'], req.authname, req.args['project'], 'delete' in req.args)

        if 'delete' in req.args:
            req.redirect(new_location)
        else:
            req.redirect(req.href('/ticket/%s' % req.args['ticket']))
        
