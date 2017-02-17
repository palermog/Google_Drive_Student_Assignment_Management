import gdata.docs
import gdata.docs.service
import gdata.spreadsheet.service
import re, os
import gdata.docs.client
import gdata.acl.data

# DATA
username=
password=
students_data= # Google Sheets format : "timestamp / firstname / lastname / email"
classcode=
assignment=

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
for row in rows:
 firstname=row.custom['firstname'].text
 lastname=row.custom['lastname'].text
 email=row.custom['email'].text
 title_doc=assignment+' - '+lastname

 print title_doc

 feeduri='/feeds/default/private/full?title='+title_doc+'&title-exact=true&max-results=5'
 feed2 = client.GetResources(uri=feeduri)
 if not feed2.entry:
  print 'No document of that title.\n'
 doc_id=feed2.entry[0]

 aclfeed=client.GetAcl(doc_id)
 found=False
 for aclentry in aclfeed.entry:
 	if aclentry.scope.value==email:
		found=True
 		print aclentry.scope.value + ' already has permission.'
 	 	break
 if found==False:

# CHANGE THE PERMISSIONS OF THE DOCUMENTS (THE STUDENT IS 'A READER' and a 'COMMENTER')
  scope = gdata.acl.data.AclScope(value=email, type='user')
  role = gdata.acl.data.AclRole(value='reader')
  role2 = gdata.acl.data.AclAdditionalRole(value='commenter')
  acl_entry = gdata.docs.data.AclEntry(scope=scope, role=role, additional_role=role2)
  client.AddAclEntry(doc_id, acl_entry, send_notifications=True)
  print title_doc + ' permissions restored to ' + email + '.'
