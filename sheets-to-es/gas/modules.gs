function toCsv() {
  // Year in JST
  let year = Utilities.formatDate(new Date(), 'Asia/Tokyo', 'yyyy');

  // csv
  let csv = setHeader()+'\n';

  for(m=1; m <= 12; m++) {
    let sheet = SpreadsheetApp
                    .getActiveSpreadsheet()
                    .getSheetByName(year+'-'+m.toString().padStart(2, '0'));

    // Column cashout
    cash_out = parse(sheet, 'E3:E47');

    csv = csv
            +year+'-'+m.toString().padStart(2, '0')+'-01'
            +','
            +cash_out+'\n';
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

function setHeader() {
  let header = 'report_date,income_tax,resident_tax,life_insurance,employment_insurance,health_insurance,welfare_pension,savings,securities,401k,rent,electricity,gas,water,newspaper,cable_tv,tennis_club,pilates,nhk,parking,car,creditcard_visa,creditcard_view,creditcard_mc,basic_life,remote_work';

  return header
}
