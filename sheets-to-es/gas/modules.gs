function toCsv() {
  // Year in JST
  let year = Utilities.formatDate(new Date(), 'Asia/Tokyo', 'yyyy');

  // csv
  let csv = '';

  for(m=1; m <= 12; m++) {
    let sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(year+'-'+m.toString().padStart(2, '0'));
    let range = sheet.getRange('E18:E48').getValues()

    csv = csv+year+'-'+m.toString().padStart(2, '0')+','

    // Clear columns with no value
    for(i=0; i < range.length; i++) {
      if(range[i].toString().length > 0) {
        csv = csv+range[i]+','
      }
    }

    csv = csv+'\n'
  } 

  blob = createBlob(csv, 'income-'+year)
  writeDrive(blob)
}

function createBlob(csv, fileName) {
  const contentType = 'text/csv';
  const charset = 'utf-8';
  const blob = Utilities.newBlob('', contentType, fileName).setDataFromString(csv, charset);
  return blob;
}

function writeDrive(blob) {
  const folderId = '1xh_p115n3JKwVcEEbb9TOWlF9W3pZZqc';
  const drive = DriveApp.getFolderById(folderId);
  drive.createFile(blob);
}
