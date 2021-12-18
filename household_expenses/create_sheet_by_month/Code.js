function CreateSheets() { 

  var source = SpreadsheetApp.getActiveSpreadsheet();
  var sheet  = source.getSheets()[1];
  var destination = SpreadsheetApp.getActiveSpreadsheet();
  var now = new Date()
 
  for(i=0; i < 12; i++) {
    let month_name = Intl.DateTimeFormat(
      'en', 
      { month: 'short' }).format(new Date(now.getFullYear(), i));  
    copied_sheet = sheet.copyTo(destination)
    copied_sheet.setName(month_name);
    copied_sheet.getRange('C1')
      .setValue((now.getFullYear()+1).toString()+'-'+(i+1).toString())
  }  
}
