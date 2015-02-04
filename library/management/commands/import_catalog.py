# this depends upon the output of xml2json.py having converted the 
# marc records from xml to a json output
import os
import json
import re
from django.core.management.base import BaseCommand, make_option

from library.models import Author, Book
from django.contrib.admindocs.utils import trim_docstring

def getif(d, k):
	try:
		return d[k]
	except KeyError:
		return None

class Command(BaseCommand):
	help = 'Imports books into the catalog'

	option_list = BaseCommand.option_list + (
		make_option('--src', dest='source_file', help='file which contains the JSON to import', default=os.path.join(os.getcwd(), 'utils', 'catalog.json')),
	)

	def handle(self, **options):
		with open(options['source_file']) as f:
			to_import_json_str = f.read()

		to_import = json.loads(to_import_json_str)
		
		num_replace_pattern = re.compile(r'[^0-9]')
		new_control_number = 9999999

		for record in to_import:
			msg = []
			title = getif(record, 'title')
			if (title is None):
				print 'no title; can\'t do anything!'
				continue
			title = title.rstrip(' /')
			
			author = getif(record, 'personal_name')
			if author is None:
				author = getif(record, 'corporate)name')	

			author = self._author_from_string(author) if author else None
			
			isbn = getif(record, 'isbn')
			control_number = getif(record, 'control_number')
			if control_number is not None:
				control_number = int(num_replace_pattern.sub('', control_number))
			else:
				control_number = new_control_number
				new_control_number += 1
			subtitle = getif(record, 'remainder_of_title')
			
			try:
				potential_books = Book.objects.filter(title=title)
				book = None
				same_book = False
				for potential_book in potential_books:
					if potential_book.control_number is not None and potential_book.control_number == control_number:
						book = potential_book
						same_book = True
						break
					elif potential_book.control_number is None:
						book = potential_book
						msg.append('update_existing')
						break
				if same_book:
					print('%s exists; continuing' % book.full_title())
					continue
				elif book is None:
					book = Book(title=title)
					msg.append('create')
			except Book.DoesNotExist:
				book = Book(title=title)
				msg.append('create')
			
			msg.append(book.title)
			
			book.author = author
			book.isbn = isbn
			book.control_number = control_number
			book.local_call_number = getif(record, 'local_call_number')
			book.subtitle = subtitle
			book.statement_of_responsibility = getif(record, 'statement_of_responsibility')
			book.publish_location = getif(record, 'pub_place')
			book.publish_company = getif(record, 'name_of_publisher')
			book.publish_date = self._pub_date_from_string(getif(record, 'date_of_publication'))
			book.extent = getif(record, 'extent')
			book.dimensions = getif(record, 'dimensions')
			book.series_statement = getif(record, 'series_statement')
			book.volume_sequential_designation = getif(record, 'volume_sequential_designation')
			book.notes = getif(record, 'general_note')
			book.summary = getif(record, 'summary')
			book.target_audience = getif(record, 'target_audience_note')
			book.topic = getif(record, 'topical_term_or_geographic_name')
			
			series_author = getif(record, 'series_personal_name')
			if series_author is not None:
				series_author = self._author_from_string(series_author)
			book.series_personal_name = series_author
			
			book.save()
			msg.append('saved')
			print " ".join(msg)
			
	def _pub_date_from_string(self, pub_date_string):
		if pub_date_string is None:
			return None
		
		pub_date = -1
		import re
		pat = re.compile(r'[^0-9 ]')
		dates = pat.sub('', pub_date_string)
		for one_date in dates.split(' '):
			if len(one_date) == 0:
				continue
			if len(one_date) > 4:
				one_date = one_date[0:4]
			one_date = int(one_date)
			if one_date > pub_date:
				pub_date = one_date
		
		return pub_date
		
			
	def _author_from_string(self, author_string):
		author_parts = [p.strip() for p in author_string.split(',')]
		if len(author_parts) == 2:
			kwargs = {
				'last_name': author_parts[0],
				'first_name': author_parts[1]
			}
		else:
			kwargs = {
				'first_name': author_string
			}
			
		try:
			author = Author.objects.get(**kwargs)
		except Author.DoesNotExist:
			author = Author(**kwargs)
			author.save()
		
		return author