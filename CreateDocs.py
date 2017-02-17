import gdata.docs
import gdata.docs.service
import gdata.spreadsheet.service
import re, os
import gdata.docs.client
import gdata.acl.data

# DATA
username=
password=
students_data=
classcode=
assignment=
#professor=

# Connect to Google-Spreadsheet
gd_client = gdata.spreadsheet.service.SpreadsheetsService()
gd_client.email = username
gd_client.password = password
gd_client.source = 'OpenSource-CreateDocs-v1'
gd_client.ProgrammaticLogin()

# Connect to Google-DocList
client = gdata.docs.client.DocsClient(source='OpenSource-CreateDocs-v1')
client.ssl = True
client.http_client.debug = False
client = gdata.docs.client.DocsClient(source='OpenSource-CreateDocs-v1')
client.ClientLogin(username, password, client.source);

#
q = gdata.spreadsheet.service.DocumentQuery()
q['title'] = students_data
q['title-exact'] = 'true'
feed = gd_client.GetSpreadsheetsFeed(query=q)
spreadsheet_id = feed.entry[0].id.text.rsplit('/',1)[1]
feed = gd_client.GetWorksheetsFeed(spreadsheet_id)
worksheet_id = feed.entry[0].id.text.rsplit('/',1)[1]
rows = gd_client.GetListFeed(spreadsheet_id, worksheet_id).entry

doclist=client.GetResources()

for row in rows:
 firstname=row.custom['firstname'].text
 lastname=row.custom['lastname'].text
 email=row.custom['email'].text
 title_doc=assignment+' - '+lastname

 found=False
 for doc in doclist.entry:
  	if doc.title.text==title_doc:
		found=True
 		print(doc.title.text + ' already exists.')
 	 	break
 if found==False:

 # CREATE A NEW DOCUMENT FOR EACH STUDENT
  new_doc = gdata.docs.data.Resource(type='document', title=title_doc)
  new_doc = client.CreateResource(new_doc)
  print 'Created:', new_doc.title.text
  scope = gdata.acl.data.AclScope(value=email, type='user')
  role = gdata.acl.data.AclRole(value='writer')
  acl_entry = gdata.docs.data.AclEntry(scope=scope, role=role)
  client.AddAclEntry(new_doc, acl_entry, send_notification=True)

#  scope = gdata.acl.data.AclScope(value=professor, type='user')
#  role = gdata.acl.data.AclRole(value='writer')
#  acl_entry = gdata.docs.data.AclEntry(scope=scope, role=role)
#  client.AddAclEntry(new_doc, acl_entry, send_notification=False)
