from trac.core import Component, implements
from trac.ticket.api import ITicketManipulator
import time
from datetime import date

class SoftDueDate(Component):
	implements(ITicketManipulator)

	def prepare_ticket(self, req, ticket, fields, actions):
		pass

	# TODO: expose this map through the Admin interface
	_priority_to_seconds = {
		'Urgent (< 1 dag)': 1 * 24 * 3600,
		'Hoog (< 3 dagen)': 3 * 24 * 3600,
		'Normaal (< 7 dagen)': 7 * 24 * 3600,
		'Laag (< 14 dagen)': 14 * 24 * 3600,
		'Nihil (< 1 maand)': 30 * 24 * 3600,
		'Een keer': 0,
	}

	def validate_ticket(self, req, ticket):
		if 'priority' not in ticket._old or ticket._old['priority'] != ticket['priority']:
			seconds = self._priority_to_seconds[ticket['priority']]
			if seconds is None:
				return [('priority', "Priority " + ticket['priority'] + " is unknown in priority map of soft-due-date convertor")]
			if seconds is 0:
				ticket['soft_due_date'] = ""
				return []
			thetime = time.time() + seconds
			thedate = date.fromtimestamp(thetime)
			ticket['soft_due_date'] = "%04d-%02d-%02d" % \
				(thedate.year, thedate.month, thedate.day)
			return []
		return []

