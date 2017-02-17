Originally adapted from python [scripts written](http://www.philosophyetc.net/2010/11/grading-with-google-docs.html) by Richard Yetter Chappel at the University of York, this set of scripts was written in collaboration with [David Warden](https://github.com/dfwarden) from [SUNY Geneseo Computing and Information Technology](https://www.geneseo.edu/cit/staff). It uses the (now outdated) Google Docs API to manage student prose assignments, allowing the instructor to be "Owner" of consistently-named files.

`Createdocs.py` creates a document for a given assignment, course and title designated in the script itself, for each student on an appropriately formatted class list on Google Sheets. Each student's document is shared individually with their Google account listed in the class list spreadsheet. Students paste the content of their assignments into the provided document.

`RemovePermissions.py` is run at the deadline to revoke students' permission to edit or view their submissions while they are graded.

`ReturnPermissions.py` is used to return viewing permissions of the files to each student.

I am currently looking for someone to help me convert what has been done here using the old Google Docs API to the [newer Google Drive API](https://developers.google.com/api-client-library/python/apis/drive/v2), since I am unfamilliar with the new API, and my python knowledge is quite rusty.
