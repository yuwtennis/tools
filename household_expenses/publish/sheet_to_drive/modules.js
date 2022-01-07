function toCsv() {
  let fileId = '1X4TPTMNBJLy0P2grxiBYRURR9nMKA7iC'
  // Year in JST
  let year = Utilities.formatDate(new Date(), 'Asia/Tokyo', 'yyyy');

  // csv
  let csv = setHeader()+'\n';

  for(m=1; m <= 12; m++) {
    let monthName = new Date(year, m).toLocaleDateString('en-US', {month: 'short'})
    let sheet = SpreadsheetApp
                    .getActiveSpreadsheet()
                    .getSheetByName(monthName);

    // Column cashout
    cash_out = parse(sheet, 'E3:E47');

    csv = csv
            +year+'-'+m.toString().padStart(2, '0')+'-01'
            +','
            +cash_out+'\n';
  } 

  blob = createBlob(csv, 'income-'+year)
  writeDrive(blob, fileId)
}

function createBlob(csv, fileName) {
  let contentType = 'text/csv';
  let charset = 'utf-8';
  let blob = Utilities.newBlob('', contentType, fileName).setDataFromString(csv, charset);

  return blob;
}

function writeDrive(blob, fileId) {
  Drive.Files.update({}, fileId, blob)
}

function parse(sheet, a1notation) {
  let range = sheet.getRange(a1notation).getValues()

  return range.filter(function(e) {
    return e != '';
  }).join();
}

function setHeader() {
  let header = 'report_date,income_tax,resident_tax,life_insurance,employment_insurance,health_insurance,welfare_pension,savings,securities,n401k,rent,electricity,gas,water,newspaper,cable_tv,tennis_club,pilates,nhk,parking,car,creditcard_visa,creditcard_view,creditcard_mc,basic_life,remote_work';

  return header
}

