import gdata.docs
import gdata.docs.service
import gdata.spreadsheet.service
import re, os
import gdata.docs.client
import gdata.acl.data
import pprint

# DATA
username=
password=
students_data= # Google Sheets format : "timestamp / firstname / lastname / email"
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
for row in rows:
 firstname=row.custom['firstname'].text
 lastname=row.custom['lastname'].text
 email=row.custom['email'].text
 title_doc=assignment+' - '+lastname


 feeduri='/feeds/default/private/full?title='+title_doc+'&title-exact=true&max-results=5'
 feed2 = client.GetResources(uri=feeduri)
 if not feed2.entry:
  print 'No document of that title.\n'
 doc_id=feed2.entry[0]
 aclfeed=client.GetAcl(doc_id)
 for aclentry in aclfeed.entry:
 	if aclentry.scope.value==professor or aclentry.scope.value==username:
 		continue
 	client.DeleteAclEntry(aclentry)
  	print(aclentry.scope.value + ' no longer has permission to view ' + title_doc)


 # pp=pprint.PrettyPrinter(indent=4)
 # pp.pprint(aclfeed.ToString())

 # REMOVE FIRST GRANTED PERMISSIONS FROM THE DOCUMENTS (OLD)
 # acl_entry = client.GetAclPermissions(doc_id.resource_id.text).entry[1]
 # client.Delete(acl_entry.GetEditLink().href, force=True)
