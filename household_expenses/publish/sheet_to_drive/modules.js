function toCsv() {
  let fileId = '1X4TPTMNBJLy0P2grxiBYRURR9nMKA7iC'
  // Year in JST
  let year = Utilities.formatDate(new Date(), 'Asia/Tokyo', 'yyyy');

  // csv
  let csv = setHeader()+'\n';

  for(m=0; m < 12; m++) {
    let monthName = new Date(year, m).toLocaleDateString('en-US', {month: 'short'})
    let sheet = SpreadsheetApp
                    .getActiveSpreadsheet()
                    .getSheetByName(monthName);

    // Column cashout
    cash_out = parse(sheet, 'E3:E54');

    csv = csv
            +year+'-'+(m+1).toString().padStart(2, '0')+'-01'
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
  let header = 'report_date,income_tax,resident_tax,life_insurance,nursing_insurance,employment_insurance,health_insurance,welfare_pension,savings,securities,n401k,mortgage,administrative_fee,repair_fee,electricity,gas,water,electricity_usage_in_kwh,gas_usage_in_m3,water_usage_in_m3,internet,cable_tv,tennis_club,pilates,nhk,car_parking,bicycle_parking,car_management,creditcard_visa,creditcard_view,creditcard_mc,basic_life';

  return header
}

