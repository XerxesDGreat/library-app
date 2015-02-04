# This depends on converting MARC records into XML using the utility
# mrc2xml.pl
marc_fields = {
	'control-fields': {
		'001': 'control_number',
		'005': 'last_transaction_ts'
	},
	'numbers-and-codes': {
		'020': {
			'a': 'isbn',
		},
		'090': {
			'a': 'local_call_number'
		}
	},
	'main-entry': {
		'100': {
			'a': 'personal_name'
		},
		'110': {
			'a': 'corporate)name'
		}
	},
	'title-and-title-related': {
		'245': {
			'a': 'title',
			'b': 'remainder_of_title',
			'c': 'statement_of_responsibility'
		},
	},
	'edition-imprint-etc': {
		'260': {
			'a': 'pub_place',
			'b': 'name_of_publisher',
			'c': 'date_of_publication'
		}
	},
	'physical-description': {
		'300': {
			'a': 'extent',
			'c': 'dimensions'
		}
	},
	'series-statement': {
		'490': {
			'a': 'series_statement',
			'v': 'volume_sequential_designation'
		}
	},
	'notes': {
		'500': {
			'a': 'general_note'
		},
		'520': {
			'a': 'summary'
		},
		'521': {
			'a': 'target_audience_note'
		}
	},
	'subject-access': {
		'650': {
			'a': 'topical_term_or_geographic_name'
		}
	},
	'series-added-entry': {
		'800': {
			'a': 'series_personal_name'
		}
	},
	'location': {
		'852': {
			'a': 'location',
			'b': 'sublocation_or_collection',
			'h': 'classification_part',
			'i': 'item_part',
			'j': 'shelving_control_number',
			'k': 'call_number_prefix',
			'p': 'piece_designation',
		}
	}
}

import xml.dom.minidom as MD
import os

with open(os.path.join(os.getcwd(), 'stdout.xml')) as f:
	xml_str = f.read()

dom_obj = MD.parseString(xml_str)

def get_text(nodelist):
	rc = []
	for node in nodelist:
		if node.nodeType == node.TEXT_NODE:
			rc.append(node.data)
	return ''.join(rc)

records = dom_obj.getElementsByTagName('mrcb')
record_objs = []
for r in records:
	record_obj = {}
	for section_name, section_def in marc_fields.iteritems():
		section_data_list = r.getElementsByTagName('mrcb-%s' % section_name)
		if len(section_data_list) < 1:
			continue
		section_data = section_data_list[0]
		for field_name, field_def in section_def.iteritems():
			field_data_list = section_data.getElementsByTagName('mrcb%s' % field_name)
			if len(field_data_list) < 1:
				continue
			field_data = field_data_list[0]
			if isinstance(field_def, basestring):
				record_obj[field_def] = get_text(field_data.childNodes)
			else:
				for sub_field_name, obj_key in field_def.iteritems():
					sub_field_data_list = field_data.getElementsByTagName('mrcb%s-%s' % (field_name, sub_field_name))
					if len(sub_field_data_list) < 1:
						continue
					sub_field_data = sub_field_data_list[0]
					record_obj[obj_key] = get_text(sub_field_data.childNodes)
	record_objs.append(record_obj)

import json
with open(os.path.join(os.getcwd(), 'catalog.json'), 'w') as f:
	f.write(json.dumps(record_objs))
				
			
