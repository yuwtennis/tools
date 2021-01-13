function toCsv() {
  // Year in JST
  let year = Utilities.formatDate(new Date(), 'Asia/Tokyo', 'yyyy');

  // csv
  let csv = '';

  for(m=1; m <= 12; m++) {
    let sheet = SpreadsheetApp
                    .getActiveSpreadsheet()
                    .getSheetByName(year+'-'+m.toString().padStart(2, '0'));

    // Column cashout
    cash_out = parse(sheet, 'E3:E47');

    csv = csv
            +year+'-'+m.toString().padStart(2, '0')
            +','
            +cash_out
            +'\n';
  } 

  blob = createBlob(csv, 'income-'+year)
  writeDrive(blob, '1xh_p115n3JKwVcEEbb9TOWlF9W3pZZqc')
}

function createBlob(csv, fileName) {
  let contentType = 'text/csv';
  let charset = 'utf-8';
  let blob = Utilities.newBlob('', contentType, fileName).setDataFromString(csv, charset);

  return blob;
}

function writeDrive(blob, folderId) {
  const drive = DriveApp.getFolderById(folderId);
  drive.createFile(blob);
}

function parse(sheet, a1notation) {
  let range = sheet.getRange(a1notation).getValues()

  return range.filter(function(e) {
    return e != '';
  }).join();
}
