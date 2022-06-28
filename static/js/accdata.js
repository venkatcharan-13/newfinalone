const endpoint = 'api/pnlData/';
const endpoint2 = 'api/balsheetData';
const endpoint3 = 'api/cashflowData';

$.ajax({
  method: "GET",
  url: endpoint,
  success: function(data) {
    console.log("Success PNL");
    fillPnlTableRows(data.income, 'income');
    fillPnlTableRows(data.cost_of_goods_sold, 'cogs');
    fillPnlTableExpenses(data.expense, 'expense');
    fillPnlTableTotals(data.gross_profit, 'grossprofit', 'Gross Profit');
    fillPnlTableTotals(data.ebitda, 'ebitda', 'EBITDA');
    fillPnlTableTotals(data.depreciation_expenses, 'dep_exp', 'Depreciation Expenses');
    fillPnlTableTotals(data.pbit, 'pbit', 'PBIT');
    fillPnlTableTotals(data.interest_expenses, 'int_exp', 'Interest Expenses');
    fillPnlTableTotals(data.pbt, 'pbt', 'PBT');
    document.getElementById('head_sales').innerHTML = data.total_income.current;
    document.getElementById('head_grossprofit').innerHTML = data.gross_profit.current;
    document.getElementById('head_cogs').innerHTML = data.cost_of_goods_sold.current? data.cost_of_goods_sold.current: 0;
    document.getElementById('head_exp').innerHTML = data.ebitda.current;
    document.getElementById('head_profit').innerHTML = 'INR 5 lac'
  },
  error: function(error_data) {
    console.log("Error1");
    console.log(error_data);
  }
})

$.ajax({
  method: "GET",
  url: endpoint2,
  success: function(data) {
    console.log("Success Balance Sheet");
    fillBalsheetRows(data.cash, 'cash');
    fillBalsheetRows(data.bank, 'bank');
    fillBalsheetRows(data.accounts_receivable, 'acc_rec');
    fillBalsheetRows(data.fixed_asset, 'fixasset');
    fillBalsheetRows(data.other_current_asset, 'ocasset');
    fillBalsheetRows(data.other_asset, 'othasset');
    fillBalsheetRows(data.stock, 'stock');
    fillBalsheetRows(data.accounts_payable, 'acc_pay');
    fillBalsheetRows(data.long_term_liability, 'ltliab');
    fillBalsheetRows(data.other_current_liability, 'ocliab');
    fillBalsheetRows(data.other_liability, 'othliab');
    fillBalsheetRows(data.equity, 'equity');
    document.getElementById('head_equity').innerHTML = data.total_equity;
    document.getElementById('head_liabilities').innerHTML = data.total_liabilities;
    document.getElementById('head_assets').innerHTML = data.total_assets;
  },
  error: function(error_data) {
    console.log("Error2");
    console.log(error_data);
  }
})

$.ajax({
  method: "GET",
  url: endpoint3,
  success: function(data) {
    console.log("Success Cashflow");
    fillCashflowTotals(data.beginning_cash_balance, 'beg_cash_bal', 'Beginning Cash Balance');
    fillCashflowRows(data.cashflow_from_operating_activities, 'cashflowA');
    fillCashflowTotals(data.net_cash_a, 'netA', 'Cashflow from Operations');
    fillCashflowRows(data.cashflow_from_investing_activities, 'cashflowB');
    fillCashflowTotals(data.net_cash_b, 'netB', 'Cashflow from Investing');
    fillCashflowRows(data.cashflow_from_financing_activities, 'cashflowC');
    fillCashflowTotals(data.net_cash_c, 'netC', 'Cashflow from Financing');
    fillCashflowTotals(data.net_change_abc, 'netABC', 'Net Change in Cash (A)+(B)+(C)');
    fillCashflowTotals(data.ending_cash_balance, 'endbal', 'Ending Cash Balance');
  },
  error: function(error_data) {
    console.log("Error3");
    console.log(error_data);
  }
})


function fillPnlTableRows(data, tid) {
  var table = document.getElementById(tid);
  data.forEach(function (object) {
    var tr = document.createElement('tr');
    tr.innerHTML = '<th style="width:30%">' + object.account_header + '</th>' +
    '<td style="width: 12%; text-align:right;">' + object.current + '</td>' +
    '<td style="width: 8%; text-align:right;">' + '' + '</td>' + 
    '<td style="width: 12%; text-align:right;">' + object.previous + '</td>' +
    '<td style="width: 8%; text-align:right;">' + '' + '</td>' + 
    '<td style="width: 12%; text-align:center;">' + object.per_change + '%</td>' +
    '<td style="width: 18%; text-align:right;">' + object.three_month_avg + '</td>';
    table.appendChild(tr);
  })
}

function fillPnlTableTotals(object, tid, head) {
  document.getElementById(tid).innerHTML = '<th style="width:30%">' + head + '</th>' +
  '<td style="width: 12%; text-align:right;">' + object.current + '</td>' +
  '<td style="width: 8%;text-align: center;">' + object.curr_per + '%</td>' + 
  '<td style="width: 12%; text-align:right;">' + object.previous + '</td>' +
  '<td style="width: 8%; text-align: center;">' + object.prev_per + '%</td>' + 
  '<td style="width: 12%; text-align:center;">' + object.per_change + '%</td>' +
  '<td style="width: 18%; text-align:right;">' + object.three_month_avg + '</td>';
}

function fillPnlTableExpenses(data, tid) {
  var table = document.getElementById(tid);
  Object.keys(data).forEach(function (category) {
    var tr = document.createElement('tr');
    tr.innerHTML = '<th>' + category + '</th>';
    table.appendChild(tr)
    data[category].forEach(function (object) {
      var tr = document.createElement('tr');
      tr.innerHTML = '<td style="width:30%">' + object.account_header + '</td>' +
      '<td style="width: 12%; text-align:right;">' + object.current + '</td>' +
      '<td style="width: 8%; text-align:right;">' + '' + '</td>' + 
      '<td style="width: 12%; text-align:right;">' + object.previous + '</td>' +
      '<td style="width: 8%; text-align:right;">' + '' + '</td>' + 
      '<td style="width: 12%; text-align:center;">' + object.per_change + '%</td>' +
      '<td style="width: 18%; text-align:right;">' + object.three_month_avg + '</td>';
      table.appendChild(tr);
    })
  })
}

function fillBalsheetRows(data, tid) {
  var table = document.getElementById(tid);
  data.forEach(function (object) {
    var tr = document.createElement('tr');
    tr.innerHTML = '<th style="width:40%">' + object.account_header + '</th>' +
    '<td style="width: 13%; text-align:right;">' + object.current + '</td>' + 
    '<td style="width: 13%; text-align:right;">' + object.previous + '</td>' +
    '<td style="width: 13%; text-align:center;">' + object.per_change + '%</td>' +
    '<td style="width: 21%; text-align:right;">' + object.three_month_avg + '</td>';
    table.appendChild(tr);
  })
}

function fillCashflowRows(data, tid) {
  var table = document.getElementById(tid);
  data.forEach(function (object) {
    var tr = document.createElement('tr');
    tr.innerHTML = '<th style="width:40%">' + object.activity + '</th>' +
    '<td style="width: 20%; text-align:right;">' + object.current + '</td>' +
    '<td style="width: 20%; text-align:right;">' + object.previous + '</td>' +
    '<td style="width: 20%; text-align:center;">' + object.per_change + '%</td>';
    table.appendChild(tr);
  })
}

function fillCashflowTotals(object, tid, head) {
  document.getElementById(tid).innerHTML = '<th style="width:40%">' + head + '</th>' +
  '<td style="width: 20%; text-align:right;">' + object.current + '</td>' +
  '<td style="width: 20%; text-align:right;">' + object.previous + '</td>' +
  '<td style="width: 20%; text-align:center;">' + object.per_change + '%</td>';
}